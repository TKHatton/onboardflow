"""FastAPI server for OnboardFlow - Cloud Run deployment."""

import os
import json
import base64
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn

from .agent import OnboardFlowAgent


app = FastAPI(
    title="OnboardFlow",
    description="Autonomous employee onboarding workflow agent",
    version="0.1.0",
)


class NewHireEvent(BaseModel):
    """New hire event payload."""
    employee_name: str
    role: str
    department: str
    start_date: str
    email: str
    manager: Optional[str] = None
    manager_email: Optional[str] = None


class PubSubMessage(BaseModel):
    """Pub/Sub message format."""
    message: dict


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "OnboardFlow",
        "version": "0.1.0",
    }


@app.post("/onboard")
async def trigger_onboarding(event: NewHireEvent):
    """Trigger onboarding workflow directly via HTTP."""
    try:
        agent = OnboardFlowAgent()
        results = await agent.execute_onboarding(
            employee_name=event.employee_name,
            role=event.role,
            department=event.department,
            start_date=event.start_date,
            email=event.email,
            manager=event.manager,
            manager_email=event.manager_email,
        )
        return {
            "success": True,
            "message": "Onboarding workflow completed",
            "results": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pubsub")
async def handle_pubsub(request: Request):
    """Handle Pub/Sub push messages."""
    try:
        # Parse Pub/Sub envelope
        envelope = await request.json()
        
        if "message" not in envelope:
            raise HTTPException(status_code=400, detail="No Pub/Sub message received")
        
        pubsub_message = envelope["message"]
        
        # Decode the data
        if "data" in pubsub_message:
            data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
            event_data = json.loads(data)
        else:
            raise HTTPException(status_code=400, detail="No data in Pub/Sub message")
        
        # Create and execute onboarding
        agent = OnboardFlowAgent()
        results = await agent.execute_onboarding(
            employee_name=event_data["employee_name"],
            role=event_data["role"],
            department=event_data["department"],
            start_date=event_data["start_date"],
            email=event_data["email"],
            manager=event_data.get("manager"),
            manager_email=event_data.get("manager_email"),
        )
        
        return {
            "success": True,
            "message": "Onboarding workflow completed",
            "results": results,
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
