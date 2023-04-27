import json
from library import slashCommand
import base64
from urllib import parse as urlparse

def process_slash_command(body):
    parsed_body = dict(urlparse.parse_qsl(base64.b64decode(str(body)).decode("ascii")))
    url = parsed_body["response_url"]
    if 'text' in parsed_body :
        text = parsed_body['text']
        day, month = map(int, text.split()[0].split('.'))
        hour = text.split()[1].split(':')[0]
        minute = text.split()[1].split(':')[1] if len(text.split()[1].split(':')) == 2 else 0
        slashCommand(day,month,int(hour),int(minute))

def lambda_handler(event, context):
    # If the lambda is trigered by a slash command
    if "body" in event:
        process_slash_command(event["body"])

        return {
            'statusCode': 200
        }
