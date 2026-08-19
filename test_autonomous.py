#!/usr/bin/env python3
"""Test the autonomous agent with real Gemini reasoning."""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from onboardflow.autonomous_agent import AutonomousAgent


async def test_autonomous_agent():
    """Test the autonomous agent with different roles."""
    
    print("=" * 80)
    print("ONBOARDFLOW AUTONOMOUS AGENT TEST")
    print("=" * 80)
    print()
    
    # Test case 1: Software Engineer
    print("TEST CASE 1: Software Engineer")
    print("-" * 80)
    
    agent = AutonomousAgent()
    
    async for update in agent.plan_onboarding(
        employee_name="Sarah Chen",
        role="Software Engineer",
        department="Engineering",
        start_date="2026-02-01",
        email="sarah.chen@company.com",
        manager="Alex Rodriguez"
    ):
        event_type = update.get("type")
        
        if event_type == "reasoning_start":
            print(f"\n🤔 {update['message']}")
        
        elif event_type == "reasoning_complete":
            print(f"\n💭 AGENT REASONING:")
            print(f"   {update['reasoning']}")
            print(f"\n📋 PLANNED STEPS: {update['steps_planned']}")
        
        elif event_type == "step_start":
            print(f"\n▶️  Step {update['step']}: {update['action']}")
            print(f"   Tool: {update['tool']}")
        
        elif event_type == "step_complete":
            print(f"   ✅ Completed: {update['tool']}")
            if 'result' in update:
                result = update['result']
                if result.get('success'):
                    print(f"      Result: {result.get('message', 'Success')}")
        
        elif event_type == "step_error":
            print(f"   ❌ Error in step {update['step']}: {update['message']}")
        
        elif event_type == "workflow_complete":
            print(f"\n{'=' * 80}")
            print(f"✅ {update['message']}")
            print(f"   Total steps: {update['total_steps']}")
            print(f"{'=' * 80}\n")
    
    # Test case 2: Marketing Manager
    print("\n\n")
    print("TEST CASE 2: Marketing Manager")
    print("-" * 80)
    
    async for update in agent.plan_onboarding(
        employee_name="Michael Torres",
        role="Marketing Manager",
        department="Marketing",
        start_date="2026-02-15",
        email="michael.torres@company.com",
        manager="Jennifer Lee"
    ):
        event_type = update.get("type")
        
        if event_type == "reasoning_start":
            print(f"\n🤔 {update['message']}")
        
        elif event_type == "reasoning_complete":
            print(f"\n💭 AGENT REASONING:")
            print(f"   {update['reasoning']}")
            print(f"\n📋 PLANNED STEPS: {update['steps_planned']}")
        
        elif event_type == "step_start":
            print(f"\n▶️  Step {update['step']}: {update['action']}")
            print(f"   Tool: {update['tool']}")
        
        elif event_type == "step_complete":
            print(f"   ✅ Completed: {update['tool']}")
        
        elif event_type == "step_error":
            print(f"   ❌ Error in step {update['step']}: {update['message']}")
        
        elif event_type == "workflow_complete":
            print(f"\n{'=' * 80}")
            print(f"✅ {update['message']}")
            print(f"   Total steps: {update['total_steps']}")
            print(f"{'=' * 80}\n")


if __name__ == "__main__":
    asyncio.run(test_autonomous_agent())
