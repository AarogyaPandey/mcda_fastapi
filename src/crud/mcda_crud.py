    
import os
import io
import zipfile
import requests
from pathlib import Path
from typing import List
from fastapi import HTTPException
import geopandas as gpd
import fiona
import rasterio
from rasterio import features, mask
from rasterio.enums import MergeAlg
import numpy as np
from minio import Minio

# Initialize MinIO client with environment variables for credentials
client = Minio(
    os.getenv("MINIO_HOSTNAME") + ":9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

# Define the bucket name
bucket_name = "aarogya"
# Check if the bucket exists, create it if it doesn't
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Function to generate a presigned URL for a file in MinIO
def get_presigned_url(key: str) -> str:
    try:
        presigned_url = client.presigned_get_object(bucket_name, key)
        return presigned_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

# Function to retrieve a raster file from a presigned URL
def get_raster_from_presigned_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve raster from URL: {str(e)}")

# Function to perform buffer analysis on a shapefile
async def perform_buffer_analysis(file_path: Path) -> List[Path]:
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        gdf = gpd.read_file(file_path)
        
        # Set CRS if not already set
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)

        # Perform buffer analysis with a buffer distance of 0.0038
        gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
        # Define output filenames for the buffered shapefile components
        output_basename = file_path.stem + "_buffered"
        output_dir = file_path.parent
        output_files = [
            output_dir / f"{output_basename}.shp",
            output_dir / f"{output_basename}.shx",
            output_dir / f"{output_basename}.dbf",
            output_dir / f"{output_basename}.cpg",
            output_dir / f"{output_basename}.prj"
        ]
        
        # Save the buffered shapefile
        gdf.to_file(output_dir / f"{output_basename}.shp")

    # Check if all components of the shapefile are saved
    if not all(file.exists() for file in output_files):
        raise HTTPException(status_code=500, detail="Failed to save all the buffered shapefile components")
    
    return output_files

# Function to rasterize a vector shapefile
async def rasterize_vector(file_paths: List[Path], raster_file_path: Path) -> Path:
    vector_file_path = next(p for p in file_paths if p.suffix == '.shp')
    
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        vector = gpd.read_file(vector_file_path)
        if vector.crs is None:
            vector = vector.set_crs(epsg=4326)

        geom = [shapes for shapes in vector.geometry]
        
        with rasterio.open(raster_file_path) as raster:
            vector['id'] = range(0, len(vector))  # Assign unique IDs to geometries
            geom_value = ((geom, value) for geom, value in zip(vector.geometry, vector['id']))

            # Rasterize the vector data
            rasterized = features.rasterize(
                geom_value,
                out_shape=raster.shape,
                transform=raster.transform,
                all_touched=True,
                fill=-99999,
                merge_alg=MergeAlg.replace,
                dtype=np.float32
            )

            # Define the output path for the rasterized file
            output_raster_path = vector_file_path.parent / f"{vector_file_path.stem}_rasterized.tif"
            
            # Save the rasterized data to a new raster file
            with rasterio.open(
                    output_raster_path, "w",
                    driver="GTiff",
                    crs=raster.crs,
                    transform=raster.transform,
                    dtype=rasterio.uint8,
                    count=1,
                    width=raster.width,
                    height=raster.height) as dst:
                dst.write(rasterized, indexes=1)
    
    return output_raster_path

# Function to mask a raster file using a shapefile
async def mask_raster(raster_file_path: Path, shapefile_path: Path) -> Path:
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        with fiona.open(shapefile_path) as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        with rasterio.open(raster_file_path) as src:
            # Apply mask to the raster file
            out_image, out_transform = mask.mask(src, shapes, crop=True, filled=True)
            out_meta = src.meta
            out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

        # Define the output path for the masked raster file
        output_masked_raster_path = raster_file_path.parent / f"{raster_file_path.stem}_masked.tif"
        with rasterio.open(output_masked_raster_path, "w", **out_meta) as dest:
            dest.write(out_image)

    return output_masked_raster_path

# Function to upload files to Minio and get their presigned URLs
async def upload_to_minio(file_paths: List[Path]) -> List[dict]:
    responses = []

    for file_path in file_paths:
        with file_path.open("rb") as file_data:
            file_name = f"mcda/{file_path.name}"
            
            # Upload file to Minio
            client.put_object(
                bucket_name,
                file_name,
                data=file_data,
                length=os.path.getsize(file_path),
                content_type="image/tiff"
            )
        
        # Generate presigned URL for the uploaded file
        presigned_url = client.presigned_get_object(bucket_name, file_name)
        
        responses.append({
            "bucket_name": bucket_name,
            "file_path": file_name,
            "presigned_url": presigned_url
        })
    
    return responses

# Function to perform weighted overlay analysis on raster files
async def perform_weighted_overlay(raster_urls: List[str], weights: List[float]) -> Path:
    rasters = []
    for url in raster_urls:
        raster_bytes = get_raster_from_presigned_url(url)
        rasters.append(raster_bytes)
        
    raster_arrays = []
    meta = None
    for raster_bytes in rasters:
        with rasterio.open(raster_bytes) as src:
            if meta is None:
                meta = src.meta  # Save metadata from the first raster
            raster_arrays.append(src.read(1))
    
    # Perform weighted overlay by summing the weighted rasters
    weighted_overlay = sum(raster * weight for raster, weight in zip(raster_arrays, weights))

    # Define the output path for the result of the weighted overlay
    output_path = Path("/tmp/result_weighted_overlay.tif")
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=weighted_overlay.shape[0],
        width=weighted_overlay.shape[1],
        count=1,
        dtype=weighted_overlay.dtype,
        crs=meta['crs'],
        transform=meta['transform']
    ) as dst:
        dst.write(weighted_overlay, 1)

    return output_path

# Function to upload files to Minio and get their presigned URLs
async def upload_to_minio(file_paths: List[Path]) -> List[dict]:
    responses = []

    for file_path in file_paths:
        with file_path.open("rb") as file_data:
            file_name = f"mcda/{file_path.name}"
            
            # Upload file to Minio
            client.put_object(
                bucket_name,
                file_name,
                data=file_data,
                length=os.path.getsize(file_path),
                content_type="image/tiff"
            )
        
        # Generate presigned URL for the uploaded file
        presigned_url = client.presigned_get_object(bucket_name, file_name)
        
        responses.append({
            "bucket_name": bucket_name,
            "file_path": file_name,
            "presigned_url": presigned_url
        })
    
    return responses    
