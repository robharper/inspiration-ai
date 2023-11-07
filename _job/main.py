import os
import base64
import json
from datetime import date
import functions_framework
from job.job import execute

# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def generate_inspiration(cloud_event):
    dry_run = os.getenv("DRY_RUN", False)


    post_date = None
    if type(cloud_event.data) == dict:
        input_b64 = cloud_event.data.get("message", {}).get("data")
        if input_b64:
            json_input = base64.b64decode(input_b64).decode()
            try:
                post_date = json.loads(json_input).get("date")
            except:
                print(f"Invalid JSON input received: {json_input}")

    # Use today's date as post's date unless overridden
    if not post_date:
        post_date = date.today().strftime("%Y-%m-%d")

    print(f"Generating inspiration for {post_date}")

    execute(post_date, dry_run=dry_run)