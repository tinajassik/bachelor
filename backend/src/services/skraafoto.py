from http.client import HTTPException
import requests
from fastapi import Response
from config import SKRAAFOTO_TOKEN

HEADERS = {'token': SKRAAFOTO_TOKEN}     

def fetch_skraafoto_item(item_id):
    """
    Fetches an item from the Skraafoto API based on the given item ID.

    :param item_id: The unique identifier of the item.
    :param headers: Headers for the request 
    :return: JSON response if the request is successful, else None.
    """
    
    base_url = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/collections/skraafotos2023/items/"
    url = f"{base_url}{item_id}"
    
    response = requests.get(url, headers=HEADERS)

    response.raise_for_status()
    return response.json()

def fetch_skraafoto_image_thumbnail(tif_url: str):
    """
    Fetches a jpg image from the Skraafoto API based on the given tiff image url.

    :param: tif_url - url for the original tif image
    """
    token = SKRAAFOTO_TOKEN
    if not token:
        raise HTTPException(status_code=500, detail="Token missing")

    encoded_url = requests.utils.quote(tif_url, safe="")
    thumbnail_url = f"https://api.dataforsyningen.dk/rest/skraafoto_cogtiler/v1.0/thumbnail.jpg?url={encoded_url}"

    response = requests.get(thumbnail_url, headers=HEADERS, stream=True)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch thumbnail")

    return Response(content=response.content, media_type="image/jpeg")

def get_image_from_url(img_url): 
    return requests.get(img_url)

def fetch_skraafoto_item_bbox(lat1, lon1, lat2, lon2, limit=10):
    """
    Fetches Skraafoto images within a bounding box defined by two latitude/longitude points.
    
    Args:
        lat1 (float): Latitude of bottom-left corner.
        lon1 (float): Longitude of bottom-left corner.
        lat2 (float): Latitude of top-right corner.
        lon2 (float): Longitude of top-right corner.
        limit (int): Number of results to retrieve. Default is 10.
    
    Returns:
        dict: JSON response from the API.
    """
    API_URL = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/search"
    TOKEN = SKRAAFOTO_TOKEN
    
    if not TOKEN:
        raise ValueError("API token is missing. Ensure the .env file contains SKRAAFOTO_TOKEN.")
    
    bbox = [lon1, lat1, lon2, lat2]
    
    params = {
        "collections":"skraafotos2023",
        "bbox": ",".join(map(str, bbox)),
        "limit": limit
    }
    
    headers = {
        "token": TOKEN,
        "Content-Type": "application/geo+json",
    }
    
    response = requests.get(API_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")