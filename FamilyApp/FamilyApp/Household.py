import Individual
import ShoppingList
from projectoxford.speech import SpeechClient
from projectoxford import audio
from Speaker import speaker

class Household(object):

    _SPEAKER_KEY = '45b766d8beba484ca8acd58ba0b98492'
    _SPEECH_KEY =  'e7e321f984f24f5299c185e9f2658a3b'

    def __init__(self):
        self.shoppingList = ShoppingList()
        self.dictionaryOfIndividuals = {}
        self.houseSpeech = SpeechClient(key = _SPEECH_KEY, locale = 'en-US', gender='Male')
        #houseSpeaker = spea

    def addInd(self, ind):
        dictionaryofIndividuals[ind.name] = ind

    def removeInd(self, name):
        del dictionaryOfIndividuals[name]

    def addToShopping(self, items):
        shoppingList.addItems(items)

    def removeFromShopping(self, items):
        shoppingLIst.deleteItems(items)


