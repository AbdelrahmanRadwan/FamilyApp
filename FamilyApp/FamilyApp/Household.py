from Individual import Individual
from ShoppingList import ShoppingList
from projectoxford.speech import SpeechClient
from projectoxford import audio
from Speaker import speaker
import pickle
import os

class Household(object):

    _SPEAKER_KEY = '45b766d8beba484ca8acd58ba0b98492'
    _SPEECH_KEY =  'e7e321f984f24f5299c185e9f2658a3b'

    def __init__(self):
        self.shoppingList = ShoppingList()
        if os.path.exists("SavedFiles/Individuals.p") and os.path.getsize("SavedFiles/Individuals.p") > 0:
            self.dictionaryOfIndividuals = pickle.load(open("SavedFiles/Individuals.p",'rb'))
        else:
            self.dictionaryOfIndividuals = {}
        self.houseSpeech = SpeechClient(key = Household._SPEECH_KEY, locale = 'en-US', gender='Male')
        if os.path.exists("SavedFiles/IDtoName.p") and os.path.getsize("SavedFiles/IDtoName.p") > 0:
            self.dictOfSpeakerIDtoName =  pickle.load(open("SavedFiles/IDtoName.p", 'rb'))
        else:
            self.dictOfSpeakerIDtoName = {}

    def addInd(self, ind):
        self.dictionaryOfIndividuals[ind.name] = ind
        self.dictOfSpeakerIDtoName[ind.speakerProfileID] = ind.name

    def removeInd(self, name):
        del self.dictionaryOfIndividuals[name]
        del  self.dictOfSpeakerIDtoName[ind.speakerProfileID]

    def addToShopping(self, items):
        self.shoppingList.addItems(items)

    def removeFromShopping(self, items):
        self.shoppingLIst.deleteItems(items)

    def finishing(self):
        pickle.dump(self.dictionaryOfIndividuals,open("SavedFiles/Individuals.txt",'wb'))
        pickle.dump(self.dictOfSpeakerIDtoName, open("SavedFiles/IDtoName.txt", 'wb'))
