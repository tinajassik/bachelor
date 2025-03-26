import os
from api import skraafoto
from PIL import Image
import math
from data import data_access
import re

images_to_split_path = os.path.join("..", "data", "skraafoto_images")

def fetch_image(item_id):
    data = skraafoto.fetch_skraafoto_item(item_id)

    img_url = data["assets"]["data"]["href"]
    img_data = skraafoto.get_image_from_url(img_url).content

    save_dir = os.path.join(images_to_split_path, item_id)
    os.makedirs(save_dir, exist_ok=True)

    img_path = os.path.join(save_dir, f"{item_id}.tif")
    with open(img_path, "wb") as f:
        f.write(img_data)

    print(f"Downloaded: {img_path}")
    return img_path

def extract_tiles(item_id):
    image_path = os.path.join(images_to_split_path, item_id, item_id + ".tif")
    image = Image.open(image_path)
    img_width, img_height = image.size
    tile_width = math.ceil(img_width * 0.10)
    tile_height = math.ceil(img_height * 0.10)

    tiles_dir = os.path.join(os.path.dirname(image_path), "tiles")
    os.makedirs(tiles_dir, exist_ok=True)

    max_cols, max_rows = math.ceil(img_width / tile_width), math.ceil(img_height / tile_height)
    num_tiles = max_cols * max_rows

    item_metadata = {"item_id":item_id,
                     "img_width":img_width,
                     "img_height":img_height}

    data_access.save_fetched_item(item_id, item_metadata,"split_tiles")


    for row in range(max_rows):
        for col in range(max_cols):
            x_min = col * tile_width
            y_min = row * tile_height
            x_max = min(x_min + tile_width, img_width)
            y_max = min(y_min + tile_height, img_height)

            tile_filename = os.path.join(tiles_dir, f"{item_id}-{x_min}-{y_min}.jpg")
            cropped_image = image.crop((x_min, y_min, x_max, y_max))
            cropped_image.save(tile_filename)

            metadata = {
                "tile_filename": tile_filename,
                "tile_width": tile_width,
                "tile_height": tile_height,
                "bbox": {
                    "x_min": x_min,
                    "y_min": y_min,
                    "x_max": x_max,
                    "y_max": y_max
                },
                "grid_column": col,
                "grid_row": row
            }
            tile_id = f"{x_min}-{y_min}"
            data_access.add_tile_to_item(item_id, metadata, tile_id)


    print(f"{num_tiles} tiles saved successfully for {item_id}.")

def find_pixel_position(tile_filename, pixel_x, pixel_y):
    parts = re.split(r'[-.]', tile_filename)
    x_min = int(parts[1])
    y_min = int(parts[2])

    pixel_pos_x = x_min + pixel_x
    pixel_pos_y = y_min + pixel_y
    return pixel_pos_x,pixel_pos_y
