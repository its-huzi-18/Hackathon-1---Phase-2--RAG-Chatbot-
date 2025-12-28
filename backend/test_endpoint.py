#!/usr/bin/env python3
"""
Test script to verify the API endpoints are properly defined
"""
import requests
import sys

def test_api_endpoints(backend_url):
    """Test if the API endpoints are accessible"""
    print(f"Testing backend API at: {backend_url}")

    # Test health endpoint
    try:
        health_response = requests.get(f"{backend_url}/health")
        print(f"Health endpoint status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"Health response: {health_response.json()}")
        else:
            print(f"Health endpoint failed with status: {health_response.status_code}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")

    # Test ask endpoint
    try:
        ask_response = requests.post(
            f"{backend_url}/ask",
            json={"question": "test"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Ask endpoint status: {ask_response.status_code}")
        if ask_response.status_code == 200:
            print("Ask endpoint working correctly")
        else:
            print(f"Ask endpoint failed with status: {ask_response.status_code}")
            print(f"Response: {ask_response.text}")
    except Exception as e:
        print(f"Error testing ask endpoint: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_endpoint.py <backend_url>")
        sys.exit(1)

    backend_url = sys.argv[1]
    test_api_endpoints(backend_url)