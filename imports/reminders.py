#!/usr/bin/env python3

class Reminders:
    def __init__(self):
        pass

    def get_reminders(self, reminder_file_location):
        remind_list = []
        with open(reminder_file_location) as reader:
            for line in reader:
                if line.strip() != "":
                    remind_list.append(line)
        return remind_list

    def add_reminder(self, reminder):
        with open("/home/nic/bin/reminders.txt", "a") as appender:
                writer.write(f"{reminder.strip()}\n")

#myremind = Reminders()
