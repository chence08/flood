import json
import re

with open("data/cleantweets.json") as f:
	data = json.load(f)

tweetData = data

# print(json.dumps(data, indent = 2))

# "2011-06-11T05:50:52+00:00": "PUB officer reported no flash flood along Holland Rd (1236hrs) #sgflood",

# location, time, level, type, month, seasonal....

##IDEAL FORMAT
# "2011-11-01T07:42:11+00:00": {
#    "Location": "Grove Dr",
#    "Water Level Percentage": 75,
#    "Flood Risk": "Moderate",
#    "SGT": "15:41:46",
#    "Date": "2011-11-01",
#    "Type": "Water Level Update"
# }

##TWEET TYPES
# "2011-11-01T07:03:23+00:00": "Moderate to heavy rain at several areas. Issued 3.03pm. #sgflood", 
# "2011-11-01T07:31:13+00:00": "NEA: Moderate/heavy thundery showers at many areas.1350-1500Hrs. Issued 3.27pm. #sgflood.",
# "2011-11-01T07:42:11+00:00": "Grove Dr:Water level rise above 75%. Moderate Flood Risk.15:41:46 #SgFlood",


# go through all the rows in data
# add location key
# add percentage
# add flood risk
# add time
# add date
# add tweet type

# print(data["2011-06-11T05:50:52+00:00"])

# make each tweet a dictionary itself and create key "tweet"
for item in data:
	x = {"tweet": data[item],
		 "Water Level Percentage": None,
		 "Location": None,
		 "Flood Risk": None,
		 "Time": None,
		 "Date": None}
	tweetData[item] = x

#print(data)

# create water level key
#for tweet in data:
	# if "%" in tweet:
		#print(data[tweet])

# add water level value
for item in data:
	if "%" in data[item]["tweet"]:
		percentage = re.search(r"\d+%", data[item]["tweet"])
		data[item]["Water Level Percentage"] = percentage.group()

# add location value
# for item in data:
# 	if "%" in data[item]["tweet"]:
# 		if "(" in data[item]["tweet"]:
# 			address = re.search(r"[\w+|\s]+\([\w+|\s]+\)|[\w+|\s|\/]+", data[item]["tweet"])
# 			# print(address)
# 			# print(data[item]["tweet"])
# 			if address is not None:
# 				data[item]["Location"] = address.group()
# 		else:
# 			address = re.search(r"[\w+|\s|\/]+", data[item]["tweet"])
# 			# print(address)
# 			# print(data[item]["tweet"])
# 			if address is not None:
# 				data[item]["Location"] = address.group()

# 		if "at" in data[item]["tweet"]:
# 			address = re.search(r"(?<=(at ))[\w+|\s|\/]+", data[item]["tweet"])
# 			print(address)
# 			print(data[item]["tweet"])
# 			if address is not None:
# 				data[item]["Location"] = address.group()

for item in data:
	if "%" in data[item]["tweet"]:
		address = re.search(r"[\w+|\s]+\([\w+|\s]+\)|[\w+|\s|\/]+", data[item]["tweet"])
		if address is not None:
			data[item]["Location"] = address.group()

		if "at" in data[item]["tweet"]:
			address = re.search(r"(?<=(at ))[\w+|\s|\/]+", data[item]["tweet"])
			if address is not None:
				data[item]["Location"] = address.group()

# add flood risk value
for item in data:
	if "Flood Risk" in data[item]["tweet"]:
		risk = re.search(r"\w+(?=( Flood Risk))", data[item]["tweet"])
		data[item]["Flood Risk"] = risk.group()
	elif "flood risk" in data[item]["tweet"]:
		risk = re.search(r"\w+(?=( flood risk))", data[item]["tweet"])
		data[item]["Flood Risk"] = risk.group()

# add time value
for item in data:
	if "hrs" in data[item]["tweet"]:
		time = re.search(r"[0-9|\:]+(?=(hrs)|( hrs))", data[item]["tweet"])
		# print(time)
		# print(data[item]["tweet"])
	elif "hours" in data[item]["tweet"]:
		time = re.search(r"[0-9|\:]+(?=(hours)|( hours))", data[item]["tweet"])
		# print(time)
		# print(data[item]["tweet"])
	elif "Issued" in data[item]["tweet"]:
		time = re.search(r"(?<=(Issued ))[0-9|\.|\:|\w]+", data[item]["tweet"])
		# print(time)
		# print(data[item]["tweet"])

	if time is not None:
		data[item]["Time"] = time.group()

# add data value:
for item in data:
	index = list(data.keys()).index(item)
	k, v = list(data.items())[index]
	date = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", k)
	data[item]["Date"] = date.group()


#print(data["2011-11-01T07:03:23+00:00"]["Water Level Percentage"])
# print(json.dumps(data, indent = 2))

with open('tweetDict.json', 'w') as outfile:
    json.dump(data, outfile, indent = 2)
