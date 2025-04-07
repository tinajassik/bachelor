import numpy as np
import cv2
import numpy as np
import georeferencing as geo
from model import TileData
from data import data_access
from services import skraafoto

def compute_homography_for_tile(tile: TileData, transformer, projection_parameters):
    tile_bbox = tile.tile_bounds_latlon
    lon_tile_min = tile_bbox['lon_min']
    lon_tile_max = tile_bbox['lon_max']
    lat_tile_min = tile_bbox['lat_min']
    lat_tile_max = tile_bbox['lat_max']
   
    world_points = generate_real_world_points(lon_tile_min, lat_tile_min, lon_tile_max, lat_tile_max)
    pixel_points = np.array([geo.latlon_to_pixel(lat,lon, transformer, projection_parameters) for lon, lat in world_points])
    homography = _compute_homography(pixel_points, world_points)
    tile.homography = homography

    return tile;

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

def get_tile_for_pixel(pixel_x, pixel_y, skraafoto_item_id):
    """
    Determines which tile the given pixel belongs to by checking its pixel bounding box. If no tile found, raises an exception. 

    :param pixel_x: X-coordinate of the pixel
    :param pixel_y: Y-coordinate of the pixel
    :param skraafoto_item_id: ID of the image chosen pixels belong to 
    :param tiles: Dictionary of tiles
    :return: The correct tile 
    """
    try:
        filtered_tiles = data_access.load_tiles_by_id(skraafoto_item_id)
        print(f"Tiles belonging to STAC item ID {skraafoto_item_id} loaded from storage.")
    except:
        print("Skraafoto image with the given ID has not been processed yet.")
        print("Starting image tiling..")
        skraafoto_item = skraafoto.fetch_skraafoto_item(skraafoto_item_id)
        filtered_tiles = geo.split_image_by_latlon(skraafoto_item,4,4)


    for tile in filtered_tiles:
        pixel_bbx = tile['pixel_bounds']
        x_min = pixel_bbx['x_min']
        x_max = pixel_bbx['x_max']
        y_min = pixel_bbx['y_min']
        y_max = pixel_bbx['y_max']
    
        print(f"Bounding Box in Pixels: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")
        print(f"Checking if ({pixel_x}, {pixel_y}) falls inside...\n")

        if x_min <= pixel_x <= x_max and y_min <= pixel_y <= y_max:
            return tile
        
    raise Exception(f"Error: No matching tile found")

def generate_real_world_points(lon_min, lat_min, lon_max, lat_max, grid_size=10):
    """
    Generates real-world latitude and longitude points inside a tile's bounding box.
    
    :param lon_min, lat_min, lon_max, lat_max: Tile bbox 
    :param num_points: Number of real-world points to generate
    :return: NumPy array of (lon, lat) real-world coordinates
    """
    lon_values = np.linspace(lon_min, lon_max, grid_size)
    lat_values = np.linspace(lat_min, lat_max, grid_size)

    lon_grid, lat_grid = np.meshgrid(lon_values, lat_values)

    grid_points = np.stack([lon_grid.ravel(), lat_grid.ravel()], axis=1)

    return grid_points;

def _compute_homography(pixels, world_coords):
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