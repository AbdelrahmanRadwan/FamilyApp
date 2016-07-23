import datetime
import requests
import json
import uuid

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'
timeZone = "Africa/Cairo"

def createReminder(alias: str, title: str, startDateTime: datetime):
    new_reminder_url = graph_api_endpoint.format('/Users'+alias+'calendar/events')
    
    # Set request headers.
    headers = {
        'Authorization' : 'Bearer {0}'.format(access_token),
        'Content-Type' : 'application/json'
        }
        data = {
        'subject' = "Reminder"+title,
        'start' = startDateTime+timeZone,
        'isReminderOn' = True,
        'reminderMinutesBeforeStart' = 0
        }
        
        r = requests.post(url = new_reminder_url, data = data, headers = headers)
        if (r.status_code == requests.codes.accepted):
            return r.status_code
        else:
            return "{0}: {1}".format(r.status_code, r.text)

def deleteReminder():
    delete_reminder_url = graph_api_endpoint.format('/Users'+alias+'calendar/events')
    
    # Set request headers.
    headers = {
        'Authorization' : 'Bearer {0}'.format(access_token),
        'Content-Type' : 'application/json'
        }
        data = {
        'subject' = "Reminder"+title,
        'start' = startDateTime+timeZone,
        'isReminderOn' = True,
        'reminderMinutesBeforeStart' = 0
        }
        
        r = requests.post(url = new_reminder_url, data = data, headers = headers)
        if (r.status_code == requests.codes.accepted):
            return r.status_code
        else:
            return "{0}: {1}".format(r.status_code, r.text)