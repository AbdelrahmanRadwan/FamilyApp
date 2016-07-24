import datetime
import requests
import json
import uuid

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'


def newEvent(alias, title, startDateTime, endDateTime , location, companions, reminder = False , notes = None):
    new_event_url = graph_api_endpoint.format('/Users'+alias+'/events')

    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }
    data = {'subject' : title,
            'start' : startDateTime,
            'end' : endDateTime,
            'location' : location,
            'attendees' : companions,
            'isReminderOn' : reminder,
            'reminderMinutesBeforeStart' : 60
            }

    r = requests.post(url = new_event_url, data = data, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)


def listEvents( alias):
    list_events_url = graph_api_endpoint.format('/Users'+alias+'/calendar/events$top=5')

    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = list_events_url, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
        #r.json()
    else:
        return "{0}: {1}".format(response.status_code, response.text)


def getEventDetailsByTitle( alias, title):
    get_event_details_url = graph_api_endpoint.format('/Users'+alias+'/calendar/events$filter=substringof(subject,'+title+')')
        
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = get_event_details_url, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
        #r.json()
        #handle: launch thread to speak the event details
    else:
        return "{0}: {1}".format(response.status_code, response.text)

def getEventDetailsByDate( alias, datetime):
    get_event_details_url = graph_api_endpoint.format("/Users"+alias+"/calendar/events$filter=substringof(start,datetime'"+datetime+"')")
        
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = get_event_details_url, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
        #r.json()
        #handle: launch thread to speak the event details
    else:
        return "{0}: {1}".format(response.status_code, response.text)


def updateEvent( alias, **options):
        #Function to identify event to be deleted using title
    update_event_url = graph_api_endpoint.format("/Users"+alias+"/calendar/events/"+id)

    headers = {'Authorization' : 'Bearer {0}'.format(access_token)
                }

    if options.get('title'):
        data ['subject'] = options['title']
    if options.get('startDateTime'):
        data ['start'] = options['startDateTime']
    if options.get('reminder'):
        data ['isReminderOn'] = options['reminder']
    if options.get('reminderTime'):
        data ['reminderMinutesBeforeStart'] = options['reminderTime']
    if options.get('endDateTime'):
        data ['end'] = options['endDateTime']

    r = requests.patch(url = get_event_details_url,data = data, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)


def delete( alias, title):

    #Function to identify event to be deleted using title
    delete_event_url = graph_api_endpoint.format("/Users"+alias+"/calendar/events/"+id)
        
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    }

    r = requests.get(url = get_event_details_url, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)
       
def identifyEvent(alias, **options):

       get_event_details_url = graph_api_endpoint.format("/Users"+alias+"/calendar/events$filter=substringof(start,datetime'"+datetime+"')")
