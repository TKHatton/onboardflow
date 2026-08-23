# Pub/Sub Integration Guide

OnboardFlow supports event-driven onboarding via Google Cloud Pub/Sub. HR systems can publish new hire events to a Pub/Sub topic, which automatically triggers the onboarding workflow.

## Architecture

```
HR System → Pub/Sub Topic → Push Subscription → Cloud Run (/api/pubsub/push) → OnboardFlow Agent
```

## Setup Instructions

### 1. Create a Pub/Sub Topic

```bash
gcloud pubsub topics create new-hire-events
```

### 2. Deploy OnboardFlow to Cloud Run

If not already deployed:

```bash
cd /home/tkhatton13/onboardflow
gcloud run deploy onboardflow \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=***"
```

Note the service URL (e.g., `https://onboardflow-xxx-uc.a.run.app`)

### 3. Create a Push Subscription

```bash
gcloud pubsub subscriptions create onboardflow-push \
  --topic=new-hire-events \
  --push-endpoint=https://onboardflow-xxx-uc.a.run.app/api/pubsub/push \
  --push-auth-service-account=pubsub-invoker@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

**Note:** Replace `onboardflow-xxx-uc.a.run.app` with your actual Cloud Run URL.

### 4. Set Up IAM Permissions

The Pub/Sub service account needs permission to invoke your Cloud Run service:

```bash
# Grant the Pub/Sub service account permission to invoke Cloud Run
gcloud run services add-iam-policy-binding onboardflow \
  --region=us-central1 \
  --member=serviceAccount:pubsub-invoker@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/run.invoker
```

## Publishing Messages

### From HR System (Python Example)

```python
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("YOUR_PROJECT_ID", "new-hire-events")

new_hire_data = {
    "employee_name": "Jane Smith",
    "role": "Product Manager",
    "department": "Product",
    "start_date": "2026-09-15",
    "email": "jane.smith@company.com",
    "manager": "John Doe"
}

# Publish message
data = json.dumps(new_hire_data).encode("utf-8")
future = publisher.publish(topic_path, data)
message_id = future.result()
print(f"Published message ID: {message_id}")
```

### From Command Line

```bash
gcloud pubsub topics publish new-hire-events \
  --message='{"employee_name":"Jane Smith","role":"Product Manager","department":"Product","start_date":"2026-09-15","email":"jane.smith@company.com","manager":"John Doe"}'
```

## Message Format

Pub/Sub messages must be JSON with these required fields:

```json
{
  "employee_name": "Jane Smith",
  "role": "Product Manager",
  "department": "Product",
  "start_date": "2026-09-15",
  "email": "jane.smith@company.com",
  "manager": "John Doe"  // optional
}
```

## Testing Locally

Use the included test script to simulate a Pub/Sub push:

```bash
# Start the backend server
cd /home/tkhatton13/onboardflow
python -m src.onboardflow.server

# In another terminal, run the test
python test_pubsub.py
```

The test script:
1. Creates a sample new hire message
2. Encodes it in Pub/Sub format (base64)
3. Sends it to `/api/pubsub/push`
4. Shows the response and workflow execution

## Monitoring

### View Pub/Sub Messages

```bash
# List messages in the topic (last 10 minutes)
gcloud pubsub subscriptions pull onboardflow-push --limit=10
```

### View Cloud Run Logs

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=onboardflow" \
  --limit=50
```

### View Workflow Execution

Each Pub/Sub message triggers a workflow with a unique ID. Check logs for:

```
[workflow-jane-smith-123456] {'type': 'reasoning_start', ...}
[workflow-jane-smith-123456] {'type': 'step_start', 'tool': 'provision_equipment', ...}
[workflow-jane-smith-123456] {'type': 'step_complete', ...}
```

## Error Handling

- **400 Bad Request**: Invalid message format or missing required fields
- **500 Internal Server Error**: Agent execution failed (check logs)
- **Retry Logic**: Pub/Sub automatically retries failed messages with exponential backoff

## Production Considerations

1. **Authentication**: The push endpoint should verify Pub/Sub authentication tokens
2. **Idempotency**: Handle duplicate messages (Pub/Sub may deliver the same message multiple times)
3. **Dead Letter Topic**: Configure a dead letter topic for messages that fail after retries
4. **Monitoring**: Set up alerts for failed message processing

## Integration with HR Systems

Common HR systems that can publish to Pub/Sub:

- **Workday**: Use Workday Studio or Cloud Connect
- **BambooHR**: Use webhooks + Cloud Functions to publish to Pub/Sub
- **Custom HRIS**: Direct integration using Pub/Sub client libraries

## Example: BambooHR Webhook

```python
# Cloud Function triggered by BambooHR webhook
from google.cloud import pubsub_v1
import functions_framework

@functions_framework.http
def bamboohr_webhook(request):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("PROJECT_ID", "new-hire-events")
    
    # Parse BambooHR webhook data
    data = request.get_json()
    new_hire = {
        "employee_name": f"{data['firstName']} {data['lastName']}",
        "role": data['jobTitle'],
        "department": data['department'],
        "start_date": data['hireDate'],
        "email": data['workEmail'],
        "manager": data.get('manager')
    }
    
    # Publish to Pub/Sub
    publisher.publish(topic_path, json.dumps(new_hire).encode("utf-8"))
    
    return "OK", 200
```

## Benefits

- **Event-Driven**: No polling, instant processing when new hires are added
- **Scalable**: Pub/Sub handles millions of messages per second
- **Reliable**: Guaranteed delivery with retries and dead letter topics
- **Decoupled**: HR systems don't need to know about OnboardFlow internals
- **Auditable**: All messages are logged and can be replayed if needed
