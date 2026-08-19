"""Firestore state tracking for OnboardFlow."""

import os
from datetime import datetime
from typing import Optional, Any
from google.cloud import firestore


class StateTracker:
    """Track onboarding workflow state in Firestore."""
    
    def __init__(self, project_id: Optional[str] = None, database_id: str = "(default)"):
        """Initialize Firestore client.
        
        Args:
            project_id: Google Cloud project ID (uses env var if not provided)
            database_id: Firestore database ID (default: "(default)")
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.database_id = database_id
        
        if self.project_id:
            self.db = firestore.Client(
                project=self.project_id,
                database=self.database_id
            )
        else:
            # Local development without project
            self.db = None
    
    async def log_workflow_start(
        self,
        employee_name: str,
        role: str,
        department: str,
        start_date: str,
        email: str,
    ) -> str:
        """Log workflow start to Firestore.
        
        Returns:
            workflow_id: Unique ID for this onboarding workflow
        """
        workflow_id = f"onboard-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if self.db:
            doc_ref = self.db.collection("onboarding_workflows").document(workflow_id)
            doc_ref.set({
                "employee_name": employee_name,
                "role": role,
                "department": department,
                "start_date": start_date,
                "email": email,
                "status": "in_progress",
                "started_at": datetime.now().isoformat(),
                "completed_at": None,
                "steps": [],
            })
        
        print(f"[STATE] Workflow started: {workflow_id}")
        return workflow_id
    
    async def log_step(
        self,
        workflow_id: str,
        step_name: str,
        success: bool,
        result: dict,
    ):
        """Log a completed step to Firestore."""
        if self.db:
            doc_ref = self.db.collection("onboarding_workflows").document(workflow_id)
            doc_ref.update({
                "steps": firestore.ArrayUnion([{
                    "step": step_name,
                    "success": success,
                    "result": result,
                    "completed_at": datetime.now().isoformat(),
                }])
            })
        
        status = "✓" if success else "✗"
        print(f"[STATE] {status} Step completed: {step_name}")
    
    async def log_workflow_complete(self, workflow_id: str):
        """Mark workflow as complete."""
        if self.db:
            doc_ref = self.db.collection("onboarding_workflows").document(workflow_id)
            doc_ref.update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
            })
        
        print(f"[STATE] Workflow completed: {workflow_id}")
    
    async def log_workflow_failed(self, workflow_id: str, error: str):
        """Mark workflow as failed."""
        if self.db:
            doc_ref = self.db.collection("onboarding_workflows").document(workflow_id)
            doc_ref.update({
                "status": "failed",
                "error": error,
                "completed_at": datetime.now().isoformat(),
            })
        
        print(f"[STATE] Workflow failed: {workflow_id} - {error}")
    
    async def get_workflow(self, workflow_id: str) -> Optional[dict]:
        """Retrieve workflow state from Firestore."""
        if self.db:
            doc_ref = self.db.collection("onboarding_workflows").document(workflow_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
        return None
