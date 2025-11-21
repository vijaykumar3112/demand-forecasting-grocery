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
    print(f"Full Response:")
    print(response.text)
    if response.status_code != 200:
        try:
            error_data = response.json()
            print(f"\nError Detail: {error_data.get('detail', 'No detail')}")
        except:
            pass
except Exception as e:
    print(f"Request Error: {e}")
    import traceback
    traceback.print_exc()
