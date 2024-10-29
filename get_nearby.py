import requests
from geopy.distance import geodesic
from dotenv import load_dotenv
import os

#debug
import inspect
import tools
debug_true = False
#debug

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variable
API_KEY = os.getenv('GOOGLE_GEOCACHING_API_KEY')
MY_ADDR = os.getenv('MY_ADDR')

# Function to get latitude and longitude of a given address
def get_coordinates(address):
    # debug
    # print(f"{inspect.currentframe().f_code.co_name}")
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug
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
    # debug
    # print(f"{inspect.currentframe().f_code.co_name}")
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug
    try:
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={keyword}&key={API_KEY}"
        response = requests.get(places_url)
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        if result['status'] == 'OK' and result['results']:
            return result['results']
        else:
            # print(f"Places API error: {result['status']}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nearby {keyword}: {e}")
        return []

# Function to calculate the distance between two points
def calculate_distance(loc1, loc2):
    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug
    return geodesic(loc1, loc2).kilometers

def get_closest(origin_coord, keyword, places, num_results):
    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    # Store the poi and distance
    lat, lng = origin_coord
    distances = []
    for place in places:
        # print('\n',place) # testing, see all nearby data
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
    closest = sorted(distances, key=lambda x: x['distance_km'])[:num_results]
    
    return closest

# Main function to get closest restaurants
def get_nearby_poi(address, keyword, radius_meters, num_results):
    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug
    coordinates = get_coordinates(address)
    if not coordinates:
        print("Address not found.")
        return
    
    lat, lng = coordinates
    places = get_nearby(lat, lng, radius_meters, keyword )

    if not places:
        # print(f"No {keyword} found nearby.")
        return [],[]

    closest = get_closest(coordinates, keyword, places, num_results )

    return places, closest

def print_items(items):
    for item in items:
        print('\n',item)
        for i, c in enumerate(items, 1):
            print(f"{i}. {c['name']}")
            print(f"   address: {c['address']}")
            print(f"   distance: {c['distance_km']:.2f} km\n")

def get_keyword_places(keywords, radius_meters, num_results):
    results = []
    # keyword = "restaurant"
    for keyword in keywords:
        places, closest = get_nearby_poi(MY_ADDR, keyword, radius_meters, num_results)
        # print(closest)
        results.append({
            'keyword': keyword,
            'places': places,
            'close': closest
        })
    for result in results:
        print("\n=========\n", keyword, '\n')
        for i, addr in enumerate(result['close'],1):
            print(f"{i}. {addr['name']}")
            print(f"    addr: {addr['address']}")
            print(f"    dist: {addr['distance_km']:.2f} km\n")
    return results
    
    


if __name__ == "__main__":
    # user_address = input("Enter your address: ")
    # keyword = input("Enter the type of landmark you are looking for: ")

    # keywords = [
    #             "bowling_alley",
    #             "restaurant",
    #             "park"
    #             ]
                
    keywords = [
        "art_gallery",
        "atm",
        "bakery",
        "bank",
        "bar",
        "book_store",
        "bowling_alley",
        "bus_station",
        "cafe",
        "clothing_store",
        "convenience_store",
        "department_store",
        "drugstore",
        "florist",
        "funeral_home",
        "furniture_store",
        "gym",
        "hardware_store",
        "home_goods_store",
        "jewelry_store",
        "library",
        "light_rail_station",
        "liquor_store",
        "movie_theater",
        "museum",
        "night_club",
        "park",
        "pet_store",
        "pharmacy",
        "primary_school",
        "restaurant",
        "school",
        "spa",
        "supermarket",
        "train_station",
        "transit_station",
        "university"
    ]

    radius_meters = 1000
    num_results = 5
    # get_keyword_places(good_keywords,radius_meters,num_results)
    results = []
    not_found = []
    found_score = 0
    # keyword = "restaurant"
    for keyword in keywords:
        #debug
        tools.print_debug("=====>" + str(keyword),debug_true)
        #debug

        places, closest = get_nearby_poi(MY_ADDR, keyword, radius_meters, num_results)

        if not places:
            # results.append({
            #     'keyword': keyword,
            #     'close': [],
            #     'found': False
            # })
            not_found.append(keyword)
        else:
            results.append({
                'keyword': keyword,
                'places': places,
                'close': closest,
                'found': True
            })
            found_score += 1
    
    
        # printing data captured from api
        # 
    #     print('\n',keyword)
    #     # print(closest)
    #     for i, c in enumerate(closest, 1):
    #         print(f"{i}. {c['name']}")
    #         print(f"   address: {c['address']}")
    #         print(f"   distance: {c['distance_km']:.2f} km\n")

    # printing stored found results
    for result in results:
        print("\n=========\n", result['keyword'], '\n')
        for i, addr in enumerate(result['close'],1):
                print(f"{i}. {addr['name']}")
                print(f"    addr: {addr['address']}")
                print(f"    dist: {addr['distance_km']:.2f} km\n")

    print(f"==========\nfound:")
    for i,r in enumerate(results,start=1):
        print(f"{i}. {r['keyword']}")
    print(f"==========\nFound Score: {found_score}\n")


    print(f"============\nnot found:")
    for i,result in enumerate(not_found,start=1):
        print(f"{i}. {result}")
    print(f"")


            