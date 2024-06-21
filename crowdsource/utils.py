import re
from geopy.geocoders import Nominatim

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
        street = address.get('road', '')
        neighbourhood = address.get('neighbourhood', '')

        if not neighbourhood:
            neighbourhood = address.get('suburb', '')

        return f'{street}, {neighbourhood}'
    else:
        return None