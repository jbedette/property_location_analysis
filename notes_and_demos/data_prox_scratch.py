import json
import geojson
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def load_geojson_data(file_path):
    # Load GeoJSON data from file
    with open(file_path, "r") as f:
        data = geojson.load(f)
    return data

def geocode_address(address):
    geolocator = Nominatim(user_agent="geo_distance_app")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError("Address not found")

def find_nearby_locations(data, center_point, radius_km):
    nearby_locations = []
    for feature in data["features"]:
        if feature["geometry"]["type"] == "Point":
            # Extract point coordinates
            point_coords = tuple(feature["geometry"]["coordinates"][::-1])  # Reverse to (lat, lon)
            
            # Calculate distance to center point
            distance = geodesic(center_point, point_coords).kilometers
            
            # Check if within radius
            if distance <= radius_km:
                feature["properties"]["distance_km"] = distance  # Optionally add distance info
                nearby_locations.append(feature)
                
    return nearby_locations

# Load GeoJSON data
file_path = "path_to_your_file.geojson"
geojson_data = load_geojson_data(file_path)

# Geocode the given address
address = "Your address here"
try:
    center_point = geocode_address(address)
except ValueError as e:
    print(e)

# Define radius in kilometers
radius_km = 5.0  # e.g., 5 kilometers

# Find nearby locations
nearby_locations = find_nearby_locations(geojson_data, center_point, radius_km)

# Print or process results
for location in nearby_locations:
    print(f"Name: {location['properties'].get('name', 'N/A')}, Distance: {location['properties']['distance_km']:.2f} km")
