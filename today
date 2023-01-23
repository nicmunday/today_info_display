#!/usr/bin/env python3

import prettytable
from _datetime import datetime, timedelta, date
import sys
import subprocess
import json

from imports import tides
from imports import episodes
from imports import threedayweather
from imports import latest_weather
from imports import googlecal
from imports import newsprocessor
from imports import reminders
from imports import moonphase


# Open settings JSON, get file locations
with open("imports/json/"
          "today_settings.json") as datefile:
    settings = json.load(datefile)

reminder_file_location = settings[
    "Reminder File Location"].strip()

shopping_file_location = settings[
    "Shopping File Location"].strip()

tides_file_location = settings[
    "Tides File Location"].strip()

episodes_file_location = settings[
    "Episodes File Location"].strip()

watch_file_location = settings[
    "Watch File Location"].strip()

moon_phase_file = settings[
    "Moon Phase File"].strip()

urgent_reminders_file = settings[
    "Urgent Reminders File"].strip()




# Create a single datetime object and then
# all the time-related vars you need in the script
# In one place for easy access

# (Currently today_day_full_ name and today_date_string
# are used in more than one section)

now = datetime.now()
today_date_str = now.strftime("%Y-%m-%d")
tomorrow_date_string = (now + timedelta(
    days=1)).strftime("%Y-%m-%d")

next_month = int(now.strftime("%m"))
next_month_year = int(now.strftime("%Y"))
readable_date_and_time = now.strftime(
    "%a %d %b %H:%M")

today_day_full_name = now.strftime("%A")
tesco_days = ["Thursday", "Sunday", "Monday"]
watch_charge_days = ["Sunday", "Monday", "Tuesday"]

read_or_rss = []
tesco_flag = False

#Set tesco day flag
for day in tesco_days:
    if day == today_day_full_name:
        tesco_flag = True

watch_flag = False

#See if it's watch charge day
#if it's watch charge day and last charge
# was more than 8 days ago

for day in watch_charge_days:
    if day == today_day_full_name:
        with open(watch_file_location) as reader:
            line = reader.readline().strip()

            if line != "" and datetime.fromisoformat(
                    line) < \
                    now-timedelta(days=8):

                watch_flag = True


# Create all the prettytable tables in one place,
# easier to change them
# later rather than hunting for them

def no_border_table():
    table = prettytable.PrettyTable()
    table.header = False
    table.border = False
    table.vrules=prettytable.NONE
    table.hrules=prettytable.NONE
    return table

def frame_table():
    table = prettytable.PrettyTable()
    table.header = False
    table.hrules = prettytable.FRAME
    table.vrules = prettytable.FRAME
    table.set_style(prettytable.DOUBLE_BORDER)
    return table

def full_table():
    table = prettytable.PrettyTable()
    table.header = False
    table.hrules = prettytable.ALL
    table.vrules = prettytable.ALL
    table.set_style(prettytable.DOUBLE_BORDER)
    return table


table = frame_table()

reminders_table_left, \
    reminders_table_right,\
    tides_eps_table_left, \
    tides_eps_table_right,\
    cal_date_table,\
    cal_event_table, \
    weather_col_1, \
    weather_col_2,  \
    weather_col_3,  \
    weather_latest = [no_border_table() for _ in range(10)]

moon_phase_table,\
    watch_charge_table,\
    urgent_reminders_table,\
    time_table,news_table = [full_table() for _ in range(5)]


####Tides and Eps Funtions ####
#(3 diff ep days == lots of re-used code

def add_tides_eps(col1, col2):
    tides_eps_table_left.add_row([col1])
    tides_eps_table_right.add_row([col2])

def form_eps_list(splitlist):
    result_list = []
    for n in range(0, len(splitlist), 2):
        if n != len(splitlist) - 1:
            result_list.append((splitlist[n],
                             splitlist[n + 1]))
    return result_list

def add_eps_to_table(eps_list):
    for n in range(0, len(eps_list), 2):
        if n == len(eps_list) - 1:
            add_tides_eps(
                f"{eps_list[n][0]} {eps_list[n][1]}", "")
        else:
            add_tides_eps(
                f"{eps_list[n][0]} {eps_list[n][1]}" ,
                f"{eps_list[n+1][0]} {eps_list[n+1][1]}")

    if eps_list != tom_eps:
        add_tides_eps(
            "%%%%%%%%%%%%%%%%%%%%" ,
            "%%%%%%%%%%%%%%%%%%%%")

def write_ep_strings(ep_list):
    return_str = ""
    for ep in ep_list:
        return_str += f"{ep[0]},{ep[1]}"
    return_str += "\n"
    return return_str


####Cal functions ####

