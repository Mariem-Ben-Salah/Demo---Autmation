import uuid
import datetime
import requests 
from requests.auth import HTTPBasicAuth
import math
from string import Template
import json
from nptime import nptime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from create_meeting import CreateMeeting

# secret = json.loads(parameters.get_secret("BRSlack"))
BotToken = "" # TO DO : Add Bot Token
client = WebClient(token=BotToken)

def GetAllUsersIds():

    """ Get the IDs of all the team members in a particular channel (including integrations : app, bot)
    :return: a list of the users IDs
    """

    response = client.conversations_members(
        channel = "" # TO DO : Add the slack channel id
    )
    Ids = response['members']
    return Ids

def GetUsersEmail() :

    """ Get the Email corresponding to a user ID
    :return: a dictionary {user_id : email_address}
    """

    UsersIds = GetAllUsersIds() # get all the IDS 
    UserIdEmail = {}
    for UserId in UsersIds :
        user = UserId
        # Get the data for every id in the list 
        response = client.users_info(
            user = user
        )
        profile = response['user']['profile']
        if ('email' in profile) : # check whether it's a user and not an app or bot
            Email = profile['email']
            UserIdEmail[UserId] = Email
    return (UserIdEmail)
    
def generateId ():
    return uuid.uuid1()
    
def jql():
    """ Calls Jira cloud API and execute a certain query
    return: a dictionnary with List of issues for each product owner 
    
    """    
    APIkey = "" # TO DO : Add API key for Jira
    emailServiceAccount = "" # TO DO : Add the email address of the service account 
    url = "https://{CompanyName}.atlassian.net/rest/api/3/search?maxResults=1000" # TO DO : Adjust the URL 
    
    auth = HTTPBasicAuth(emailServiceAccount, APIkey)

    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json"
    }

    request = """status = Review AND project in {x,y,z} AND assignee != EMPTY AND type in(Bug,Story)""" # TO DO : Adjust the query
    query ={'jql' : request}

    resp = requests.get(
       url,
       headers=headers,
       params=query,
       auth=auth
    )

    issue_link = "https://{CompanyName}.atlassian.net/browse/" # TO DO : Adjust the issue link 
    data=resp.json()
    issues = data["issues"]
    new_issues = []
    grouped_data = {}
    for issue in issues :
        data = {
        "key": issue["key"],
        "link" : issue_link+issue["key"],
        "summary": issue["fields"]["summary"],
        "type": issue["fields"]["issuetype"]["name"],
        "assignee": issue["fields"]["assignee"]["displayName"] if issue['fields']['assignee'] else "unassigned"
        
    } 
        new_issues.append(data)
    
    for item in new_issues:
        assignee = item['assignee']
        if assignee in grouped_data:
            grouped_data[assignee].append(item)
        else:
            grouped_data[assignee] = [item]

    return grouped_data

def highlight_word_request(text, word, slide_id, style=None,link_url=None):

    """Generates a list of Google Slides API requests to highlight a specified word in a text box on a slide.

    Args:
        text (str): The text containing the word to highlight.
        word (str): The word to highlight.
        slide_id (int): The ID of the slide containing the text box.
        style (str, optional): The highlighting style to apply to the word. 
            Possible values are "color" (to apply a green color), "bold" (to apply bold formatting), 
            or None (to apply no formatting). Defaults to None.
        link_url (str, optional): The URL to link to when the highlighted word is clicked. 
            If None, no link is added. Defaults to None.

    Returns:
        List[Dict]: A list of Google Slides API requests that, when executed, highlight the specified word 
        in the text box on the slide.

    Example:
        To highlight the word "apple" in a text box on slide with ID 1234 using a green color and add a link 
        to www.example.com when the word is clicked, the following request list can be generated:
        
        requests = highlight_word_request("I like to eat apples.", "apple", 1234, style="color", link_url="www.example.com")
    """
    word_start = text.find(word)
    word_end = word_start + len(word)
    requests = []
    if style == "color":
        requests.append({
            "updateTextStyle": {
                "objectId": f"textboxId{slide_id}",
                "textRange": {
                    "type": "FIXED_RANGE",
                    "startIndex": word_start,
                    "endIndex": word_end
                },
                "style": {
                    "foregroundColor": {
                        "opaqueColor": {
                            "rgbColor": {
                                "red": 0.0,
                                "green": 0.827,
                                "blue": 0.6
                            }
                        }
                    }
                },
                "fields": "foregroundColor"
            }
        })
    elif style == "bold":
        requests.append({
            "updateTextStyle": {
                "objectId": f"textboxId{slide_id}",
                "textRange": {
                    "type": "FIXED_RANGE",
                    "startIndex": word_start,
                    "endIndex": word_end
                },
                "style": {
                    "bold": True
                },
                "fields": "bold"
            }
        })
    if link_url:
        requests.append({
            "updateTextStyle": {
                "objectId": f"textboxId{slide_id}",
                "textRange": {
                    "type": "FIXED_RANGE",
                    "startIndex": word_start,
                    "endIndex": word_end
                },
                "style": {
                    "link": {
                        "url": link_url
                    }
                },
                "fields": "link"
            }
        })
    return requests

