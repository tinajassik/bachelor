from fastapi import HTTPException
from services import skraafoto
from model import GeoLocation, GeoLocations
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


def get_geolocations_for_pixels(item_id: str, pixel_coords: list[tuple[int, int]]) -> dict:
    """
    Given a list of pixel (x, y) pairs and a Skraafoto image item_id, compute and return a list of geographic coordinates
    and generate a map with all the projected points.
    """
    try:
        latlon_points = []

        bbox = skraafoto.fetch_skraafoto_item(item_id)['bbox']

        for (pixel_x, pixel_y) in pixel_coords:
            tile = pixel_to_latlong.get_tile_for_pixel(pixel_x, pixel_y, item_id)
            geo_location = pixel_to_latlong.convert_pixel_to_world_homography(pixel_x, pixel_y, tile['homography'])
            latlon_points.append((geo_location[1], geo_location[0])) 

        plots.generate_map_with_projected_points(
            points=[(lat, lon) for lat, lon in latlon_points],
            bbox=bbox,
            file_name="projected_points_map"
        )

        return GeoLocations(geolocations=latlon_points, map_url="http://localhost:8000/static/maps/projected_points_map.html").to_dict()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

