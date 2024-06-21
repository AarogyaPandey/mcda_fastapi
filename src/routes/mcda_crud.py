
# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from pathlib import Path
# from src.auth.jwthandler import get_current_user
# import src.crud.mcda_crud as mcda

# router = APIRouter()

# @router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
# async def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
#     temp_file_path = Path("/tmp") / file.filename
#     with temp_file_path.open("wb") as buffer:
#         buffer.write(await file.read())
#     try:
#         output_files = await mcda.perform_buffer_analysis(temp_file_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

#     try:
#         response = await mcda.upload_to_minio(output_files)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")

#     return JSONResponse(content=response)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from pathlib import Path
# from src.auth.jwthandler import get_current_user
# import src.crud.mcda_crud as mcda

# router = APIRouter()

# @router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
# async def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):

#     temp_file_path = Path("/tmp") / file.filename
#     with temp_file_path.open("wb") as buffer:
#         buffer.write(await file.read())

#     try:
#         buffered_files = await mcda.perform_buffer_analysis(temp_file_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

#     try:
#         rasterized_file = await mcda.rasterize_vector(buffered_files)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Rasterization failed: {str(e)}")

#     try:
#         response = await mcda.upload_to_minio([rasterized_file])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")

#     return JSONResponse(content=response)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from pathlib import Path
# from src.auth.jwthandler import get_current_user
# import src.crud.mcda_crud as mcda

# router = APIRouter()

# @router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
# async def upload_file(
#     dang_shapefile: UploadFile=File(...),
#     dang_road: UploadFile = File(...),
#     dang_river: UploadFile = File(...),
#     dang_settlement: UploadFile = File(...),
#     rasterfile: UploadFile = File(...),
#     current_user=Depends(get_current_user)
# ):
#     temp_masking_shp = Path("/tmp") / dang_shapefile.filename
#     with temp_masking_shp.open("wb") as buffer:
#         buffer.write(await dang_shapefile.read())
        
#     temp_road_path = Path("/tmp") / dang_road.filename
#     with temp_road_path.open("wb") as buffer:
#         buffer.write(await dang_road.read())

#     temp_river_path = Path("/tmp") / dang_river.filename
#     with temp_river_path.open("wb") as buffer:
#         buffer.write(await dang_river.read()) 

#     temp_settlement_path = Path("/tmp") / dang_settlement.filename
#     with temp_settlement_path.open("wb") as buffer:
#         buffer.write(await dang_settlement.read())

    
#     temp_rasterfile_path = Path("/tmp") / rasterfile.filename
#     with temp_rasterfile_path.open("wb") as buffer:
#         buffer.write(await rasterfile.read())

#     try:
#         buffered_road = await mcda.perform_buffer_analysis(temp_road_path)
#         buffered_river = await mcda.perform_buffer_analysis(temp_river_path)
#         buffered_settlement = await mcda.perform_buffer_analysis(temp_settlement_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

#     try:
#         rasterized_road = await mcda.rasterize_vector(buffered_road, temp_rasterfile_path)
#         rasterized_river = await mcda.rasterize_vector(buffered_river, temp_rasterfile_path)
#         rasterized_settlement = await mcda.rasterize_vector(buffered_settlement, temp_rasterfile_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Rasterization failed: {str(e)}")
    
#     try:
#         rasterized_road_mask = await mcda.mask_raster(rasterized_road, temp_masking_shp)
#         rasterized_river_mask = await mcda.mask_raster(rasterized_river, temp_masking_shp)
#         rasterized_settlement_mask = await mcda.mask_raster(rasterized_settlement, temp_masking_shp)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Masking failed: {str(e)}")
    
#     # try:
#     #     response = await mcda.upload_to_minio([rasterized_road])
#     #     response = await mcda.upload_to_minio([rasterized_river])
#     #     response = await mcda.upload_to_minio([rasterized_settlement])
#     # except Exception as e:
#     #     raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")
    
#     try:
#         response = await mcda.upload_to_minio([rasterized_road_mask])
#         response = await mcda.upload_to_minio([rasterized_river_mask])
#         response = await mcda.upload_to_minio([rasterized_settlement_mask])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")

