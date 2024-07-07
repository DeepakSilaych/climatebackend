import re
from geopy.geocoders import Nominatim
import requests
from datetime import datetime, timedelta

def geolocate_text(location_text):
    print(location_text)
    geolocator = Nominatim(user_agent="text_geolocator")
    processed_text = process_text(f"Mumbai, {location_text}")
    location = geolocator.geocode(processed_text)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def process_text(location_text):
    processed_text = location_text.lower()
    processed_text = re.sub(r'[^\w\s]', '', processed_text)
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    return processed_text

def cord_to_text(lat, long):
    geolocator = Nominatim(user_agent="cord_to_text")
    location = geolocator.reverse(f"{lat}, {long}")
    if location:
        address = location.raw.get('address', {})
        name = address.get('road', '')
        neighbourhood = address.get('neighbourhood', '')

        if not neighbourhood:
            neighbourhood = address.get('suburb', '')
        
        if not name:
            name = location.raw.get('name', '')

        return f'{name}, {neighbourhood}'
    else:
        return None
    


# API endpoint URLs
things_list_url = "https://app.aurassure.com/-/api/iot-platform/v1.1.0/clients/10684/applications/16/things/list"
things_data_url = "https://app.aurassure.com/-/api/iot-platform/v1.1.0/clients/10082/applications/16/things/data"

# Headers for authentication
headers = {
    "Access-Id": "lX1d9akADFVLiYhB",
    "Access-Key": "NsKeyQDu9zgbED9KINEeYhIvRzbcSr1VKtDhbTMaUQMlAtPA8sOyjDm8Q85CBH9d",
    "Content-Type": "application/json"
}

def get_sensors_list():
    try:
        response = requests.get(things_list_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sensors list: {e}")
        return None

def get_water_level_data(thing_id, from_time, upto_time):
    try:
        # Prepare request body
        payload = {
            "data_type": "raw",
            "aggregation_period": 0,
            "parameters": ["us_mb"],
            "parameter_attributes": [],
            "things": [thing_id],
            "from_time": from_time,
            "upto_time": upto_time
        }
        
        response = requests.post(things_data_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad response status
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching water level data for thing_id {thing_id}: {e}")
        return None

def main():
    # Fetch list of sensors
    sensors_list = get_sensors_list()
    
    if sensors_list and "things" in sensors_list:
        # Iterate over each sensor
        for sensor in sensors_list['things']:
            thing_id = sensor['id']
            
            # Fetch data for the last hour (adjust time range as per your requirement)
            now = datetime.utcnow()
            from_time = int((now - timedelta(hours=1)).timestamp())
            upto_time = int(now.timestamp())
            
            # Fetch water level data
            water_level_data = get_water_level_data(thing_id, from_time, upto_time)
            
            if water_level_data and "data" in water_level_data:
                # Example: Print first few entries of water level data
                print(f"Water level data for sensor {thing_id} ({sensor['name']}):")
                for entry in water_level_data["data"]:
                    time = datetime.utcfromtimestamp(entry["time"]).strftime('%Y-%m-%d %H:%M:%S')
                    water_level = entry["parameter_values"]["us_mb"]
                    print(f"  Time: {time}, Water Level: {water_level} {sensor['parameters'][0]['unit']}")
            else:
                print(f"No water level data found for sensor {thing_id}")

if __name__ == "__main__":
    main()