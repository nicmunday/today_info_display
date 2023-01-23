#!/usr/bin/env python3
import feedparser
import json
class Tides:
    def __init__(self):

        with open("/home/nic/bin/imports/json/locations.json") as reader:
            loc_file = json.load(reader)

        location = loc_file["tide times"]["location"]

        tide_feed = feedparser.parse(
            f"https://www.tidetimes.org.uk/{location}-tide-times.rss")

        self.tides = tide_feed.entries[0].\
            summary_detail.value.split('<br />')

        self.tides = self.tides[2:-1]


