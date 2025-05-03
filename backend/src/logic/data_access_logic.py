from data import data_access, image_access
from fastapi import HTTPException, Response
from utils import image_handler

def get_all_processed_stac_item_ids():
    """
    Fetches all processed STAC item IDs from the data access layer.
    """
    try:
        return data_access.get_all_stac_ids()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while loading data: {str(e)}")

def get_stac_item_jpeg(item_id: str) -> Response:
    """
    Retrieves a JPEG image for a given STAC item ID.
    Converts TIFF to JPEG if necessary and returns as an HTTP response.
    """
    try:
        image_path = image_access.get_or_fetch_image_by_id(item_id)
        img_jpeg = image_handler.convert_tiff_to_jpeg(image_path)
        return Response(content=img_jpeg, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while retrieving an image from Skraafoto: {str(e)}")