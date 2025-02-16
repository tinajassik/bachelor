import os
import requests

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
    return response.json();

def get_image_from_url(img_url): 
    return requests.get(img_url)