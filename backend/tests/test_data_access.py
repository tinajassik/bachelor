from data.data_access import (
    save_to_file,
    load_dict,
    load_tiles_by_id,
    _recursively_load_dict,
    get_all_stac_ids
)
import h5py
from model import TileData
import pytest
import os
import pytest
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEST_DIR = os.path.join(BASE_DIR, "backend", "tests")
TEST_FILENAME = "test_tile_data"
TEST_PATH = os.path.join(TEST_DIR, f"{TEST_FILENAME}.h5")


@pytest.fixture
def mock_new_tiles():
    homography_matrix = np.identity(3)
    tile1 = TileData(
        tile_bounds_latlon={
            "lat_min": 55.0,
            "lat_max": 56.0,
            "lon_min": 10.0,
            "lon_max": 11.0
        },
        pixel_bounds={
            "x_min": 0,
            "x_max": 1000,
            "y_min": 0,
            "y_max": 1000
        },
        homography=homography_matrix
    )

    tile2 = TileData(
        tile_bounds_latlon={
            "lat_min": 56.0,
            "lat_max": 57.0,
            "lon_min": 11.0,
            "lon_max": 12.0
        },
        pixel_bounds={
            "x_min": 1000,
            "x_max": 2000,
            "y_min": 0,
            "y_max": 1000
        },
        homography=homography_matrix
    )

    return {
        "tile_1": [tile1],
        "tile_2": [tile2]
    }

def test_save_to_file(mock_new_tiles):
    """Testing saving 2 new tiles to hdf5 file"""
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)

    save_to_file(mock_new_tiles, save_dir=TEST_DIR, filename=TEST_FILENAME)

    assert os.path.exists(TEST_PATH), "HDF5 file was not created"

    with h5py.File(TEST_PATH, 'r') as h5file:
        assert "tile_1" in h5file, "'tile_1' group not found in file"
        loaded = _recursively_load_dict(h5file, "/tile_1/0")
        assert loaded["tile_bounds_latlon"]["lat_min"] == 55.0
        assert loaded["pixel_bounds"]["x_max"] == 1000

    os.remove(TEST_PATH)

def test_load_dict(mock_new_tiles):
    """Testing loading the file"""
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)

    save_to_file(mock_new_tiles, save_dir=TEST_DIR, filename=TEST_FILENAME)

    loaded_data = load_dict(save_dir=TEST_DIR, filename=TEST_FILENAME)

    assert "tile_1" in loaded_data, "'tile_1' not found in loaded data"

    tile_data = loaded_data["tile_1"]["0"]
    assert tile_data["tile_bounds_latlon"]["lat_min"] == 55.0
    assert tile_data["pixel_bounds"]["x_max"] == 1000

    np.testing.assert_array_equal(
        tile_data["homography"],
        np.identity(3),
        err_msg="Homography matrix doesn't match"
    )

    os.remove(TEST_PATH)

def test_load_tiles_by_id(mock_new_tiles):
    """Testing loading tiles by id"""
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)

    save_to_file(mock_new_tiles, save_dir=TEST_DIR, filename=TEST_FILENAME)

    loaded_tiles = load_tiles_by_id("tile_1",save_dir=TEST_DIR, filename=TEST_FILENAME)

    assert isinstance(loaded_tiles, list)
    assert len(loaded_tiles) == 1

    tile_data = loaded_tiles[0]
    assert tile_data["tile_bounds_latlon"]["lat_min"] == 55.0
    assert tile_data["pixel_bounds"]["x_max"] == 1000
    np.testing.assert_array_equal(tile_data["homography"], np.identity(3))

    os.remove(TEST_PATH)

def test_get_all_stac_ids(mock_new_tiles):
    """Testing getting all stac ids"""
    if os.path.exists(TEST_PATH):
        os.remove(TEST_PATH)

    save_to_file(mock_new_tiles, save_dir=TEST_DIR, filename=TEST_FILENAME)

    ids = get_all_stac_ids(save_dir=TEST_DIR, filename=TEST_FILENAME)

    assert isinstance(ids, list)
    assert "tile_1" in ids

    os.remove(TEST_PATH)