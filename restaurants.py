import requests
from geopy.distance import geodesic
from dotenv import load_dotenv
import os

load_dotenv()

# Constants
API_KEY = os.getenv('GOOGLE_GEOCACHING_API_KEY')
# Function to get latitude and longitude of a given address
def get_coordinates(address):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        result = response.json()
        if result['results']:
            location = result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None

# Function to get nearby restaurants
def get_nearby_restaurants(lat, lng, radius=5000, keyword="restaurant"):
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=restaurant&key={API_KEY}"
    response = requests.get(places_url)
    if response.status_code == 200:
        result = response.json()
        if result['results']:
            return result['results']
    return []

# Function to calculate the distance between two points
def calculate_distance(loc1, loc2):
    return geodesic(loc1, loc2).kilometers

# Main function to get closest restaurants
def get_closest_restaurants(address, n=5):
    coordinates = get_coordinates(address)
    if not coordinates:
        print("Address not found.")
        return
    
    lat, lng = coordinates
    restaurants = get_nearby_restaurants(lat, lng)

    # Store the restaurant and distance
    restaurant_distances = []
    for restaurant in restaurants:
        rest_lat = restaurant['geometry']['location']['lat']
        rest_lng = restaurant['geometry']['location']['lng']
        distance = calculate_distance((lat, lng), (rest_lat, rest_lng))
        restaurant_distances.append({
            'name': restaurant['name'],
            'address': restaurant['vicinity'],
            'distance_km': distance
        })

    # Sort restaurants by distance and return the closest ones
    closest_restaurants = sorted(restaurant_distances, key=lambda x: x['distance_km'])[:n]

    for i, rest in enumerate(closest_restaurants, 1):
        print(f"{i}. {rest['name']}")
        print(f"   Address: {rest['address']}")
        print(f"   Distance: {rest['distance_km']:.2f} km\n")

if __name__ == "__main__":
    user_address = input("Enter your address: ")
    get_closest_restaurants(user_address)
