import requests
import logging

def fetch_aws_data(station_id):
    url = "https://dmwebtwo.mcgm.gov.in/api/tabWeatherForecastData/loadById"
    headers = {
        "Authorization": "Basic RE1BUElVU0VSOkRNYXBpdXNlclBhJCR3b3JkQDEyMzQ="
    }
    payload = {"id": station_id}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return parse_data(data)
    except requests.exceptions.RequestException as e:
        # Log error
        logging.error(f"Failed to fetch data for station {station_id}: {e}")
        return None

def parse_data(data):
    location_data = data.get('locationList', {})
    dummy_data = data.get('dummyTestRaingaugeDataDetails', {})
    
    result = {
        'temp_out': parse_value(dummy_data.get('tempOut')),
        'out_humidity': parse_value(dummy_data.get('outHumidity')),
        'wind_speed': parse_value(dummy_data.get('windSpeed')),
        'rain': parse_value(dummy_data.get('rain')),
    }
    return result

def parse_value(value):
    if value is None or value == '---':
        return None
    try:
        return float(value)
    except ValueError:
        # Handle cases where value cannot be converted to float
        logging.error(f"Failed to parse value '{value}' as float.")
        return None
    
    