def no_cal_events():
    cal_event_table.add_row(["", ""])
    cal_event_table.add_row(["", ""])
    cal_event_table.add_row(["","No Events Upcoming"])
    cal_event_table.add_row(["", ""])
    cal_event_table.add_row(["", ""])

def add_to_cal_tabs(date_table1, date_table2,
                    event_table1, event_table2):
    cal_date_table.add_row([date_table1, date_table2])
    cal_event_table.add_row([event_table1, event_table2])


####   Reminders Functions   ####

def add_reminder_to_list(list, count):
    remsplit = reminder.split(",")
    for rem in remsplit:
        if rem.strip() == "Today" or \
                rem.strip() == today_day_full_name:

            if count == 0:
                reminders_right_list.append("")
            if count == 3:
                reminders_left_list.append("")
            list.append(remsplit[-1].strip())
            count += 1
    return count, list




####   A single Weather Function   ####

def add_weather_col(tab,day):
    tab.add_column("", [
        "","",day['day'],
        day['description'],
        day['max'] + " " + day['min'],
        day['wind'],
        day["sunrise"],
        day["sunset"]])







####   TIDES   ####


# tide info only changes once a day, so no
# point accessing the rss feed more than that
# read the existing tides csv file which has the
# date it was written and the tide info




# See if the stored tides are from today
# If not, get RSS tides and write new tides to file.

with open(tides_file_location) as reader:
    top_line = reader.readline()
tide_info = top_line.split(",")
info_date = tide_info.pop(0)

#arg -ft == 'force tides' -> get RSS no matter what

if info_date != today_date_str or "-ft" in sys.argv:
    my_tide = tides.Tides()
    tide_info = my_tide.tides

    with open(tides_file_location, "w") as writer:
        writer.write(today_date_str + "," +
                     (",").join(tide_info))

    read_or_rss.append("RSS Tides")
else:
    read_or_rss.append("Read Tides")


for n in range(0, len(tide_info), 2):
    if n == len(tide_info)-1:
        add_tides_eps(tide_info[n], "")

    else:
        add_tides_eps(tide_info[n], tide_info[n + 1])




####    EPISODES    ####

# Line break between tides and eps


# Only need to read eps from rss once a day.
# Write to file that time, read from file other times
# (Exception being if "-fe" (Force Eps) option is
# included with program run)

# If the date at the top of the saved eps is today
# and no "-fe" flag, use those eps
with open(episodes_file_location) as reader:
    episode_file = reader.readlines()

# if it's today

if len(episode_file) > 0 and episode_file[0].strip() == today_date_str and\
        "-fe" not in sys.argv:

#Each line should have a day's worth of episodes
    yest_eps_string = episode_file[1].strip()
    today_eps_string = episode_file[2].strip()
    tom_eps_string = episode_file[3].strip()

# call form_eps_list function for each above day string
    yest_eps , today_eps , tom_eps = [
        form_eps_list(item) for item in [
        yest_eps_string.split(","),
        today_eps_string.split(","),
        tom_eps_string.split(",")
    ]]

    read_or_rss.append("Read Eps")

# if not today, RSS eps it is.
else:
    eps_obj = episodes.Episodes()

#Form the day episodes lists from the RSS
    yest_eps, today_eps, tom_eps = [
        eps_obj.get_eps_list(day) for day in [
            "yesterday", "today", "tomorrow"
        ]]

#Since we got the RSS, let's write them to disk

    writeList = [write_ep_strings(item) for item in [
        yest_eps, today_eps, tom_eps]]

    with open(episodes_file_location, "w") as writer:
        writer.write(f"{today_date_str.strip()} \n {''.join(writeList)}")

    read_or_rss.append("RSS Eps")

#And now regardless of disk-read or RSS
#Print eps to tables (and various line separators)

add_tides_eps(
    "~~~~~~~~~~~~~~~~~~~~~~~~~" ,
    "~~~~~~~~~~~~~~~~~~~~~~~~~")
add_tides_eps("", "")

[add_eps_to_table(item) for item in [
    yest_eps, today_eps, tom_eps]]

add_tides_eps("", "")


# get the current month and next month calendars
# from linux 'cal' program

# Note you cannot use a timedate.timedelta because
# it has no "month" value, you can
# increase/decrease by time values, days, weeks or
# years but not months.
# hence the roundabout code - get the month num,
# make it int, add 1, unless it's 12.
if next_month == 12:
    next_month = 1
    next_month_year += 1
else:
    next_month += 1
if next_month < 10:
    next_month = "0"+str(next_month)

cal = subprocess.run(["/usr/bin/cal"],
                     capture_output=True,
                     text=True)

cal2 = subprocess.run([f"/usr/bin/cal",
                       f"{next_month}",
                       f"{next_month_year}"],
                      capture_output=True, text=True)

calout = cal.stdout
cal2out = cal2.stdout


