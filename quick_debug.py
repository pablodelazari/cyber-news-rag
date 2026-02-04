import requests
import os
from dotenv import load_dotenv

load_dotenv()

def deep_debug():
    token = os.getenv("HACKERONE_API_TOKEN")
    identifier = os.getenv("HACKERONE_API_IDENTIFIER")
    url = "https://api.hackerone.com/v1/hacker"
    
    # Testing with minimal params
    params = {"page[size]": 1}
    print(f"Testing {url} with params: {params}...")
    try:
        r = requests.get(url, auth=(identifier, token), params=params, timeout=10)
        print(f"Status: {r.status_code}")
        print(r.text[:200])
    except Exception as e:
        print(e)
        
    # Testing with Sort Only
    params2 = {"page[size]": 3, "sort": "-latest_disclosable_activity_at"}
    print(f"\nTesting with Sort: {params2}")
    try:
        r = requests.get(url, auth=(identifier, token), params=params2, timeout=10)
        print(f"Status: {r.status_code}")
    except: pass

if __name__ == "__main__":
    deep_debug()
