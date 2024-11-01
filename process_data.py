import json
import tools

#debug
import inspect
debug_true = False
#debug

# idea:
# 1. load data
# 2. for each point, 
#     - collapse all points within a certain km range into a single point that:
#         1. has a count of reports 
#         2. has a list of dates reported
#         3. makes note of first report and last report
#         4. keeps vehicle bool
#         5. records the general coordinate
#         6. fixes coordinate
# 3. as we process, remove items from the list to reduce process time 
# 4. creates or replaces a created list

# anatomy of current:
# load data
#     split into reports
#     sort reports by coord 0
#     sort reports by coord 1
#     pop off front,
#         iterate through finding coords within 100 meters
#         break when hitting something too far
#         save data points
# write to processed data file

def data_coord_fix(coord):
    return (coord[1],coord[0])

def load_parse_data(file):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    sites = []
    processed_data = []

    with open(file) as g:
        data = json.load(g)

    for site in data['features']:
        sites.append(site)
        
    sites = sorted(sites,key=lambda x: x['geometry']['coordinates'][0])
    sites = sorted(sites,key=lambda x: x['geometry']['coordinates'][1])
    i = 0
    length = len(sites)
    while sites:
        base_site = sites.pop(0)
        base_coords = data_coord_fix(base_site['geometry']['coordinates'])
        base_count = 1
        dates = [base_site['properties']['inc_date_create']]
        i += 1
        print(f"processing #: {i}, siteslen: {len(sites)}, removed: {length - len(sites)}")
        length = len(sites)
        for site in sites:
            # 0.1 is 100 meters
            if (tools.calculate_distance(base_coords,data_coord_fix(site['geometry']['coordinates'])) < 0.1):
                base_count += 1
                dates.append(site['properties']['inc_date_create'])
                sites.pop(0)
            else:
                break
        report = {
            'count': base_count,
            'dates': dates,
            'coordinates': base_coords
        }
        processed_data.append(report)
    
    return processed_data

# load file, 
def process():

    # files = [
    #     "./data/IRP_Campsite_Reports.geojson",
    #     "./data/IRP_Clean_Sites.geojson"
    # ]

    data = load_parse_data("./data/IRP_Campsite_Reports.geojson")
    # for d in data:
    #     print(f"{d}")

    with open('./processed_data/campsites_aggreg.json','w') as outfile:
        json.dump(data,outfile,indent=4)
