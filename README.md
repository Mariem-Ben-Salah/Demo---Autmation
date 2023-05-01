# :rocket: Demo-Automation :rocket:
This repository contains a Python implementation of an automation process to create Google Slides and Google Meet meetings for demos.

![Build Status](https://img.shields.io/travis/Mariem-Ben-Salah/Demo-Automation.svg)  ![Coverage Status](https://img.shields.io/coveralls/Mariem-Ben-Salah/Demo-Automation.svg)
[![Build Status](https://travis-ci.com/Mariem-Ben-Salah/Demo-Automation.svg)](https://travis-ci.com/Mariem-Ben-Salah/Demo-Automation)


## 🤖 Introduction

The demo is a process that typically occurs once a month. During this meeting, team members and product owners showcase what they've been working on during the previous period. Despite its simplicity, this process can sometimes take up a significant amount of time on the agenda, which is why we have decided to automate it.

## 📂 Repository Structure

- `create_meeting.py`: contains functions to create a Google Meet meeting.
- `lambda_function.py`: the main script that runs the automation process.
- `library.py`: contains helper functions for the automation process.
- `Template` : A folder containg all the _.template_ files required for the Google Slides creation.
- `requirements.txt`: a file contaning all the neccessary packages to upload to Lambda.
- `README.me`: this file.

## 📝 Requirements

The packages required to run the automation process can be found in _requirements.txt _

You also need to have a Google Cloud Platform account and enable the Google Slides and Google Calendar APIs.

## 🛠️ How to use

To use the automation process, you need to set up the following:
1. Clone this repository.
2. Set up a Google Cloud Platform project and enable the Google Slides and Google Calendar APIs.
3. Create a service account with access to the Google Slides and Google Calendar APIs, and download the JSON credentials file.
4. Run those commands for the _requirement.txt_ `pip3 install --upgrade -r requirements.txt --target python/lib/python3.8/site-packages/` and `zip -r -9 dependencies.zip python`
5. Add _dependencies.zip_ as a lambda layer
6. Deploy the Lambda function to your AWS account.
7. Check the \# TO DO
8. Add an _API Gateway_ as a trigger to your Lambda.
9. Create your Bot/App on https://api.slack.com/apps 
10. Add the required bot and user scopes (channels:read, groups:read, im:read, mpim:read, users:read, users:read.email)
11. Install the bot to your workspace
12. Add the bot to the wanted channels
13. Set up a Slash Command to trigger the Lambda function when wanted.

After setting up, you can run the automation process with the command: <span style="color:red">/demo DD.MM HH:SS</span>

* The MM field is mandatory. The default value is 00
* The start time of the meeting is HH:SS
* The end time of the meeting is start time + 1h30  

For Example : 
  - <span style="color:red">/demo 24.4 17:35 :</span> Plan the demo for 24th April At 17:35
  - <span style="color:red">/demo 6.4 9 :</span> Plan the demo for 6th April at 9 am


## 📝 Notes

- This project assumes that the target audience for the demo is internal employees, so access to the Google Meet event is restricted to users within the same G Suite domain.
- The `create_meeting.py` script uses the `google-auth` and `google-api-python-client` libraries, so make sure to install them before running the script.

## 👤 Author

- Mariem Ben Salah 
