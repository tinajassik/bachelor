from fastapi import APIRouter, HTTPException
import requests
from services import skraafoto

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
