import os
from typing import List 
from services import skraafoto
from utils import image_handler
from utils import tile_splitter_stat

TIF_IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "skraafoto_images"))

def get_or_fetch_image_by_id(stac_item_id) -> str: 
    """
    Check if the .tif image exists locally; if not, fetch and save it.
    Returns the path to the image file.
    """
    base_dir = os.path.join(TIF_IMAGES_DIR, stac_item_id)
    os.makedirs(TIF_IMAGES_DIR, exist_ok=True)

    file_name = f"{stac_item_id}.tif"
    file_path = os.path.join(TIF_IMAGES_DIR, stac_item_id, file_name)

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
    
def get_cropped_images(stac_item_id) -> List[str]:
    """
    Returns a list of paths to all cropped images for an item defined by stac item id.
    """
    base_dir = os.path.join(TIF_IMAGES_DIR, stac_item_id)

    if not os.path.exists(base_dir):
        tile_splitter_stat.fetch_image(stac_item_id)
    
    base_dir = os.path.join(TIF_IMAGES_DIR, stac_item_id, "tiles")

    if not os.path.exists(base_dir):
        tile_splitter_stat.extract_tiles(stac_item_id)
        
    img_paths = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".png"):
                img_paths.append(os.path.join(root, file))
    return img_paths