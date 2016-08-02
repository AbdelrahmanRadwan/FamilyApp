import datetime
import requests
import json
import uuid

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'

#def dateTimeTimeZone( year, month, day, hour = 12, minute =0 , second = 0):
#    st = str(datetime.date(year, month, day)) + "T" + str(datetime.time(hour, minute, second))
#    return st 

def newEvent(access_token,alias, title:str, startDateTime:datetime , endDateTime:datetime=None , location=None, companions=None, reminder:bool = False , notes = None):
    new_event_url = graph_api_endpoint.format('/Users/'+alias+'/calendar/events')

    startDateTime = str(startDateTime.date()) + "T" + str(startDateTime.time())
    #print ("\n" + startDateTime)
    endDateTime = str(endDateTime.date()) + "T" + str(endDateTime.time())

    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }
    data = {
            'subject' : title,
            'start' : {'dateTime' : startDateTime, 'timeZone' : 'Africa/Cairo'},
            'end' : {'dateTime' : endDateTime, 'timeZone' : 'Africa/Cairo'},
            #'originalEndTimeZone' : 'Africa/Cairo',
            #'originalStartTimeZone' : 'Africa/Cairo',
            #'responseStatus': {'response': 'Accepted', 'time': '2016-08-03T08:16:00Z'},
            'iCalUId': str(uuid.uuid4()),
            #'location' : location,
            #'attendees' : companions,
            'isReminderOn' : reminder,
            'reminderMinutesBeforeStart' : 60
            }

    #print (type(data))
    #print (str(data))
    #print (data)
    r = requests.post(url = new_event_url, json = data, headers = headers)
    if (r.status_code == requests.codes.accepted):
        return r.status_code
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def listEvents(access_token, alias):
    list_events_url = graph_api_endpoint.format('/Users/'+alias +'/calendar/events?$select=subject,start,end')
    #print(list_events_url)
    #print(access_token)
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
    data = {}

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

def sendEmail(access_token, alias, emailAddress, subject, content):
	# The resource URL for the sendMail action.
  send_mail_url = graph_api_endpoint.format('/Users/' +alias+ '/microsoft.graph.sendMail')	
	# Set request headers.
  headers = { 
		'User-Agent' : 'python_tutorial/1.0',
		'Authorization' : 'Bearer {0}'.format(access_token),
		'Accept' : 'application/json',
		'Content-Type' : 'application/json'
	}						
	# Use these headers to instrument calls. Makes it easier
	# to correlate requests and responses in case of problems
	# and is a recommended best practice.
  request_id = str(uuid.uuid4())
  instrumentation = { 
		'client-request-id' : request_id,
		'return-client-request-id' : 'true' 
	}
  headers.update(instrumentation)

	# Create the email that is to be sent with API.
  email = {
		'Message': {
			'Subject': subject,
			'Body': {
				'ContentType': 'HTML',
				'Content': content
			},
			'ToRecipients': [
				{
					'EmailAddress': {
						'Address': emailAddress
					}
				}
			]
		},
		'SaveToSentItems': 'true'
	}   

  response = requests.post(url = send_mail_url, headers = headers, data = json.dumps(email), params = None)

	# Check if the response is 202 (success) or not (failure).
  if (response.status_code == requests.codes.accepted):
    return response.status_code
  else:
    return "{0}: {1}".format(response.status_code, response.text)