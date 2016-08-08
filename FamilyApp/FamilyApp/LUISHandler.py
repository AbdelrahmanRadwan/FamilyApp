from luis_sdk import *
from luis_client import LUISClient
from luis_response import LUISResponse
from luis_entity import LUISEntity
from projectoxford import speech, audio
import Event
import ShoppingList
import Todo
import datetime

class LUISHandler(object):

    _LUIS_APP_ID = '83c8433d-d8b8-4191-85cf-997965b21c1c'
    _LUIS_APP_SECRET = '7a80c853b5184b239d2aaf9b013e3dec'

    _SPEECH_KEY =  'e7e321f984f24f5299c185e9f2658a3b'

    SpCl = speech.SpeechClient(_SPEECH_KEY,  locale = 'en-US', gender='Male')
    LuisCl = LUISClient(_LUIS_APP_ID, _LUIS_APP_SECRET, True, True)

    callBacks = { 'AddEvent' : Event.newEvent,
                 'ListEvents' : Event.listEvents,
                 'DeleteEvent' : Event.delete,
                 'GetEventDetails' : Event.getEventDetailsByDate,
                 'ChangeEventDetails' : Event.updateEvent,
                 'AddEventDetails' : Event.updateEvent,
                 'AddReminder' : Event.updateEvent
                 }

    def __init__(self, householdInds, currentSpeaker):

        self.inds = householdInds
        self.currentSpeaker = currentSpeaker

    def convo(self, text):
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
        
                self.on_success(res, self.listOfQueries)
            else:
                LUISHandler.SpCl.say('Sorry could you phrase that more clearly')
                res =LUISHandler.SpCl.recognize(require_high_confidence = True)
                convo(res)
        except Exception as exc:
            self.on_failure(exc)

    def callAppropriateFunc(self,intName, ent, paramDict , listOfQueries):
        
        #processing alias and access_token
        if paramDict['alias'] is not None:
            access_token = inds[paramDict['alias']].graphInfo.access_token
            alias = inds[paramDict['alias']].graphInfo.access_token
        else:
            access_token = currentSpeaker.graphInfo.access_token
            alias = currentSpeaker.graphInfo.access_token

        startDateTime = datetime.datetime()

        #processing startdatetime
        if type(paramDict['startDateTime']) is str:
            startDateTime = paramDict['startDateTime']
        elif type(paramDict['startDateTime']) is list :
            if paramDict['startDateTime'][1:] == paramDict['startDateTime'][:1]:
                startDateTime = paramDict['startDateTime'][0]
            else:
                for eachdatetime in paramDict['startDateTime']:
                    if eachdatetime['date'] is not None:
                        startDateTime.date = eachdatetime['date']
                    elif eachdatetime['time'] is not None:
                        ##check this 
                        startDateTime.time = eachdatetime['time'][1:]
                if startDateTime.date() is None:
                    startDateTime.date = datetime.date.today()
                if startDateTime.time() is None:
                    startDateTime.time = datetime.time(12)

            ################################################
            #ALL THESE CALLS HAVE TO BE PUT IN THREADS
            #################################################
        if intName == 'AddEvent':
            Event.newEvent(access_token, alias, paramDict['title'],startDateTime,None,paramDict['location'],paramDict['attendees'],paramDict['reminder'],paramDict['reminderTime'])
        elif intName == 'ListEvents':
            Event.listEvents(access_token, alias, paramDict['title'], paramDict['startDateTime'], paramDict['attendees'])
        elif intName == 'CheckFree':
            Event.listEvents(access_token, alias, paramDict['title'], paramDict['startDateTime'])

        elif intName == 'AddReminder' or 'ChangeEventDetail' or 'DeleteEvent' or 'GetEventDetails':
            
            eventID = Event.identifyEvent(access_token, alias, paramDict['title'], paramDict['startDateTime'], paramDict['attendees'])

            if intName == 'DeleteEvent':
                Event.delete(access_token,alias,eventID)
            elif intName == 'AddReminder':
                Event.updateEvent(access_token, alias,eventID, reminder = True)
            elif intName == 'ChangeEventDetail' :
                Event.updateEvent(access_token, alias, eventID , paramDict['changeDateTime'], paramDict['changelocation'], paramDict['changeattendees'])
            elif intName == 'GetEventDetails':
                Event.getEventDetails(access_token, alias, eventID, paramDict['title'], paramDict['location'],paramDict['startDateTime'],paramDict['attendees'])


    def on_success(self, res:LUISResponse, listOfQueries:list):
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
    
        for eachParam in pars:
            values = eachParam.get_param_values()
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

        callAppropriateFunc(intName, ent, paramDict , listOfQueries)

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
