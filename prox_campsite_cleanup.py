# import data from pdx arcgis public stuff
# take address, find all locations within data that are within a certain radius of addr


import json
import tools

#debug
import inspect
#debug

debug_true = False


# simple
with open("./data/IRP_Campsite_Reports.geojson") as f:
    campsite_reports = json.load(f)

with open("./data/IRP_Clean_Sites.geojson") as g:
    cleanup_reports = json.load(g)

def addr_proximity_to_locations(origin_coord,rad_dist):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    campsites = []
    cleanups = []

    # print(campsite_reports.keys())
    c_feat = campsite_reports['features']
    print(c_feat[0]['properties'])


    for site in campsite_reports['features']:
        campsites.append(site)

    for camp in campsites:
        print(camp)
        

    # for camp in campsite_reports:
    #     print(f"\norigin_coord_type: {type(origin_coord)}, camp_coord_type: {type(camp['coordinates'])}\n")
    #     dist = tools.calculate_distance(origin_coord,camp['coordinates'])
    #     if(dist <= rad_dist):
    #         campsites.append({'point': camp,'dist_km': dist})
    # campsites = sorted(campsites,key=lambda x: x['dist_km'])

    # for c_site in cleanup_reports:
    #     dist = tools.calculate_distance(origin_coord,c_site['coordinates'])
    #     if(dist <= rad_dist):
    #         cleanups.append({'point': c_site,'dist_km': dist})
    # cleanups = sorted(cleanups,key=lambda x: x['dist_km'])

    return campsites, cleanups

# end simple

files = [
    "./data/IRP_Campsite_Reports.geojson",
    "./data/IRP_Clean_Sites.geojson"
]

def data_coord_fix(coord):
    return (coord[1],coord[0])

def load_parse_data(file):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    sites = []

    with open(file) as g:
        data = json.load(g)

    for site in data['features']:
        sites.append(site)
    
    return sites

def prox_to_data (origin_coord, rad_dist, data):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    sites = []
    for site in data:

    # # debug
    #     print(f"============\n{site['geometry']['coordinates']}")
    #     print(f"\n{origin_coord}\n")
    # return sites
    # # debug

        dist = tools.calculate_distance(origin_coord,data_coord_fix(site['geometry']['coordinates']))
        if(dist <= rad_dist):
            sites.append({'point': site,'dist_km': dist})
    return sorted(sites,key=lambda x: x['dist_km'])

def addr_prox_to_locations(origin_coord,rad_dist):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    
    campsite_data = load_parse_data(files[0])
    # cleanup_data = load_parse_data(files[1])

    campsites = prox_to_data(origin_coord, rad_dist, campsite_data)
    # cleanups = prox_to_data(origin_coord, rad_dist, cleanup_data)

    cleanups = []

    return campsites, cleanups