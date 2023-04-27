# :rocket: Demo-Autmation :rocket:
This repository contains a Python implementation of an automation process to create Google Slides and Google Meet meetings for demos.

📂 Repository Structure

- `create_meeting.py`: A script to create a Google Meet event.
- `lambda_function.py`: The Lambda function that runs the automation process.
- `library.py`: A library containing helper functions for the automation process.

## 📝 Requirements
The following packages are required to run the automation process:

- google-auth
- google-api-python-client
- numpy
- pandas
- pytz
You also need to have a Google Cloud Platform account and enable the Google Slides and Google Calendar APIs.

## 🛠️ How to use

To use the automation process, you need to set up the following:
1. Clone this repository.
2. Set up a Google Cloud Platform project and enable the Google Slides and Google Calendar APIs.
3. Create a service account with access to the Google Slides and Google Calendar APIs, and download the JSON credentials file.
4. Set the credentials file path as an environment variable `GOOGLE_APPLICATION_CREDENTIALS`.
5. Deploy the Lambda function to your AWS account.
6. Set up a CloudWatch Events rule to trigger the Lambda function at a desired interval.

After setting up, you can run the automation process with the command:

## 📑 Files

- lambda_function.py: the main script that runs the automation process.
- library.py: contains helper functions used in the automation process.
- create_meeting.py: contains functions to create a Google Meet meeting.
- config.json: configuration file for the automation process.
- credentials.json: Google API credentials file.
- README.md: this file.

## 📝 Notes

- This project assumes that the target audience for the demo is internal employees, so access to the Google Meet event is restricted to users within the same G Suite domain.
- The `create_meeting.py` script uses the `google-auth` and `google-api-python-client` libraries, so make sure to install them before running the script.
- This project is a proof-of-concept and is not meant to be used in production environments.

## 👤 Author

- Mariem Ben Salah 
