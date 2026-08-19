#!/usr/bin/env python3
"""OnboardFlow CLI - Test the onboarding workflow."""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from onboardflow.agent import OnboardFlowAgent


async def test_onboarding():
    """Test the onboarding workflow with sample data."""
    print("=" * 60)
    print("OnboardFlow - Testing Onboarding Workflow")
    print("=" * 60)
    
    # Sample new hire data
    new_hire = {
        "employee_name": "Sarah Chen",
        "role": "Senior Software Engineer",
        "department": "Engineering",
        "start_date": "2026-09-15",
        "email": "sarah.chen@example.com",
        "manager": "Alex Rodriguez",
        "manager_email": "alex.rodriguez@example.com",
    }
    
    print(f"\nNew Hire Details:")
    print(f"  Name: {new_hire['employee_name']}")
    print(f"  Role: {new_hire['role']}")
    print(f"  Department: {new_hire['department']}")
    print(f"  Start Date: {new_hire['start_date']}")
    print(f"  Email: {new_hire['email']}")
    print(f"  Manager: {new_hire['manager']}")
    
    # Create agent and execute workflow
    agent = OnboardFlowAgent()
    
    print("\n" + "=" * 60)
    print("Executing Onboarding Workflow...")
    print("=" * 60)
    
    results = await agent.execute_onboarding(**new_hire)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Workflow Summary")
    print("=" * 60)
    print(f"Employee: {results['employee_name']}")
    print(f"Started: {results['started_at']}")
    print(f"Completed: {results['completed_at']}")
    print(f"Status: {results['status']}")
    print(f"\nSteps Completed: {len(results['steps'])}")
    
    for i, step in enumerate(results['steps'], 1):
        status = "✓" if step['result']['success'] else "✗"
        print(f"  {status} Step {i}: {step['step']}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    asyncio.run(test_onboarding())
