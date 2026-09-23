import sys
from fastapi.testclient import TestClient
from main import app

# Initialize the diagnostic client
client = TestClient(app)

def run_diagnostics():
    print("========================================")
    print("NEXUS MATRIX : DIAGNOSTIC ENGINE")
    print("========================================\n")
    
    # TEST 1: Global Floor Pull
    print("[TEST 1] Pinging Global Matrix Floor (?category=all)")
    response = client.get("/api/matrix?category=all")
    
    if response.status_code == 200:
        data = response.json()
        print(f"-> Status: {data.get('status').upper()}")
        
        items = data.get('items', [])
        print(f"-> Items Cleared to Floor: {len(items)}\n")
        
        for item in items:
            name = item.get('name')
            cost = item.get('cost')
            retail = item.get('price')
            margin = item.get('margin_pct')
            print(f"   [+] {name}")
            print(f"       Cost: ${cost:.2f} | Retail: ${retail:.2f} | Margin: {margin}%\n")
    else:
        print(f"-> [ERROR] API failed with status: {response.status_code}\n")

    # TEST 2: Hunter Agent Verification
    print("----------------------------------------")
    print("[TEST 2] Verifying vp_acquisitions Agent (Room 21)")
    response = client.get("/api/matrix?category=room 21: pre-release acquisitions")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        if items:
            print("-> [SUCCESS] Hunter Agent intercepted the pre-release.")
            print(f"-> Target Secured: {items[0]['name']}")
            print(f"-> Authorized Purchase Price: ${items[0]['cost']:.2f} (20% over MSRP)")
        else:
            print("-> [FAILED] Hunter agent did not return the item.")
    else:
        print(f"-> [ERROR] API failed with status: {response.status_code}")
        
    print("\n========================================")
    print("DIAGNOSTIC COMPLETE")
    print("========================================")

if __name__ == "__main__":
    run_diagnostics()
