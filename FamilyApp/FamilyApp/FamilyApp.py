#!/usr/bin/python3


from Authorize import authorise  
from projectoxford import speech
from Individual import Individual
import Event
import datetime
from Speaker import speaker

while(1):
    inputName = input("Please enter your first name to begin. \n")
    res = input(inputName + ", is this the name you wanted? [y/n]\n" )
    if res == 'y':
        break
print("\nCreating profile.")
person = Individual(inputName)
print("Profile created. " +person.speakerProfileID)

person.login()

person.enroll()

speaker.print_all_profiles()

print("speak now")
wav = "Recordings/tester.wav"
fileOpen = wave.open(wav,'w')
fileOpen.setnchannels(1)
fileOpen.setsampwidth(2)
fileOpen.setframerate(16000)
audio.record(wav=fileOpen,seconds=23, quiet_seconds=1)
print("done recording")

dd = speaker.identify_file(Individual._SPEAKER_KEY,wav, person.speakerProfileID)
print(dd)
#r = Event.newEvent(person.graphInfo.access_token, person.graphInfo.getAUD(),"Test Event", startDateTime=datetime.datetime(2016,7,26,18), endDateTime=datetime.datetime(2016,7,26,19),reminder = True)
#print(r)
#
#token = r.json()

#token = auth_helper.get_token_from_code(, 'urn:ietf:wg:oauth:2.0:oob')
 
# print ("hello world")
# testWav = "George001.wav"
# print (testWav)
# audio.play(testWav)
 
# speechCl = speech.SpeechClient(key = 'e7e321f984f24f5299c185e9f2658a3b', gender='Male')
  
# speechCl.say("Please remain quiet while I calibrate.")
# speechCl.calibrate_audio_recording()
 
# speechCl.say("Done calibrating.")

# while 1:

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