# Write Tides, Eps, month cals.
table.add_row([tides_eps_table_left,
               tides_eps_table_right,
               calout, cal2out])


####   Populate Moon Phase Table   ####

with open(moon_phase_file) as reader:
    moon_list = reader.readlines()

# If moon was last calculated > 4 hours ago or
# "-fm" option was sent to today call (fm = force moon)
# then calculate a new moon degrees/phase and write it to disk

if len(moon_list) < 1 or \
        moon_list[0].strip() == "" or  \
        datetime.fromisoformat(
    moon_list[0].strip()) < (now - timedelta(hours=4)) or \
        "-fm" in sys.argv:

    saved_mmon_time = datetime.fromisoformat(
        moon_list[0].strip())
    my_moon = moonphase.MoonPhase(now)
    moon_phase = my_moon.get_phase()
    moon_degrees = my_moon.degrees
    with open(moon_phase_file, "w") as writer:

        writer.write(str(now) + "\n" +
                     moon_phase + "\n" +
                     str(moon_degrees) + "\n")

    read_or_rss.append("Calculated Moon")
    saved_moon_time = now

#Otherwise read it from disk
else:
    saved_moon_time = datetime.fromisoformat(
        moon_list[0].strip())
    moon_phase = moon_list[1].strip()
    moon_degrees = moon_list[2].strip()
    read_or_rss.append("Read Moon")

moon_degrees = round(float(moon_degrees), 2)

moon_phase_table.add_row([
    f"{moon_degrees}\u00B0|{moon_phase}"
    f"|{saved_moon_time.strftime('%H:%M')}"])




####   Populate News Table  ####

news = newsprocessor.NewsProcessor().new_stories([])
new_stories =  f"{len(news)} New Stories"
news_table.add_row([new_stories])

####   Populate Urgent Reminders Table   ####

urgentflag = False

with open(urgent_reminders_file) as reader:
    urgent_reminders = reader.readlines()

for urgent_reminder in urgent_reminders:
    if urgent_reminder.strip() != "":

        urgent_reminders_table.add_row([
            urgent_reminder.strip()])

        urgentflag = True


####   Populate Time Table   ####

time_table.add_row([readable_date_and_time])

# is it likely time to charge my smartwatch?
if watch_flag:
    time_table.add_row(["Charge Watch"])







# Moon/time/news doesn't get added to table until
# just before cal/reminders (literally line before)
# This is because on bin day, bin is added to
# this row, but only know it's bin day when
# done cal stuff. So decided to do it all
# at same time for simplicity/readability.







####    CALENDAR     ####


# -c from user == don't include calendar stuff
if "-c" not in sys.argv:
    not_today_events = []
    todayevents = []
    datesevents = []


  ####   GET CAL EVENTS   ####

    # Get cal events from 3 hours ago until 7 days from now.

    start_time = str(now - timedelta(hours=3))
    start_time = start_time[:10]+"T"+start_time[11:]+"Z"
    end_time = str(date.today() +
                   timedelta(days=7)) + "T23:59:59Z"

    cal = googlecal.GoogleCal()
    events = cal.get_cal_events(start_time, end_time)



    if events:

        events.sort()
        binflag = False
        for event in events:
            #check if event is bin related, if it is,
            # add to the news table

            if event[1].strip() == "Grey Bin" or \
                    event[1].strip() == "Green Bin":

                if not binflag:
                    if event[0][:10] == tomorrow_date_string:

                        bin_day = datetime.fromisoformat(
                            event[0]).strftime("%a")

                        news_table.add_row([bin_day +
                                            " - " + event[1]])

            #                 binflag = True

            else:
                # not bin then
                # check if date is date and time or just
                # date (date is 10 chars)
                # create datesplit list which is date and
                # time or date and blank if no time
                if len(event[0]) > 11:
                    datesplit = event[0].split()
                else:
                    datesplit = [event[0], ""]

                # turn datesplit into readable string =
                # DAYNAME DD MONTH
                readable_date = datetime.fromisoformat(
                    datesplit[0]).strftime("%a %d %b")

                # if cal event date == today's date add to
                # today events list -  kept  separate to
                # be printed before other cal stuff
                # unless option -rad (Remove All Day)
                # passed and event has no time

                if datesplit[0] == today_date_str:

                    if "-rad" not in sys.argv or (
                            datesplit[1] != "" and
                            "-rad" in sys.argv):

                        todayevents.append((
                            readable_date, datesplit[1],
                            event[1], event[2]))
                else:
                    # if non bin and non today event,
                    # add to not today events list
                    not_today_events.append((
                        readable_date, datesplit[1],
                        event[1], event[2]))

        # Add todays events to 2 calendar tables first

        add_to_cal_tabs("","","","")

        for event in todayevents:
            add_to_cal_tabs(event[0], event[1],
                            event[2], event[3])

        if len(todayevents) > 0:
            add_to_cal_tabs(
                "@@@@@@@@@@", "@@@@@",
                "@@@@@@@@@@@@@@@@@@@@@@@@@", "@@")


        for event in not_today_events:
            add_to_cal_tabs(event[0], event[1],
                            event[2], event[3])

        if len(todayevents) == 0 and len(not_today_events) == 0:
            no_cal_events()



    else:
        no_cal_events()

