import os 
from services import skraafoto
from utils import image_handler

tif_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "images_for_frontend"))

def get_or_fetch_image_by_id(stac_item_id) -> str: 
    """
    Check if the .tif image exists locally; if not, fetch and save it.
    Returns the path to the image file.
    """
    os.makedirs(tif_images_dir, exist_ok=True)

    file_name = f"{stac_item_id}.tif"
    file_path = os.path.join(tif_images_dir, file_name)

    if os.path.exists(file_path):
        print(f"[✓] Tiff image for given ID found: {file_path}")
        return file_path
    
    item_json = skraafoto.fetch_skraafoto_item(stac_item_id)
    img_url = image_handler.extract_selected_image(item_json)
    response = skraafoto.get_image_from_url(img_url)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"[+] Saved to: {file_path}")
        return file_path
    else:
        raise Exception(f"Image not found or failed to download: {img_url} (Status {response.status_code})")