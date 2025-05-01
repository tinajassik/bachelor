import requests
from fastapi import HTTPException 
from services import skraafoto

def fetch_skraafoto_item(item_id: str):
    """
    Fetches metadata for a Skraafoto image by its item ID.
    Handles all exceptions and converts them to HTTPException for API layer.
    """
    try:
        return skraafoto.fetch_skraafoto_item(item_id)

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        detail = e.response.text if e.response else str(e)
        raise HTTPException(status_code=status_code, detail=f"Skraafoto API error: {detail}")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail="Failed to connect to Skraafoto API")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
def fetch_skraafoto_thumbnail(tif_url: str):
    """
    Fetches a thumbnail JPEG image from the Skraafoto API given a TIF URL.
    Handles all exceptions and raises HTTPException for use in the API layer.
    """
    try:
        return skraafoto.fetch_skraafoto_image_thumbnail(tif_url)

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        detail = e.response.text if e.response else str(e)
        raise HTTPException(status_code=status_code, detail=f"Skraafoto API error: {detail}")

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="Failed to connect to Skraafoto API")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")