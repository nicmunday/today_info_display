#!/usr/bin/env python3

from __future__ import print_function
import datetime
import os.path
import subprocess
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCal:
    def __init__(self):
        pass

    def get_cal_events(self, start_time, end_time):

        try:
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('/home/nic/bin/imports/json/token.json'):
                creds = Credentials.from_authorized_user_file('/home/nic/bin/imports/json/token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        '/home/nic/bin/imports/json/credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('/home/nic/bin/imports/json/token.json', 'w') as token:
                    token.write(creds.to_json())


            service = build('calendar', 'v3', credentials=creds)


#############   ACCESS CAL, STORE RESULTS IN LIST   ############


            returnlist = []
            events = []



            events_result = service.events().list(calendarId='primary', timeMin=start_time,
                                                  timeMax=end_time, singleEvents=True,
                                                  orderBy='startTime').execute()

            events = events_result.get('items', [])

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if len(start) > 10:
                    end = start[11:16]
                    start = start[:10] + " " + end
                returnlist.append((start, event['summary'], "Pr"))

            return(returnlist)

        except RefreshError:
            subprocess.run(["rm", "/home/nic/bin/imports/token.json"])
            self.get_cal_events(start_time, end_time)