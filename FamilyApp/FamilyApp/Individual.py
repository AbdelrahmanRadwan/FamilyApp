from Authorize import authorise
from Speaker import speaker
from Speaker import EnrollmentResponse
from projectoxford import speech
from projectoxford import audio
import random
import wave

_SPEAKER_KEY = 'ac0e581a57e647e0a38afd0e51639a70'
_SUCCESSFULL_ENROLLMENT = "succeeded"
sp = speech.SpeechClient(key = 'e7e321f984f24f5299c185e9f2658a3b', gender='Male')

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

    def enroll(self):

        enrollmess = "Please speak the text shown on the screen."
        successfullMess = "Enrollement was successfull. "+self.name+ " now enrolled." #How can I help " + self.name +"?"
        repeatEnroll = "Enrollment was not successful. Please say the following text."
        try:
            count=0
            sp.say("Beginning enrollment.")
            sp.say(enrollmess)
            while(count<4):
                count+=1
                #Print the text that should be spoken to enroll
                print(speaker.enrollmentExcerpts[random.randint(0,len(speaker.enrollmentExcerpts)-1)])
                wav = "Recordings/"+self.name+str(count)+".wav"
                fileOpen = wave.open(wav,'w')
                fileOpen.setnchannels(1)
                fileOpen.setsampwidth(2)
                fileOpen.setframerate(16000)
                audio.record(wav=fileOpen,seconds=23, quiet_seconds=1)
                print("done recording")
                enrollRes = speaker.enroll_profile(_SPEAKER_KEY,self.speakerProfileID, wav)
                print("Waiting for enrollment results")
                #print("enrollRes type:" + type(enrollRes))
                if enrollRes.get_enrollment_status == _SUCCESSFULL_ENROLLMENT :
                    sp.say(successfullMess)
                    break
                else:
                    sp.say(repeatEnroll)
        except: 
             print("Enrollment failed")
