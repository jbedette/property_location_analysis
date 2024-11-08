from dotenv import load_dotenv
import os

# my files
# import get_nearby
# import keywords
import tools
# import prox_campsite_cleanup
# import process_data
import data_compile


# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variable
API_KEY = os.getenv('GOOGLE_GEOCACHING_API_KEY')
MY_ADDR = os.getenv('MY_ADDR')

# if __name__ == "main":
radius_meters = 1000
num_results = 5
origin_coord = tools.get_coordinates(MY_ADDR,API_KEY)

data_compile.get_data(origin_coord,API_KEY)

