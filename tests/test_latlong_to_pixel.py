import numpy as np
import pytest
from unittest.mock import patch
from georeferencing.latlong_to_pixel import (
    latlon_to_pixel,
    precompute_projection_params,
    _extract_camera_parameters,
    _calculate_pixel_values,
    _get_safe_elevation
)
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

def test_precompute_projection_params(mock_skraafoto_item):
    """Test if precompute_projection_params returns the correct data structure."""
    params = precompute_projection_params(mock_skraafoto_item)
    assert isinstance(params, np.ndarray)
    assert params.shape == (3, 4)

def test_latlon_to_pixel_valid_input(mock_transformer, mock_projection_parameters, mock_elevation):
    """Test if latlon_to_pixel returns a pixel coordinate for a valid input."""
    lat, lon = 55.0, 10.0
    pixel = latlon_to_pixel(lat, lon, mock_transformer, mock_projection_parameters)
    assert isinstance(pixel, tuple)
    assert len(pixel) == 2
    assert all(isinstance(coord, float) for coord in pixel)

def test_latlon_to_pixel_invalid_input(mock_transformer, mock_projection_parameters, mock_elevation):
    """Test if latlon_to_pixel handles invalid input gracefully."""
    lat, lon = "invalid", "input"
    with pytest.raises(TypeError):
        latlon_to_pixel(lat, lon, mock_transformer, mock_projection_parameters)

def test__extract_camera_parameters(mock_skraafoto_item):
    """Test if _extract_camera_parameters correctly extracts camera parameters."""
    params = _extract_camera_parameters(mock_skraafoto_item)
    assert isinstance(params, dict)
    assert "rotation_matrix" in params
    assert "camera_position" in params
    assert "focal_length_mm" in params
    assert "pixel_size" in params
    assert "principal_point_offset" in params
    assert "sensor_dimensions" in params

def test__calculate_pixel_values(mock_skraafoto_item, mock_elevation):
    """Test if _calculate_pixel_values returns correct pixel values."""
    camera_params = _extract_camera_parameters(mock_skraafoto_item)
    pixel_values = _calculate_pixel_values(camera_params)
    assert isinstance(pixel_values, dict)
    assert "f" in pixel_values
    assert "x0" in pixel_values
    assert "y0" in pixel_values

def test__get_safe_elevation_valid(mock_elevation):
    """Test if _get_safe_elevation returns a valid elevation."""
    x_world, y_world = 563893.68, 6254753.55
    elevation = _get_safe_elevation(x_world, y_world)
    assert isinstance(elevation, float)
    assert elevation == 42.0
