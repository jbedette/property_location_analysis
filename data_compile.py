import prox_campsite_cleanup
import get_nearby
import keywords

def get_data(origin_coord, API_KEY):
    radius_meters = 1000
    num_results = 5

    pois_data = get_nearby.process_poi(keywords.keywords, radius_meters, num_results, origin_coord, API_KEY)
    poi_count = len(pois_data)
    print(f"poi_count: {poi_count}")

    pois = get_nearby.get_poi_info(pois_data)

    # debug
    campsites = []
    # debug

    # campsites = prox_campsite_cleanup.origin_prox_to_data(origin_coord,.2)
    # camp_count = len(campsites)
    # print(f"camp_count: {camp_count}")
    return pois, campsites
