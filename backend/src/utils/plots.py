from PIL import Image
import matplotlib.pyplot as plt
import io
import folium

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
    
    folium.Marker(
        location=[lat, lon],
        popup=f"Transformed Point\nLat: {lat}, Lon: {lon}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    m.save(f"{file_name}.html")