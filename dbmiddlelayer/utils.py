import requests
import json

url = "http://your-api-url/api/daywise-prediction/"

data = {
    "station": 24,
    "date": "2024-07-04 00:00:00",  
    "day1": 5.2,
    "day2": 3.8,
    "day3": 4.1
}

data_json = json.dumps(data)

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=data_json, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())