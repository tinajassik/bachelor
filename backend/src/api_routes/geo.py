from fastapi import APIRouter, HTTPException, Response
import requests
from services import skraafoto
from georeferencing import pixel_to_latlong
from model import GeoLocation
from utils import plots, image_handler
from data import data_access, image_access

router = APIRouter()

@router.get("/test")  
def test_route():
    return {"message": "Python Backend API is working! xixi"}

@router.get("/item")
def fetch_skraafoto_item(item_id: str):
    """
    Fetches an item from the Skraafoto API based on the given item ID.
    Returns appropriate HTTP status codes on failure.
    """
    try:
        return skraafoto.fetch_skraafoto_item(item_id)
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        detail = e.response.text if e.response else str(e)
        raise HTTPException(status_code=status_code, detail=detail)

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail="Failed to connect to Skraafoto API")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/thumbnail")
def fetch_skraafoto_image_thumbnail(tif_url: str):
    """
    Fetches a a thumbnail jpg image from the Skraafoto API based on the given tif URL.
    Returns appropriate HTTP status codes on failure.
    """
    try:
        return skraafoto.fetch_skraafoto_image_thumbnail(tif_url)
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        detail = e.response.text if e.response else str(e)
        raise HTTPException(status_code=status_code, detail=detail)

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail="Failed to connect to Skraafoto API")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/location")
def get_geolocation_for_pixels(item_id: str, pixel_x: int, pixel_y: int):
    """
    Retrives geographic coordinates for specified pixels on a given image. Image is specified by item_id. 
    Generates html with the transformed coordinates. 
    """
    try:
        tile = pixel_to_latlong.get_tile_for_pixel(pixel_x, pixel_y, item_id);
        geo_location = pixel_to_latlong.convert_pixel_to_world_homography(pixel_x, pixel_y, tile['homography'])
        bbox = skraafoto.fetch_skraafoto_item(item_id)['bbox'];
        plots.generate_map_with_projected_point(geo_location[1], geo_location[0], bbox,"projected_point_map");
        return GeoLocation(geo_location[0],geo_location[1], "http://localhost:8000/static/maps/projected_point_map.html").to_dict();

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/items")
def get_processed_stac_item_ids():
    """
    Retrieves a list of processed STAC Item ids. 
    """
    try:
        return data_access.get_all_stac_ids();

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    
@router.get("/image")
def get_stac_item_image(item_id):
    """
    Retrieves a jpeg image of the selected location. If image is saved locally, it read bytes and returns them, else fetches an image from Skraafoto. 
    """
    try:
        image_path = image_access.get_or_fetch_image_by_id(item_id)
        img_jpeg = image_handler.convert_tiff_to_jpeg(image_path)
        return Response(content=img_jpeg, media_type="image/jpeg")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while retrieving an image from Skraafoto: {e}")
