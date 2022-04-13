import json

'''
In order to minimize asymmetry in data we constrict our data to complete years only.
Our first tweet: "2012-01-12T04:56:22+00:00"
Our last tweet: "2021-12-31T03:08:20+00:00"

2012 to 2021 is 9 full years of data.

cleantweets.json contain all tweets with hashtag "sgflood",
deemed relevant to floods.

Targeted tweet formats:
These are our target concept.

1. (tweets after "2016-07-08T02:42:05+00:00")
"Commonwealth Lane / Commonwealth Dr:Water level falls below 90%. High Flood Risk..11:08:19 #SGFlood"
<Location>:Water level <rises/falls> <above/below> <percentage>%. <Moderate/High> Flood Risk..<HH:MM:SS>

2. (tweets before "2016-07-08T02:42:05+00:00")
"Tanjong Penjuru / Penjuru Rd:Water level falls below 90%. High Flood Risk.18:03:00 #SgFlood"

difference: one full stop only after "Flood Risk"
'''

# with open('cleantweets.json', 'r') as f1:
#     data = json.load(f1)

# restrictByYear = {}
# for tag, tweet in data.items():
#     year = int(tag[:4])
#     if 2012 <= year <= 2021:
#         restrictByYear[tag] = tweet.lower()

# with open('restrictByYear.json', 'w') as g1:
#     json.dump(restrictByYear, g1, indent = 4)

########################################################

# with open('restrictByYear.json', 'r') as f2:
#     data = json.load(f2)

# restrictByYear_LEFTOVERS = {}
# floodRisks = {}
# for tag, tweet in data.items():
#     if "flood risk" in tweet:
#         floodRisks[tag] = tweet
#     else:
#         restrictByYear_LEFTOVERS[tag] = tweet

# with open('floodRisks.json', 'w') as g2:
#     json.dump(floodRisks, g2, indent = 4)

# with open('restrictByYear_LEFTOVERS.json', 'w') as g3:
#     json.dump(restrictByYear_LEFTOVERS, g3, indent = 4)

########################################################

'''
Now we generate some dashboard of
1. all possible locations, merge same locations with spelling differences
2. count yearly trends
3. KEY OBSERVATION: 
...
'''

with open('floodRisks.json', 'r') as f3:
    data = json.load(f3)

with open('pub-water-level-sensors/sensors.json', 'r') as sss:
    sensors = json.load(sss)

sensorLocations = sensors.keys()

from collections import defaultdict as ddict
from difflib import get_close_matches

dashboard = {
    "locations": ddict(int),
    "tweetsPerYear": ddict(int),
    "coords": {}
}

errorCount = 0

for tag, tweet in data.items():
    location = tweet.partition(":")[0].strip()
    year = tag[:4]
    dashboard["locations"][location] += 1
    dashboard["tweetsPerYear"][year] += 1
    try:
        if location not in dashboard["coords"]:
            dashboard["coords"][location] = sensors[location]
    except KeyError:
        if location not in dashboard["coords"]:
            errorCount += 1
            dashboard["coords"][location] = get_close_matches(location, sensorLocations)

# # create list of locations that appeared at least 10 times, since low chance
# # of identical spelling mistakes.

# freqLocations = [location for location, frequency
#                     in dashboard["locations"].items() if frequency >= 10]

# finalLocations = []

# for location, frequency in dashboard["locations"].items():
#     if frequency < 10:
#         dashboard["locations"][location] = get_close_matches(location, freqLocations)

sortedLocations = {k: v for k, v in 
                    sorted(dashboard["locations"].items(),
                    key=lambda item: item[1], reverse=True)}

dashboard["locations"] = sortedLocations

with open('dashboard.json', 'w') as g4:
    json.dump(dashboard, g4, indent = 4)

print("number of distinct locations: ", len(dashboard["locations"]))
print(errorCount)