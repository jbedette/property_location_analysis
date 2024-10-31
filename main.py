from dotenv import load_dotenv
import os

# my files
import get_nearby
import keywords
import tools
import prox_campsite_cleanup

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variable
API_KEY = os.getenv('GOOGLE_GEOCACHING_API_KEY')
MY_ADDR = os.getenv('MY_ADDR')

# if __name__ == "main":
# print("yo")
radius_meters = 1000
num_results = 5
origin_coord = tools.get_coordinates(MY_ADDR,API_KEY)
# print(origin_coord)
# get_nearby.process_poi(keywords.keywords, radius_meters, num_results, origin_coord, API_KEY)
# campsites, cleanups = prox_campsite_cleanup.addr_proximity_to_locations(origin_coord,radius_meters) 

# radius_meters/1000 because func works in km
campsites, cleanups = prox_campsite_cleanup.addr_prox_to_locations(origin_coord,radius_meters/1000) 

if not campsites:
    print(f"no campsites found nearby")
else:
    print(f"=========\nCampsites\n")
    for i,camp in enumerate(campsites,start=1):

        print(f"{i}: {camp['dist_km']}")
    print(f"\n=========")


    