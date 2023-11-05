from job.ai import generate_quote, generate_image
from job.gcp import upload_image

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("IMAGES_BUCKET_NAME")

def execute(dry_run=False):
    # Generate the inspirational quote
    quote_data = generate_quote(dry_run=dry_run)

    # Create the inspirational image
    background = generate_image(quote_data["description"], dry_run=dry_run)

    # image = build_image(quote_data, background)
    image = background

    # Upload the image
    image_url = upload_image(project_id=GCP_PROJECT_ID, bucket_name=BUCKET_NAME, filename="test.jpg", image=image)

    # Generate the markdown

    # Upload the markdown