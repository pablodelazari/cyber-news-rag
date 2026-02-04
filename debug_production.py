import requests
import os
from dotenv import load_dotenv

load_dotenv()

def debug_production():
    token = os.getenv("HACKERONE_API_TOKEN")
    identifier = os.getenv("HACKERONE_API_IDENTIFIER")
    
    # 1. Base Endpoint
    url = "https://api.hackerone.com/v1/hackers/hacktivity"
    
    print(f"--- PRODUCTION DEBUG ---")
    print(f"User: {identifier}")
    print(f"Token: {token[:5]}...")
    print(f"Endpoint: {url}")

    # Test 1: No Params (Auth Check)
    print("\n[TEST 1] No Parameters (Checking Auth)...")
    try:
        r = requests.get(url, auth=(identifier, token), timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code != 200:
            print(f"Response: {r.text}")
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    # Test 2: Sort Param
    print("\n[TEST 2] Adding 'sort' param...")
    params = {"sort": "-latest_disclosable_activity_at"}
    try:
        r = requests.get(url, auth=(identifier, token), params=params, timeout=10)
        print(f"Status: {r.status_code}")
    except Exception as e: print(e)

    # Test 3: QueryString Param (The likely culprit)
    print("\n[TEST 3] Adding 'queryString' param...")
    params = {"queryString": "disclosed:true"}
    try:
        r = requests.get(url, auth=(identifier, token), params=params, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code != 200:
            print(f"Response: {r.text}")
    except Exception as e: print(e)

    # Test 4: All Params Combined
    print("\n[TEST 4] Full Application Params...")
    params = {
        "page[size]": 3,
        "sort": "-latest_disclosable_activity_at",
        "queryString": "disclosed:true"
    }
    try:
        r = requests.get(url, auth=(identifier, token), params=params, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("✅ SUCCESS with full params!")
        else:
            print("❌ FAILED with full params.")
            print(f"Response: {r.text}")
    except Exception as e: print(e)

if __name__ == "__main__":
    debug_production()
