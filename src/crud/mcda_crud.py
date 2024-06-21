# import zipfile
# import io
# import os
# from minio import Minio
# from datetime import datetime
# import json
# from typing import Any
# from fastapi import UploadFile
# import geopandas as gpd
# import fiona
# from fastapi import HTTPException
# from pathlib import Path

# # =================================================================================================
# client = Minio(
#     os.getenv("MINIO_HOSTNAME") + ":9000",
#     access_key=os.getenv("MINIO_ACCESS_KEY"),
#     secret_key=os.getenv("MINIO_SECRET_KEY"),
#     secure=False
# )

# bucket_name = "aarogya"
# if not client.bucket_exists(bucket_name):
#     client.make_bucket(bucket_name)

# async def upload_file(file: UploadFile, current_user: Any):
#     zip_data = await file.read()
    
#     with zipfile.ZipFile(io.BytesIO(zip_data), "w") as zip_ref:
#         zip_ref.extractall("/tmp")

#     file_path = f"{file.filename}"
#     zip_data = io.BytesIO(zip_data)

#     client.put_object(
#         bucket_name,
#         file_path,
#         zip_data,
#         length=zip_data.getbuffer().nbytes,
#         content_type="application/zip"
#     )

#     presigned_url = client.presigned_get_object(bucket_name, file_path)

#     return {
#         "bucket_name": bucket_name,
#         "file_path": file_path,
#         "presigned_url": presigned_url
#     }
# # =======================================xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx============================
# async def buffer_shp(file_path:Path) -> Path:
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         gdf = gpd.read_file(file_path)
#         print(gdf, 'kkkkkkkkkkkkkkkkkkkk')

#         if gdf.crs is None:
#             gdf = gdf.set_crs(epsg=4326)

#         gdf['geometry'] = gdf['geometry'].buffer(0.0038)
#         output_path = file_path.parent / f"{file_path.stem}_buffered.shp"
#         gdf.to_file(output_path)

#         print(f"Buffered shapefile saved successfully at {output_path}")

# ==================================xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=================================
# ++++++++++++++++++++++++Corrected one++++++++++++++++++++++++++++++++++++++
# import os
# import io
# import zipfile
# from datetime import datetime
# from pathlib import Path
# from typing import List
# from fastapi import HTTPException
# import geopandas as gpd
# import fiona
# from minio import Minio
# import os
# import io
# import zipfile
# from datetime import datetime
# from pathlib import Path
# from typing import List
# from fastapi import HTTPException
# import geopandas as gpd
# import fiona
# from minio import Minio

# client = Minio(
#     os.getenv("MINIO_HOSTNAME") + ":9000",
#     access_key=os.getenv("MINIO_ACCESS_KEY"),
#     secret_key=os.getenv("MINIO_SECRET_KEY"),
#     secure=False
# )

# bucket_name = "aarogya"
# if not client.bucket_exists(bucket_name):
#     client.make_bucket(bucket_name)

# async def perform_buffer_analysis(file_path: Path) -> List[Path]:
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         gdf = gpd.read_file(file_path)
        
#         if gdf.crs is None:
#             gdf = gdf.set_crs(epsg=4326)

#         gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
#         output_basename = file_path.stem + "_buffered"
#         output_dir = file_path.parent
#         output_files = [
#             output_dir / f"{output_basename}.shp",
#             output_dir / f"{output_basename}.shx",
#             output_dir / f"{output_basename}.dbf",
#             output_dir / f"{output_basename}.cpg",
#             output_dir / f"{output_basename}.prj"
#         ]
        
#         gdf.to_file(output_dir / f"{output_basename}.shp")

#     if not all(file.exists() for file in output_files):
#         raise HTTPException(status_code=500, detail="Failed to save buffered shapefile")
    
#     return output_files

# async def upload_to_minio(file_paths: List[Path]) -> dict:
#     zip_data = io.BytesIO()
    
#     with zipfile.ZipFile(zip_data, 'w') as zip_file:
#         for file_path in file_paths:
#             zip_file.write(file_path, file_path.name)
    
