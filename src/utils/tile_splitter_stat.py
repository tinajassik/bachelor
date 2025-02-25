import os
import json
from api import skraafoto
from PIL import Image

def load_metadata(metadata_file):
    """Loads the existing metadata file or creates a new one."""
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f)
    return {}

def save_metadata(metadata, metadata_file):
    """Saves metadata to a single JSON file."""
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

def fetch_image(item_id, metadata_file):
    metadata = load_metadata(metadata_file)
    data = skraafoto.fetch_skraafoto_item(item_id)

    img_url = data["assets"]["data"]["href"]
    img_data = skraafoto.get_image_from_url(img_url).content

    save_dir = os.path.join("..", "data", "skraafoto_images", item_id)
    os.makedirs(save_dir, exist_ok=True)

    img_path = os.path.join(save_dir, f"{item_id}.tif")
    with open(img_path, "wb") as f:
        f.write(img_data)

    bbox = data.get("bbox", [])
    metadata[item_id] = {"item_id": item_id, "bbox": bbox, "tiles": []}

    save_metadata(metadata, metadata_file)
    print(f"Downloaded: {img_path} with metadata.")
    return img_path

def extract_tiles(image_path, item_id, metadata_file, tile_size=1000, num_tiles=10):
    image = Image.open(image_path)
    width, height = image.size
    metadata = load_metadata(metadata_file)

    if item_id not in metadata:
        print(f"Skipping {item_id} (metadata missing).")
        return

    tiles_dir = os.path.join(os.path.dirname(image_path), "tiles")
    os.makedirs(tiles_dir, exist_ok=True)

    max_cols, max_rows = width // tile_size, height // tile_size
    total_possible_tiles = max_cols * max_rows
    num_tiles = min(num_tiles, total_possible_tiles)

    tile_positions = [(col * tile_size, row * tile_size) for row in range(max_rows) for col in range(max_cols)][:num_tiles]
    metadata[item_id]["tiles"] = []

    for i, (x, y) in enumerate(tile_positions):
        tile_filename = os.path.join(tiles_dir, f"tile_{i+1}.jpg")
        cropped_image = image.crop((x, y, x + tile_size, y + tile_size))
        cropped_image.save(tile_filename)
        metadata[item_id]["tiles"].append({
            "tile_id": i+1,
            "tile_filename": tile_filename,
            "bbox": {"x_min": x, "y_min": y, "x_max": x + tile_size, "y_max": y + tile_size}
        })

    save_metadata(metadata, metadata_file)
    print(f"{num_tiles} tiles saved successfully for {item_id}.")

def extract_tiles_for_all_images(metadata_file, tile_size=1000, num_tiles=10):
    metadata = load_metadata(metadata_file)
    for item_id in metadata.keys():
        image_path = os.path.join("..", "data", "skraafoto_images", item_id, f"{item_id}.tif")
        if os.path.exists(image_path):
            extract_tiles(image_path, item_id, metadata_file, tile_size, num_tiles)
        else:
            print(f"Skipping {item_id} (image missing).")
