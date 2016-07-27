from Authorize import authorise
from Speaker import speaker
from Speaker import EnrollmentResponse
from projectoxford import speech
from projectoxford import audio
import random
import wave



class Individual(object):
    """description of class"""
    numOfIndividuals = 0
    random.seed()
    _SPEAKER_KEY = 'ac0e581a57e647e0a38afd0e51639a70'
    _SUCCESSFULL_ENROLLMENT = "Enrolled"
    sp = speech.SpeechClient(key = 'e7e321f984f24f5299c185e9f2658a3b', gender='Male')

    def __init__(self, name, graphInfo = None):
        self.name = name
        self.graphInfo = graphInfo
        Individual.numOfIndividuals +=1

    def createProfile(self):
        try:
            self.speakerProfileID = speaker.create_profile(Individual._SPEAKER_KEY,'EN-US')
            print("Profile created. " )
        except:
            print("Error creating the speaker user profile")

    def login(self):
        try:
            self.graphInfo =authorise.loginProcess()
            
        except:
            Print("Login failed")

    def enroll(self):

        enrollmess = "Beginning enrollment. Please speak the text shown on the screen."
        successfullMess = "Enrollment was successfull. "+self.name+ " now enrolled." #How can I help " + self.name +"?"
        repeatEnroll = "Enrollment was not successful. Please say the following text."
        try:
            count=0
            
            audio.play("Recordings/enrollMess2.wav")
            while(count<3):
                count+=1
                #Print the text that should be spoken to enroll
                print(speaker.enrollmentExcerpts[random.randint(0,len(speaker.enrollmentExcerpts)-1)])
                wav = "Recordings/"+self.name+str(count)+".wav"
                fileOpen = wave.open(wav,'w')
                fileOpen.setnchannels(1)
                fileOpen.setsampwidth(2)
                fileOpen.setframerate(16000)
                print("\nRecording")
                audio.record(wav=fileOpen,seconds=25,wait_for_sound=True)
                print("\nDone recording")
                audio.play("Recordings/waiting.wav")
                enrollRes = speaker.enroll_profile(Individual._SPEAKER_KEY,self.speakerProfileID, wav)
                
                #print("enrollRes type:" + type(enrollRes))
                #print ( enrollRes.get_enrollment_status())
                if enrollRes.get_enrollment_status() == Individual._SUCCESSFULL_ENROLLMENT :
                    Individual.sp.say(successfullMess)
                    break
                elif count==3 :
                    audio.play("Recordings/enrollFail.wav")
                else:
                    audio.play("Recordings/repeatEnroll.wav")
        except: 
             print("Enrollment failed")
             audio.play("Recordings/enrollFail.wav")