#     return JSONResponse(content=response)



# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from pathlib import Path
# from src.auth.jwthandler import get_current_user
# import src.crud.mcda_crud as mcda
# from typing import List

# router = APIRouter()

# @router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
# async def upload_file(
#     dang_shapefile: UploadFile = File(...),
#     river_shapefile: UploadFile = File(...),
#     road_shapefile: UploadFile = File(...),
#     settlement_shapefile: UploadFile = File(...),
#     rasterfile: UploadFile = File(...),
#     current_user=Depends(get_current_user)
# ):
#     temp_Dangsh_path = Path("/tmp") / dang_shapefile.filename
#     with temp_Dangsh_path.open("wb") as boundary:
#         boundary.write(await dang_shapefile.read())

#     temp_riversh_path = Path("/tmp") / river_shapefile.filename
#     with temp_riversh_path.open("wb") as buffer:
#         buffer.write(await river_shapefile.read())

#     temp_roadsh_path = Path("/tmp") / road_shapefile.filename
#     with temp_roadsh_path.open("wb") as buffer:
#         buffer.write(await road_shapefile.read())
    
#     temp_settlementsh_path = Path("/tmp")/settlement_shapefile.filename
#     with temp_settlementsh_path.open("wb") as buffer:
#         buffer.write(await settlement_shapefile.read())

#     temp_rasterfile_path = Path("/tmp") / rasterfile.filename
#     with temp_rasterfile_path.open("wb") as buffer:
#         buffer.write(await rasterfile.read())

#     try:
#         buffered_river = await mcda.perform_buffer_analysis(temp_riversh_path)
#         buffered_road = await mcda.perform_buffer_analysis(temp_roadsh_path)
#         buffered_settlement = await mcda.perform_buffer_analysis(temp_settlementsh_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

#     try:
#         rasterized_river = await mcda.rasterize_vector(buffered_river, temp_rasterfile_path)
#         rasterized_road = await mcda.rasterize_vector(buffered_road, temp_rasterfile_path)
#         rasterized_settlement = await mcda.rasterize_vector(buffered_settlement, temp_rasterfile_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Rasterization failed: {str(e)}")
    
#     try:
#         masked_river = await mcda.mask_raster(rasterized_river, temp_Dangsh_path)
#         masked_road = await mcda.mask_raster(rasterized_road, temp_Dangsh_path)
#         masked_settlement = await mcda.mask_raster(rasterized_settlement,temp_Dangsh_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Masking failed: {str(e)}")

#     try:
#         response = await mcda.upload_to_minio([masked_river])
#         response = await mcda.upload_to_minio([masked_road])
#         response = await mcda.upload_to_minio([masked_settlement])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")
#     return JSONResponse(content=response)


# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
# from fastapi.responses import JSONResponse
# from pathlib import Path
# from typing import List
# import src.crud.mcda_crud as mcda
# from src.auth.jwthandler import get_current_user
# router = APIRouter()

# @router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
# async def upload_file(
#     dang_shapefile: UploadFile = File(...),
#     river_shapefile: UploadFile = File(...),
#     road_shapefile: UploadFile = File(...),
#     settlement_shapefile: UploadFile = File(...),
#     rasterfile: UploadFile = File(...),
#     weights: List[float] = Form(...),
#     current_user=Depends(get_current_user)
# ):

#     temp_Dangsh_path = Path("/tmp") / dang_shapefile.filename
#     with temp_Dangsh_path.open("wb") as boundary:
#         boundary.write(await dang_shapefile.read())

#     temp_riversh_path = Path("/tmp") / river_shapefile.filename
#     with temp_riversh_path.open("wb") as buffer:
#         buffer.write(await river_shapefile.read())

#     temp_roadsh_path = Path("/tmp") / road_shapefile.filename
#     with temp_roadsh_path.open("wb") as buffer:
#         buffer.write(await road_shapefile.read())
    
#     temp_settlementsh_path = Path("/tmp") / settlement_shapefile.filename
#     with temp_settlementsh_path.open("wb") as buffer:
#         buffer.write(await settlement_shapefile.read())

