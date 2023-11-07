from io import BytesIO
from google.cloud.storage import Client

def upload_image(project_id, bucket_name, filename, image, dry_run=False):
    """
    Upload an image to GCS
    """
    if dry_run:
        print(f"Dry run: Using static image URL")
        return "https://images.unsplash.com/photo-1698778755355-e269c65b5e16?auto=format&fit=crop&q=80&w=512&h=512"
    else:
        storage_client = Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        image_bytes = BytesIO()
        image.save(image_bytes, format="jpeg")
        blob.upload_from_string(image_bytes.getvalue(), content_type="image/jpeg")

        print(f"Uploaded image to {blob.public_url}")
        return blob.public_url
