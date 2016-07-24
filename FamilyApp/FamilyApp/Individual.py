from Authorize import authorise
from Speaker import speaker
from Speaker import EnrollmentResponse
from projectoxford import speech
from projectoxford import audio
_SPEAKER_KEY = ac0e581a57e647e0a38afd0e51639a70

class Individual(object):
    """description of class"""
    numOfIndividuals = 0

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
        try:
            count=0
            speech.say("Beginning enrollment.")
            while(count<4):
                enrollmess = "Please speak the sentence shown on the screen."
                speech.say(enrollmess)
                audio.record(
                enrollRes = speaker.enroll_profile(_SPEAKER_KEY,speakerProfileID, wavFile)
                enrollRes.get_enrollment_status()

        except: 
             Print("Enrollment failed")