#     temp_rasterfile_path = Path("/tmp") / rasterfile.filename
#     with temp_rasterfile_path.open("wb") as buffer:
#         buffer.write(await rasterfile.read())

#     # Perform buffer analysis
#     try:
#         buffered_river = await mcda.perform_buffer_analysis(temp_riversh_path)
#         buffered_road = await mcda.perform_buffer_analysis(temp_roadsh_path)
#         buffered_settlement = await mcda.perform_buffer_analysis(temp_settlementsh_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

#     # Perform rasterization
#     try:
#         rasterized_river = await mcda.rasterize_vector(buffered_river, temp_rasterfile_path)
#         rasterized_road = await mcda.rasterize_vector(buffered_road, temp_rasterfile_path)
#         rasterized_settlement = await mcda.rasterize_vector(buffered_settlement, temp_rasterfile_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Rasterization failed: {str(e)}")
    
#     # Perform masking
#     try:
#         masked_river = await mcda.mask_raster(rasterized_river, temp_Dangsh_path)
#         masked_road = await mcda.mask_raster(rasterized_road, temp_Dangsh_path)
#         masked_settlement = await mcda.mask_raster(rasterized_settlement, temp_Dangsh_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Masking failed: {str(e)}")

#     # Perform weighted overlay
#     try:
#         weighted_overlay_result = await mcda.weighted_overlay(
#             masked_settlement, masked_river, masked_road, weights
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Weighted overlay failed: {str(e)}")

#     # Upload result to Minio
#     try:
#         response = await mcda.upload_to_minio([weighted_overlay_result])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")
    
#     return JSONResponse(content=response)


from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pathlib import Path
from src.auth.jwthandler import get_current_user
import src.crud.mcda_crud as mcda
from typing import List

router = APIRouter()

@router.post("/api/mcda/upload", tags=['MCDA'], dependencies=[Depends(get_current_user)])
async def upload_file(
    dang_shapefile: UploadFile = File(...),
    river_shapefile: UploadFile = File(...),
    road_shapefile: UploadFile = File(...),
    settlement_shapefile: UploadFile = File(...),
    rasterfile: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    temp_Dangsh_path = Path("/tmp") / dang_shapefile.filename
    with temp_Dangsh_path.open("wb") as boundary:
        boundary.write(await dang_shapefile.read())

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
        buffered_river = await mcda.perform_buffer_analysis(temp_riversh_path)
        buffered_road = await mcda.perform_buffer_analysis(temp_roadsh_path)
        buffered_settlement = await mcda.perform_buffer_analysis(temp_settlementsh_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Buffer analysis failed: {str(e)}")

    try:
        rasterized_river = await mcda.rasterize_vector(buffered_river, temp_rasterfile_path)
        rasterized_road = await mcda.rasterize_vector(buffered_road, temp_rasterfile_path)
        rasterized_settlement = await mcda.rasterize_vector(buffered_settlement, temp_rasterfile_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rasterization failed: {str(e)}")
    try:
        masked_river = await mcda.mask_raster(rasterized_river, temp_Dangsh_path)
        masked_road = await mcda.mask_raster(rasterized_road, temp_Dangsh_path)
        masked_settlement = await mcda.mask_raster(rasterized_settlement,temp_Dangsh_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Masking failed: {str(e)}")
    try:
        river_response = await mcda.upload_to_minio([masked_river])
        road_response = await mcda.upload_to_minio([masked_road])
        settlement_response = await mcda.upload_to_minio([masked_settlement])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")

    return JSONResponse(content={"river_response": river_response, "road_response": road_response, "settlement_response": settlement_response})

@router.post("/api/mcda/weighted_overlay", tags=['MCDA'], dependencies=[Depends(get_current_user)])
async def weighted_overlay(
    river_weight: float,
    road_weight: float,
    settlement_weight: float,
    current_user=Depends(get_current_user)
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
        overlay_result_path = await mcda.perform_weighted_overlay(raster_urls, weights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weighted overlay analysis failed: {str(e)}")
    
    try:
        response = await mcda.upload_to_minio([overlay_result_path])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload to Minio failed: {str(e)}")
