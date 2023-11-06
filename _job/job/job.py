import os
from datetime import date
from job.ai import generate_quote, generate_image
from job.gcp import upload_image
from job.jekyll import build_page
from job.github import upload

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BUCKET_NAME = os.getenv("IMAGES_BUCKET_NAME")

GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def execute(dry_run=False):
    # Use today's date as post's date unless overridden
    post_date = os.getenv("DATE_OVERRIDE", date.today().strftime("%Y-%m-%d"))

    # Generate the inspirational quote using LLM
    quote_data = generate_quote(dry_run=dry_run)

    # Create the inspirational image using DALL-E
    image = generate_image(quote_data["description"], dry_run=dry_run)

    # image = build_image(quote_data, image)

    # Upload the image to Cloud Storage
    image_url = upload_image(project_id=GCP_PROJECT_ID, bucket_name=BUCKET_NAME, filename=f"{post_date}.jpg", image=image)

    # Generate the markdown
    markdown = build_page(post_date, quote_data, image_url)

    # Upload the markdown
    title = quote_data["title"].lower().replace(" ", "-")
    upload(gh_token=GITHUB_TOKEN, repo=GITHUB_REPO, path=f"_posts/{post_date}-{title}.markdown", content=markdown)