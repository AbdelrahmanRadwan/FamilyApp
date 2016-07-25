from Authorize import authorise
from Speaker import speaker
from Speaker import EnrollmentResponse
from projectoxford import speech
from projectoxford import audio
import random

_SPEAKER_KEY = ac0e581a57e647e0a38afd0e51639a70
_SUCCESSFULL_ENROLLMENT = "succeeded"

class Individual(object):
    """description of class"""
    numOfIndividuals = 0
    random.seed()

    def __init__(self, name):
        self.name = name
        Individual.numOfIndividuals +=1

        try:
            self.speakerProfileID = speaker.create_profile(_SPEAKER_KEY,'EN-US')
        except:
            print("Error creating the speaker user profile")

    def login(self):
        try:
            userInfo =authorise.loginProcess
            self.userInfo = userInfo
        except:
            Print("Login failed")

    def enroll(self, wavFile):

        enrollmess = "Please speak the text shown on the screen."
        successfullMess = "Enrollement was successfull. "+self.name+ " now enrolled." #How can I help " + self.name +"?"
        repeatEnroll = "Enrollment was not successful. Please say the following text."
        try:
            count=0
            speech.say("Beginning enrollment.")
            speech.say(enrollmess)
            while(count<4):
                count+=1
                #Print the text that should be spoken to enroll
                print(speaker.enrollmentExcerpts[random.randint(0,speaker.enrollmentExcerpts.count-1)])
                wav = "Recordings/"+self.name+count+".wav"
                audio.record(wav,channels = 1,sample_rate = 16000,bits_per_sample=16,seconds=23,wait_for_sound=True)
                enrollRes = speaker.enroll_profile(_SPEAKER_KEY,self.speakerProfileID, wav)
                print("Waiting for enrollment results")
                print("enrollRes type:" + type(enrollRes))
                if enrollRes.get_enrollment_status == _SUCCESSFULL_ENROLLMENT :
                    say(successfullMess)
                    break
                else:
                    say(repeatEnroll)
        except: 
             Print("Enrollment failed")