#     zip_data.seek(0)
#     file_name = f"mcda/{file_paths[0].stem}.zip" 
    
#     client.put_object(
#         bucket_name,
#         file_name,
#         zip_data,
#         length=zip_data.getbuffer().nbytes,
#         content_type="application/zip"
#     )
    
#     presigned_url = client.presigned_get_object(bucket_name, file_name)
    
#     return {
#         "bucket_name": bucket_name,
#         "file_path": file_name,
#         "presigned_url": presigned_url
#     }    
    
# +++++++++++++++++++++++++++++++++Until here++++++++++++++++++++++++++++++++++++++++++
# import os
# import io
# import zipfile
# from datetime import datetime
# from pathlib import Path
# from typing import List
# from fastapi import HTTPException
# import geopandas as gpd
# import fiona
# import rasterio
# from rasterio import features
# from rasterio.enums import MergeAlg
# from rasterio.plot import show
# import matplotlib.pyplot as plt
# import numpy as np
# from minio import Minio

# client = Minio(
#     os.getenv("MINIO_HOSTNAME") + ":9000",
#     access_key=os.getenv("MINIO_ACCESS_KEY"),
#     secret_key=os.getenv("MINIO_SECRET_KEY"),
#     secure=False
# )

# bucket_name = "aarogya"
# if not client.bucket_exists(bucket_name):
#     client.make_bucket(bucket_name)

# async def perform_buffer_analysis(file_path: Path) -> List[Path]:
#     print("river",file_path)
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         gdf = gpd.read_file(file_path)
        
#         if gdf.crs is None:
#             gdf = gdf.set_crs(epsg=4326)

#         gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
#         output_basename = file_path.stem + "_buffered"
#         output_dir = file_path.parent
#         output_files = [
#             output_dir / f"{output_basename}.shp",
#             output_dir / f"{output_basename}.shx",
#             output_dir / f"{output_basename}.dbf",
#             output_dir / f"{output_basename}.cpg",
#             output_dir / f"{output_basename}.prj"
#         ]
        
#         gdf.to_file(output_dir / f"{output_basename}.shp")

#     if not all(file.exists() for file in output_files):
#         raise HTTPException(status_code=500, detail="Failed to save all the buffered shapefile components")
    
#     return output_files

# async def rasterize_vector(file_paths: List[Path]) -> Path:
#     print("filepath for buffer ",file_paths)
#     vector_file_path = next(p for p in file_paths if p.suffix == '.shp')
#     print(vector_file_path, '==================================================================')
#     # Get the raster template from Minio bucket
#     raster_template_path = Path("http://127.0.0.1:9000/aarogya/rasterized_dang%20%281%29.tif?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=6NQ6X5R9Y78254EKURR9%2F20240619%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240619T043413Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI2TlE2WDVSOVk3ODI1NEVLVVJSOSIsImV4cCI6MTcxODgxMTMzMSwicGFyZW50IjoiYWFyb2d5YTEyMyJ9._Uuq91elp9XLtX1KJOdGKD1g6-nVdurvcFS3ENZBnWhxdKFxCn--gCTGKZhes-rRhSM6MJcs6AetcdtBV5um8g&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=d70f7fc7bb7c79959647bb08f379e73d5930c8dfc113233189374834e779bc20")  # Replace with the actual path from Minio bucket
#     print(raster_template_path, '++++++++++++++++++++++++++++++++++++++++++++++++++')
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         vector = gpd.read_file(vector_file_path)
#         print(vector, '++++++++++++++++++++++++++++++++++#########################################')
#         if vector.crs is None:
#             vector = vector.set_crs(epsg=4326)

#         geom = [shapes for shapes in vector.geometry]
#         print(geom, ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
#         raster = rasterio.open(raster_template_path)
#         print(raster, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#         vector['id'] = range(0, len(vector))
#         geom_value = ((geom, value) for geom, value in zip(vector.geometry, vector['id']))

#         rasterized = features.rasterize(
#             geom_value,
#             out_shape=raster.shape,
#             transform=raster.transform,
#             all_touched=True,
#             fill=-99999,
#             merge_alg=MergeAlg.replace,
#             dtype=np.float32
#         )

