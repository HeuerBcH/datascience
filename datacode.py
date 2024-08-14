import sys
import docplex.mp
import os
import subprocess
os.system("cls")

class XPoint (object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "P(%g_%g)" % (self.x, self.y)
    
class NamedPoint(XPoint):
    def __init__(self, name, x, y):
        XPoint.__init__(self, x, y)
        self.name = name

    def __str__(self):
        return self.name
    
try:
    import geopy.distance
except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])  
        import geopy.distance

from geopy.distance import great_circle

def get_distance(p1, p2):
     return great_circle((p1.y, p1.x), (p2.y, p2.x)).miles

def build_libraries_from_url(url, name_pos, lat_long_pos):
    import requests
    import json

    r = requests.get(url)
    myjson = json.loads(r.text, parse_constant='utf-8')
    myjson = myjson['data']

    libraries = []
    k = 1
    for location in myjson:
        uname = location[name_pos]
        try:
            latitude = float(location[lat_long_pos][1])
            longitude = float(location[lat_long_pos][2])
        except TypeError:
            latitude = longitude = None
        try:
            name = str(uname)
        except:
            name = "???"
        name = "P_%s_%d" % (name, k)
        if latitude and longitude:
            cp = NamedPoint(name, longitude, latitude)
            libraries.append(cp)
            k+=1
    return libraries

libraries = build_libraries_from_url('https://data.cityofchicago.org/api/views/x8fc-8rcq/rows.json?accessType=DOWNLOAD',
                                   name_pos=10,
                                   lat_long_pos=16)

print("There are %d public libraries in Chicago" % (len(libraries)))

nb_shops = 5
print("We would like to open %d coffee shops" % nb_shops)

try:
    import folium
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "folium"]) 
    import folium

map_osm = folium.Map(location=[41.878, -87.629], zoom_start=11)
for library in libraries:
    lt = library.y
    lg = library.x
    folium.Marker([lt, lg]).add_to(map_osm)
map_osm

map_osm.save('chicago_libraries_map.html')


