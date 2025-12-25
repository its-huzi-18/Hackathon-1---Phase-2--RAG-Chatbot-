#!/usr/bin/env python3
"""
Simple test script to verify the RAG Chatbot API is working
"""

import requests
import json
import time

def test_api():
    """Test the RAG Chatbot API"""
    base_url = "http://localhost:8000"

    print("Testing RAG Chatbot API...")
    print(f"Base URL: {base_url}")

    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✓ Health check passed: {health_data['status']}")
            print(f"   ✓ Collections: {health_data['collections']}")
        else:
            print(f"   ✗ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
        print("   Make sure the API server is running on http://localhost:8000")
        return

    # Test 2: Collections endpoint
    print("\n2. Testing collections endpoint...")
    try:
        response = requests.get(f"{base_url}/collections")
        if response.status_code == 200:
            collections_data = response.json()
            print(f"   ✓ Collections retrieved: {collections_data['collections']}")
        else:
            print(f"   ✗ Collections endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Collections endpoint error: {e}")

    # Test 3: Query endpoint (if collections exist)
    print("\n3. Testing query endpoint...")
    try:
        query_data = {
            "query": "What is this book about?",
            "top_k": 3
        }

        response = requests.post(
            f"{base_url}/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps(query_data)
        )

        if response.status_code == 200:
            query_result = response.json()
            print(f"   ✓ Query successful")
            print(f"   Query: {query_result['query']}")
            print(f"   Response: {query_result['response'][:100]}...")
            print(f"   Sources: {query_result['total_chunks']}")
        else:
            print(f"   ✗ Query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Query endpoint error: {e}")
        print("   This might be because there's no content in the database yet.")
        print("   Make sure to run process_book.py first to populate the knowledge base.")

    print("\n" + "="*50)
    print("API Test Complete!")
    print("\nNext steps:")
    print("1. If you haven't processed your book content yet, run: python process_book.py")
    print("2. Make sure your API server is running: python start_api.py")
    print("3. Then run this test again")

if __name__ == "__main__":
    test_api()