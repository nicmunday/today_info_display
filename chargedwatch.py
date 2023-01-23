#!/usr/bin/env python3
import datetime
import json

with open("imports/json/today_settings.json") as reader:
    data = json.load(reader)
    file_loc = data["Watch File Location"]

today = datetime.date.today()

with open(file_loc, "w") as writer:
    writer.write(str(today))
print(today)
