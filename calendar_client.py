from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from config import MY_NAME, TIMEZONE
from datetime import datetime
import os

def get_calendar_service():
    if not os.path.exists("token.json"):
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", "https://www.googleapis.com/auth/calendar")
        credential = flow.run_local_server(port = 0)
        with open("token.json", "x") as f:
            f.write(credential.to_json())
    else:
        credential = Credentials.from_authorized_user_file("token.json")
        if credential.expired:
            try:
                credential.refresh(Request())
                with open("token.json", "w") as f:
                    f.write(credential.to_json())
            except:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", "https://www.googleapis.com/auth/calendar")
                credential = flow.run_local_server(port = 0)
                with open("token.json", "w") as f:
                    f.write(credential.to_json())
    return build("calendar", "v3", credentials = credential)

def create_events(dates, schedule):
    service = get_calendar_service()
    if len(dates) > 8:
        next_month = dates[8]
    info = tuple(zip(dates, schedule))
    year = datetime.now().year

    for pair in info:
        if MY_NAME in pair:
            month = pair[0]
            pass
        elif "OFF" in pair or not pair[1]:
            pass
        else:
            day = pair[0]
            if day == "1":
                month = next_month
            time = pair[1].split("-")

            start_time = time[0]
            if ":" in start_time:
                if start_time.endswith("p"):
                    start_time = start_time.replace("p", "PM")
                elif start_time.endswith("a"):
                    start_time = start_time.replace("a", "AM")
                else:
                    start_time = start_time + "AM"
            else:
                if start_time.endswith("p"):
                    start_time = start_time.replace("p", ":00PM")
                elif start_time.endswith("a"):
                    start_time = start_time.replace("a", ":00AM")
                else:
                    start_time = start_time + ":00AM"

            end_time = time[1]
            if ":" in end_time:
                if end_time.endswith("p"):
                    end_time = end_time.replace("p", "PM")
                elif end_time.endswith("a"):
                    end_time = end_time.replace("a", "AM")
                else:
                    end_time = end_time + "AM"
            else: 
                if end_time.endswith("p"):
                    end_time = end_time.replace("p", ":00PM")
                elif end_time.endswith("a"):
                    end_time = end_time.replace("a", ":00AM")
                else:
                    end_time = end_time + ":00AM"
            
            formatted_start_time = datetime.strptime(str(year) + month + str(day) + start_time, "%Y%B%d%I:%M%p")
            formatted_end_time = datetime.strptime(str(year) + month + str(day) + end_time, "%Y%B%d%I:%M%p")
            
            formatted_start_time = datetime.strftime(formatted_start_time, "%Y-%m-%dT%H:%M:%S")
            formatted_end_time = datetime.strftime(formatted_end_time, "%Y-%m-%dT%H:%M:%S")

            event = {
                "summary" : "Work @ Bloom Coffee and Kitchen",
                "start": {
                    "dateTime": formatted_start_time,
                    "timeZone" : TIMEZONE
                },                
                "end": {
                    "dateTime": formatted_end_time,
                    "timeZone": TIMEZONE
                }
            }
            
            service.events().insert(calendarId = "primary", body = event).execute()
