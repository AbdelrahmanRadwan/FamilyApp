from Individual import Individual
from ShoppingList import ShoppingList
from projectoxford.speech import SpeechClient
from projectoxford import audio
from Speaker import speaker
import pickle

class Household(object):

    _SPEAKER_KEY = '45b766d8beba484ca8acd58ba0b98492'
    _SPEECH_KEY =  'e7e321f984f24f5299c185e9f2658a3b'

    def __init__(self):
        self.shoppingList = ShoppingList()
        self.dictionaryOfIndividuals = {}
        self.houseSpeech = SpeechClient(key = Household._SPEECH_KEY, locale = 'en-US', gender='Male')
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


