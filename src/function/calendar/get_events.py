import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from src.utils import SCOPES

def get_credentials(self):
        """
        Get and refresh Gmail API credentials
        """
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

def get_calendar_events(self, start_date=None, end_date=None):
    """
    Get events from Google Calendar.
    """

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        raise Exception("Credentials are not valid or missing.")

    service = build("calendar", "v3", credentials=creds)

    try:
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        if not events:
            return "No upcoming events found."
        
        return events
    except Exception as error:
        return f"An error occurred: {error}"