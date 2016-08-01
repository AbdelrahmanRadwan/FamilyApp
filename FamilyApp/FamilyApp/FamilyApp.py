#!/usr/bin/python3

from Authorize import authorise  
from projectoxford import speech, audio 
from Household import Household
from Individual import Individual
import Event
from Speaker import speaker, IdentificationServiceHttpClientHelper
import wave
import datetime

myHome = Household()

def houseHoldEnrollmentProcess():
    while (1):
        while(1):
            inputName = input("Please enter your first name to begin. \n")
            res = input(inputName + ", is this the name you wanted? [y/n]\n" )
            if res == 'y':
                break

        person = Individual(speakerKey = myHome._SPEAKER_KEY,speechClient = myHome.houseSpeech, name= inputName)
        person.login()

        myHome.addInd(person)
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

        #speaker.print_all_profiles(myHome._SPEAKER_KEY)
        audio.play("Recordings/enrollPrompt.wav")
        response =myHome.houseSpeech.recognize(locale='en-US', require_high_confidence= True)
        if response.lower().find("yes")==-1 :
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
        print ("\nResponse:" + response)

        helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(myHome._SPEAKER_KEY)
        listOfProfiles = helper.get_all_profiles()
        listOfIDs =[]
        for profiles in listOfProfiles:
            listOfIDs.append(profiles.get_profile_id())

        #print(listOfIDs)
        iden = speaker.identify_file(myHome._SPEAKER_KEY, wavFile, listOfIDs)
        print("Identified: " , iden)
        print("User: " , myHome.dictOfSpeakerIDtoName[iden.get_identified_profile_id()])

        audio.play("Recordings/checkEnrollPrompt.wav")
        response =myHome.houseSpeech.recognize(locale='en-US', require_high_confidence= True)
        if response.lower().find("yes")==-1 :
            break


def graphInteraction():
    one = Event.listEvents(myHome.dictionaryOfIndividuals["Alia"].graphInfo.access_token, 't-alhass@microsoft.com' )
    print(one)

    startdatetime = Event.dateTimeTimeZone(2016,8,1,13,30,0)
    enddatetime = Event.dateTimeTimeZone(2016,8,1,14,30,0)

    two = Event.newEvent(myHome.dictionaryOfIndividuals["Alia"].graphInfo.access_token, 't-alhass@microsoft.com' ,"Test Event", startDateTime=startdatetime, endDateTime=enddatetime,reminder = True)
    print(two)

    three = Event.listEvents(myHome.dictionaryOfIndividuals["Alia"].graphInfo.access_token, 't-alhass@microsoft.com' )
    print(three)

    content = "Content of the email that should be sent."
    r = Event.sendEmail(myHome.dictionaryOfIndividuals["Alia"].graphInfo.access_token,'t-alhass@microsoft.com', 'aliahassan95@aucegypt.edu','Tester Email', content)
    print(r)

#token = r.json()



#houseHoldEnrollmentProcess()

checkingEnrollment()

#graphInteraction()