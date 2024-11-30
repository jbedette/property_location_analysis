from dotenv import load_dotenv
import os

# my files
# import get_nearby
# import keywords
import tools
# import prox_campsite_cleanup
# import process_data
import data_compile
import map_build
import basic_map


# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variable
API_KEY = os.getenv('GOOGLE_GEOCACHING_API_KEY')
MY_ADDR = os.getenv('MY_ADDR')

print("start")
# if __name__ == "main":
radius_meters = 1000
num_results = 5

origin_coord = tools.get_coordinates(MY_ADDR,API_KEY)
pois, campsites = data_compile.get_data(origin_coord,API_KEY)

# for section in pois:
#     if(section['keyword'] == 'restaurant'):
#         print('\n')
#         print(section)
# #         for item in section:
#             # print('\n')
#             # print(item['close'])
# map_build.process_location(API_KEY)
basic_map.generate_map(origin_coord,pois,map_name="my_addr.html")



