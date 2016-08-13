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
            'body' : {'content':companions, 'contentType': 'text'},
            'isReminderOn' : reminder,
            'reminderMinutesBeforeStart' : reminderTime
            }

    #print (type(data))
    #print (str(data))
    #print (data)
    r = requests.post(url = new_event_url, json = data, headers = headers)
    if (r.status_code == requests.codes.accepted):
        return r.status_code
        r = r.json()
        print(r.json())
    else:
        return "{0}: {1}".format(r.status_code, r.text)


def listEvents(access_token, alias, title=None, startDateTime=None, attendees=None):

    filter = []
    if title is not None:
        filter.append('$filter=contains(subject, '+ title+')')
    #if startDateTime is not None:
    #    s = startDateTime
    #    filter.append('$filter=substringof('+str(s.date())+',start/dateTime)')
    if attendees is not None:
        filter.append('$filter=contains(body/content,' + attendees+')')

    sep = '&'
    filters = sep.join(filter)

    list_events_url = graph_api_endpoint.format('/Users/'+alias +'/calendar/events?$select=subject,start,body,location&' +filters )
    #print(list_events_url)
    #print(access_token)
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = list_events_url, headers = headers)
    if (r.status_code == requests.codes.ok):
        r = r.json()
        speechResp = "You have: "
        desiredEvents = []
        for events in r['value'] :
            if events['start']['dateTime'][:events['start']['dateTime'].index('T')] == str(startDateTime.date()) :
                desiredEvents.append(events)
                speechResp += events['subject'] 
                if len(events['body']['content'])>0 :
                    speechResp += " with " + events['body']['content']
                speechResp += " at " + events['start']['dateTime'][events['start']['dateTime'].index('T')+1:events['start']['dateTime'].index('T')+5]
                speechResp += ", "
        print(r)
        return speechResp
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

        toSay = ""
        self.dictOfInfo = {}
        with r['value'] as r :
            if options.get('title'):
                s = r['subject']
                toSay += "event is " + s
            if options.get('location'):
                l = r['location']
                toSay += " location is " + l
            if options.get('startDateTime'):
                dt = r['start']['dateTime']
                toSay += " date is " + 
            if options.get('attendees'):
                self.dictOfInfo['attendees'] = r['body']['content']
       
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
        data['body']['content'] = options['attendees']

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
    if options.get('title') is not None:
        filter.append('$filter=contains(subject, '+ options.get('title') +')')
    #if startDateTime is not None:
    #    s = startDateTime
    #    filter.append('$filter=substringof('+str(s.date())+',start/dateTime)')
    if options.get('attendees') is not None:
        filter.append('$filter=contains(body/content,' + options.get('attendees') +')')

    sep = '&'
    filters = sep.join(filter)


    id_event_url = graph_api_endpoint.format('/Users/'+alias +'/calendar/events/?select=id,start&' + filters)
    #print(list_events_url)
    #print(access_token)
    # Set request headers.
    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json',
    'Content-Type' : 'application/json'
    }

    r = requests.get(url = id_event_url, headers = headers)
    if (r.status_code == requests.codes.accepted):
        return r.status_code
        r = r.json()

        desiredEvents = []
        for events in r['value'] :
            if events['start']['dateTime'][:events['start']['dateTime'].index('T')] == str(startDateTime.date()) :
                desiredEvents.append(events)
             

        if  len(desiredEvents) == 1 :
            return desiredEvents['id']
        elif  len(desiredEvents) == 0 :
            raise TooFewValues()
        elif len(desiredEvents) > 1 :
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