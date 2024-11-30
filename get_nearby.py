import requests

#debug
import inspect
import tools
debug_true = False
#debug



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
            distance = tools.calculate_distance((lat, lng), (p_lat, p_lng))
            distances.append({
                'name': place['name'],
                'address': place['vicinity'],
                'distance_km': distance,
                'lat': place['geometry']['location']['lat'],
                'lng': place['geometry']['location']['lng']
            })
        except KeyError:
            print(f"Error retrieving data for a {keyword}: {place}")
            continue

    # Sort restaurants by distance and return the closest ones
    closest = sorted(distances, key=lambda x: x['distance_km'])[:num_results]
    
    return closest


def get_keyword_places(origin_coord, keywords, radius_meters, num_results):
    results = []
    # keyword = "restaurant"
    for keyword in keywords:
        places, closest = get_nearby_poi(origin_coord, keyword, radius_meters, num_results)
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
    
# Function to get nearby restaurants
def get_nearby(KEY, lat, lng, radius, keyword):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    try:
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={keyword}&key={KEY}"
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

# Main function to get closest restaurants
def get_nearby_poi(origin_coord, KEY, keyword, radius_meters, num_results):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    if not origin_coord:
        print("Address not found.")
        return
    
    lat, lng = origin_coord
    places = get_nearby(KEY, lat, lng, radius_meters, keyword )

    if not places:
        # print(f"No {keyword} found nearby.")
        return [],[]

    closest = get_closest(origin_coord, keyword, places, num_results )

    return places, closest
    
def process_poi(keywords,radius_meters,num_results,origin_coord, KEY):
                
    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    results = []
    not_found = []
    found_score = 0
    for keyword in keywords:
        #debug
        tools.print_debug("=====>" + str(keyword),debug_true)
        #debug

        # # loading bar
        # tools.loading_bar()

        places, closest = get_nearby_poi(origin_coord, KEY, keyword, radius_meters, num_results)

        if not places:
            not_found.append(keyword)
        else:
            results.append({
                'keyword': keyword,
                'places': places,
                'close': closest,
                'found': True
            })
            found_score += 1

    #debug
    print_poi_data(results,not_found,False) 
    #debug


    return results

def print_poi_data(results,not_found,flag):
    if(flag == True):
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
        # print(f"==========\nFound Score: {found_score}\n")


        print(f"============\nnot found:")
        for i,result in enumerate(not_found,start=1):
            print(f"{i}. {result}")
        print(f"")

def get_poi_info(results):
    out = [] 
    for result in results:
        # print("\n=========\n", result['keyword'], '\n')
        for i, addr in enumerate(result['close'],1):
                out.append({
                    'num':i,
                    'category':"good",
                    'keyword':result['keyword'],
                    'name':addr['name'],
                    'addr':addr['address'],
                    'dist':addr['distance_km'],
                    'lat':addr['lat'],
                    'lng':addr['lng']
                    })
    return out
            

