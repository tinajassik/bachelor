from fastapi import APIRouter, HTTPException
import requests
import os
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


# @router.get("/fetch/bbox")
# def fetch_skraafoto_item_bbox(lat1: float, lon1: float, lat2: float, lon2: float, limit: int = 10):
#     """
#     Fetches Skraafoto images within a bounding box defined by two latitude/longitude points.
    
#     Args:
#         lat1 (float): Latitude of the bottom-left corner.
#         lon1 (float): Longitude of the bottom-left corner.
#         lat2 (float): Latitude of the top-right corner.
#         lon2 (float): Longitude of the top-right corner.
#         limit (int): Number of results to retrieve. Default is 10.
    
#     Returns:
#         dict: JSON response from the API.
#     """
#     bbox = [lon1, lat1, lon2, lat2]
#     params = {
#         "bbox": ",".join(map(str, bbox)),
#         "limit": limit
#     }

#     headers = HEADERS.copy()
#     headers["Content-Type"] = "application/geo+json"
    
#     response = requests.get(BASE_SEARCH_URL, params=params, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HTTPException(status_code=response.status_code, detail=f"Error fetching bounding box items: {response.text}")


# @router.get("/fetch/image")
# def get_image_from_url(img_url: str):
#     """
#     Fetches an image from a given URL.
    
#     Args:
#         img_url (str): The direct URL to the image.
    
#     Returns:
#         bytes: The image content.
#     """
#     response = requests.get(img_url)

#     if response.status_code == 200:
#         return response.content
#     else:
#         raise HTTPException(status_code=response.status_code, detail="Failed to fetch image.")
