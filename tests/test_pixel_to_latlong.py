import pytest 
from georeferencing import get_tile_for_pixel, generate_real_world_points
from georeferencing import pixel_to_latlong
from data import data_access
from api import skraafoto, elevation
import numpy as np
from unittest.mock import MagicMock

def test_get_tile_for_pixel_found(monkeypatch):
    
    correct_tile = {
        'pixel_bounds': {
            'x_min': 100,
            'x_max': 200,
            'y_min': 100,
            'y_max': 200
        }
    }
    wrong_tile = {
        'pixel_bounds': {
            'x_min': 0,
            'x_max': 100,
            'y_min': 0,
            'y_max': 100
        }
    }

    def mock_load_tiles_by_id(skraafoto_item_id):
        return [correct_tile,wrong_tile]

    monkeypatch.setattr(data_access, "load_tiles_by_id", mock_load_tiles_by_id)

    result = get_tile_for_pixel(150, 150, "fake_id")
    assert result == correct_tile

def test_get_tile_for_pixel_not_found(monkeypatch):

    def mock_load_tiles_by_id(skraafoto_item_id):
        return [{
            'pixel_bounds': {
                'x_min': 0,
                'x_max': 50,
                'y_min': 0,
                'y_max': 50
            }
        }]
    
    monkeypatch.setattr(data_access, "load_tiles_by_id", mock_load_tiles_by_id)

    with pytest.raises(Exception, match="No matching tile found"):
        get_tile_for_pixel(150, 150, "fake_id")

def test_get_tile_for_pixel_fallback(monkeypatch):
    def mock_load_tiles_by_id(skraafoto_item_id):
        raise Exception("Not processed")

    mock_fetch_item = MagicMock(return_value= 
        {
        "id": 0,
        "bbox": [10.02735779313822,56.44316104991162,10.04643090008056,56.45315022217864],
        "properties": {
            "proj:shape": [1000, 1000],
            "pers:crs": 25832,
            'pers:rotation_matrix': [0.999978703666698,-0.006414293854261042,0.0012037638561555805,0.003654657893290839,
                                     0.7031873638655363, 0.7109952002478784,-0.005407003676085722,-0.7109756593120392,0.7031958306027261],
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
    })

    mock_split_image_by_latlon = MagicMock(return_value= 
        [{
            'pixel_bounds': {
                'x_min': 10,
                'x_max': 20,
                'y_min': 10,
                'y_max': 20
            }
        }
        ])
    
    monkeypatch.setattr(elevation, "get_elevation", lambda x, y: 42)
    monkeypatch.setattr(data_access, "load_tiles_by_id", mock_load_tiles_by_id)
    monkeypatch.setattr(skraafoto, "fetch_skraafoto_item", mock_fetch_item)
    monkeypatch.setattr(pixel_to_latlong.geo, "split_image_by_latlon", mock_split_image_by_latlon)

    result = get_tile_for_pixel(15, 15, "fallback_case")

    mock_fetch_item.assert_called_once()
    mock_split_image_by_latlon.assert_called_once()
    assert result['pixel_bounds']['x_min'] == 10

def test_generate_real_world_points_shape():
    lon_min, lat_min = 10.0, 55.0
    lon_max, lat_max = 11.0, 56.0
    grid_size = 5

    points = generate_real_world_points(lon_min, lat_min, lon_max, lat_max, grid_size)

    assert points.shape == (grid_size * grid_size, 2)

def test_generate_real_world_points_values():
    lon_min, lat_min = 0.0, 0.0
    lon_max, lat_max = 1.0, 1.0
    grid_size = 2

    points = generate_real_world_points(lon_min, lat_min, lon_max, lat_max, grid_size)

    expected_points = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0]
    ])

    assert np.allclose(points, expected_points)

