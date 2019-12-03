import json 
with open("custom.geo.json") as json_file:
    json_data = json.load(json_file) # or geojson.load(json_file)
	
	
print(json_data.keys())
print(json_data["features"])