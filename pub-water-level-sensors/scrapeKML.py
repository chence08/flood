from pykml import parser
import re

with open("pub-waterlevelsensors-20211015.kml", "r") as myfile:
    doc = parser.parse(myfile)

folder = doc.getroot().Document.Folder

sensors = {}

for i in folder.Placemark:
    desc = i.description.text
    station_name = re.search('<td>(.*)</td>', desc).group(1)
    coords = i.Point.coordinates.text.split(',')[:2]
    coords = list(map(float, coords))
    coords.reverse() # KML shows longitude before latitude, correct this inconvenience
    sensors[station_name.lower()] = coords

import json
with open('sensors.json', 'w') as g:
    json.dump(sensors, g, indent = 4)