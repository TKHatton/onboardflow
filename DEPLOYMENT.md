# OnboardFlow Deployment Guide

This guide walks you through deploying OnboardFlow to Google Cloud.

## Prerequisites

- Google Cloud account with billing enabled
- gcloud CLI installed and authenticated
- Docker installed
- Gemini API key

## Step 1: Set Up Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

## Step 2: Create Firestore Database

```bash
gcloud firestore databases create \
  --location=us-central1 \
  --database-id="(default)"
```

## Step 3: Create Pub/Sub Topic

```bash
gcloud pubsub topics create new-hire-events
```

## Step 4: Build and Push Docker Image

```bash
# Build the image
docker build -t gcr.io/$PROJECT_ID/onboardflow:latest .

# Authenticate Docker
gcloud auth configure-docker

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/onboardflow:latest
```

## Step 5: Deploy to Cloud Run

```bash
gcloud run deploy onboardflow \
  --image gcr.io/$PROJECT_ID/onboardflow:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
  --set-env-vars="GOOGLE_API_KEY=your-gemini-api-key"
```

Note the service URL returned after deployment.

## Step 6: Set Up Pub/Sub Push Subscription

```bash
SERVICE_URL=$(gcloud run services describe onboardflow --region=us-central1 --format='value(status.url)')

gcloud pubsub subscriptions create onboardflow-sub \
  --topic=new-hire-events \
  --push-endpoint=$SERVICE_URL/pubsub \
  --ack-deadline=60
```

## Step 7: Test the Deployment

### Option A: HTTP Request

```bash
curl -X POST $SERVICE_URL/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "employee_name": "Sarah Chen",
    "role": "Senior Software Engineer",
    "department": "Engineering",
    "start_date": "2026-09-15",
    "email": "sarah.chen@example.com",
    "manager": "Alex Rodriguez",
    "manager_email": "alex.rodriguez@example.com"
  }'
```

### Option B: Pub/Sub Message

```bash
gcloud pubsub topics publish new-hire-events \
  --message='{
    "employee_name": "Sarah Chen",
    "role": "Senior Software Engineer",
    "department": "Engineering",
    "start_date": "2026-09-15",
    "email": "sarah.chen@example.com",
    "manager": "Alex Rodriguez",
    "manager_email": "alex.rodriguez@example.com"
  }'
```

## Step 8: Verify in Firestore

```bash
# View onboarding workflows
gcloud firestore queries execute \
  --database-id="(default)" \
  --collection-id="onboarding_workflows"
```

## Step 9: Monitor Logs

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=onboardflow" --limit=50
```

## Cost Management

To minimize costs:
- Cloud Run scales to zero when idle (no charges)
- Firestore has generous free tier
- Pub/Sub has free tier for low volume
- Use Gemini Flash (cheaper than Pro)

Set budget alerts:
```bash
gcloud billing budgets create \
  --billing-account=YOUR_BILLING_ACCOUNT \
  --display-name="OnboardFlow Budget" \
  --budget-amount=10 \
  --threshold-rules-percent=50,90,100
```

## Cleanup

To delete all resources:
```bash
gcloud run services delete onboardflow --region=us-central1
gcloud pubsub subscriptions delete onboardflow-sub
gcloud pubsub topics delete new-hire-events
gcloud firestore databases delete --database-id="(default)"
```

## Troubleshooting

### Agent fails to initialize
- Check Gemini API key is set correctly
- Verify API key has access to Gemini 3.5 Flash

### Firestore writes fail
- Check service account has Firestore permissions
- Verify database exists in correct region

### Pub/Sub messages not triggering
- Verify push endpoint URL is correct
- Check Cloud Run service allows unauthenticated access
- Review Cloud Run logs for errors

## Production Considerations

For production deployment:
1. Use Secret Manager for API keys
2. Set up proper IAM roles
3. Enable VPC Service Controls
4. Configure Cloud Armor for DDoS protection
5. Set up Cloud Monitoring alerts
6. Implement proper error handling and retries
7. Add authentication to endpoints
8. Set up CI/CD pipeline

## Support

For issues or questions:
- Check Cloud Run logs
- Review Firestore state
- Test locally with `python demo.py`
- Consult Google ADK documentation
