from flask import Flask, request, jsonify
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)

# Helper function to generate nearby points
def generate_nearby_points(location_coords, num_points=5, distance_km=1):
    points = []
    for i in range(num_points):
        points.append((
            location_coords[0] + (i * 0.001),  # Slight variation
            location_coords[1] + (i * 0.001)
        ))
    return points

@app.route('/process', methods=['POST'])
def process_location():
    data = request.json
    state = data['state']
    city = data['city']
    address = data['address']

    full_address = f"{address}, {city}, {state}"
    geolocator = Nominatim(user_agent="redfin_locator")
    location = geolocator.geocode(full_address)

    if location:
        # Generate map
        map_center = (location.latitude, location.longitude)
        map_obj = folium.Map(location=map_center, zoom_start=15)

        # Add original location marker
        folium.Marker(map_center, popup="Original Address", icon=folium.Icon(color="blue")).add_to(map_obj)

        # Generate and add nearby points
        nearby_points = generate_nearby_points(map_center)
        for idx, point in enumerate(nearby_points):
            folium.Marker(point, popup=f"Point {idx+1}", icon=folium.Icon(color="green")).add_to(map_obj)

        # Save map as an HTML file
        map_file = "map.html"
        map_obj.save(map_file)

        return jsonify({"mapUrl": f"http://localhost:5000/{map_file}"})
    else:
        return jsonify({"error": "Could not geocode the address."}), 400

@app.route('/map.html', methods=['GET'])
def serve_map():
    return app.send_static_file('map.html')

if __name__ == "__main__":
    app.run(debug=True)
