import requests
import os

def get_elevation(lon: float, lat: float):
    """
    Fetch elevation data for given coordinates from the Denmark Elevation Model API.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.

    Returns:
        float: Elevation value in meters.
    """

    username = os.getenv("HEIGHT_MODEL_USERNAME")
    password = os.getenv("HEIGHT_MODEL_PASSWORD")

    height_model_response =  requests.get(f"https://services.datafordeler.dk/DHMTerraen/DHMKoter/1.0.0/GEOREST/HentKoter?username={username}&password={password}&geop=POINT({lon}%20{lat})")
    height_model_response.raise_for_status()
    return height_model_response.json()["HentKoterRespons"]["data"][0]["kote"]