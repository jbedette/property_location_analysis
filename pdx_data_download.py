import requests
import schedule
import time
from datetime import datetime

def download_data():
    url = "https://opendata.arcgis.com/datasets/b7965b3e95db40c0bcb92e36ab7d3357_0.geojson"  # Link to GeoJSON file
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        filename = f"./data/pdx_data_{datetime.now().strftime('%Y-%m-%d')}.geojson"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Data downloaded and saved as {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")

# Schedule the download to happen every Monday at 10 AM
schedule.every().tuesday.at("11:41").do(download_data)

print("Scheduler started. Data will download weekly.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
