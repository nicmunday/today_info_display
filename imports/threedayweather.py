#!/usr/bin/env python3
import feedparser

class ThreeDayWeather:

    def __init__(self):

        #The BBC Weather Three day forecast RSS feed
        self.three_day_feed = feedparser.parse(
            "https://weather-broker-cdn.api.bbci.co.uk/en/"
            "forecast/rss/3day/2633749")

        # Various elements of the date & time so I can ditch the
        # ones I don't want (year, seconds, and "GMT"
        self.publist = self.three_day_feed.feed[
            'published'].split()

        # publist[0][:-1] removes the last char of the date, which
        # in this feed is a comma I don't want
        self.published = f"{self.publist[0][:-1].strip()} " \
                         f"{self.publist[1].strip()} " \
                         f"{self.publist[2].strip()} " \
                         f"{self.publist[4][:-3]}"






    def convert_feed_to_data(self, weather_feed):
        feed_title = weather_feed.title
        feed_summary = weather_feed.summary

        title_list = feed_title.split(",")
        summary_list = feed_summary.split(",")

        description_list = title_list[0].split(":")
        weather_data = {"day": description_list[0].strip(),
                        "description": description_list[1].strip(),
                        "max": "", "min": "", "wind": "", "sunrise":
                            "", "sunset": ""}

        for item in summary_list:
            item_split = item.split()
            if item_split[1] == "Temperature:":
                if item_split[0] == "Maximum":
                    weather_data["max"] = f"Max: {item_split[2]}"
                elif item_split[0] == "Minimum":
                    weather_data["min"] = f"Min: {item_split[2]}"
            elif item_split[0] == "Wind" and item_split[1] == "Speed:":
                weather_data["wind"] = f"Wind: {item_split[2]}"
            elif item_split[0] == "Sunrise:":
                weather_data["sunrise"] = f"Sunrise: {item_split[1]}"
            elif item_split[0] == "Sunset:":
                weather_data["sunset"] = f"Sunset: {item_split[1]}"

        return weather_data

    def today(self):
        today_weather = self.convert_feed_to_data(
            self.three_day_feed.entries[0])
        return today_weather


    def tomorrow(self):
        tomorrow_weather = self.convert_feed_to_data(
            self.three_day_feed.entries[1])
        return tomorrow_weather


    def day_after_tomorrow(self):
        day_after_tomorrow_weather = self.convert_feed_to_data(
            self.three_day_feed.entries[2])
        return day_after_tomorrow_weather

