import folium

def generate_map(center_point, points, map_name="generated_map.html"):
    # Create a map centered at the specified origin point
    mymap = folium.Map(location=center_point, zoom_start=15)

    folium.Marker(
            location=center_point,
            popup="Center Point",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mymap)

    # Add each point to the map
    for point in points:
        lat = point["lat"]
        lng = point["lng"]
        info = point.get("name", ""),  # Default to an empty string if no 'info' is provided
        folium.Marker(location=[lat, lng], popup=info,icon=folium.Icon(color='green',icon="info-sign")).add_to(mymap)

    # Save the map as an HTML file
    mymap.save(map_name)
    print(f"Map saved as '{map_name}'")