#     output_raster_path = vector_file_path.parent / f"{vector_file_path.stem}_rasterized.tif"
    
#     with rasterio.open(
#             output_raster_path, "w",
#             driver="GTiff",
#             crs=raster.crs,
#             transform=raster.transform,
#             dtype=rasterio.uint8,
#             count=1,
#             width=raster.width,
#             height=raster.height) as dst:
#         dst.write(rasterized, indexes=1)
    
#     return output_raster_path

# async def upload_to_minio(file_paths: List[Path]) -> dict:
#     zip_data = io.BytesIO()
    
#     with zipfile.ZipFile(zip_data, 'w') as zip_file:
#         for file_path in file_paths:
#             zip_file.write(file_path, file_path.name)
    
#     zip_data.seek(0)
#     file_name = f"mcda/{file_paths[0].stem}.zip" 
    
#     client.put_object(
#         bucket_name,
#         file_name,
#         zip_data,
#         length=zip_data.getbuffer().nbytes,
#         content_type="application/zip"
#     )
    
#     presigned_url = client.presigned_get_object(bucket_name, file_name)
    
#     return {
#         "bucket_name": bucket_name,
#         "file_path": file_name,
#         "presigned_url": presigned_url
#     } 

# ============================================================================================================
# import os
# import io
# import zipfile
# import requests
# from datetime import datetime
# from pathlib import Path
# from typing import List
# from fastapi import HTTPException
# import geopandas as gpd
# import fiona
# import rasterio
# from rasterio import features
# from rasterio.enums import MergeAlg
# import numpy as np
# from minio import Minio
# from rasterio import mask
# client = Minio(
#     os.getenv("MINIO_HOSTNAME") + ":9000",
#     access_key=os.getenv("MINIO_ACCESS_KEY"),
#     secret_key=os.getenv("MINIO_SECRET_KEY"),
#     secure=False
# )

# bucket_name = "aarogya"
# if not client.bucket_exists(bucket_name):
#     client.make_bucket(bucket_name)

# def get_presigned_url(key: str) -> str:
#     try:
#         presigned_url = client.presigned_get_object(bucket_name, key)
#         return presigned_url
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

# def get_raster_from_presigned_url(url: str):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return io.BytesIO(response.content)
#     except requests.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"Failed to retrieve raster template from URL: {str(e)}")

# async def perform_buffer_analysis(file_path: Path) -> List[Path]:
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         gdf = gpd.read_file(file_path)
        
#         if gdf.crs is None:
#             gdf = gdf.set_crs(epsg=4326)

#         gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
#         output_basename = file_path.stem + "_buffered"
#         output_dir = file_path.parent
#         output_files = [
#             output_dir / f"{output_basename}.shp",
#             output_dir / f"{output_basename}.shx",
#             output_dir / f"{output_basename}.dbf",
#             output_dir / f"{output_basename}.cpg",
#             output_dir / f"{output_basename}.prj"
#         ]
        
#         gdf.to_file(output_dir / f"{output_basename}.shp")

#     if not all(file.exists() for file in output_files):
#         raise HTTPException(status_code=500, detail="Failed to save all the buffered shapefile components")
    
#     return output_files

# async def rasterize_vector(file_paths: List[Path], raster_file_path: Path) -> Path:
#     vector_file_path = next(p for p in file_paths if p.suffix == '.shp')
    
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         vector = gpd.read_file(vector_file_path)
#         if vector.crs is None:
#             vector = vector.set_crs(epsg=4326)

#         geom = [shapes for shapes in vector.geometry]
        
#         with rasterio.open(raster_file_path) as raster:
#             vector['id'] = range(0, len(vector))
#             geom_value = ((geom, value) for geom, value in zip(vector.geometry, vector['id']))

#             rasterized = features.rasterize(
#                 geom_value,
#                 out_shape=raster.shape,
#                 transform=raster.transform,
#                 all_touched=True,
#                 fill=-99999,
#                 merge_alg=MergeAlg.replace,
#                 dtype=np.float32
#             )

