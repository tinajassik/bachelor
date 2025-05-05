from unittest.mock import patch
from utils.tile_splitter_stat import (
    extract_tiles,
    find_pixel_position
)
import os
import re

from PIL import Image
IMG_PATH = os.path.join("backend","tests","data_tests")

def test_extract_tiles_num(tmp_path):
    """Testing if image is split into correct number of tiles"""
    item_id = "test-id"
    image_dir = tmp_path / item_id
    image_dir.mkdir(parents=True)
    image_path = image_dir / f"{item_id}.tif"

    image = Image.new("RGB", (10750, 8700))
    image.save(image_path)

    with patch("utils.tile_splitter_stat.images_to_split_path", tmp_path):
        extract_tiles(item_id, grid_scale=0.04)

        tiles_dir = image_dir / "tiles"
        tile_files = list(tiles_dir.glob("*.png"))
        assert len(tile_files) == 625

def test_extract_tiles_names(tmp_path):
    """Testing extracted tiles names"""
    item_id = "test-id"
    image_width = 10750
    image_height = 8700

    image_dir = tmp_path / item_id
    image_dir.mkdir(parents=True)
    image_path = image_dir / f"{item_id}.tif"

    image = Image.new("RGB", (image_width, image_height))
    image.save(image_path)

    with patch("utils.tile_splitter_stat.images_to_split_path", tmp_path):
        extract_tiles(item_id, grid_scale=0.04)

        tiles_dir = image_dir / "tiles"
        tile_files = list(tiles_dir.glob("*.png"))

        for tile in tile_files:
            match = re.search(rf"{item_id}-(\d+)-(\d+)\.png", tile.name)
            assert match, f"Filename format invalid: {tile.name}"
            x_min, y_min = int(match.group(1)), int(match.group(2))

            assert x_min < image_width, f"x_min {x_min} exceeds image width"
            assert y_min < image_height, f"y_min {y_min} exceeds image height"

def test_find_pixel_position():
    """Testing finding correct pixel"""
    filename = "item-100-200.png"
    pixel_x, pixel_y = 10, 15
    result = find_pixel_position(filename, pixel_x, pixel_y)
    assert result == (110, 215)


