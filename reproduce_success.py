import requests

def reproduce():
    # Credentials that worked in Step 393
    identifier = "octopus_blackbelt"
    token = "qu7L9MibY8oEDyWyhFEEwn6yAjQB3uP/bErcVeo8SpU="
    
    url = "https://api.hackerone.com/v1/hackers/hacktivity"
    params = {"page[size]": 1}

    print(f"Testing {url} with hardcoded credentials...")
    print(f"User: {identifier}")
    print(f"Token: {token[:5]}...")

    try:
        r = requests.get(url, auth=(identifier, token), params=params, timeout=15)
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text[:300]}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    reproduce()