#             output_raster_path = vector_file_path.parent / f"{vector_file_path.stem}_rasterized.tif"
            
#             with rasterio.open(
#                     output_raster_path, "w",
#                     driver="GTiff",
#                     crs=raster.crs,
#                     transform=raster.transform,
#                     dtype=rasterio.uint8,
#                     count=1,
#                     width=raster.width,
#                     height=raster.height) as dst:
#                 dst.write(rasterized, indexes=1)
    
#     return output_raster_path

# async def mask_raster(raster_file_path: Path, shapefile_path: Path) -> Path:
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         with fiona.open(shapefile_path) as shapefile:
#             shapes = [feature["geometry"] for feature in shapefile]
#         with rasterio.open(raster_file_path) as src:
#             out_image, out_transform = mask.mask(src, shapes, crop=True, filled=True)
#             out_meta = src.meta
#             out_meta.update({"driver": "GTiff", 
#                              "height": out_image.shape[1], 
#                              "width": out_image.shape[2], 
#                              "transform": out_transform})

#         output_masked_raster_path = raster_file_path.parent / f"{raster_file_path.stem}_masked.tif"
#         with rasterio.open(output_masked_raster_path, "w", **out_meta) as dest:
#             dest.write(out_image)

#     return output_masked_raster_path
# # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
# async def weighted_overlay(weighted_path_settlement: Path, weighted_path_river: Path, weighted_path_road: Path) -> Path:
#     road_weight = float(input("Enter weight for road: "))
#     settlement_weight = float(input("Enter weight for settlement: "))
#     river_weight = float(input("Enter weight for river: "))

#     with rasterio.open(weighted_path_road) as weighted_raster:
#         weighted_array_road = weighted_raster.read(1)
#         weighted_array_road = weighted_array_road / weighted_array_road.max()
#         weighted_array_road = weighted_array_road * road_weight

#     with rasterio.open(weighted_path_settlement) as raster:
#         weighted_array_settlement = raster.read(1)
#         weighted_array_settlement = weighted_array_settlement / weighted_array_settlement.max()
#         weighted_array_settlement = weighted_array_settlement * settlement_weight
        
#     with rasterio.open(weighted_path_river) as raster:
#         weighted_array_river = raster.read(2)
#         weighted_array_river = weighted_array_river / weighted_array_river.max()
#         weighted_array_river = weighted_array_river * river_weight

#     weighted_overlay_array = (weighted_array_road + weighted_array_settlement + weighted_array_river)

#     output_weighted_overlay_path = weighted_path_road.parent / f"{weighted_path_road.stem}_weighted_overlay.tif"
#     with rasterio.open(
#             output_weighted_overlay_path, "w",
#             driver="GTiff",
#             crs=raster.crs,
#             transform=raster.transform,
#             dtype=rasterio.uint8,
#             count=1,
#             width=raster.width,
#             height=raster.height) as dst:
#         dst.write(weighted_overlay_array, indexes=1)

#     return output_weighted_overlay_path
# # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# async def upload_to_minio(file_paths: List[Path]) -> dict:
#     zip_data = io.BytesIO()
    
#     with zipfile.ZipFile(zip_data, 'w') as zip_file:
#         for file_path in file_paths:
#             zip_file.write(file_path, file_path.name)
    
#     zip_data.seek(0)
#     file_name = f"mcda/{file_paths[0].stem}.zip" 
    
#     client.put_object(
#         bucket_name,
#         file_name,
#         zip_data,
#         length=zip_data.getbuffer().nbytes,
#         content_type="application/zip"
#     )
    
#     presigned_url = client.presigned_get_object(bucket_name, file_name)
    
#     return {
#         "bucket_name": bucket_name,
#         "file_path": file_name,
#         "presigned_url": presigned_url
#     }
  
# import os
# import io
# import zipfile
# import requests
# from datetime import datetime
# from pathlib import Path
# from typing import List
# from fastapi import HTTPException
# import geopandas as gpd
# import fiona
# import rasterio
# from rasterio import features, mask
# from rasterio.enums import MergeAlg
# from rasterio.plot import show
# import numpy as np
# from minio import Minio