def createSlide(day,month,year):

    """ Copy a Google Slides Template and fill it with the return value of jql()
    
    return: Link to the created Google Slides 
    """
    CLIENT_SECRET_FILE = 'credentials.json' # get the service-account json key 
    file_id = "" # TO DO : Add the file id of the Google Slides template
    folder_id = [""] # TO DO : Add the folder id of where you want to create the new Google Slides
    

    API_NAME_SLIDES = 'slides'
    API_VERSION_SLIDES = 'v1'
    SCOPES_SLIDES = ['https://www.googleapis.com/auth/presentations']

    API_NAME_DRIVE = 'drive'
    API_VERSION_DRIVE = 'v3'
    SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
    
    credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE,scopes=SCOPES_DRIVE)
    service_drive = build(API_NAME_DRIVE, API_VERSION_DRIVE, credentials=credentials)

    credentials = service_account.Credentials.from_service_account_file(CLIENT_SECRET_FILE,scopes=SCOPES_SLIDES)
    service_slides = build(API_NAME_SLIDES, API_VERSION_SLIDES, credentials=credentials)
    wanted_datetime = datetime.date(int(year),int(month),int(day))#datetime of the next tuestday
    week_num = wanted_datetime.isocalendar()[1]  # Using isocalendar() function
    file_metadata = {
        'name' : str(year) + '_KW'+  str(week_num) + "_Demo",
        'mimeType': 'application/vnd.google-apps.presentation',
        'parents': folder_id,
    }
    resp = service_drive.files().copy(
        fileId=file_id,
        body=file_metadata,
        supportsAllDrives=True
            ).execute()
    Presentation_ID = resp["id"]
    
    # Call the Slides API
    presentation = service_slides.presentations().get(
        presentationId=Presentation_ID).execute()
    slides = presentation.get('slides')

    IssuesDict = jql()
 
    body = {'requests': []}
    with open("template/inserttext.template","r") as textT :
        text = Template(textT.read())
    insertText = "Demo - Knowledge transfer {0:02d}.{1:02d}.{2}".format(day, month, year)

    result =  text.substitute(
        {
            "element_id" : slides[0]["pageElements"][0]["objectId"],
            "text" : insertText,
            "insertionIndex" : 28
        })
    body["requests"].append(json.loads(result))
    body["requests"].append({
      "deleteText": {
        "objectId": slides[0]["pageElements"][0]["objectId"],
        "textRange": {
          "type": "FROM_START_INDEX",
          "startIndex": 28 + len(insertText)
        }
      }
    }) 
    nbLinesCreated = 20
    limitLignePage = 20
    
    for name,value in IssuesDict.items():
        
        if nbLinesCreated + len(value) + 2 > limitLignePage :
            slideId = generateId()
            with open("template/slide.template","r") as slideT :
                slide = Template(slideT.read())
            result =  slide.substitute(
                {
                    "pageId" : slideId,
                    "insertionIndex" : len(slides) - 1
                })
            body["requests"].append(json.loads(result))
        
            with open("template/textbox.template","r") as textboxT :
                textbox = Template(textboxT.read())

            result =  textbox.substitute(
                {
                    "pageId" : slideId,
                    "textboxId" : "textboxId" + str(slideId)
                })
            body["requests"].append(json.loads(result))
            nbLinesCreated = 0
        for issue in value:
            with open("template/inserttext.template","r") as text :
                text = Template(text.read())
            text2 = f"\n\t○ {issue.get('type')} -  [{issue.get('key')}] {issue.get('summary')}"
            body["requests"].append(json.loads(text.substitute(
                {
                    "element_id": f"textboxId{slideId}",
                    "text": text2,
                    "insertionIndex": 0
                }
            ),strict=False))
            body["requests"].append(highlight_word_request(text2, issue.get("type"), slideId,'color'))
            body["requests"].append(highlight_word_request(text2, f"[{issue.get('key')}]", slideId, style=None, link_url=issue.get("link")))
            nbLinesCreated += 1
        with open("template/inserttext.template","r") as text :
                text = Template(text.read())
        text2 = f"\n\n• {str(name)} :"
        body["requests"].append(json.loads(text.substitute(
        {
            "element_id": f"textboxId{slideId}",
            "text": text2,
            "insertionIndex": 0
        }
        ),strict=False))
        body["requests"].append(highlight_word_request(text2,str(name) + " :", slideId,'bold'))
        nbLinesCreated += 2
    response = service_slides.presentations() \
        .batchUpdate(presentationId=Presentation_ID, body=body).execute()
    return ("https://docs.google.com/presentation/d/"+ str(Presentation_ID))

def get_year(month: int, day: int) -> int:
    """ Returns the year of the next occurrence of a given month and day combination.

    Args:
        month (int): The month of the target date.
        day (int): The day of the target date.

    Returns:
        int: The year of the next occurrence of the specified month and day.

    Example:
        To get the year of the next occurrence of December 25th, the following function call can be made:
        
        year = get_year(12, 25)
    """
    today = datetime.date.today()
    target = datetime.date(today.year, month, day)
    if target < today:
        target = target.replace(year=today.year + 1)
    return target.year
    
def slashCommand(day: int, month: int, hour: int, minute: int) -> None:
    """ Creates a Google Slides presentation and a Google Calendar meeting for a given date and time.

    Args:
        day (int): The day of the target date.
        month (int): The month of the target date.
        hour (int): The hour of the target time.
        minute (int): The minute of the target time.

    Returns:
        None

    Example:
        To create a Google Slides presentation and a Google Calendar meeting for May 3rd, 2023 at 2:30 PM, 
        the following function call can be made:

        slashCommand(3, 5, 14, 30)
    """
    # Create the google slides
    year=int(get_year(month,day))
    url = createSlide(day,month,year)
    # Create the meeting
    Emails = GetUsersEmail()
    Emails = [i for i in Emails.values()] # Get only the emails without the IDs
    end_time = nptime(int(hour),int(minute)) + datetime.timedelta(hours=1, minutes=30)
    end_time_str = end_time.strftime("%H:%M")
    end_time_hours, end_time_minutes = end_time_str.split(":")
    CreateMeeting(year,int(month),int(day),int(hour),int(minute),int(end_time_hours),int(end_time_minutes),Emails,url)
    
    