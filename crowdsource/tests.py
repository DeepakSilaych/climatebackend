from geopy.geocoders import Nominatim

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
        return 'Location not found'

print(cord_to_text(19.0760, 72.8777))  # Output: 'Mumbai Pune Expressway, Pimpri-Chinchwad'