# # Initialize MinIO client
# client = Minio(
#     os.getenv("MINIO_HOSTNAME") + ":9000",
#     access_key=os.getenv("MINIO_ACCESS_KEY"),
#     secret_key=os.getenv("MINIO_SECRET_KEY"),
#     secure=False
# )

# bucket_name = "aarogya"
# if not client.bucket_exists(bucket_name):
#     client.make_bucket(bucket_name)

# def get_presigned_url(key: str) -> str:
#     try:
#         presigned_url = client.presigned_get_object(bucket_name, key)
#         return presigned_url
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

# def get_raster_from_presigned_url(url: str):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return io.BytesIO(response.content)
#     except requests.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"Failed to retrieve raster from URL: {str(e)}")

# async def perform_buffer_analysis(file_path: Path) -> List[Path]:
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         gdf = gpd.read_file(file_path)
        
#         if gdf.crs is None:
#             gdf = gdf.set_crs(epsg=4326)

#         gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
#         output_basename = file_path.stem + "_buffered"
#         output_dir = file_path.parent
#         output_files = [
#             output_dir / f"{output_basename}.shp",
#             output_dir / f"{output_basename}.shx",
#             output_dir / f"{output_basename}.dbf",
#             output_dir / f"{output_basename}.cpg",
#             output_dir / f"{output_basename}.prj"
#         ]
        
#         gdf.to_file(output_dir / f"{output_basename}.shp")

#     if not all(file.exists() for file in output_files):
#         raise HTTPException(status_code=500, detail="Failed to save all the buffered shapefile components")
    
#     return output_files

# async def rasterize_vector(file_paths: List[Path], raster_file_path: Path) -> Path:
#     vector_file_path = next(p for p in file_paths if p.suffix == '.shp')
    
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         vector = gpd.read_file(vector_file_path)
#         if vector.crs is None:
#             vector = vector.set_crs(epsg=4326)

#         geom = [shapes for shapes in vector.geometry]
        
#         with rasterio.open(raster_file_path) as raster:
#             vector['id'] = range(0, len(vector))
#             geom_value = ((geom, value) for geom, value in zip(vector.geometry, vector['id']))

#             rasterized = features.rasterize(
#                 geom_value,
#                 out_shape=raster.shape,
#                 transform=raster.transform,
#                 all_touched=True,
#                 fill=-99999,
#                 merge_alg=MergeAlg.replace,
#                 dtype=np.float32
#             )

#             output_raster_path = vector_file_path.parent / f"{vector_file_path.stem}_rasterized.tif"
            
#             with rasterio.open(
#                     output_raster_path, "w",
#                     driver="GTiff",
#                     crs=raster.crs,
#                     transform=raster.transform,
#                     dtype=rasterio.uint8,
#                     count=1,
#                     width=raster.width,
#                     height=raster.height) as dst:
#                 dst.write(rasterized, indexes=1)
    
#     return output_raster_path

# async def mask_raster(raster_file_path: Path, shapefile_path: Path) -> Path:
#     with fiona.Env(SHAPE_RESTORE_SHX='YES'):
#         with fiona.open(shapefile_path) as shapefile:
#             shapes = [feature["geometry"] for feature in shapefile]
#         with rasterio.open(raster_file_path) as src:
#             out_image, out_transform = mask.mask(src, shapes, crop=True, filled=True)
#             out_meta = src.meta
#             out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

#         output_masked_raster_path = raster_file_path.parent / f"{raster_file_path.stem}_masked.tif"
#         with rasterio.open(output_masked_raster_path, "w", **out_meta) as dest:
#             dest.write(out_image)

#     return output_masked_raster_path

# async def perform_weighted_overlay(raster_urls: List[str], weights: List[float]) -> Path:
#     if len(raster_urls) != len(weights):
#         raise ValueError("Number of raster URLs and weights must match")

#     rasters = [rasterio.open(get_raster_from_presigned_url(url)) for url in raster_urls]
    
