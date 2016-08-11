#!/usr/bin/python3

from Authorize import authorise  
from projectoxford import speech, audio
from Household import Household
from Individual import Individual
import Event
from Speaker import IdentificationServiceHttpClientHelper
import wave
import datetime
import LUISHandler 
import time

myHome = Household()
currentSpeaker = None
luishandler = LUISHandler.LUISHandler(myHome.dictionaryOfIndividuals,currentSpeaker)


def graphInteraction(person:Individual):

    #one = Event.listEvents(person.graphInfo.access_token, person.graphInfo.userPrincipleName)
    #print("\nListing Events\n" + one)

    startdatetime = datetime.datetime(2016,11,11,12)
    enddatetime = datetime.datetime(2016,11,11,13)


    two = Event.newEvent(person.graphInfo.access_token, person.graphInfo.userPrincipleName,"Test Event 2", startDateTime=startdatetime,endDateTime=enddatetime, reminder = True)
    print(" Adding event " + two)

    #three = Event.listEvents(person.graphInfo.access_token, person.graphInfo.userPrincipleName )
    #print("\nListing Events\n" + three)

    #content = "Content of the email that should be sent."
    #r = Event.sendEmail(person.graphInfo.access_token, person.graphInfo.userPrincipleName, 'aliahassan95@aucegypt.edu','Tester Email', content)
    #print(r)


def houseHoldEnrollmentProcess():
    firstloop = True
    while (1):
        
        #if firstloop ==True:
        #    firstloop= False
        #    audio.play("Recordings/firstEnrollPrompt.wav")
        #    response =myHome.houseSpeech.recognize(locale='en-US', require_high_confidence= True)
        #    if response.lower().find("yes")==-1 :
        #        break

        while(1):
            inputName = input("Please enter your first name to begin. \n")
            res = input(inputName + ", is this the name you wanted? [y/n]\n" )
            if res == 'y':
                break

        person = Individual(speaker = myHome.houseSpeaker,speechClient = myHome.houseSpeech, name= inputName)
        person.login()

        #graphInteraction(person)

        #print("\nCreating profile.")
        #person.createProfile()
        #print("Profile created. " +person.speakerProfileID)

        ##print(person.graphInfo.user_info_json)

        #print("Please remain quiet while I calibrate")
        #myHome.houseSpeech.calibrate_audio_recording()
        #print("Done calibrating")
        #myHome.houseSpeech.quiet_threshold = myHome.houseSpeech.quiet_threshold*1.1

        #person.enroll()

        #if person.enrolled ==False :
        #    print("Something went wrong with enrollment. Unenrolling Speaker.")
        #else:
            #myHome.addInd(person)

        ##speaker.print_all_profiles(myHome._SPEAKER_KEY)
        #audio.play("Recordings/enrollPrompt.wav")
        #response =myHome.houseSpeech.recognize(locale='en-US', require_high_confidence= True)
        #if response.lower().find("yes")==-1 :
        #    break

        myHome.addInd(person)
        global currentSpeaker
        currentSpeaker = person
        break

def checkingEnrollment():

    while(1):
        audio.play("Recordings/checkingEnrollment.wav")

        wavFile = "Recordings/speakerCheck.wav"
        fileOpen = wave.open(wavFile,'w')
        fileOpen.setnchannels(1)
        fileOpen.setsampwidth(2)
        fileOpen.setframerate(16000)
        audio.play(speech._BEEP_WAV)
        audio.record(wav=fileOpen, seconds=10, wait_for_sound = True)
        print("Done recording")
        fileOpen.close()

        waveRead = open(wavFile, 'rb')
        response = myHome.houseSpeech.recognize(require_high_confidence = True, wav = waveRead.read())
        #print ("\nResponse:" + response)

        helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(myHome._SPEAKER_KEY)
        listOfProfiles = helper.get_all_profiles()
        listOfIDs =[]
        for profiles in listOfProfiles:
            listOfIDs.append(profiles.get_profile_id())

        #print(listOfIDs)
        iden = myHome.houseSpeaker.identify_file( wavFile, listOfIDs)
        print("Identified: " , iden)
        if (myHome.dictOfSpeakerIDtoName.get(iden.get_identified_profile_id()))!= None :
            print("User: " , myHome.dictOfSpeakerIDtoName[iden.get_identified_profile_id()])
        else: 
            print("User currently not enrolled.")

        audio.play("Recordings/checkEnrollPrompt.wav")
        response =myHome.houseSpeech.recognize(locale='en-US', require_high_confidence= True)
        if response.lower().find("yes")==-1 :
            break


def howCanIHelp():

    
    listOfProfiles = myHome.houseSpeaker.get_all_profiles()
    listOfIDs =[]
    for profiles in listOfProfiles:
        listOfIDs.append(profiles.get_profile_id())

    firstloop = True
    while(1):
        if firstloop==True :
            audio.play("Recordings/howCanIHelp.wav")
            firstloop= False
        
        wavFile = "Recordings/instruction.wav"
        fileOpen = wave.open(wavFile,'w')
        fileOpen.setnchannels(1)
        fileOpen.setsampwidth(2)
        fileOpen.setframerate(16000)
        print("start speaking")
        audio.play(speech._BEEP_WAV)
        audio.record(wav=fileOpen, seconds=10, wait_for_sound = True)
        print("Done recording")
        fileOpen.close()

        waveRead = open(wavFile, 'rb')
        print(time.clock())
        response = myHome.houseSpeech.recognize(require_high_confidence = True, wav = waveRead.read())
        print(time.clock())
        print ("\nResponse:" + response)

        #print(listOfIDs)
        print(time.clock())
        iden = myHome.houseSpeaker.identify_file( wavFile, listOfIDs)
        print(time.clock())
        print("Identified: " , iden)
        if iden.get_confidence() == 'High' or 'Normal' :
            global currentSpeaker
            currentSpeaker = myHome.dictionaryOfIndividuals[ myHome.dictionaryOfSpeakerIDtoName[ iden.get_identified_profile_id() ]]
        else :
            ##handle low confidence speaker iden 
            pass
        luishandler.convo(response)

        #if (myHome.dictOfSpeakerIDtoName.get(iden.get_identified_profile_id()))!= None :
        #    user = myHome.dictOfSpeakerIDtoName.get(iden.get_identified_profile_id())
        #    print( user + " said: " +response)
        #    myHome.houseSpeech.say( user + " said: " +response)
        #else: 
        #    print("User currently not enrolled.")
        #    print("Instruction is: " +response)

        #audio.play("Recordings/needAnythingElse.wav")
        #response =myHome.houseSpeech.recognize(locale='en-US', require_high_confidence= True)
        #if response.lower().find("yes")==-1 :
        #    break
    


#token = r.json()


houseHoldEnrollmentProcess()

#checkingEnrollment()

howCanIHelp()

#graphInteraction(currentSpeaker)

#myHome.finishing()

#luisUrl = 'https://api.projectoxford.ai/luis/v1/application?id=45ddef93-d4d8-4d55-8d38-b725e908925d&subscription-key=7a80c853b5184b239d2aaf9b013e3dec&q='
#luisCl = luis.LuisClient( luisUrl)

#intent, entity ,type = luisCl.query(" book me a flight from cairo")

#print(intent)
#print(entity)
#print(type)

#text = 'add a meeting on monday the 3rd at 7 pm '



