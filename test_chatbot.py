#!/usr/bin/env python3
"""
Test script to verify the chatbot API endpoints are working properly
"""
import requests
import json

def test_api_endpoints():
    # Test the API endpoints
    base_url = "http://localhost:8000"  # Default, can be changed

    print("Testing API endpoints...")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Health endpoint is working")
            health_data = response.json()
            print(f"  Collections: {health_data.get('collections', [])}")
        else:
            print("✗ Health endpoint failed")
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")

    # Test /ask endpoint
    try:
        test_payload = {
            "question": "What is this book about?"
        }
        response = requests.post(
            f"{base_url}/ask",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_payload)
        )
        if response.status_code == 200:
            print("✓ /ask endpoint is working")
            data = response.json()
            print(f"  Sample response: {data.get('answer', '')[:100]}...")
        else:
            print(f"✗ /ask endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ /ask endpoint error: {e}")

    # Test /query endpoint
    try:
        test_payload = {
            "query": "What is this book about?",
            "top_k": 3,
            "collection_name": "book_knowledge_base"
        }
        response = requests.post(
            f"{base_url}/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_payload)
        )
        if response.status_code == 200:
            print("✓ /query endpoint is working")
            data = response.json()
            print(f"  Sample response: {data.get('response', '')[:100]}...")
        else:
            print(f"✗ /query endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ /query endpoint error: {e}")

if __name__ == "__main__":
    print("Testing the RAG Chatbot API endpoints...")
    print("Note: Make sure the backend API server is running on http://localhost:8000")
    test_api_endpoints()