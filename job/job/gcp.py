from io import BytesIO
from google.cloud.storage import Client

def upload_image(project_id, bucket_name, filename, image, dry_run=False):
    """
    Upload an image to GCS
    """
    if dry_run:
        filename = "result.jpg"
        image.save(filename)
        return filename
    else:
        storage_client = Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        image_bytes = BytesIO()
        image.save(image_bytes, format="jpeg")
        blob.upload_from_string(image_bytes.getvalue(), content_type="image/jpeg")
