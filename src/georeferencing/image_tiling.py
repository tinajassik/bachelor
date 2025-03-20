import numpy as np
from model import TileData
from pyproj import Transformer
from data import data_access
import georeferencing as geo 
TILES_OUPTUT_FOLDER = "../data/tiles/"

def split_image_by_latlon(skraafoto_item_json, lat_steps, lon_steps):
    """
    Splits an image into tiles based on lat/lon space. Computes Homographies for each tile. Saves tile data to .h5.

    :param skraafoto_item_json: Skraafoto STAC Item 
    :param image: Skraafoto Image as a byte array 
    :param lat_steps: Number of divisions along latitude
    :param lon_steps: Number of divisions along longitude
    :return: List of processed tiles
    """
    img_height, img_width = skraafoto_item_json['properties']['proj:shape'][:2]

    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{skraafoto_item_json['properties']['pers:crs']}", always_xy=True)
    projection_parameters = geo.precompute_projection_params(skraafoto_item_json)
 
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

            pixel_coords = [geo.latlon_to_pixel(lat, lon, transformer, projection_parameters) for lat, lon in corners_latlon]

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

            tile = TileData(tile_bounds_latlon, pixel_bounds)
            tile = geo.compute_homography_for_tile(tile, transformer, projection_parameters)
            tiles_dict[skraafoto_item_json['id']].append(tile.to_dict())
            
    data_access.save_to_file(tiles_dict)
    return tiles_dict[skraafoto_item_json['id']]