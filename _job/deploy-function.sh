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