else:
    add_to_cal_tabs("","","","")





####   REMINDERS   ####



# Get Reminders
my_reminder = reminders.Reminders()
current_reminders = my_reminder.get_reminders(
    reminder_file_location)




# Instead of adding reminders straight to  tables, add
# to lists. This is for formatting. Won't know how many
# blank lines between date/news & reminders until have
# gone through reminders list and seen what we're printing

# len(current_reminders) doesn't work as a check because
# some reminders only printed certain days

reminders_right_list = []
reminders_left_list = []
shopping_list = []



count = 0
for reminder in current_reminders:
    if reminder.strip() != "":
        if count < 3:

            count, reminders_right_list = \
                add_reminder_to_list(
                reminders_right_list, count)


        elif count < 6 and not tesco_flag:

            count, reminders_left_list = \
                add_reminder_to_list(
                reminders_left_list, count)


        elif tesco_flag:

            count, reminders_right_list = \
                add_reminder_to_list(
                reminders_right_list, count)
        else:
            if count % 2 == 0:
                count, reminders_right_list = \
                    add_reminder_to_list(
                    reminders_right_list, count)
            else:
                count, reminders_left_list = \
                    add_reminder_to_list(
                        reminders_left_list, count)





#If today is the day before a tesco delivery,
# add shopping list to reminders

if tesco_flag:
    with open(shopping_file_location) as reader:
        shopping = reader.readlines()

    if len(shopping) > 0 and len(
            reminders_left_list) == 0:

        reminders_left_list.append("")

    for line in shopping:
        shopping_list.append(line.strip())
        count += 1

if count > 6 and not tesco_flag:
    if count % 2 == 1:
        reminders_left_list.append("")
elif count > 3 and not tesco_flag:
    difference = 6 - count
    for _ in range(difference):
        reminders_left_list.append("")


# First 3 reminders go in right column. Nums 4-6,
# left column. After that they alternate.
# Fewer that 8 reminders (4 rows of two columns)
# you want two blank rows above them for spacing.
# More that 8 reminders, one blank row.

if count < 8 and not tesco_flag:
    reminders_table_left.add_row([""])
    reminders_table_right.add_row([""])

for row in reminders_left_list:
    reminders_table_left.add_row([row])
for row in reminders_right_list:
    reminders_table_right.add_row([row])
if tesco_flag:
    #for item in shopping_list:
    for n in range (0, len(shopping_list)):
        # if n == len(shopping_list)-1:

        reminders_table_left.add_row([
            shopping_list[n]])
        # else:
        #     reminders_table_left.add_row([
        #         shopping_list[n] + " ||| " +
        #         shopping_list[n+1]])




# Finally we print the earlier moon/news/etc row
if not urgentflag:
    urgent_reminders_table = ""

table.add_row([moon_phase_table, time_table,
               urgent_reminders_table, news_table])

# and finally add all cal and reminder
# (and date/news) stuff to the main table.
table.add_row([cal_date_table, cal_event_table,
               reminders_table_left, reminders_table_right])




####   WEATHER   ####

# No weather if -w sent with program run
if "-w" not in sys.argv:

    # **NOTE** Executive decision: not worth saving
    # weather to disk, changes too often.

    # a weather (or ThreeDayWeather) object
    forecast = threedayweather.ThreeDayWeather()

    # Use said object to get forecasts for today,
    # tomorrow and the day after
    today_weather = forecast.today()
    tomorrow_weather = forecast.tomorrow()
    third_day_weather = forecast.day_after_tomorrow()

    # And a latest weather object from a different
    # module (because different rss feed.)
    latest = latest_weather.LatestWeather()

       # And finally, build the weather sections.

    [add_weather_col(tab, day) for tab, day in [
        (weather_col_1, today_weather),
        (weather_col_2,tomorrow_weather),
        (weather_col_3,third_day_weather)]]

    weather_latest.add_column("", [
        "","", "Latest " + latest.time, "",
        latest.conditions,
        latest.temp, "",
        "Pub: " + forecast.publist[1] +
        " " + forecast.publist[2] +
        " " + forecast.publist[4][:5]])



    # # And finally... Add weather columns to the main table.
    table.add_row([weather_col_1, weather_col_2,
                   weather_col_3, weather_latest])


#Ok, finally is actually printing the main table.
# Bit of a waste of time if you don't. :)
print(table)
print(read_or_rss)
