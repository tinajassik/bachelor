import os
from services import skraafoto
from PIL import Image
import math
import re
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

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

def fetch_images_by_bbox(lat1=55.61372384290898, lon1=12.374812877864615, lat2=55.72902270965818, lon2=12.579909089919651, limit=50):
    """
    Fetches a number of items (limit) within the specified bounding box. The intial coordinates are located in Copenhagen.
    """
    if limit > 1000:
        print(f"Limit: {limit} exceeds 1000. The number of fetched images will be reduced to 1000")
    limit = min(limit, 1000)
    images_id = []
    
    data = skraafoto.fetch_skraafoto_item_bbox (lat1, lon1, lat2, lon2, limit)
    matched = data["context"]["matched"]

    if matched < limit:
        print(f"Only {matched} image(s) matched your query — less than the requested limit of {limit}.")

    for feature in data["features"]:
        item_id = feature["id"]
        img_url = feature["assets"]["data"]["href"]

        img_data = skraafoto.get_image_from_url(img_url).content

        save_dir = os.path.join(images_to_split_path, item_id)
        os.makedirs(save_dir, exist_ok=True)

        img_path = os.path.join(save_dir, f"{item_id}.tif")
        images_id.append(item_id)
        with open(img_path, "wb") as f:
            f.write(img_data)

    return images_id
    

def extract_tiles(item_id, grid_scale=0.04):
    image_path = os.path.join(images_to_split_path, item_id, item_id + ".tif")
    image = Image.open(image_path)
    img_width, img_height = image.size
    tile_width = math.ceil(img_width * grid_scale)
    tile_height = math.ceil(img_height * grid_scale)

    tiles_dir = os.path.join(os.path.dirname(image_path), "tiles")
    os.makedirs(tiles_dir, exist_ok=True)

    max_cols, max_rows = math.ceil(img_width / tile_width), math.ceil(img_height / tile_height)
    num_tiles = max_cols * max_rows

    for row in range(max_rows):
        for col in range(max_cols):
            x_min = col * tile_width
            y_min = row * tile_height
            x_max = min(x_min + tile_width, img_width)
            y_max = min(y_min + tile_height, img_height)

            tile_filename = os.path.join(tiles_dir, f"{item_id}-{x_min}-{y_min}.png")
            cropped_image = image.crop((x_min, y_min, x_max, y_max))
            cropped_image.save(tile_filename)

    print(f"{num_tiles} tiles saved successfully for {item_id}.")

def find_pixel_position(tile_filename, pixel_x, pixel_y, image_height):
    parts = re.split(r'[-.]', tile_filename)
    x_min = int(parts[1])
    y_min = int(re.split(r'[_]', parts[2])[0])

    pixel_pos_x = x_min + pixel_x
    pixel_pos_y_image = y_min + pixel_y

    # flip Y from top-left origin to bottom-left origin
    pixel_pos_y = image_height - pixel_pos_y_image
    return pixel_pos_x,pixel_pos_y
