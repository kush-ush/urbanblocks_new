import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import geopandas as gpd
from urbanblocks_pro.backend.app.core.zoning_engine import process_shapefile

router = APIRouter()

@router.post("/upload-shapefile/")
async def upload_shapefile(
    shp: UploadFile = File(...),
    shx: UploadFile = File(...),
    dbf: UploadFile = File(...),
    prj: UploadFile = File(...),
    filename: str = Form(...)
):
    # Step 1: Create folder to save all parts
    save_dir = os.path.join("data", "shapefiles", filename)
    os.makedirs(save_dir, exist_ok=True)

    # Step 2: Save all parts
    for f in [shp, shx, dbf, prj]:
        ext = os.path.splitext(f.filename)[1].lower()
        file_path = os.path.join(save_dir, filename + ext)
        try:
            with open(file_path, "wb") as out_file:
                out_file.write(await f.read())
        except Exception as e:
            return JSONResponse(content={"status": "error", "message": f"❌ Failed to save {f.filename}: {str(e)}"}, status_code=500)

    # Step 3: Read the shapefile
    shp_path = os.path.join(save_dir, filename + ".shp")
    try:
        gdf = gpd.read_file(shp_path)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"❌ Failed to read shapefile: {str(e)}"}, status_code=500)

    # Step 4: Save as GeoJSON
    geojson_path = os.path.join(save_dir, filename + ".geojson")
    try:
        gdf.to_file(geojson_path, driver='GeoJSON')
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"❌ GeoJSON conversion failed: {str(e)}"}, status_code=500)

    # Step 5: Process zones
    zone_info = process_shapefile(shp_path)

    # ✅ Done
    return {
        "status": "success",
        "message": f"✅ '{filename}' processed successfully!",
        "num_features": len(gdf),
        "columns": gdf.columns.tolist(),
        "geojson_path": geojson_path,
        "zone_info": zone_info
    }
