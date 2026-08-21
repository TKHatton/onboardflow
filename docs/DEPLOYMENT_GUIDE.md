# OnboardFlow - Google Cloud Deployment Guide

This guide walks you through deploying OnboardFlow to Google Cloud Platform for the hackathon submission.

## Prerequisites

- Google Cloud account with billing enabled
- gcloud CLI installed and authenticated
- Docker installed
- Gemini API key (from https://aistudio.google.com/apikey)

## Step 1: Create Google Cloud Project

```bash
# Set your project ID (must be globally unique)
export PROJECT_ID=onboardflow-yourname-2026
gcloud projects create $PROJECT_ID

# Set as active project
gcloud config set project $PROJECT_ID

# Enable billing (required for Cloud Run)
# Visit: https://console.cloud.google.com/billing
```

## Step 2: Enable Required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com
```

## Step 3: Create Artifact Registry Repository

```bash
# Create repository for Docker images
gcloud artifacts repositories create onboardflow \
  --repository-format=docker \
  --location=us-central1 \
  --description="OnboardFlow Docker images"
```

## Step 4: Build and Push Backend Docker Image

```bash
# Navigate to project root
cd /path/to/onboardflow

# Build the image
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/$PROJECT_ID/onboardflow/backend:latest

# Verify the image was pushed
gcloud artifacts docker images list us-central1-docker.pkg.dev/$PROJECT_ID/onboardflow
```

## Step 5: Deploy Backend to Cloud Run

```bash
# Deploy with environment variables
gcloud run deploy onboardflow-backend \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/onboardflow/backend:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=***" \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10

# Note the service URL from the output
export BACKEND_URL=$(gcloud run services describe onboardflow-backend --region=us-central1 --format='value(status.url)')
echo "Backend URL: $BACKEND_URL"
```

## Step 6: Build Frontend with Backend URL

```bash
cd frontend

# Create production build with backend URL
VITE_API_URL=$BACKEND_URL npm run build

# Verify the build
ls -la dist/
```

## Step 7: Deploy Frontend to Cloud Run

```bash
# Create a simple nginx config for serving the frontend
cat > nginx.conf << 'EOF'
server {
    listen 8080;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        return 404;
    }
}
EOF

# Create Dockerfile for frontend
cat > Dockerfile.frontend << 'EOF'
FROM nginx:alpine
COPY dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
EOF

# Build and push frontend image
gcloud builds submit \
  --file=Dockerfile.frontend \
  --tag=us-central1-docker.pkg.dev/$PROJECT_ID/onboardflow/frontend:latest

# Deploy frontend
gcloud run deploy onboardflow-frontend \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/onboardflow/frontend:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=256Mi \
  --cpu=1

# Get frontend URL
export FRONTEND_URL=$(gcloud run services describe onboardflow-frontend --region=us-central1 --format='value(status.url)')
echo "Frontend URL: $FRONTEND_URL"
```

## Step 8: Configure CORS (if needed)

If the frontend can't reach the backend, update the backend CORS settings:

```bash
# Update backend to allow frontend origin
gcloud run services update onboardflow-backend \
  --set-env-vars="CORS_ORIGINS=$FRONTEND_URL" \
  --region=us-central1
```

## Step 9: Test Deployment

```bash
# Test backend health
curl $BACKEND_URL/health

# Test frontend (open in browser)
echo "Open in browser: $FRONTEND_URL"

# Test a sample onboarding workflow
curl -X POST $BACKEND_URL/api/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "employee_name": "Test User",
    "role": "Software Engineer",
    "department": "Engineering",
    "start_date": "2026-02-01",
    "email": "test@example.com",
    "manager": "Test Manager"
  }'
```

## Step 10: Verify Everything Works

1. Open the frontend URL in your browser
2. Fill out the onboarding form
3. Click "Start Onboarding"
4. Watch the real-time dashboard
5. Test the chatbot

## Cost Management

To minimize costs during the hackathon:

- **Cloud Run**: Only pay for requests (free tier: 2M requests/month)
- **Gemini API**: Free tier available (check current limits)
- **Artifact Registry**: Free tier: 5GB storage
- **Min instances**: Set to 0 (already configured)

Monitor costs:
```bash
gcloud billing accounts list
# Visit: https://console.cloud.google.com/billing
```

## Troubleshooting

### Backend not starting
```bash
# Check logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=onboardflow-backend" --limit=50

# Common issues:
# - Missing GOOGLE_API_KEY
# - Insufficient memory (increase to 1Gi)
# - API not enabled
```

### Frontend can't reach backend
```bash
# Check CORS settings
# Ensure VITE_API_URL was set during build
# Rebuild frontend with correct URL
```

### Gemini API errors
```bash
# Verify API key is valid
# Check quota limits: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
# Ensure billing is enabled
```

## Cleanup

To delete all resources after the hackathon:

```bash
# Delete Cloud Run services
gcloud run services delete onboardflow-backend --region=us-central1
gcloud run services delete onboardflow-frontend --region=us-central1

# Delete Artifact Registry
gcloud artifacts repositories delete onboardflow --location=us-central1

# Delete project (removes everything)
gcloud projects delete $PROJECT_ID
```

## Submission URLs

For your Devpost submission, you'll need:

- **Backend URL**: `$BACKEND_URL`
- **Frontend URL**: `$FRONTEND_URL`
- **GitHub Repo**: https://github.com/TKHatton/onboardflow

Save these URLs for your submission!
