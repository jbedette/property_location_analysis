import json
import tools
import inspect
import concurrent.futures
from itertools import compress

# Debugging flag
debug_true = False

def data_coord_fix(coord):
    return (coord[1], coord[0])

def load_parse_data(file):
    """Load data and prepare for processing."""
    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name, debug_true)
    # debug

    sites = []
    with open(file) as g:
        data = json.load(g)
    for site in data['features']:
        sites.append(site)
        
    # Sorting by coordinates for potential efficiency
    sites = sorted(sites, key=lambda x: (x['geometry']['coordinates'][1], x['geometry']['coordinates'][0]))
    return sites

def check_distance(base_coords, sites, max_distance=0.1):
    """Check distances for each site relative to base_coords."""
    return [tools.calculate_distance(base_coords, data_coord_fix(site['geometry']['coordinates'])) < max_distance for site in sites]

def process_site(base_site, sites):
    """Process a base site, aggregating points within the specified range."""
    base_coords = data_coord_fix(base_site['geometry']['coordinates'])
    dates = [base_site['properties']['inc_date_create']]
    count = 1

    # Filter sites within range using check_distance
    with concurrent.futures.ProcessPoolExecutor() as executor:
        in_range = executor.submit(check_distance, base_coords, sites).result()

    close_sites = list(compress(sites, in_range))

    for site in close_sites:
        count += 1
        dates.append(site['properties']['inc_date_create'])
    
    return {
        'count': count,
        'dates': dates,
        'coordinates': base_coords
    }, close_sites

def main(file_path, output_file='aggreg_campsites.json'):
    """Main function to load data, process sites, and save output."""
    sites = load_parse_data(file_path)
    processed_data = []
    i = 0

    while sites:
        base_site = sites.pop(0)
        i += 1
        print(len(sites))
        print(f"Processing site #{i}")

        # Process each base site and aggregate close sites
        report, close_sites = process_site(base_site, sites)
        
        # Remove processed close sites from sites list
        for close_site in close_sites:
            sites.remove(close_site)

        processed_data.append(report)

    # Save the results to a JSON file
    with open(output_file, 'w') as outfile:
        json.dump(processed_data, outfile, indent=4)
    print(f"Aggregated data has been saved to '{output_file}'.")

# Example usage
# main('./data/IRP_Campsite_Reports.geojson')
