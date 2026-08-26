#!/usr/bin/env python3
"""
Test script to simulate a Pub/Sub push message to OnboardFlow.
This demonstrates the event-driven architecture where HR systems
can publish new hire events to Pub/Sub.
"""

import os
import requests
import json
import base64

# Backend URL. Override with BACKEND_URL to target a deployed instance, e.g.
# BACKEND_URL=https://onboardflow-883489836236.europe-west1.run.app python test_pubsub.py
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Sample new hire data
new_hire_data = {
    "employee_name": "Alex Johnson",
    "role": "Senior Software Engineer",
    "department": "Engineering",
    "start_date": "2026-09-01",
    "email": "alex.johnson@company.com",
    "manager": "Sarah Chen"
}

# Encode data as base64 (Pub/Sub format)
data_json = json.dumps(new_hire_data)
data_base64 = base64.b64encode(data_json.encode("utf-8")).decode("utf-8")

# Create Pub/Sub message envelope
pubsub_message = {
    "message": {
        "data": data_base64,
        "messageId": "test-message-123",
        "publishTime": "2026-08-23T18:00:00.000Z"
    }
}

print("=" * 60)
print("OnboardFlow - Pub/Sub Integration Test")
print("=" * 60)
print()
print("Simulating Pub/Sub push message...")
print()
print("New Hire Data:")
print(json.dumps(new_hire_data, indent=2))
print()
print("Sending to:", f"{BACKEND_URL}/api/pubsub/push")
print()

try:
    # Send POST request to Pub/Sub push endpoint
    response = requests.post(
        f"{BACKEND_URL}/api/pubsub/push",
        json=pubsub_message,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print("Response Status:", response.status_code)
    print()
    
    if response.status_code == 200:
        print("✓ SUCCESS: Pub/Sub message processed successfully!")
        print()
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        print()
        print("The onboarding workflow has been triggered automatically.")
        print("Check the backend logs to see the agent executing tools.")
    else:
        print("✗ FAILED: Unexpected status code")
        print()
        print("Response:")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("✗ ERROR: Could not connect to backend")
    print()
    print("Make sure the backend is running:")
    print("  cd /home/tkhatton13/onboardflow")
    print("  python -m src.onboardflow.server")
    
except Exception as e:
    print(f"✗ ERROR: {e}")

print()
print("=" * 60)
