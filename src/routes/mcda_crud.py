
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from src.auth.jwthandler import get_current_user
import src.crud.mcda_crud as mcda
from typing import List

router = APIRouter()

# Define a POST endpoint for uploading files
@router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
async def upload_file(
    boundary_shp: UploadFile = File(...),
    river_shapefile: UploadFile = File(...),
    road_shapefile: UploadFile = File(...),
    settlement_shapefile: UploadFile = File(...),
    rasterfile: UploadFile = File(...),
    current_user=Depends(get_current_user) # Ensure the user is authenticated
):
    # Save the uploaded shapefiles and raster file to temporary paths
    temp_Dangsh_path = Path("/tmp") / boundary_shp.filename
    with temp_Dangsh_path.open("wb") as boundary:
        boundary.write(await boundary_shp.read())

    temp_riversh_path = Path("/tmp") / river_shapefile.filename
    with temp_riversh_path.open("wb") as buffer:
        buffer.write(await river_shapefile.read())

    temp_roadsh_path = Path("/tmp") / road_shapefile.filename
    with temp_roadsh_path.open("wb") as buffer:
        buffer.write(await road_shapefile.read())
    
    temp_settlementsh_path = Path("/tmp") / settlement_shapefile.filename
    with temp_settlementsh_path.open("wb") as buffer:
        buffer.write(await settlement_shapefile.read())

    temp_rasterfile_path = Path("/tmp") / rasterfile.filename
    with temp_rasterfile_path.open("wb") as buffer:
        buffer.write(await rasterfile.read())

    try:
        # Perform buffer analysis on the shapefiles
        buffered_river = await mcda.perform_buffer_analysis(temp_riversh_path)
        buffered_road = await mcda.perform_buffer_analysis(temp_roadsh_path)
        buffered_settlement = await mcda.perform_buffer_analysis(temp_settlementsh_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

    try:
        # Rasterize the buffered shapefiles using the raster file
        rasterized_river = await mcda.rasterize_vector(buffered_river, temp_rasterfile_path)
        rasterized_road = await mcda.rasterize_vector(buffered_road, temp_rasterfile_path)
        rasterized_settlement = await mcda.rasterize_vector(buffered_settlement, temp_rasterfile_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rasterization failed: {str(e)}")
    
    try:
        # Mask the rasterized files with the Boundary shapefile
        masked_river = await mcda.mask_raster(rasterized_river, temp_Dangsh_path)
        masked_road = await mcda.mask_raster(rasterized_road, temp_Dangsh_path)
        masked_settlement = await mcda.mask_raster(rasterized_settlement, temp_Dangsh_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Masking failed: {str(e)}")
    
    try:
        # Upload the masked files to Minio
        river_response = await mcda.upload_to_minio([masked_river])
        road_response = await mcda.upload_to_minio([masked_road])
        settlement_response = await mcda.upload_to_minio([masked_settlement])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")

    return JSONResponse(content={"river_response": river_response, "road_response": road_response, "settlement_response": settlement_response})

# Define a POST endpoint for performing weighted overlay analysis
@router.post("/api/mcda/weighted_overlay", tags=['MCDA'], dependencies=[Depends(get_current_user)])
async def weighted_overlay(
    river_weight: float,
    road_weight: float,
    settlement_weight: float,
    current_user=Depends(get_current_user) # Ensure the user is authenticated
):
    # Retrieve presigned URLs for the masked raster files
    try:
        river_url = mcda.get_presigned_url("mcda/river_dang_buffered_rasterized_masked.tif")
        road_url = mcda.get_presigned_url("mcda/road_dang_buffered_rasterized_masked.tif")
        settlement_url = mcda.get_presigned_url("mcda/settlement_area_dang_buffered_rasterized_masked.tif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URLs: {str(e)}")

    raster_urls = [river_url, road_url, settlement_url]
    weights = [river_weight, road_weight, settlement_weight]

    try:
        # Perform weighted overlay analysis with the given URLs and weights
        overlay_result_path = await mcda.perform_weighted_overlay(raster_urls, weights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weighted overlay analysis failed: {str(e)}")
    
    try:
        # Upload the result of the weighted overlay analysis to Minio
        response = await mcda.upload_to_minio([overlay_result_path])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")

    return JSONResponse(content={"overlay_result": response})
