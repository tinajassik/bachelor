from fastapi import HTTPException
from services import skraafoto
from model import GeoLocation  
from georeferencing import pixel_to_latlong
from utils import plots
import traceback

def get_geolocation_for_pixel(item_id: str, pixel_x: int, pixel_y: int) -> dict:
    """
    Given a pixel location and a Skraafoto image item_id, compute and return geographic coordinates
    and a generated map showing the projected point.
    """
    try:
        tile = pixel_to_latlong.get_tile_for_pixel(pixel_x, pixel_y, item_id)
        geo_location = pixel_to_latlong.convert_pixel_to_world_homography(pixel_x, pixel_y, tile['homography'])
        bbox = skraafoto.fetch_skraafoto_item(item_id)['bbox']

        plots.generate_map_with_projected_point(
            lat=geo_location[1], lon=geo_location[0], bbox=bbox, file_name="projected_point_map"
        )

        return GeoLocation(geo_location[0],geo_location[1], "http://localhost:8000/static/maps/projected_point_map.html").to_dict();


    except Exception as e:
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
