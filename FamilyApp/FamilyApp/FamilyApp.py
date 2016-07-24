#!/usr/bin/python3


from Authorize import authorise  
from projectoxford import speech

authorise.loginProcess()

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