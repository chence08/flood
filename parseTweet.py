import json

with open('pubtweets.txt') as f:
    json_list = list(f)

clean = {}

for json_str in json_list:
    result = json.loads(json_str)
    # print(result['content'])
    # print(result['date'])
    # print(isinstance(str(result['hashtags'][0]), str))
    # break
    if result['hashtags']:
        if str(result['hashtags'][0]).lower() == "sgflood":
            clean[result['date']] = result['content']
    
with open('cleantweets.txt', 'w') as g:
    json.dump(clean, g, indent = 4, sort_keys=True)