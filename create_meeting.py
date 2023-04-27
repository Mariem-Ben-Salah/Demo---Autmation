import datetime,json
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import uuid

SCOPES = ['https://www.googleapis.com/auth/calendar']
API_NAME = 'calendar'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = 'credentials.json' # get the service-account json key 

calendar_id = '' # TO DO: Add Email of the person / service account that we are going to impersonate
credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE,scopes=SCOPES, subject=calendar_id)
service = build(API_NAME, API_VERSION, credentials=credentials,cache_discovery=False)

event_body = {
    'summary' : 'EIS CLS - Demo',
    'start' : {
        'timeZone' : 'Europe/Zurich',
    },
    'end': {
        'timeZone' : 'Europe/Zurich',
    },
    
    'attachments': [], # List of the attachments
    'attendees': [], # List of the attendees
    'conferenceData': {
        'createRequest': {
            'requestId': 'randomString'+str(uuid.uuid1()), # Generate a random requestId for every meeting, requestId should be unique
            'conferenceSolutionKey': {'type': 'hangoutsMeet'},
        },
    },
}

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    """ Convert a date tuple (year, month, day, hour, minute) to a String 
    :params year, month, day, hour, minute : The date to convert 
    :return: a format string 1900-01-01T00:00:00
    
   """
    var = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), 0).isoformat()
    return (datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), 0).isoformat())
	
def CreateMeeting(year, month, day, startTimeH, startTimeM, endTimeH, endTimeM, Emails, URL= None):
    """ Create the google Meetings
    
    :params year, month, day : The date of the meeting
    :params startTimeH,startTimeM : Start time of the meeting (13,40) --> 13:40
    :params endTimeH, endTimeM : End time of the meeting (14,45) --> 14:45
    :param Emails : List of Emails to whom we are sending the invitations
    :param URL : a link (of a document, video, ... ) attached to the meeting
    :return:  a json with information of the created meeting
                
    """

    event_body['start']['dateTime'] = convert_to_RFC_datetime(year,month,day,startTimeH,startTimeM)
    event_body['end']['dateTime'] = convert_to_RFC_datetime(year,month,day,endTimeH,endTimeM)
    for email in Emails : 
        event_body['attendees'].append({'email': email})

    if URL :
        event_body['attachments'].append({'title' : 'Link to The Demo Presentation','fileUrl' : URL})
        
    event = service.events().insert(
        calendarId = calendar_id,
        sendNotifications = True, 
        supportsAttachments = True,
        body = event_body,
        conferenceDataVersion = 1,
    ).execute()
    
    return(event)