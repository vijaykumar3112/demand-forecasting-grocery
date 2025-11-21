import requests
import json

url = "http://localhost:8000/predict"
payload = {
    "item_id": 1,
    "store_id": 1,
    "date": "2024-12-01",
    "on_promotion": False
}

try:
    response = requests.post(url, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print(f"\n✅ Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\n❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Connection Error: {e}")
