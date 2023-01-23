#!/usr/bin/env python3
import feedparser
import json
class Episodes:
    def __init__(self):
        with open ("imports/json/my_episodes_user_data.json") as datafile:
            data = json.load(datafile)
        self.USER = data["User ID"]
        self.API_KEY = data["API Key"]

    def get_eps_list(self, which_feed):
        feed = feedparser.parse(f"https://www.myepisodes.com/"
                                f"rss.php?feed={which_feed}&"
                                f"showignored=1&onlyunacquired=1&"
                                f"uid={self.USER}&pwdmd5={self.API_KEY}")
        eps = []
        wednesdayflag = False
        jackryanflag = False
        ignoreList = [
            "The Daily Show with Trevor Noah",
            "The Tonight Show Starring Jimmy Fallon",
            "The Graham Norton Show",
            "The Late Show with Stephen Colbert",
            "Last Week Tonight with John Oliver",
            "The Late Late Show with James Corden",
            "Avenue 5",
            "Late Night with Seth Meyers",
            "The Jonathan Ross Show",
            "NCIS: Hawai'i",
            "Station 19",
            "Match of the Day",
            "Jimmy Kimmel Live",
            "Live at the Apollo",
            "No Episodes",
        ]

        for show in range(len(feed.entries)):
            ep = feed.entries[show].title.split(" ][ ")
            ep[0] = ep[0][2:].strip()
            #Too Long for my nice neat screen!
            if ep[0] == "Frankie Boyle's New World Order":
                ep[0] = "FB New World Order"

# Some shows drop a series at a time (Wednesday, Jack Ryan,
# currently.) We only want these to show up once so employ
            # a flag system and only add them to list once.

            if ep[0] not in ignoreList:
                if ep[0] == "Wednesday":
                    if not wednesdayflag:
                        eps.append((ep[0], ep[1]))
                        wednesdayflag = True
                if ep[0] == "Tom Clancy's Jack Ryan":
                    if not jackryanflag:
                        eps.append((ep[0], ep[1]))
                        jackryanflag = True
                else:
                    eps.append((ep[0], ep[1]))



        if len(eps) == 0:
            eps.append(("No Episodes", ""))
        return(eps)



    def yesterday(self):
        return(self.get_eps_list("yesterday"))

    def today(self):
        return(self.get_eps_list("today"))

    def tomorrow(self):
        return(self.get_eps_list("tomorrow"))