#     meta = rasters[0].meta
#     meta.update(dtype=rasterio.float32)
    
#     overlay_result = np.zeros(rasters[0].shape, dtype=np.float32)
    
#     for raster, weight in zip(rasters, weights):
#         overlay_result += raster.read(1) * weight
    
#     output_overlay_path = Path("/tmp") / "weighted_overlay.tif"
#     with rasterio.open(output_overlay_path, "w", **meta) as dst:
#         dst.write(overlay_result, 1)
    
#     return output_overlay_path

# async def upload_to_minio(file_paths: List[Path]) -> dict:
#     zip_data = io.BytesIO()
    
#     with zipfile.ZipFile(zip_data, 'w') as zip_file:
#         for file_path in file_paths:
#             zip_file.write(file_path, file_path.name)
    
#     zip_data.seek(0)
#     file_name = f"mcda/{file_paths[0].stem}.zip"  
    
#     client.put_object(
#         bucket_name,
#         file_name,
#         zip_data,
#         length=zip_data.getbuffer().nbytes,
#         content_type="application/zip"
#     )
    
#     presigned_url = client.presigned_get_object(bucket_name, file_name)
    
#     return {
#         "bucket_name": bucket_name,
#         "file_path": file_name,
#         "presigned_url": presigned_url
#     }
    
    
import os
import io
import zipfile
import requests
from datetime import datetime
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

# Initialize MinIO client
client = Minio(
    os.getenv("MINIO_HOSTNAME") + ":9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

bucket_name = "aarogya"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

def get_presigned_url(key: str) -> str:
    try:
        presigned_url = client.presigned_get_object(bucket_name, key)
        return presigned_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

def get_raster_from_presigned_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve raster from URL: {str(e)}")

async def perform_buffer_analysis(file_path: Path) -> List[Path]:
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        gdf = gpd.read_file(file_path)
        
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)

        gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
        output_basename = file_path.stem + "_buffered"
        output_dir = file_path.parent
        output_files = [
            output_dir / f"{output_basename}.shp",
            output_dir / f"{output_basename}.shx",
            output_dir / f"{output_basename}.dbf",
            output_dir / f"{output_basename}.cpg",
            output_dir / f"{output_basename}.prj"
        ]
        
        gdf.to_file(output_dir / f"{output_basename}.shp")

    if not all(file.exists() for file in output_files):
        raise HTTPException(status_code=500, detail="Failed to save all the buffered shapefile components")
    
    return output_files

async def rasterize_vector(file_paths: List[Path], raster_file_path: Path) -> Path:
    vector_file_path = next(p for p in file_paths if p.suffix == '.shp')
    
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        vector = gpd.read_file(vector_file_path)
        if vector.crs is None:
            vector = vector.set_crs(epsg=4326)

        geom = [shapes for shapes in vector.geometry]
        
        with rasterio.open(raster_file_path) as raster:
            vector['id'] = range(0, len(vector))
            geom_value = ((geom, value) for geom, value in zip(vector.geometry, vector['id']))

            rasterized = features.rasterize(
                geom_value,
                out_shape=raster.shape,
                transform=raster.transform,
                all_touched=True,
                fill=-99999,
                merge_alg=MergeAlg.replace,
                dtype=np.float32
            )

            output_raster_path = vector_file_path.parent / f"{vector_file_path.stem}_rasterized.tif"
            
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

async def mask_raster(raster_file_path: Path, shapefile_path: Path) -> Path:
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        with fiona.open(shapefile_path) as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        with rasterio.open(raster_file_path) as src:
            out_image, out_transform = mask.mask(src, shapes, crop=True, filled=True)
            out_meta = src.meta
            out_meta.update({"driver": "GTiff", 
                             "height": out_image.shape[1], 
                             "width": out_image.shape[2], 
                             "transform": out_transform})

        output_masked_raster_path = raster_file_path.parent / f"{raster_file_path.stem}_masked.tif"
        with rasterio.open(output_masked_raster_path, "w", **out_meta) as dest:
            dest.write(out_image)

    return output_masked_raster_path

