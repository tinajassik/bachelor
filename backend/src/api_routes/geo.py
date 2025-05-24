from fastapi import APIRouter, File, UploadFile
from logic import skraafoto_logic, georeferencing_logic, data_access_logic, car_detection_logic

router = APIRouter()

@router.get("/test")  
def test_route():
    return {"message": "Python Backend API is working! xixi"}

@router.get("/item")
def fetch_skraafoto_item(item_id: str):
    """
    Fetches an item from the Skraafoto API based on the given item ID.
    """
    return skraafoto_logic.fetch_skraafoto_item(item_id)
   
    
@router.get("/thumbnail")
def fetch_skraafoto_image_thumbnail(tif_url: str):
    """
    Fetches a a thumbnail jpg image from the Skraafoto API based on the given tif URL.
    """
    return skraafoto_logic.fetch_skraafoto_thumbnail(tif_url)
    
    
@router.get("/location")
def get_geolocation_for_pixels(item_id: str, pixel_x: int, pixel_y: int):
    """
    Retrives geographic coordinates for specified pixels on a given image. Image is specified by item_id. 
    Generates html with the transformed coordinates. 
    """
    return georeferencing_logic.get_geolocation_for_pixel(item_id, pixel_x, pixel_y)

@router.get("/items")
def get_processed_stac_item_ids():
    """
    Retrieves a list of processed STAC Item ids. 
    """
    return data_access_logic.get_all_processed_stac_item_ids()

    
@router.get("/image")
def get_stac_item_image(item_id):
    """
    Retrieves a jpeg image of the selected location. If image is saved locally, it read bytes and returns them, else fetches an image from Skraafoto. 
    """
    return data_access_logic.get_stac_item_jpeg(item_id)

@router.post("/detect")
async def detect_cars(file: UploadFile = File(...)):
    """
    Runs a prediction on the car detection model. Returns detection predictions and projected geographic locations.
    """
    return await car_detection_logic.detect_cars(file)

@router.get("/images")
def get_cropped_images(item_id):
    """
    Crops an already fetched Skraafoto into smaller images and return them in a .ZIP folder.
    """
    return data_access_logic.get_cropped_images(item_id)
