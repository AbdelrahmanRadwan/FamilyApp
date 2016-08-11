import datetime
import requests
import json
import uuid

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'

#def dateTimeTimeZone( year, month, day, hour = 12, minute =0 , second = 0):
#    st = str(datetime.date(year, month, day)) + "T" + str(datetime.time(hour, minute, second))
#    return st 

class TooManyValues(ValueError):

    pass
    

class TooFewValues(ValueError):
    pass


def newEvent(access_token,alias, title:str, startDateTime:datetime , endDateTime:datetime=None , location=None, companions="", reminder:bool = False ,reminderTime = 60, notes = None):
    new_event_url = graph_api_endpoint.format('/Users/'+alias+'/calendar/events')

    startDateTime = str(startDateTime.date()) + "T" + str(startDateTime.time())
    
    #print ("\n" + startDateTime)
    if endDateTime is not None:
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
            #'iCalUId': str(uuid.uuid4()),
            #'location' : location,
            'itemBody' : {'content':companions, 'contentType': 'string'},
            'isReminderOn' : reminder,
            'reminderMinutesBeforeStart' : reminderTime
            }

    #print (type(data))
    #print (str(data))
    #print (data)
    r = requests.post(url = new_event_url, json = data, headers = headers)
    if (r.status_code == requests.codes.accepted):
        return r.status_code
        print(r.json())
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def listEvents(access_token, alias, title=None, startDateTime=None, attendees=None):


    list_events_url = graph_api_endpoint.format('/Users/'+alias +'/calendar/events?$select=subject,start&$filter=substringof('+title+',subject)')
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


def getEventDetails(access_token, alias,id, **options):

    get_event_details_url = graph_api_endpoint.format('/Users/'+alias+'/calendar/events/' +id)
        
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = get_event_details_url, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
        r.json()

        self.dictOfInfo = {}
        for events in r:
            if options.get('title'):
                self.dictOfInfo['title'] = r['title']
            if options.get('location'):
                self.dictOfInfo['location'] = r['location']
            if options.get('startDateTime'):
                self.dictOfInfo['startDateTime'] = r['startDateTime']
            if options.get('attendees'):
                self.dictOfInfo['attendees'] = r['itemBody']['content']
        #handle: launch thread to speak the event details
    else:
        return "{0}: {1}".format(response.status_code, response.text)



def updateEvent(access_token, alias,id, **options):
    update_event_url = graph_api_endpoint.format("/Users/"+alias+"/calendar/events/"+id)

    headers = {'Authorization' : 'Bearer {0}'.format(access_token)
                }
    data = {}

    if options.get('title'):
        data ['subject'] = options['title']
    if options.get('startDateTime'):
        data ['start'] = options['startDateTime']
    if options.get('attendees'):
        data['itemBody']['content'] = options['attendees']

    r = requests.patch(url = get_event_details_url,data = data, headers = headers)
    if (response.status_code == requests.codes.accepted):
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)


def delete(access_token, alias, id):

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
       
def identifyEvent(access_token, alias, **options):
    #filter options
    filter = []
    if options.get('title'):
        filter.append('?$filter=substringof('+options['title']+',subject)')
    if options.get('location'):
        filter.append('?$filter=substringof('+options['location']+',location)')
    if options.get('startDateTime'):
        s = datetime.datetime()
        if options['startDateTime'].date() is not None:
            s.date = options['startDateTime'].date()
        if options['startDateTime'].time() is not None:
            s.time = options['startDateTime'].time()

            filter.append('?$filter=substringof('+s.date+'T'+s.time+',start)')
        if options.get('attendees'):
            filter.append('?$filter=substringof('+options['attendees']+',itemBody/content)')

    list_events_url = graph_api_endpoint.format('/Users/'+alias +'/calendar/events/?select=id')
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
        r = r.json()
        if  len(r['value']) == 1 :
            return r['value']['id']
        elif  len(r['value']) == 0 :
            raise TooFewValues()
        elif len(r['value']) > 1 :
            raise TooManyValues(r)
    else:
        return "{0}: {1}".format(r.status_code, r.text)
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