# async def weighted_overlay(weighted_path_settlement: Path, weighted_path_river: Path, weighted_path_road: Path) -> Path:
#     road_weight = float(input("Enter weight for road: "))
#     settlement_weight = float(input("Enter weight for settlement: "))
#     river_weight = float(input("Enter weight for river: "))

#     with rasterio.open(weighted_path_road) as weighted_raster:
#         weighted_array_road = weighted_raster.read(1)
#         weighted_array_road = weighted_array_road / weighted_array_road.max()
#         weighted_array_road = weighted_array_road * road_weight

#     with rasterio.open(weighted_path_settlement) as raster:
#         weighted_array_settlement = raster.read(1)
#         weighted_array_settlement = weighted_array_settlement / weighted_array_settlement.max()
#         weighted_array_settlement = weighted_array_settlement * settlement_weight
        
#     with rasterio.open(weighted_path_river) as raster:
#         weighted_array_river = raster.read(2)
#         weighted_array_river = weighted_array_river / weighted_array_river.max()
#         weighted_array_river = weighted_array_river * river_weight

#     weighted_overlay_array = (weighted_array_road + weighted_array_settlement + weighted_array_river)

#     output_weighted_overlay_path = weighted_path_road.parent / f"{weighted_path_road.stem}_weighted_overlay.tif"
#     with rasterio.open(
#             output_weighted_overlay_path, "w",
#             driver="GTiff",
#             crs=raster.crs,
#             transform=raster.transform,
#             dtype=rasterio.uint8,
#             count=1,
#             width=raster.width,
#             height=raster.height) as dst:
#         dst.write(weighted_overlay_array, indexes=1)

#     return output_weighted_overlay_path

# async def weighted_overlay(weighted_path_settlement: Path, weighted_path_river: Path, weighted_path_road: Path, weights: List[float]) -> Path:
#     road_weight, settlement_weight, river_weight = weights

#     with rasterio.open(weighted_path_road) as weighted_raster:
#         weighted_array_road = weighted_raster.read(1)
#         weighted_array_road = weighted_array_road / weighted_array_road.max()
#         weighted_array_road = weighted_array_road * road_weight

#     with rasterio.open(weighted_path_settlement) as raster:
#         weighted_array_settlement = raster.read(1)
#         weighted_array_settlement = weighted_array_settlement / weighted_array_settlement.max()
#         weighted_array_settlement = weighted_array_settlement * settlement_weight
        
#     with rasterio.open(weighted_path_river) as raster:
#         weighted_array_river = raster.read(1)
#         weighted_array_river = weighted_array_river / weighted_array_river.max()
#         weighted_array_river = weighted_array_river * river_weight

#     weighted_overlay_array = (weighted_array_road + weighted_array_settlement + weighted_array_river)

#     output_weighted_overlay_path = weighted_path_road.parent / f"{weighted_path_road.stem}_weighted_overlay.tif"
#     with rasterio.open(
#             output_weighted_overlay_path, "w",
#             driver="GTiff",
#             crs=raster.crs,
#             transform=raster.transform,
#             dtype=rasterio.uint8,
#             count=1,
#             width=raster.width,
#             height=raster.height) as dst:
#         dst.write(weighted_overlay_array, indexes=1)

#     return output_weighted_overlay_path


# async def upload_to_minio(file_paths: List[Path]) -> dict:
#     zip_data = io.BytesIO()
    
#     with zipfile.ZipFile(zip_data, 'w') as zip_file:
#         for file_path in file_paths:
#             zip_file.write(file_path, file_path.name)
    
#     zip_data.seek(0)
#     file_name = f"mcda/{file_paths[0].stem}.zip" 
    
#     client.put_object(
#         bucket_name,
#         file_name,
#         zip_data,
#         length=zip_data.getbuffer().nbytes,
#         content_type="application/zip"
#     )
    
#     presigned_url = client.presigned_get_object(bucket_name, file_name)
    
#     return {
#         "b  ucket_name": bucket_name,
#         "file_path": file_name,
#         "presigned_url": presigned_url
#     }
    

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

