#!/usr/bin/env python3
"""
OnboardFlow Demo Script
Demonstrates the autonomous onboarding workflow with real-time state tracking.
"""

import asyncio
import json
from datetime import datetime
from src.onboardflow.agent import OnboardFlowAgent


async def demo_onboarding_workflow():
    """Demonstrate the complete onboarding workflow."""
    
    print("=" * 80)
    print("ONBOARDFLOW DEMO: Autonomous Employee Onboarding")
    print("=" * 80)
    print()
    print("Scenario: A new employee (Sarah Chen) is being hired as a Senior Software")
    print("Engineer. When HR adds her to the system, OnboardFlow automatically:")
    print("  1. Creates a Jira ticket for the onboarding process")
    print("  2. Sends a welcome message to the team Slack channel")
    print("  3. Schedules an orientation meeting")
    print("  4. Sends a welcome email to the new hire")
    print("  5. Tracks all actions in Firestore for audit and state management")
    print()
    print("-" * 80)
    print()
    
    # Initialize agent
    agent = OnboardFlowAgent()
    
    # New hire data
    new_hire = {
        "employee_name": "Sarah Chen",
        "role": "Senior Software Engineer",
        "department": "Engineering",
        "start_date": "2026-09-15",
        "email": "sarah.chen@example.com",
        "manager": "Alex Rodriguez",
        "manager_email": "alex.rodriguez@example.com"
    }
    
    print("NEW HIRE DETAILS:")
    print(json.dumps(new_hire, indent=2))
    print()
    print("-" * 80)
    print()
    print("EXECUTING ONBOARDING WORKFLOW...")
    print()
    
    # Execute workflow
    results = await agent.execute_onboarding(**new_hire)
    
    print()
    print("-" * 80)
    print()
    print("WORKFLOW COMPLETE!")
    print()
    print("RESULTS SUMMARY:")
    print(f"  Workflow ID: {results['workflow_id']}")
    print(f"  Status: {results['status']}")
    print(f"  Started: {results['started_at']}")
    print(f"  Completed: {results['completed_at']}")
    print()
    print("STEPS EXECUTED:")
    for i, step in enumerate(results['steps'], 1):
        tool_result = step['result']
        status = "✓" if tool_result.get('success') else "✗"
        print(f"  {status} Step {i}: {step['step']}")
        if not tool_result.get('success'):
            print(f"      Error: {tool_result.get('error', 'Unknown error')}")
    
    print()
    print("-" * 80)
    print()
    print("FIRESTORE STATE:")
    print("  All workflow state has been persisted to Firestore.")
    print("  This enables:")
    print("    • Audit trail of all onboarding actions")
    print("    • Resume capability if workflow fails mid-execution")
    print("    • Analytics and reporting on onboarding metrics")
    print("    • State inspection for debugging")
    print()
    print("=" * 80)
    print()
    print("DEMO COMPLETE")
    print()
    print("Key Features Demonstrated:")
    print("  ✓ Autonomous workflow execution (no human intervention)")
    print("  ✓ Multi-tool orchestration (Jira, Slack, Calendar, Email)")
    print("  ✓ State tracking and persistence (Firestore)")
    print("  ✓ Error handling and graceful degradation")
    print("  ✓ Real-time logging and observability")
    print()
    print("Built with:")
    print("  • Google ADK (Agent Development Kit)")
    print("  • Gemini 3.5 Flash")
    print("  • Google Cloud Run")
    print("  • Google Firestore")
    print("  • Google Pub/Sub")
    print()


if __name__ == "__main__":
    asyncio.run(demo_onboarding_workflow())
