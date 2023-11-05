import os
import functions_framework
from job.job import execute

# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def generate_inspiration(cloud_event):
    dry_run = os.getenv("DRY_RUN", False)
    execute(dry_run=dry_run)