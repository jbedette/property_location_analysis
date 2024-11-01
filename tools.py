import requests
from geopy.distance import geodesic

def calculate_distance(loc1, loc2):
    return geodesic(loc1, loc2).kilometers

def print_debug(name, debug_true):
    if(debug_true):
        print(f"{name}")


# to be moved here, just placeholder for now
# Function to get latitude and longitude of a given address
def get_coordinates(address, KEY):
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={KEY}"
        response = requests.get(geocode_url)
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        if result['status'] == 'OK' and result['results']:
            location = result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Geocoding error: {result['status']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geocoding data: {e}")
        return None
