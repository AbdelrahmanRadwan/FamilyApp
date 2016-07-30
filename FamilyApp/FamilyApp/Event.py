import datetime
import requests
import json
import uuid

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'


def newEvent(access_token,alias, title, startDateTime, endDateTime=None , location=None, companions=None, reminder = False , notes = None):
    new_event_url = graph_api_endpoint.format('/Users/'+alias+'/calendar/events')

    
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }
    data = {"subject" : title,
            "start" : {"@odata.type": {"dateTime" : str(startDateTime), "timeZone" : "Africa/Cairo"}},
            "end" : {"@odata.type": {"dateTime" : str(endDateTime), "timeZone" : "Africa/Cairo"}},
            "location" : location,
            "attendees" : companions,
            "isReminderOn" : reminder,
            "reminderMinutesBeforeStart" : str(60)
            }

    #data = json.dumps(data)
    #print (type(data))
    #print (str(data))
    r = requests.post(url = new_event_url, data = json.dumps(data), headers = headers)
    if (r.status_code == requests.codes.accepted):
        return r.status_code
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def listEvents(access_token, alias):
    list_events_url = graph_api_endpoint.format('/me/events')
    print(list_events_url)
    print(access_token)
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = list_events_url, headers = headers)
    if (r.status_code == requests.codes.accepted):
        return r.status_code
        #r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def getEventDetailsByTitle(access_token, alias, title):
    get_event_details_url = graph_api_endpoint.format('/Users/'+alias+'/calendar/events$filter=substringof(subject,'+title+')')
        
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

def getEventDetailsByDate(access_token, alias, datetime):
    get_event_details_url = graph_api_endpoint.format("/Users/"+alias+"/calendar/events$filter=substringof(start,datetime'"+datetime+"')")
        
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


def updateEvent(access_token, alias, **options):
        #Function to identify event to be deleted using title
    update_event_url = graph_api_endpoint.format("/Users/"+alias+"/calendar/events/"+id)

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


def delete(access_token, alias, title):

    #Function to identify event to be deleted using title
    delete_event_url = graph_api_endpoint.format("/Users/"+alias+"/calendar/events/"+id)
        
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    }

    r = requests.get(url = get_event_details_url, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)
       
#def identifyEvent(alias, **options):

#       get_event_details_url = graph_api_endpoint.format("/Users/"+alias+"/calendar/events$filter=substringof(start,datetime'"+datetime+"')")
