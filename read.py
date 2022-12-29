import json
import datetime

openFile = open("dist/ALCX/2022-Dec.json")

jsonData = json.load(openFile)

for data in jsonData:
	# print(data['timestamp'])
	print(datetime.datetime.fromtimestamp(int(data['timestamp']) / 1000))