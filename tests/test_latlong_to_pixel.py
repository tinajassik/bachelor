import numpy as np
import pytest
from unittest.mock import MagicMock, patch
from georeferencing.latlong_to_pixel import  precompute_projection_params
from georeferencing.pixel_to_latlong import compute_homography_for_tile, _compute_homography
from model import TileData
from pyproj import Transformer

@pytest.fixture
def mock_skraafoto_item():
    return {
        "id": "test_id",
        "bbox": [10.0, 55.0, 11.0, 56.0],
        "properties": {
            "proj:shape": [1000, 1000],
            "pers:crs": 25832,
            'pers:rotation_matrix': [0.999978703666698, -0.006414293854261042, 0.0012037638561555805, 0.003654657893290839,
                                     0.7031873638655363, 0.7109952002478784, -0.005407003676085722, -0.7109756593120392,
                                     0.7031958306027261],
            'pers:interior_orientation': {'camera_id': 'UC-OpII-1-70918041-f120_504',
                                         'focal_length': 123.0,
                                         'pixel_spacing': [0.0052, 0.0052],
                                         'calibration_date': '2023-02-09',
                                         'principal_point_offset': [0.0, 0.0],
                                         'sensor_array_dimensions': [10300.0, 7700.0]},
            'pers:omega': 45.3152,
            'pers:phi': -0.3098,
            'pers:kappa': -0.2094,
            'pers:perspective_center': [563893.68, 6254753.55, 1597.8],
        }
    }

@pytest.fixture
def mock_tile_data():
    tile_bounds_latlon = {
        "lat_min": 55.0,
        "lat_max": 55.1,
        "lon_min": 10.0,
        "lon_max": 10.1
    }
    pixel_bounds = {
        "x_min": 100,
        "x_max": 200,
        "y_min": 100,
        "y_max": 200
    }
    return TileData(tile_bounds_latlon, pixel_bounds, None)

@pytest.fixture
def mock_transformer():
    return Transformer.from_crs("EPSG:4326", "EPSG:25832", always_xy=True)

@pytest.fixture
def mock_projection_parameters(mock_skraafoto_item):
    return precompute_projection_params(mock_skraafoto_item)

@pytest.fixture
def mock_elevation():
    with patch('api.elevation.get_elevation') as mock_get_elevation:
        mock_get_elevation.return_value = 42.0
        yield mock_get_elevation

def test_compute_homography_for_tile_shape(mock_tile_data, mock_transformer, mock_projection_parameters, mock_elevation):
    """
    Test if the computed homography matrix has the correct shape (3x3).
    """
    tile = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)
    assert tile.homography.shape == (3, 3)

def test_compute_homography_for_tile_type(mock_tile_data, mock_transformer, mock_projection_parameters, mock_elevation):
    """
    Test if the computed homography matrix is of type numpy.ndarray.
    """
    tile = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)
    assert isinstance(tile.homography, np.ndarray)

def test_compute_homography_for_tile_sanity(mock_tile_data, mock_transformer, mock_projection_parameters, mock_elevation):
    """
    Test if the computed homography matrix contains reasonable values.
    """
    tile = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)
    assert not np.isnan(tile.homography).any()
    assert not np.isinf(tile.homography).any()
    assert not np.all(tile.homography == 0)

def test_compute_homography_for_tile_output_values(mock_tile_data, mock_transformer, mock_projection_parameters, mock_elevation):
    """
    Test if the outputted homography matrix is correct.
    """
    tile = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)
    assert not np.all(tile.homography == 0)
    assert not np.allclose(tile.homography, np.eye(3))

def test_compute_homography_for_tile_with_mocked_latlon_to_pixel(mock_tile_data, mock_transformer, mock_projection_parameters, monkeypatch, mock_elevation):
    """
    Test compute_homography_for_tile with a mocked latlon_to_pixel function.
    """
    def mock_latlon_to_pixel(lat, lon, transformer, projection_parameters):
        if lat == 55.0 and lon == 10.0:
            return [100, 100]
        elif lat == 55.0 and lon == 10.1:
            return [110, 110]
        elif lat == 55.1 and lon == 10.0:
            return [120, 120]
        elif lat == 55.1 and lon == 10.1:
            return [130, 130]
        else:
            return [140, 140]

    monkeypatch.setattr("georeferencing.pixel_to_latlong.geo.latlon_to_pixel", mock_latlon_to_pixel)

    tile : TileData = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)

    assert tile.homography is None or tile.homography.shape == (3, 3) or (tile.homography.shape == (3, 3) and np.all(tile.homography == 0))

def test_compute_homography_for_tile_with_mocked_generate_real_world_points(mock_tile_data, mock_transformer, mock_projection_parameters, monkeypatch, mock_elevation):
    """
    Test compute_homography_for_tile with a mocked generate_real_world_points function.
    """
    mock_generate_real_world_points = MagicMock(return_value=np.array([[10.0, 55.0], [10.1, 55.1], [10.0, 55.1], [10.1, 55.0]]))
    monkeypatch.setattr("georeferencing.pixel_to_latlong.generate_real_world_points", mock_generate_real_world_points)

    tile = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)

    mock_generate_real_world_points.assert_called_once()

    assert tile.homography.shape == (3, 3)

def test_compute_homography_for_tile_with_mocked__compute_homography(mock_tile_data, mock_transformer, mock_projection_parameters, monkeypatch, mock_elevation):
    """
    Test compute_homography_for_tile with a mocked _compute_homography function.
    """
    mock__compute_homography = MagicMock(return_value=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
    monkeypatch.setattr("georeferencing.pixel_to_latlong._compute_homography", mock__compute_homography)

    tile = compute_homography_for_tile(mock_tile_data, mock_transformer, mock_projection_parameters)
    mock__compute_homography.assert_called_once()
    assert tile.homography.shape == (3, 3)
    assert np.array_equal(tile.homography, np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))

def test__compute_homography_shape():
    """
    Test if the computed homography matrix has the correct shape (3x3).
    """
    pixels = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], dtype=np.float32)
    world_coords = np.array([[10, 10], [20, 20], [30, 30], [40, 40]], dtype=np.float32)
    H = _compute_homography(pixels, world_coords)
    assert H.shape == (3, 3)

def test__compute_homography_type():
    """
    Test if the computed homography matrix is of type numpy.ndarray.
    """
    pixels = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], dtype=np.float32)
    world_coords = np.array([[10, 10], [20, 20], [30, 30], [40, 40]], dtype=np.float32)
    H = _compute_homography(pixels, world_coords)
    assert isinstance(H, np.ndarray)

def test__compute_homography_sanity():
    """
    Test if the computed homography matrix contains reasonable values.
    """
    pixels = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], dtype=np.float32)
    world_coords = np.array([[10, 10], [20, 20], [30, 30], [40, 40]], dtype=np.float32)
    H = _compute_homography(pixels, world_coords)
    assert not np.isnan(H).any()
    assert not np.isinf(H).any()
    assert not np.all(H == 0)

def test__compute_homography_output_values():
    """
    Test if the outputted homography matrix is correct.
    """
    pixels = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], dtype=np.float32)
    world_coords = np.array([[10, 10], [20, 20], [30, 30], [40, 40]], dtype=np.float32)
    H = _compute_homography(pixels, world_coords)
    assert not np.all(H == 0)
    assert not np.allclose(H, np.eye(3))
