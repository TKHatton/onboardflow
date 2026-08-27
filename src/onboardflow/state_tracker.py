"""Firestore state tracking for OnboardFlow.

Best-effort: any Firestore error (missing permissions, no credentials on a
local dev machine, network issues) is caught and logged, never allowed to
break the onboarding workflow itself. Without a usable Firestore client,
every method here is a silent no-op.
"""

import os
from datetime import datetime
from typing import Optional, Any

try:
    from google.cloud import firestore
except ImportError:  # pragma: no cover - dependency is always installed in prod
    firestore = None


class StateTracker:
    """Track onboarding workflow state in Firestore."""

    COLLECTION = "onboarding_workflows"

    def __init__(self, project_id: Optional[str] = None, database_id: str = "(default)"):
        """Initialize a Firestore client, if one can be created.

        Args:
            project_id: Google Cloud project ID. If not given, the client
                library resolves it from GOOGLE_CLOUD_PROJECT, Application
                Default Credentials, or the GCP metadata server (which is how
                this works on Cloud Run with no configuration needed).
            database_id: Firestore database ID (default: "(default)")
        """
        self.db = None
        if firestore is None:
            return
        try:
            self.db = firestore.Client(
                project=project_id or os.getenv("GOOGLE_CLOUD_PROJECT"),
                database=database_id,
            )
        except Exception as e:
            print(f"[STATE] Firestore unavailable, state tracking disabled: {e}")

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
            workflow_id: Unique ID for this onboarding workflow. Generated
            even when Firestore is unavailable, so callers always get one.
        """
        workflow_id = f"onboard-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        if self.db:
            try:
                doc_ref = self.db.collection(self.COLLECTION).document(workflow_id)
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
            except Exception as e:
                print(f"[STATE] Failed to log workflow start: {e}")

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
            try:
                doc_ref = self.db.collection(self.COLLECTION).document(workflow_id)
                doc_ref.update({
                    "steps": firestore.ArrayUnion([{
                        "step": step_name,
                        "success": success,
                        "result": result,
                        "completed_at": datetime.now().isoformat(),
                    }])
                })
            except Exception as e:
                print(f"[STATE] Failed to log step: {e}")

        status = "OK" if success else "FAILED"
        print(f"[STATE] {status}: {step_name}")

    async def log_workflow_complete(self, workflow_id: str):
        """Mark workflow as complete."""
        if self.db:
            try:
                doc_ref = self.db.collection(self.COLLECTION).document(workflow_id)
                doc_ref.update({
                    "status": "completed",
                    "completed_at": datetime.now().isoformat(),
                })
            except Exception as e:
                print(f"[STATE] Failed to mark workflow complete: {e}")

        print(f"[STATE] Workflow completed: {workflow_id}")

    async def log_workflow_failed(self, workflow_id: str, error: str):
        """Mark workflow as failed."""
        if self.db:
            try:
                doc_ref = self.db.collection(self.COLLECTION).document(workflow_id)
                doc_ref.update({
                    "status": "failed",
                    "error": error,
                    "completed_at": datetime.now().isoformat(),
                })
            except Exception as e:
                print(f"[STATE] Failed to mark workflow failed: {e}")

        print(f"[STATE] Workflow failed: {workflow_id} - {error}")

    async def get_workflow(self, workflow_id: str) -> Optional[dict]:
        """Retrieve full workflow state from Firestore, including its steps."""
        if not self.db:
            return None
        try:
            doc_ref = self.db.collection(self.COLLECTION).document(workflow_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                data["workflow_id"] = doc.id
                return data
        except Exception as e:
            print(f"[STATE] Failed to get workflow: {e}")
        return None

    async def list_recent_workflows(self, limit: int = 20) -> list[dict]:
        """List the most recent onboarding workflows, newest first.

        Returns a lightweight summary per workflow (no step detail) for a
        history list view. Empty list if Firestore is unavailable.
        """
        if not self.db:
            return []
        try:
            query = (
                self.db.collection(self.COLLECTION)
                .order_by("started_at", direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            results = []
            for doc in query.stream():
                data = doc.to_dict() or {}
                results.append({
                    "workflow_id": doc.id,
                    "employee_name": data.get("employee_name"),
                    "role": data.get("role"),
                    "department": data.get("department"),
                    "status": data.get("status"),
                    "started_at": data.get("started_at"),
                    "completed_at": data.get("completed_at"),
                    "step_count": len(data.get("steps", [])),
                })
            return results
        except Exception as e:
            print(f"[STATE] Failed to list workflows: {e}")
            return []
