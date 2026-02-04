import requests
import os
from dotenv import load_dotenv

load_dotenv()

def debug_api():
    token = os.getenv("HACKERONE_API_TOKEN")
    
    # List of identifiers to test
    identifiers_to_test = [
        "octopus_blackbelt", # Username
        "api_token",         # Generic guess
        "api_Identifier",     # Another common default
        "hackerone",         # Another guess
    ]

    url = "https://api.hackerone.com/v1/hackers/hacktivity"
    
    print(f"--- DEBUGGING NEW TOKEN ---")
    print(f"Token loaded: '{token[:5]}...{token[-5:]}'")
    print(f"Target URL: {url}\n")
    
    for ident in identifiers_to_test:
        print(f"Testing Identifier: '{ident}' ... ", end="")
        try:
            response = requests.get(
                url, 
                auth=(ident, token),
                params={"page[size]": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ SUCCESS! (Status: 200)")
                print(f"\n>>> FOUND VALID IDENTIFIER: {ident}")
                return
            elif response.status_code == 401:
                print(f"❌ Failed (401 Unauthorized)")
            else:
                print(f"⚠️ Error ({response.status_code})")
                print(f"Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"Exception: {e}")

    print("\n❌ All attempts failed.")

if __name__ == "__main__":
    debug_api()
