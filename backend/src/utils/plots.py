from PIL import Image
import matplotlib.pyplot as plt
import io
import folium
import os 
from typing import List, Tuple

def plot_pixel_on_image(projected_point, img): 
    image = Image.open(io.BytesIO(img.content))

    plt.figure(figsize=(10, 10))
    plt.imshow(image)

    pixel_x = projected_point[0]  
    pixel_y = image.height - projected_point[1]  

    plt.plot(pixel_x, pixel_y, 'ro', markersize=5, label='Calculated Pixel')
    plt.legend()
    plt.title("Skraafoto Image with Calculated Pixel Overlay")
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.show()

def generate_map_with_projected_point(lat,lon, bbox, file_name): 
    map_center = [(bbox[1] + bbox[3]) / 2, (bbox[0] + bbox[2]) / 2] 
    m = folium.Map(location=map_center, zoom_start=15)
    m.get_root().html.add_child(folium.Element(__get_js_script(m)))

    folium.Marker(
        location=[lat, lon],
        popup=f"Transformed Point\nLat: {lat}, Lon: {lon}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    __save_map(file_name, m)

def generate_map_with_projected_points(points: List[Tuple[float, float]], bbox: Tuple[float, float, float, float], file_name: str):
    map_center = [(bbox[1] + bbox[3]) / 2, (bbox[0] + bbox[2]) / 2]
    m = folium.Map(location=map_center, zoom_start=15)
    m.get_root().html.add_child(folium.Element(__get_js_script(m)))
    for idx, (lat, lon) in enumerate(points):
        folium.Marker(
            location=[lat, lon],
            popup=f"Point {idx + 1}\nLat: {lat}, Lon: {lon}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    __save_map(file_name, m)

def __save_map(file_name: str, map: folium.Map):
    maps_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "maps"))
    os.makedirs(maps_dir, exist_ok=True)
    
    map_path = os.path.join(maps_dir, f"{file_name}.html")
    map.save(map_path)

def __get_js_script(m: folium.Map):
    return  f"""
            <script>
                window.onload = function() {{
                    var map = window.{m.get_name()};
                    map.on('click', function(e) {{
                        var lat = e.latlng.lat;
                        var lng = e.latlng.lng;
                        L.popup()
                            .setLatLng(e.latlng)
                            .setContent("You clicked at<br>Lat: " + lat + "<br>Lon: " + lng)
                            .openOn(map);
                    }});
                }};
            </script>
            """