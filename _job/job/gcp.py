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
        try:
            blob.upload_from_string(image_bytes.getvalue(), content_type="image/jpeg")
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None

        public_url = blob.public_url
        print(f"Uploaded image to {public_url}")
        return public_url
