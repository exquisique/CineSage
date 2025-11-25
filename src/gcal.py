import os
import datetime
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"Could not find {CREDENTIALS_FILE}. Please download it from Google Cloud Console.")
                
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def list_upcoming_events(max_results=10):
    """Shows basic usage of the Google Calendar API."""
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=max_results, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def create_movie_event(title: str, start_time: datetime.datetime, duration_minutes: int = 120):
    """Creates a calendar event for the movie."""
    service = get_calendar_service()
    
    end_time = start_time + datetime.timedelta(minutes=duration_minutes)
    
    event = {
        'summary': f'Movie Night: {title}',
        'description': f'Scheduled viewing of {title}. Popcorn time!',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC', # Best to handle timezones properly in a real app
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def find_next_available_slot(duration_minutes: int = 120):
    """
    Very basic slot finder. Looks for a gap in the next 7 days.
    This is a simplified version.
    """
    service = get_calendar_service()
    now = datetime.datetime.utcnow()
    
    # Check next 7 days
    time_min = now.isoformat() + 'Z'
    time_max = (now + datetime.timedelta(days=7)).isoformat() + 'Z'
    
    events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                        timeMax=time_max, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    # Simple logic: Check evenings (18:00 - 22:00) for gaps
    # This is a placeholder for more complex logic
    
    # For now, let's just return a suggestion for "Tomorrow at 8 PM" as a mock
    # because real slot finding requires complex timezone and working hours logic
    tomorrow_8pm = (now + datetime.timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0)
    return tomorrow_8pm
