import geopandas as gpd

def process_shapefile(shapefile_path: str) -> dict:
    try:
        gdf = gpd.read_file(shapefile_path)
        zone_col = next((col for col in ['zone_type', 'ZoneName', 'ZoneCode'] if col in gdf.columns), None)
        if zone_col:
            zone_summary = gdf[zone_col].value_counts().to_dict()
        else:
            zone_summary = {"Unknown": len(gdf)}

        return {
            "status": "success",
            "total_features": len(gdf),
            "zone_summary": zone_summary
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
