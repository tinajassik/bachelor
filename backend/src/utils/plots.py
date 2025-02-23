from PIL import Image
import matplotlib.pyplot as plt
import io


def plot_pixel_on_image(projected_point, img): 
    # Convert the image content to a file-like object
    image = Image.open(io.BytesIO(img.content))

    # Display the image with matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(image)

    pixel_x = projected_point[0]  
    pixel_y = image.height - projected_point[1]  

    # Plot the pixel as a red dot
    plt.plot(pixel_x, pixel_y, 'ro', markersize=5, label='Calculated Pixel')
    plt.legend()
    plt.title("Skraafoto Image with Calculated Pixel Overlay")
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.show()