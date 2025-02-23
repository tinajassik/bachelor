import numpy as np
import cv2
from PIL import Image
import io
import numpy as np
from georeferencing.latlong_to_pixel import latlon_to_pixel

def compute_homography(pixels, world_coords):
    """
    Computes homography matrix H that maps 2D image pixels to 2D world coordinates.

    :param pixels: List of (x, y) image points.
    :param world_coords: List of corresponding (X, Y) world coordinates.
    :return: 3x3 homography matrix H.
    """
    pixels = np.array(pixels, dtype=np.float32)
    world_coords = np.array(world_coords, dtype=np.float32)

    H, _ = cv2.findHomography(pixels, world_coords, method=cv2.RANSAC)
    return H

def convert_pixel_to_world_homography(x, y, H):
    """
    Uses homography matrix H to convert image pixel (x, y) to world coordinates (X, Y).

    :param x: Pixel x-coordinate
    :param y: Pixel y-coordinate
    :param H: homography matrix
    :return: (X, Y) world coordinates
    """
    pixel_homog = np.array([x, y, 1], dtype=np.float32).reshape(3, 1)
    world_homog = H @ pixel_homog  # apply homography
    world_x = world_homog[0, 0] / world_homog[2, 0]
    world_y = world_homog[1, 0] / world_homog[2, 0]

    return world_x, world_y

def generate_real_world_points(lon_min, lat_min, lon_max, lat_max, num_points=10):
    """
    Generates real-world latitude and longitude points inside a tile's bounding box.
    
    :param lon_min, lat_min, lon_max, lat_max: Tile bbox 
    :param num_points: Number of real-world points to generate
    :return: NumPy array of (lon, lat) real-world coordinates
    """
    lon_values = np.random.uniform(lon_min, lon_max, num_points)
    lat_values = np.random.uniform(lat_min, lat_max, num_points)
    
    return np.column_stack((lon_values, lat_values))

def split_image_and_compute_homographies(img, skraafoto_item_json, num_points=10):
    """
    Splits an image into 4 tiles and computes homographies.

    :param img: PIL Image or image bytes
    :param skraafoto_item_json: Skraafoto STAC item  
    :param num_points: Number of real-world points to generate for homography computation
    :return: Dictionary mapping tiles to their homography matrices
    """

    image = Image.open(io.BytesIO(img.content))

    image = np.array(image)
    h, w, _ = image.shape
    
    h_half, w_half = h // 2, w // 2

    lon_min, lat_min, lon_max, lat_max = skraafoto_item_json['bbox'] 

    # most likely not accurate
    lat_center = (lat_min + lat_max) / 2
    lon_center = (lon_min + lon_max) / 2

    tiles = {
        "tile_1": image[0:h_half, 0:w_half],    
        "tile_2": image[0:h_half, w_half:w],    
        "tile_3": image[h_half:h, 0:w_half],    
        "tile_4": image[h_half:h, w_half:w]  
    }

    tile_bboxes = {
    f"tile_1[{lon_min},{lat_center},{lon_center},{lat_max}]": (lon_min, lat_center, lon_center, lat_max),
    f"tile_2[{lon_center},{lat_center},{lon_max},{lat_max}]": (lon_center, lat_center, lon_max, lat_max),
    f"tile_3[{lon_min},{lat_min},{lon_center},{lat_center}]": (lon_min, lat_min, lon_center, lat_center),
    f"tile_4[{lon_center},{lat_min},{lon_max},{lat_center}]": (lon_center, lat_min, lon_max, lat_center),
    }

    homographies = {}

    for tile_name, bbox in tile_bboxes.items():
        lon_tile_min, lat_tile_min, lon_tile_max, lat_tile_max = bbox
        world_points = generate_real_world_points(lon_tile_min, lat_tile_min, lon_tile_max, lat_tile_max, num_points)
        pixel_points = np.array([latlon_to_pixel(lat,lon, skraafoto_item_json) for lon, lat in world_points])
        homographies[tile_name] = compute_homography(pixel_points,world_points)

    return {"tiles": tiles, "homographies": homographies}

def find_tile_for_pixel(pixel_x, pixel_y, tile_homographies, item):
    """
    Determines which tile the given pixel belongs to by checking its bounding box.

    :param pixel_x: X-coordinate of the pixel
    :param pixel_y: Y-coordinate of the pixel
    :param tile_homographies: Dictionary of tile bounding boxes with their homographies
    :param item: skraafoto response json 
    :return: The correct tile name and its homography matrix
    """
    for tile_name, _ in tile_homographies.items():
        lon_tile_min, lat_tile_min, lon_tile_max, lat_tile_max = extract_bbox_from_tile_name(tile_name)
        
        x_min, y_min = latlon_to_pixel(lat_tile_min, lon_tile_min, item) 
        x_max, y_max = latlon_to_pixel(lat_tile_max, lon_tile_max, item)

        print(f"Tile: {tile_name}")
        print(f"Bounding Box in Pixels: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")
        print(f"Checking if ({pixel_x}, {pixel_y}) falls inside...\n")

        if x_min <= pixel_x <= x_max and y_min <= pixel_y <= y_max:
            return tile_name, tile_homographies[tile_name]

    raise Exception(f"Error: No matching tile found")

def extract_bbox_from_tile_name(tile_name):
    """
    Extracts the bounding box (lon_min, lat_min, lon_max, lat_max) from a tile name.
    """
    bbox_string = tile_name.split("[")[1].split("]")[0] 

    return map(float, bbox_string.split(","))