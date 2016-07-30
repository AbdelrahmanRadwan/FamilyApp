#!/usr/bin/python3


from Authorize import authorise  
from projectoxford import speech, audio
from Household import Household
from Individual import Individual
import Event
from Speaker import speaker, IdentificationServiceHttpClientHelper
import wave


myHome = Household()
#while(1):
#    inputName = input("Please enter your first name to begin. \n")
#    res = input(inputName + ", is this the name you wanted? [y/n]\n" )
#    if res == 'y':
#        break

#person = Individual(speakerKey = myHome._SPEAKER_KEY,speechKey = myHome._SPEECH_KEY, name= inputName)
#person.login()

#print("\nCreating profile.")
#person.createProfile()
#print("Profile created. " +person.speakerProfileID)

#print(person.graphInfo.user_info_json)

##print("Please remain quiet while I calibrate")
##sp.calibrate_audio_recording()
##print("Done calibrating")

#person.enroll()

#if person.enrolled ==False :
#    print("Something went wrong with enrollment. Unenrolling Speaker.")

#speaker.print_all_profiles(myHome._SPEAKER_KEY)
print("Please remain quiet while I calibrate")
myHome.houseSpeech.calibrate_audio_recording()
print("Done calibrating")
myHome.houseSpeech.quiet_threshold = myHome.houseSpeech.quiet_threshold*1.1
print("Speak now")

response, wavFile = myHome.houseSpeech.recognize(sec = 10, require_high_confidence = True)
#wavFile = "Recordings/testing.wav"
#fileOpen = wave.open(wavFile,'w')
#fileOpen.setnchannels(1)
#fileOpen.setsampwidth(2)
#fileOpen.setframerate(16000)

#audio.record(wav=fileOpen, seconds=10, wait_for_sound = True, quiet_threshold=myHome.houseSpeech.quiet_threshold)
print("Done recording")

helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(myHome._SPEAKER_KEY)
listOfProfiles = helper.get_all_profiles()
listOfIDs =[]
for profiles in listOfProfiles:
    listOfIDs.append(profiles.get_profile_id())

#print(listOfIDs)

dd = speaker.identify_file(myHome._SPEAKER_KEY, wavFile, listOfIDs)
print("Test" , dd)

#r = Event.listEvents(person.graphInfo.access_token, person.graphInfo.getTID() )
##r = Event.newEvent(person.graphInfo.access_token, person.graphInfo.getAUD(),"Test Event", startDateTime=datetime.datetime(2016,7,26,18), endDateTime=datetime.datetime(2016,7,26,19),reminder = True)
#print(r)
#
#token = r.json()

#token = auth_helper.get_token_from_code(, 'urn:ietf:wg:oauth:2.0:oob')
 
# print ("hello world")
# testWav = "George001.wav"
# print (testWav)
# audio.play(testWav)
 
#speechCl = speech.SpeechClient(key = 'e7e321f984f24f5299c185e9f2658a3b', gender='Male')
  
#speechCl.say("Please remain quiet while I calibrate.")
#speechCl.calibrate_audio_recording()
 
#speechCl.say("Done calibrating.")

#while True:

#     try:
# 		#conversation instantiated and started until user is done.
#         speechCl.say("How can I help?")
#         response = speechCl.recognize( locale='en-US', require_high_confidence= True)
#         if response.lower().find("done")!=-1:
#             speechCl.say("Happy to help.")
#             break
#         else:
#             speechCl.say(response)
#     except speech.LowConfidenceError:
#         print("I couldn't understand what you said I'm sorry")