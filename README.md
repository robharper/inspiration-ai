# Inspirational AI

> Terrible quotes, daily.

You can view this site live a https://www.robharper.ca/inspiration-ai

## What is this?
This is a really simple project that wires together a bunch of technology with a little bit of code to create a website of daily terrible "inspirational" quotes. Technology used:
- Google Cloud Functions
- OpenAI GPT 3.5
- OpenAI DALL-E
- Google Cloud Storage
- GitHub Pages
- Jekyll

The following diagram shows how things are wired together:

![System Diagram](_assets/system-overview.png)

## Deploy
Before running locally or deploying, create an `.env.yaml` file in the `_job` directory containing:
```
OPENAI_API_KEY: {key from OpenAI}

IMAGES_BUCKET_NAME: {Cloud Storage Bucket Name}
GCP_PROJECT_ID: {Project ID}

GITHUB_REPO: {GitHub repo: username/reponame}
GITHUB_TOKEN: {GitHub token, must be able to create content at the above repo}
```

### GCP
Before continuing, ensure that the following APIs are enabled:
- Cloud Run
- Cloud Build
- EventArc
- Cloud Functions
- Cloud Storage

### Setup a Service Account
Create it
```
gcloud iam service-accounts create inspiration-ai-uploader --project inspiration-ai
```

Give it permissions:
```
# Allow it to upload to Cloud Storage
gcloud projects add-iam-policy-binding inspiration-ai --member="serviceAccount:inspiration-ai-uploader@inspiration-ai.iam.gserviceaccount.com" --role=roles/storage.objectCreator

# Allow it to invoke a Cloud Function
gcloud projects add-iam-policy-binding inspiration-ai --member="serviceAccount:inspiration-ai-uploader@inspiration-ai.iam.gserviceaccount.com" --role=roles/run.invoker
```

### Create a Cloud Storage Bucket

### Create a Pub/Sub Topic
To create a pubsub topic to trigger the cloud function, run:
```
gcloud pubsub topics create inspiration-ai_generate
```

### Deploy the Cloud Function
See [_job/deploy_function.sh](./_job/deploy_function.sh):
```
gcloud functions deploy inspiration-ai-function \
--project=inspiration-ai \
--gen2 \
--runtime=python311 \
--region=northamerica-northeast1 \
--source=. \
--entry-point=generate_inspiration \
--trigger-topic=inspiration-ai_generate \
--service-account=inspiration-ai-uploader@inspiration-ai.iam.gserviceaccount.com \
--env-vars-file .env.yaml
```

## Testing
```
gcloud pubsub topics publish inspiration-ai_generate --message="Testing 123" --project=inspiration-ai
```