import os
import requests
import json
import pyproj
from dotenv import load_dotenv


def fetch_skraafoto_item(item_id):
    """
    Fetches an item from the Skraafoto API based on the given item ID.

    :param item_id: The unique identifier of the item.
    :param headers: Headers for the request 
    :return: JSON response if the request is successful, else None.
    """

    headers = {
        'token': os.getenv("SKRAAFOTO_TOKEN")
    }     

    base_url = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/collections/skraafotos2023/items/"
    url = f"{base_url}{item_id}"
    
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json()

def get_image_from_url(img_url): 
    return requests.get(img_url)


def fetch_skraafoto_item_bbox(lat1, lon1, lat2, lon2, limit=10):
    """
    Fetches Skraafoto images within a bounding box defined by two latitude/longitude points.
    Reads API credentials from a .env file.
    
    Args:
        lat1 (float): Latitude of bottom-left corner.
        lon1 (float): Longitude of bottom-left corner.
        lat2 (float): Latitude of top-right corner.
        lon2 (float): Longitude of top-right corner.
        limit (int): Number of results to retrieve. Default is 10.
    
    Returns:
        dict: JSON response from the API.
    """
    # Load environment variables
    API_URL = "https://api.dataforsyningen.dk/rest/skraafoto_api/v1.0/search"
    TOKEN = os.getenv("SKRAAFOTO_TOKEN")
    
    if not TOKEN:
        raise ValueError("API token is missing. Ensure the .env file contains SKRAAFOTO_TOKEN.")
    
    # Define bounding box
    bbox = [lon1, lat1, lon2, lat2]
    
    # API request parameters
    params = {
        "bbox": ",".join(map(str, bbox)),
        "limit": limit
    }
    
    # API headers
    headers = {
        "token": TOKEN,
        "Content-Type": "application/geo+json"
    }
    
    # Send API request
    response = requests.get(API_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
