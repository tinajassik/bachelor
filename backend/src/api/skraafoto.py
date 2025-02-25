import os
import requests
from fastapi import APIRouter, HTTPException

# Initialize API router
router = APIRouter()

# API base URLs
BASE_ITEM_URL = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/collections/skraafotos2023/items/"
BASE_SEARCH_URL = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/search"

# Load API token from environment variables
API_KEY = os.getenv("SKRAAFOTO_TOKEN")

if not API_KEY:
    raise ValueError("API token is missing. Ensure the .env file contains SKRAAFOTO_TOKEN.")

# general API headers
HEADERS = {
    "token": API_KEY
}

@router.get("/test")  
def test_route():
    return {"message": "Skraafoto API is working!"}

@router.get("/fetch/item/{item_id}")
def fetch_skraafoto_item(item_id: str):
    """
    Fetches an item from the Skraafoto API based on the given item ID.

    :param item_id: The unique identifier of the item.
    :param headers: Headers for the request 
    :return: JSON response if the request is successful, else None.
    """
    url = f"{BASE_ITEM_URL}{item_id}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching item: {response.text}")


@router.get("/fetch/bbox")
def fetch_skraafoto_item_bbox(lat1: float, lon1: float, lat2: float, lon2: float, limit: int = 10):
    """
    Fetches Skraafoto images within a bounding box defined by two latitude/longitude points.
    
    Args:
        lat1 (float): Latitude of the bottom-left corner.
        lon1 (float): Longitude of the bottom-left corner.
        lat2 (float): Latitude of the top-right corner.
        lon2 (float): Longitude of the top-right corner.
        limit (int): Number of results to retrieve. Default is 10.
    
    Returns:
        dict: JSON response from the API.
    """
    bbox = [lon1, lat1, lon2, lat2]
    params = {
        "bbox": ",".join(map(str, bbox)),
        "limit": limit
    }

    headers = HEADERS.copy()
    headers["Content-Type"] = "application/geo+json"
    
    response = requests.get(BASE_SEARCH_URL, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching bounding box items: {response.text}")


@router.get("/fetch/image")
def get_image_from_url(img_url: str):
    """
    Fetches an image from a given URL.
    
    Args:
        img_url (str): The direct URL to the image.
    
    Returns:
        bytes: The image content.
    """
    response = requests.get(img_url)

    if response.status_code == 200:
        return response.content
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch image.")
