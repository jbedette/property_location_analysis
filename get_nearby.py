import requests
from geopy.distance import geodesic
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variable
API_KEY = os.getenv('GOOGLE_GEOCACHING_API_KEY')
MY_ADDR = os.getenv('MY_ADDR')

# Function to get latitude and longitude of a given address
def get_coordinates(address):
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
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

# Function to get nearby restaurants
def get_nearby(lat, lng, radius, keyword):
    try:
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={keyword}&key={API_KEY}"
        response = requests.get(places_url)
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        if result['status'] == 'OK' and result['results']:
            return result['results']
        else:
            print(f"Places API error: {result['status']}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nearby {keyword}: {e}")
        return []

# Function to calculate the distance between two points
def calculate_distance(loc1, loc2):
    return geodesic(loc1, loc2).kilometers

# Main function to get closest restaurants
def get_closest(address, n, keyword):
    coordinates = get_coordinates(address)
    if not coordinates:
        print("Address not found.")
        return
    
    lat, lng = coordinates
    # 5000 is arb num for testing
    places = get_nearby(lat, lng, 5000, keyword )

    if not places:
        print("No {keyword} found nearby.")
        return

    # Store the restaurant and distance
    distances = []
    for place in places:
        try:
            p_lat = place['geometry']['location']['lat']
            p_lng = place['geometry']['location']['lng']
            distance = calculate_distance((lat, lng), (p_lat, p_lng))
            distances.append({
                'name': place['name'],
                'address': place['vicinity'],
                'distance_km': distance
            })
        except KeyError:
            print(f"Error retrieving data for a {keyword}: {place}")
            continue

    # Sort restaurants by distance and return the closest ones
    closest = sorted(distances, key=lambda x: x['distance_km'])[:n]

    for i, place in enumerate(closest, 1):
        print(f"{i}. {place['name']}")
        print(f"   Address: {place['address']}")
        print(f"   Distance: {place['distance_km']:.2f} km\n")

if __name__ == "__main__":
    # user_address = input("Enter your address: ")
    # keyword = input("Enter the type of landmark you are looking for: ")
    # get_closest(user_address, 5, keyword )
    get_closest(MY_ADDR, 5, "restaurant")
    get_closest(MY_ADDR, 5, "park")
