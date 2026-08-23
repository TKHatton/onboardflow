#!/usr/bin/env python3
"""Test OnboardFlow imports and basic structure."""
import sys
sys.path.insert(0, 'src')

try:
    from onboardflow.server import app
    print("✓ Server import OK")
    print(f"  Routes: {[r.path for r in app.routes if hasattr(r, 'path')]}")
except Exception as e:
    print(f"✗ Server import failed: {e}")

try:
    from onboardflow.autonomous_agent import AutonomousAgent
    print("✓ AutonomousAgent import OK")
except Exception as e:
    print(f"✗ AutonomousAgent import failed: {e}")

# Check if GOOGLE_API_KEY is set
import os
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"✓ GOOGLE_API_KEY is set ({len(api_key)} chars)")
else:
    print("✗ GOOGLE_API_KEY not set - cannot test live Gemini path")
