#!/usr/bin/env python3
"""
Simple test script to verify Flask backend endpoints
"""
import requests
import json

def test_endpoints():
    base_url = "http://13.60.252.71:5000"

    print("Testing Flask Backend Endpoints...")
    print("=" * 50)

    # Test trains endpoint
    try:
        print("1. Testing /trains endpoint...")
        response = requests.get(f"{base_url}/trains")
        if response.status_code == 200:
            trains = response.json()
            print(f"   ✓ Success! Found {len(trains)} trains")
            print(f"   Sample train: {trains[0] if trains else 'None'}")
        else:
            print(f"   ✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test specific train endpoint
    try:
        print("\n2. Testing /train/1 endpoint...")
        response = requests.get(f"{base_url}/train/1")
        if response.status_code == 200:
            train = response.json()
            print(f"   ✓ Success! Train data: {train}")
        else:
            print(f"   ✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test train report data endpoint
    try:
        print("\n3. Testing /train-report-data endpoint...")
        params = {"name": "debojeetor rajdhani express", "status": "Unfinished", "id": "1"}
        response = requests.get(f"{base_url}/train-report-data", params=params)
        if response.status_code == 200:
            report = response.json()
            print(f"   ✓ Success! Report contains {len(report.get('door_details', []))} doors")
        else:
            print(f"   ✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

if __name__ == "__main__":
    test_endpoints()
