import os
import argparse
from job.ai import generate_quote, generate_image
from job.gcp import upload_image

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("IMAGES_BUCKET_NAME")
IMAGES_PATH = os.getenv("IMAGES_PATH")

def regenerate_image(prompt, date, dry_run=False, fetch_only=False):
    # Create the inspirational image using DALL-E
    image = generate_image(prompt, dry_run=dry_run)

    # image = build_image(quote_data, image)

    # Upload the image to Cloud Storage
    if not fetch_only:
        image_url = upload_image(project_id=GCP_PROJECT_ID, bucket_name=BUCKET_NAME, filename=f"{IMAGES_PATH}/{date}.jpg", image=image, dry_run=dry_run)
        return image_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='regenerate_image', description='Reruns DALL-E to generate a new image for a given date')
    parser.add_argument('prompt')
    parser.add_argument('date')
    parser.add_argument('-d', '--dryrun', action='store_true')
    parser.add_argument('-f', '--fetch', action='store_true')

    args = parser.parse_args()

    result = regenerate_image(args.prompt, args.date, dry_run=args.dryrun, fetch_only=args.fetch)
    print(result)