#!/usr/bin/env python3
"""
Test script to verify the API endpoints are working properly
"""
import sys
import os
import requests
import time

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_api_locally():
    """Test the API endpoints locally by importing and running them directly"""
    print("Testing API endpoints...")

    # Import the API app directly
    try:
        from backend.api import app
        print("+ Successfully imported API app")
        print(f"+ Number of routes: {len(app.router.routes)}")

        # Print available routes
        print("\nAvailable routes:")
        for route in app.router.routes:
            methods = getattr(route, 'methods', 'N/A') if hasattr(route, 'methods') else 'N/A'
            path = getattr(route, 'path', 'N/A')
            print(f"  - {path} ({methods})")

        # Check if /ask endpoint exists
        ask_endpoint_exists = any(route.path == '/ask' for route in app.router.routes if hasattr(route, 'path'))
        if ask_endpoint_exists:
            print("+ /ask endpoint exists")
        else:
            print("- /ask endpoint NOT found")
            return False

        # Check if /health endpoint exists
        health_endpoint_exists = any(route.path == '/health' for route in app.router.routes if hasattr(route, 'path'))
        if health_endpoint_exists:
            print("+ /health endpoint exists")
        else:
            print("- /health endpoint NOT found")
            return False

        return True

    except Exception as e:
        print(f"- Error importing API: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_locally()
    if success:
        print("\n+ All API endpoints are properly defined!")
    else:
        print("\n- There are issues with the API endpoints")
        sys.exit(1)