# Initialize MinIO client
client = Minio(
    os.getenv("MINIO_HOSTNAME") + ":9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

bucket_name = "aarogya"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

def get_presigned_url(key: str) -> str:
    try:
        presigned_url = client.presigned_get_object(bucket_name, key)
        return presigned_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

def get_raster_from_presigned_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return io.BytesIO(response.content)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve raster from URL: {str(e)}")

async def perform_buffer_analysis(file_path: Path) -> List[Path]:
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        gdf = gpd.read_file(file_path)
        
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)

        gdf['geometry'] = gdf['geometry'].buffer(0.0038)
        
        output_basename = file_path.stem + "_buffered"
        output_dir = file_path.parent
        output_files = [
            output_dir / f"{output_basename}.shp",
            output_dir / f"{output_basename}.shx",
            output_dir / f"{output_basename}.dbf",
            output_dir / f"{output_basename}.cpg",
            output_dir / f"{output_basename}.prj"
        ]
        
        gdf.to_file(output_dir / f"{output_basename}.shp")

    if not all(file.exists() for file in output_files):
        raise HTTPException(status_code=500, detail="Failed to save all the buffered shapefile components")
    
    return output_files

async def rasterize_vector(file_paths: List[Path], raster_file_path: Path) -> Path:
    vector_file_path = next(p for p in file_paths if p.suffix == '.shp')
    
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        vector = gpd.read_file(vector_file_path)
        if vector.crs is None:
            vector = vector.set_crs(epsg=4326)

        geom = [shapes for shapes in vector.geometry]
        
        with rasterio.open(raster_file_path) as raster:
            vector['id'] = range(0, len(vector))
            geom_value = ((geom, value) for geom, value in zip(vector.geometry, vector['id']))

            rasterized = features.rasterize(
                geom_value,
                out_shape=raster.shape,
                transform=raster.transform,
                all_touched=True,
                fill=-99999,
                merge_alg=MergeAlg.replace,
                dtype=np.float32
            )

            output_raster_path = vector_file_path.parent / f"{vector_file_path.stem}_rasterized.tif"
            
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

async def mask_raster(raster_file_path: Path, shapefile_path: Path) -> Path:
    with fiona.Env(SHAPE_RESTORE_SHX='YES'):
        with fiona.open(shapefile_path) as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        with rasterio.open(raster_file_path) as src:
            out_image, out_transform = mask.mask(src, shapes, crop=True, filled=True)
            out_meta = src.meta
            out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

        output_masked_raster_path = raster_file_path.parent / f"{raster_file_path.stem}_masked.tif"
        with rasterio.open(output_masked_raster_path, "w", **out_meta) as dest:
            dest.write(out_image)

    return output_masked_raster_path

async def upload_to_minio(file_paths: List[Path]) -> List[dict]:
    responses = []

    for file_path in file_paths:
        with file_path.open("rb") as file_data:
            file_name = f"mcda/{file_path.name}"
            
            client.put_object(
                bucket_name,
                file_name,
                data=file_data,
                length=os.path.getsize(file_path),
                content_type="image/tiff"
            )
        
        presigned_url = client.presigned_get_object(bucket_name, file_name)
        
        responses.append({
            "bucket_name": bucket_name,
            "file_path": file_name,
            "presigned_url": presigned_url
        })
    
    return responses
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
                meta = src.meta
            raster_arrays.append(src.read(1))
    
    weighted_overlay = sum(raster * weight for raster, weight in zip(raster_arrays, weights))

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

async def upload_to_minio(file_paths: List[Path]) -> List[dict]:
    responses = []

    for file_path in file_paths:
        with file_path.open("rb") as file_data:
            file_name = f"mcda/{file_path.name}"
            
            client.put_object(
                bucket_name,
                file_name,
                data=file_data,
                length=os.path.getsize(file_path),
                content_type="image/tiff"
            )
        
        presigned_url = client.presigned_get_object(bucket_name, file_name)
        
        responses.append({
            "bucket_name": bucket_name,
            "file_path": file_name,
            "presigned_url": presigned_url
        })
    
    return responses    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
