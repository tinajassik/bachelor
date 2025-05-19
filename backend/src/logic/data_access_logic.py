from io import BytesIO
import os
import zipfile
from data import data_access, image_access
from fastapi import HTTPException, Response
from utils import image_handler

def get_all_processed_stac_item_ids():
    """
    Fetches all processed STAC item IDs from the data access layer.
    """
    try:
        return data_access.get_all_stac_ids()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while loading data: {str(e)}")

def get_stac_item_jpeg(item_id: str) -> Response:
    """
    Retrieves a JPEG image for a given STAC item ID.
    Converts TIFF to JPEG if necessary and returns as an HTTP response.
    """
    try:
        image_path = image_access.get_or_fetch_image_by_id(item_id)
        img_jpeg = image_handler.convert_tiff_to_jpeg(image_path)
        return Response(content=img_jpeg, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while retrieving an image from Skraafoto: {str(e)}")
    
def get_cropped_images(item_id: str) -> Response:
    """
    Retrieves all cropped PNG images for a given STAC item ID
    and returns them as a zipped response.
    """
    try:
        image_paths = image_access.get_cropped_images(item_id)

        if not image_paths:
            raise HTTPException(status_code=404, detail="No cropped images found.")

        zip_stream = BytesIO()
        with zipfile.ZipFile(zip_stream, "w") as zipf:
            for path in image_paths:
                with open(path, "rb") as img_file:
                    img_bytes = img_file.read()
                    arcname = os.path.basename(path)
                    zipf.writestr(arcname, img_bytes)


        zip_stream.seek(0)
        return Response(
            content=zip_stream.read(),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={item_id}_cropped_images.zip"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cropped images: {str(e)}")