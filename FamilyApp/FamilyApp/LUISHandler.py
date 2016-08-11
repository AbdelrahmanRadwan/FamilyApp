from luis_sdk import *
from luis_client import LUISClient
from luis_response import LUISResponse
from luis_entity import LUISEntity
from projectoxford import speech, audio
import Event
import ShoppingList
import Todo
import datetime
import Individual


class LUISHandler(object):

    #Familia
    _LUIS_APP_ID = '064067b9-a41f-476c-9d82-9fbb115fcf88'
    _LUIS_APP_SECRET = '3a1943947f00483ab502d6cae5e15198'

    _SPEECH_KEY =  'e7e321f984f24f5299c185e9f2658a3b'

    SpCl = speech.SpeechClient(_SPEECH_KEY,  locale = 'en-US', gender='Male')
    LuisCl = LUISClient(_LUIS_APP_ID, _LUIS_APP_SECRET, True, True)

    callBacks = { 'AddEvent' : Event.newEvent,
                 'ListEvents' : Event.listEvents,
                 'DeleteEvent' : Event.delete,
                 'GetEventDetails' : Event.getEventDetails,
                 'ChangeEventDetails' : Event.updateEvent,
                 'AddEventDetails' : Event.updateEvent,
                 'AddReminder' : Event.updateEvent
                 }

    def __init__(self, householdInds, currentSpeaker:Individual):

        self.inds = householdInds
        self.currentSpeaker = currentSpeaker

    def convo(self, text, currentSpeaker:Individual):
        self.listOfQueries =[text]
        try :
            res = LUISHandler.LuisCl.predict_sync(text)
   
            if res.get_top_intent().get_score() >0.7:
                if res.get_dialog() is not None :
                    while not res.get_dialog().is_finished():
                        print(res.get_dialog().get_status())
                        LUISHandler.SpCl.say( res.get_dialog().get_prompt())
                        audio.play(speech._BEEP_WAV)
                        try:
                            answer = LUISHandler.SpCl.recognize(require_high_confidence = True)
                        except speech.LowConfidenceError or ValueError:
                            LUISHandler.SpCl.say('Sorry could you say that more clearly')
                            answer =LUISHandler.SpCl.recognize(require_high_confidence = True)
                            self.listOfQueries.append(answer)

                        res = LUISHandler.LuisCl.reply(answer, res)
        
                self.on_success(res, self.listOfQueries, currentSpeaker)
            else:
                LUISHandler.SpCl.say('Sorry could you phrase that more clearly')
                res =LUISHandler.SpCl.recognize(require_high_confidence = True)
                convo(res)
        except Exception as exc:
            self.on_failure(exc)

    def processDateTime(self, input):
        #processing startdatetime

        ###################################################
        #HAVENT PROCESS IF IT'S A WEEK AS A WHOLE OR A MONTH ETC
        ###################################################
        self.startDateTime = datetime.datetime.now()
        if type(input) is dict:
            if 'date' in input.keys() :
                date = input['date']
                date = date.replace('XXXX',str(datetime.date.today().year))
                if int(date[-2:]) > datetime.date.today().day :
                    date = date.replace('XX',str(datetime.date.today().month))
                else:
                    date = date.replace('XX',str(datetime.date.today().month+1))
                self.startDateTime = datetime.datetime.strptime( date, '%Y-%m-%d')
                self.startDateTime.replace(hour = 12)
            elif 'time' in input.keys() :
                self.startDateTime.date = datetime.date.today()
                time = split(input['time'],':')
                self.startDateTime.replace(hour = time[0], minute = time[1], second = time[2])

        elif type(input) is list :
            if input[1:] == input[:1]:
                date = input[0]
                date = date.replace('XXXX',str(datetime.date.today().year))
                if int(date[-2:]) > datetime.date.today().day :
                    date = date.replace('XX',str(datetime.date.today().month))
                else:
                    date = date.replace('XX',str(datetime.date.today().month+1))
                dt = split(input[0], '-: ')
                self.startDateTime = datetime.datetime(dt[0], dt[1], dt[2],dt[3],dt[4])
            else:
                for eachdatetime in input:
                    if eachdatetime['date'] is not None:
                        date = eachdatetime['date']
                        date = date.replace('XXXX',str(datetime.date.today().year))
                        if int(date[-2:]) > datetime.date.today().day :
                            date = date.replace('XX',str(datetime.date.today().month))
                        else:
                            date = date.replace('XX',str(datetime.date.today().month+1))
                        self.startDateTime.date = datetime.datetime.strptime(date)
                    elif eachdatetime['time'] is not None:
                        ##check this 
                        self.startDateTime.time = eachdatetime['time'][1:]

                if self.startDateTime.date() is None:
                    self.startDateTime = datetime.date.today()
                if self.startDateTime.time() is None:
                    self.startDateTime.replace(hour = 12)

        return self.startDateTime

    def callAppropriateFunc(self,intName, ent, paramDict , listOfQueries, currentSpeaker:Individual):
        
        #processing alias and access_token
        if 'alias' in paramDict.keys() :
            access_token = inds[paramDict['alias']].graphInfo.access_token
            alias = inds[paramDict['alias']].graphInfo.id
        else:
            access_token = currentSpeaker.graphInfo.access_token
            alias = currentSpeaker.graphInfo.id

        startDateTime = self.processDateTime(paramDict['datetime'])
        endDateTime = startDateTime +datetime.timedelta(0,0,0,0,0,1,0)

        loc = paramDict['location'] if 'location' in paramDict.keys() else None
        atten = paramDict['attendees'] if 'attendees' in paramDict.keys() else None
        rem = paramDict['reminder'] if 'reminder' in paramDict.keys() else None
        remtime = paramDict['reminderTime'] if 'reminderTime' in paramDict.keys() else None

            ################################################
            #ALL THESE CALLS HAVE TO BE PUT IN THREADS
            #################################################
        if intName == 'AddEvent':
            try:
                r = Event.newEvent(access_token = access_token, 
                               alias = alias, 
                               title = paramDict['title'],
                               startDateTime = startDateTime,
                               endDateTime = endDateTime,
                               location = loc,
                               companions =  atten,
                               reminder = rem,
                               reminderTime = remtime)
                print(r)
            except Exception as exc:
                print (exc)

        elif intName == 'ListEvents':
            Event.listEvents(access_token, alias, paramDict['title'], startDateTime, atten)
        elif intName == 'CheckFree':
            Event.listEvents(access_token, alias, paramDict['title'], startDateTime)

        elif intName == 'AddReminder' or 'ChangeEventDetail' or 'DeleteEvent' or 'GetEventDetails':
            
            try :
                eventID = Event.identifyEvent(access_token, alias, paramDict['title'], paramDict['startDateTime'], paramDict['attendees'])
            except Event.TooFewValues as exc:
                print(exc)
                pass
            except Event.TooManyValues as exc:
                print(exc)
                pass

            if intName == 'DeleteEvent':
                Event.delete(access_token,alias,eventID)
            elif intName == 'AddReminder':
                Event.updateEvent(access_token, alias,eventID, reminder = True)
            elif intName == 'ChangeEventDetail' :
                Event.updateEvent(access_token, alias, eventID , paramDict['changeDateTime'], paramDict['changelocation'], paramDict['changeattendees'])
            elif intName == 'GetEventDetails':
                Event.getEventDetails(access_token, alias, eventID, paramDict['title'], paramDict['location'],paramDict['startDateTime'],paramDict['attendees'])


    def on_success(self, res:LUISResponse, listOfQueries:list, currentSpeaker:Individual):
        '''
        A callback function that processes the luis_response object
        if the prediction succeeds.
        :param res: a luis_response object containing the response data.
        :return: None
        '''
        intName  = res.get_top_intent().get_name()
        ent = res.get_entities()
        if res.get_top_intent().get_actions() is not None:
            pars = res.get_top_intent().get_actions()[0].get_parameters()
    
        paramDict = {}
        for eachParam in pars:
            values = eachParam.get_parameter_values()
            if len(values) == 1 :
               if 'builtin.datetime' in values[0].get_type():
                    paramDict[eachParam.get_name()] = values[0].get_resolution()
                    #if 'date' in values[0].get_resolution():
                    #    paramDict[eachParam.get_name()] = values[0].get_resolution()['date']
                    #elif 'time' in values[0].get_resolution():
                    #    paramDict[eachParam.get_name()] = values[0].get_resolution()['time']
                    #elif 'duration' in values[0].get_resolution():
                    #    paramDict[eachParam.get_name()] = values[0].get_resolution()['duration']
               else:
                    paramDict[eachParam.get_name()] = values[0].get_name()
            elif len(values) >1:
                listOfVals = []
                for eachVal in values :
                    if 'builtin.datetime' in eachVal.get_type():
                        listOfVals.append(eachVal.get_resolution())
                        #if 'date' in eachVal.get_resolution():
                        #    listOfVals.append(eachVal.get_resolution()['date'])
                        #elif 'time' in eachVal.get_resolution():
                        #    listOfVals.append(eachVal.get_resolution()['time'])
                        #elif 'duration' in eachVal.get_resolution():
                        #    listOfVals.append(eachVal.get_resolution()['duration'])
                else:
                    listOfVals.append(eachVal.get_name())
                paramDict[eachParam.get_name()] = listOfVals 

        self.callAppropriateFunc(intName, ent, paramDict , listOfQueries, currentSpeaker)

    def on_failure(self, err):
        '''
        A callback function that processes the error object
        if the prediction fails.
        :param err: An Exception object.
        :return: None
        '''
        print(err)
        try:
            SpCl.say("Sorry something went wrong")
        except:
            audio.play("Recordings/internetError.wav")
