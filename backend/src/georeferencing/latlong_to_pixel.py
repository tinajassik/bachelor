from pyproj import Transformer
from sympy import Matrix, eye
from api import elevation

def latlon_to_pixel(latitude, longitude, skraafoto_item_json):
    """
    Converts latitude/longitude to pixel coordinates on a Skraafoto image.

    :param latitude: Latitude coordinate.
    :param longitude: Longitude coordinate.
    :param crs: EPSG code for the projection.
    :param camera_params: Dictionary with Skraafoto camera parameters.
    :return: (x_pixel, y_pixel) pixel coordinates on the image.
    """
    
    # convert lat/lon to the correct CRS
    crs = _extract_crs_information(skraafoto_item_json)['crs']
    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{crs}", always_xy=True)
    x_world, y_world = transformer.transform(longitude, latitude)
    
    # get the height value
    z_world = _get_safe_elevation(x_world, y_world)

    # get camera parameters
    camera_params = _extract_camera_parameters(skraafoto_item_json);
    m11, m12, m13, m21, m22, m23, m31, m32, m33 = camera_params["rotation_matrix"]
    Xc, Yc, Zc = camera_params["camera_position"]
    calculated_pixel_values = _calculate_pixel_values(camera_params)
    f = calculated_pixel_values["f"]
    x0 = calculated_pixel_values["x0"]
    y0 = calculated_pixel_values["y0"]
    
    # define Matrices

    ## Rotation Matrix (R)
    R = Matrix([
        [m11, m12, m13],
        [m21, m22, m23],
        [m31, m32, m33]
    ])

    ## Intrinsic Matrix (K)
    K = Matrix([
        [-f, 0, x0],
        [0, -f, y0],
        [0, 0, 1]
    ])

    ## Identity Matrix (I) for 3D Transformation
    I = eye(3)

    ## Translation Matrix (T)
    translation = Matrix([[-Xc], [-Yc], [-Zc]])
    T = Matrix.hstack(I, translation)

    ## Compute K * R * T (Projection Matrix)
    KRT = K * R * T

    # Define the 3D Point in Homogeneous Coordinates
    point_3D = Matrix([x_world, y_world, z_world, 1])

    # Compute Pixel Mapping
    mapping = KRT * point_3D

    ## Normalize to get pixel coordinates
    pixel_x = mapping[0] / mapping[2]
    pixel_y = mapping[1] / mapping[2]

    ## Final projected 2D point
    projected_2D_point_final = (float(pixel_x), float(pixel_y))

    return projected_2D_point_final

## based on Skraafoto documentation for georeferencing
def _extract_camera_parameters(item_json):
    """
    Extracts camera parameters from the Skraafoto item JSON.

    :param item_json: JSON response from the Skraafoto API.
    :return: Dictionary containing camera parameters.
    """
    props = item_json["properties"]

    camera_params = {
        "rotation_matrix": props["pers:rotation_matrix"],
        "camera_position": props["pers:perspective_center"],  # Xc, Yc, Zc
        "focal_length_mm": props["pers:interior_orientation"]["focal_length"],
        "principal_point_offset": props["pers:interior_orientation"]["principal_point_offset"],  # (ppo_x, ppo_y)
        "pixel_size": props["pers:interior_orientation"]["pixel_spacing"][0],
        "sensor_dimensions": props["pers:interior_orientation"]["sensor_array_dimensions"],  # (cols, rows)
    }
    
    return camera_params

## based on Skraafoto documentation for georeferencing
def _calculate_pixel_values(camera_params):
    """
    Calculates pixel values using camera parameters.

    :param camera_params: Dictionary containing extracted camera parameters.
    :return: Dictionary containing calculated pixel values.
    """
    f_mm = camera_params["focal_length_mm"]
    ppo_x, ppo_y = camera_params["principal_point_offset"]
    pixel_size = camera_params["pixel_size"]
    sensor_cols, sensor_rows = camera_params["sensor_dimensions"]

    calculated_values = {
        "f": f_mm / pixel_size,  # Focal length in pixels
        "x0": sensor_cols * 0.5 + ppo_x / pixel_size,  # Principal point X
        "y0": sensor_rows * 0.5 + ppo_y / pixel_size,  # Principal point Y
    }

    return calculated_values

def _extract_crs_information(item_json):
    """
    Extracts CRS (coordinate reference system) information.

    :param item_json: JSON response from the Skraafoto API.
    :return: Dictionary containing CRS and image URL.
    """
    props = item_json["properties"]
    
    return {
        "crs": props["pers:crs"],
        "vertical_crs": props["pers:vertical_crs"]
    }

def _get_safe_elevation(x_world, y_world, fallback=31):
    """
    Get elevation for (x_world, y_world). If it fails, try nearby points. 
    If all fail, return fallback elevation.
    
    :param x_world: UTM X coordinate
    :param y_world: UTM Y coordinate
    :param fallback: Default elevation if no data is found
    :return: Elevation in meters
    """
    
    z_world = elevation.get_elevation(x_world, y_world)
    
    if z_world is not None:
        return z_world  

    offsets = [-0.1, 0, 0.1]
    for dx in offsets:
        for dy in offsets:
            z_world = elevation.get_elevation(x_world + dx, y_world + dy)
            if z_world is not None:
                print(f"✔ Found elevation at offset ({dx}, {dy}): {z_world}")
                return z_world

    print(f"⚠️ No elevation found for ({x_world}, {y_world}). Using fallback: {fallback}m")
    return fallback
