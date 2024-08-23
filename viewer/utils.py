import rasterio

def get_raster_data(file_path):
    with rasterio.open(file_path) as src:
        return {
            "bounds": src.bounds,
            "width": src.width,
            "height": src.height,
            "crs": src.crs.to_string(),
        }
