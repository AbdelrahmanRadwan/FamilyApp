import datetime
import requests
import json
import uuid

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'

def createCalendar(alias)
    new_calendar_url = graph_api_endpoint.format('/Users'+alias+'/calendars')
        
        # Set request headers.
        headers = {
        'Authorization' : 'Bearer {0}'.format(access_token),
        'Content-Type' : 'application/json'
        }
        data = {
        'name' = 'default'
        }

        r = requests.post(url = new_calendar_url, data = data, headers = headers)
        if (r.status_code == requests.codes.accepted):
            return r.status_code
        else:
            return "{0}: {1}".format(r.status_code, r.text)

