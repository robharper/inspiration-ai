from io import BytesIO
from google.cloud.storage import Client

def upload_image(project_id, bucket_name, filename, image, dry_run=False):
    """
    Upload an image to GCS
    """
    if dry_run:
        output_url = f"http://{bucket_name}/{filename}"
        print(f"Dry run: Would upload image to {output_url}")
        return output_url
    else:
        storage_client = Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        image_bytes = BytesIO()
        image.save(image_bytes, format="jpeg")
        blob.upload_from_string(image_bytes.getvalue(), content_type="image/jpeg")

        public_url = f"http://{bucket_name}/{filename}"
        print(f"Uploaded image to {blob.public_url} --> {public_url}")
        return public_url
