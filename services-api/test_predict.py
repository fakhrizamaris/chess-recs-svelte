import requests
import json

url = "http://localhost:8001/predict"
payload = {
    "user_rating": 1500,
    "favorite_openings": ["Sicilian Defense"],
    # Alpha 0.3 means 70% Collaborative score!
    "alpha": 0.3
}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
        exit()
        
    data = response.json()
    if len(data) > 0:
        print("First Recommendation:")
        print(f"Opening: {data[0].get('opening_name')}")
        print(f"Hybrid Score: {data[0].get('hybrid_score')}")
        print(f"Content Score: {data[0].get('cb_score')}")
        print(f"Collab Score:  {data[0].get('cf_score')}") 
        # Check if CF score is non-zero
        if data[0].get('cf_score', 0) > 0:
            print("✅ Collaborative Filtering working!")
        else:
            print("❌ Collaborative Filtering score is ZERO!")
            
        print("-" * 20)
        # print(json.dumps(data[0], indent=2))
    else:
        print("No recommendations returned")
except Exception as e:
    print(f"Error: {e}")
