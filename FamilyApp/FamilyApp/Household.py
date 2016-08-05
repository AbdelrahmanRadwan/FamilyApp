from Individual import Individual
from ShoppingList import ShoppingList
from projectoxford.speech import SpeechClient
from projectoxford import audio
from Speaker import speaker
import json
import pickle
import os

class Household(object):

    _SPEAKER_KEY = '45b766d8beba484ca8acd58ba0b98492'
    _SPEECH_KEY =  'e7e321f984f24f5299c185e9f2658a3b'
    _IND_FILEPATH = "SavedFiles/Individuals.txt"
    _IDTONAME_FILEPATH = "SavedFiles/IDtoName.txt"

    def __init__(self):
        self.shoppingList = ShoppingList()
        if os.path.exists(Household._IND_FILEPATH) and os.path.getsize(Household._IND_FILEPATH) > 0:
            indFileRead = open(Household._IND_FILEPATH, 'rb')
            self.dictionaryOfIndividuals = pickle.load(indFileRead)
            indFileRead.close()
        else:
            self.dictionaryOfIndividuals = {}

        self.houseSpeech = SpeechClient(key = Household._SPEECH_KEY, locale = 'en-US', gender='Male')
        if os.path.exists(Household._IDTONAME_FILEPATH) and os.path.getsize(Household._IDTONAME_FILEPATH) > 0:
            idFileRead = open(Household._IDTONAME_FILEPATH,'rb')
            self.dictionaryOfSpeakerIDtoName = pickle.load(idFileRead)
            idFileRead.close()
        else:
            self.dictionaryOfSpeakerIDtoName = {}
        


    def addInd(self, ind):
        self.dictionaryOfIndividuals[ind.name] = ind
        #self.dictionaryOfSpeakerIDtoName[ind.speakerProfileID] = ind.name

    def removeInd(self, name):
        del self.dictionaryOfIndividuals[name]
        del self.dictionaryOfSpeakerIDtoName[ind.speakerProfileID]

    def addToShopping(self, items):
        self.shoppingList.addItems(items)

    def removeFromShopping(self, items):
        self.shoppingLIst.deleteItems(items)

    def finishing(self):
        try:
            indFileWrite =  open(Household._IND_FILEPATH, 'wb')
            #for inds in self.dictionaryOfIndividuals :
            
            pickle.dump(self.dictionaryOfIndividuals,indFileWrite, pickle.HIGHEST_PROTOCOL)
            indFileWrite.close()
        except:
            print("Couldn't write individual json's to file")

        try:
            idFileWrite =  open(Household._IDTONAME_FILEPATH, 'wb')
            #for ids in self.dictionaryOfSpeakerIDtoName :
            pickle.dump(self.dictionaryOfSpeakerIDtoName,idFileWrite, pickle.HIGHEST_PROTOCOL)
            idFileWrite.close()
        except:
            print("Couldn't write id json's to file")

        self.shoppingList.finishing()