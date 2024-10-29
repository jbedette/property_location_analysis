# import data from pdx arcgis public stuff
# take address, find all locations within data that are within a certain radius of addr


import json
import tools

with open("./data/IRP_Campsite_Reports.geojson") as f:
    campsite_reports = json.load(f)

with open("./data/IRP_Campsite_Reports.geojson") as g:
    cleanup_reports = json.load(g)

def addr_proximity_to_locations(origin_coord,rad_dist):
    campsites = []
    cleanups = []
    for camp in campsite_reports:
        dist = tools.calculate_distance(origin_coord,camp['coordinates'])
        if(dist <= rad_dist):
            campsites.append({'point': camp,'dist_km': dist})
    campsites = sorted(campsites,key=lambda x: x['dist_km'])

    for c_site in cleanup_reports:
        dist = tools.calculate_distance(origin_coord,c_site['coordinates'])
        if(dist <= rad_dist):
            cleanups.append({'point': c_site,'dist_km': dist})
    cleanups = sorted(cleanups,key=lambda x: x['dist_km'])
    return campsites, cleanups


