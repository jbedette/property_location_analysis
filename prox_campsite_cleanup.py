# import data from pdx arcgis public stuff
# take address, find all locations within data that are within a certain radius of addr


import json
import tools

#debug
import inspect
debug_true = False
#debug


def prox_to_data (origin_coord, rad_dist, data):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    sites = []
    for site in data:
        # dist = tools.calculate_distance(origin_coord,data_coord_fix(site['geometry']['coordinates']))
        dist = tools.calculate_distance(origin_coord,site['coordinates'])
        if(dist <= rad_dist):
            sites.append({'point': site,'dist_km': dist})
    return sorted(sites,key=lambda x: x['dist_km'])

def origin_prox_to_data(origin_coord,rad_dist):

    # debug
    tools.print_debug(inspect.currentframe().f_code.co_name,debug_true)
    # debug

    nearby_camp_hotspots = []
    with open("./processed_data/campsites_aggreg.json") as f:
        campsites = json.load(f)
    nearby_camp_hotspots = prox_to_data(origin_coord,rad_dist,campsites)
    print_sites(nearby_camp_hotspots,False)
    return nearby_camp_hotspots

def print_sites(sites,flag):
    if(flag):
        for i, site in enumerate(sites):
            print(f"{i}:{site}")
    
    
