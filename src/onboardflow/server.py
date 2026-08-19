"""FastAPI server with SSE streaming for real-time workflow updates."""

import os
import json
import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

from .autonomous_agent import AutonomousAgent


app = FastAPI(
    title="OnboardFlow API",
    description="Autonomous employee onboarding with real-time streaming",
    version="2.0.0",
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewHireRequest(BaseModel):
    """New hire request payload."""
    employee_name: str
    role: str
    department: str
    start_date: str
    email: str
    manager: str | None = None


class ChatRequest(BaseModel):
    """Chat question payload."""
    employee_name: str
    question: str
    context: dict | None = None


@app.get("/")
async def root():
    """Health check."""
    return {
        "status": "healthy",
        "service": "OnboardFlow",
        "version": "2.0.0",
        "features": ["autonomous_reasoning", "real_time_streaming", "multi_tool_orchestration"]
    }


@app.post("/api/onboard")
async def start_onboarding(request: NewHireRequest):
    """
    Start autonomous onboarding workflow.
    Returns workflow_id for streaming updates.
    """
    # For now, just return a workflow_id
    # The actual workflow will be started via the stream endpoint
    workflow_id = f"workflow-{request.employee_name.lower().replace(' ', '-')}"
    
    return {
        "workflow_id": workflow_id,
        "message": "Use /api/onboard/stream to start and stream the workflow",
        "employee": request.employee_name
    }


@app.post("/api/onboard/stream")
async def stream_onboarding(request: NewHireRequest):
    """
    Start onboarding workflow and stream updates via SSE.
    This is the main endpoint for the React frontend.
    """
    
    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events from autonomous agent."""
        try:
            agent = AutonomousAgent()
            
            async for update in agent.plan_onboarding(
                employee_name=request.employee_name,
                role=request.role,
                department=request.department,
                start_date=request.start_date,
                email=request.email,
                manager=request.manager,
            ):
                # Format as SSE
                yield f"data: {json.dumps(update)}\n\n"
                
                # Small delay for visual effect in demo
                await asyncio.sleep(0.5)
                
        except Exception as e:
            error_event = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Answer onboarding questions using the chatbot.
    """
    try:
        agent = AutonomousAgent()
        response = agent.chat(
            employee_name=request.employee_name,
            question=request.question,
            context=request.context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
