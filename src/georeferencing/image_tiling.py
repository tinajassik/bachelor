import numpy as np
from PIL import Image
from georeferencing import latlong_to_pixel, pixel_to_latlong
import os
from model import TileData

TILES_OUPTUT_FOLDER = "../data/tiles/"

def split_image_by_latlon(skraafoto_item_json, image, lat_steps, lon_steps):
    """
    Splits an image into tiles based on lat/lon space. Saves tiles as jpeg. Computes Homographies.

    :param skraafoto_item_json: Skraafoto STAC Item 
    :param image: Skraafoto Image as a byte array 
    :param lat_steps: Number of divisions along latitude
    :param lon_steps: Number of divisions along longitude
    :return: Dictionary {stac_item_id: list of tiles}
    """
    img_height, img_width = image.shape[:2]
 
    lon_min, lat_min, lon_max, lat_max = skraafoto_item_json['bbox'] 
    
    lat_edges = np.linspace(lat_min, lat_max, lat_steps + 1)
    lon_edges = np.linspace(lon_min, lon_max, lon_steps + 1)

    tiles_dict = {}
    tiles_dict[skraafoto_item_json['id']] = []

    for i in range(lat_steps):
        for j in range(lon_steps):
            # lat,lon bounding box for this tile
            tile_lat_min = lat_edges[i]
            tile_lat_max = lat_edges[i + 1]
            tile_lon_min = lon_edges[j]
            tile_lon_max = lon_edges[j + 1]

            corners_latlon = [
                (tile_lat_min, tile_lon_min),
                (tile_lat_min, tile_lon_max),
                (tile_lat_max, tile_lon_min),
                (tile_lat_max, tile_lon_max)
            ]

            pixel_coords = [latlong_to_pixel.latlon_to_pixel(lat, lon, skraafoto_item_json) for lat, lon in corners_latlon]

            x_pixels = [pt[0] for pt in pixel_coords]
            y_pixels = [pt[1] for pt in pixel_coords]

            # bbox in pixel space
            x_min = int(max(0, min(x_pixels)))
            x_max = int(min(img_width, max(x_pixels)))
            y_min = int(max(0, min(y_pixels)))
            y_max = int(min(img_height, max(y_pixels)))

            tile_bounds_latlon = {
                    "lat_min": tile_lat_min,
                    "lat_max": tile_lat_max,
                    "lon_min": tile_lon_min,
                    "lon_max": tile_lon_max
            }

            pixel_bounds = {
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max
            }

            tile_path = _save_tile(image[y_min:y_max, x_min:x_max], tile_bounds_latlon, f"{TILES_OUPTUT_FOLDER}{skraafoto_item_json['id']}")
            tile = TileData(tile_path, tile_bounds_latlon, pixel_bounds)
            tile = pixel_to_latlong.compute_homography_for_tile(tile, skraafoto_item_json)
            tiles_dict[skraafoto_item_json['id']].append(tile)

    return tiles_dict

    
def _save_tile(tile_img, tile_bounds_latlon, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    tile_img = Image.fromarray(tile_img)
    filename = f"tile[{tile_bounds_latlon['lon_min']},{tile_bounds_latlon['lat_min']},{tile_bounds_latlon['lon_max']},{tile_bounds_latlon['lat_max']}].jpeg"
    file_path = os.path.join(output_folder, filename)
    tile_img.save(file_path) 
    return file_path
               