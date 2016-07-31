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
while(1):
    inputName = input("Please enter your first name to begin. \n")
    res = input(inputName + ", is this the name you wanted? [y/n]\n" )
    if res == 'y':
        break

person = Individual(speakerKey = myHome._SPEAKER_KEY,speechKey = myHome._SPEECH_KEY, name= inputName)
person.login()

#content = "Content of the email that should be sent."
#r = Event.sendEmail(person.graphInfo.access_token, person.graphInfo.getTID, 'aliahassan95@aucegypt.edu','Tester Email', content)
#print(r)

#print("\nCreating profile.")
#person.createProfile()
#print("Profile created. " +person.speakerProfileID)

#print(person.graphInfo.user_info_json)

#person.enroll()

#if person.enrolled ==False :
#    print("Something went wrong with enrollment. Unenrolling Speaker.")

#speaker.print_all_profiles(myHome._SPEAKER_KEY)

#print("Please remain quiet while I calibrate")
#myHome.houseSpeech.calibrate_audio_recording()
#print("Done calibrating")
#myHome.houseSpeech.quiet_threshold = myHome.houseSpeech.quiet_threshold*1.1
#print("Speak now")

#wavFile = "Recordings/speakerCheck.wav"
#fileOpen = wave.open(wavFile,'w')
#fileOpen.setnchannels(1)
#fileOpen.setsampwidth(2)
#fileOpen.setframerate(16000)
#audio.record(wav=fileOpen, seconds=10, wait_for_sound = True, quiet_threshold=myHome.houseSpeech.quiet_threshold)
#print("Done recording")
#fileOpen.close()

#waveRead = open(wavFile, 'rb')
##ww = waveRead.readframes(waveRead._nframes)
##opened = wave.open( ww, 'r')
#response = myHome.houseSpeech.recognize(sec = 10, require_high_confidence = True, wav = waveRead.read())
#print ("response" + response)

#helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(myHome._SPEAKER_KEY)
#listOfProfiles = helper.get_all_profiles()
#listOfIDs =[]
#for profiles in listOfProfiles:
#    listOfIDs.append(profiles.get_profile_id())

##print(listOfIDs)

#dd = speaker.identify_file(myHome._SPEAKER_KEY, wavFile, listOfIDs)
#print("Test" , dd)


#one = Event.listEvents(person.graphInfo.access_token, person.graphInfo.getTID() )
#print(one)

two = Event.newEvent(person.graphInfo.access_token, 't-alhass@microsoft.com' ,"Test Event", startDateTime=datetime.datetime(2016,7,26,18), endDateTime=datetime.datetime(2016,7,26,19),reminder = True)
print(two)

#three = Event.listEvents(person.graphInfo.access_token, person.graphInfo.getTID() )
#print(three)


#token = r.json()

