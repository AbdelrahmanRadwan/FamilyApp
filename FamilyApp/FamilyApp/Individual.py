from Authorize import authorise
from Speaker import speaker
from Speaker import EnrollmentResponse
from projectoxford import speech
from projectoxford import audio
import random
import wave
#import Todo
import Reminders

class Individual(object):
    """description of class"""

    random.seed()

    _SUCCESSFULL_ENROLLMENT = "Enrolled"

    def __init__(self,speakerKey, speechKey, name, graphInfo = None):
        self.speakerKey = speakerKey
        self.speechKey = speechKey
        self.name = name
        self.graphInfo = graphInfo
        self.enrolled = False
        self.reminders = Reminders()
        self.todoList = Todo()

        personSpeech = SpeechClient(key = speechKey, locale = 'en-US', gender='Male')

    def createProfile(self):
        try:
            self.speakerProfileID = speaker.create_profile(self.speakerKey,'EN-US')
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
                enrollRes = speaker.enroll_profile(self.speakerKey,self.speakerProfileID, wav)
                
                #print("enrollRes type:" + type(enrollRes))
                #print ( enrollRes.get_enrollment_status())
                if enrollRes.get_enrollment_status() == Individual._SUCCESSFULL_ENROLLMENT :
                    personSpeech.say(successfullMess)
                    self.enrolled = True
                    break
                elif count==3 :
                    audio.play("Recordings/enrollFail.wav")
                else:
                    audio.play("Recordings/repeatEnroll.wav")
        except: 
             print("Enrollment failed")
             audio.play("Recordings/enrollFail.wav")
