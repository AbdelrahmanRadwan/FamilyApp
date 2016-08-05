import os 
import pickle 
import audio
import speech

class Item(object):

     def __init__(self, name, quantity = 1):
        self.name = name 
        self.quantity = quantity

class ShoppingList(object):
    """description of class"""

    _SHOPPING_FILEPATH = "SavedFiles/Shopping.txt"


    def __init__(self):

        self.shopping = []
        if os.path.exists(ShoppingList._SHOPPING_FILEPATH) and os.path.getsize(ShoppingList._SHOPPING_FILEPATH) > 0:
            shopFileRead = open(ShoppingList._SHOPPING_FILEPATH, 'rb')
            self.shopping = pickle.load(shopFileRead)
            shopFileRead.close()

    def checkIfOnList(self, Item):
        for items in self.shopping :
            if items.name == Item.name :
                return self.shopping.index(items)
            else :
                return -1

    def addItems(self, itemList:list ):
        for items in itemList:
            ind = self.checkIfOnList(items)
            if ind != -1:
                self.shopping[ind].quantity +=items.quantity 
            else:
                self.shopping.append(items)

    def deleteItems(self, itemList:list):
        for names in itemList:
            for inList in self.shopping :
                if names == inList.name :
                    self.shopping.remove(inList)


    def clearList(self):
        self.shopping.clear()

    def deleteList(self):
        del self

    def finishing(self):
        try:
            shopFileWrite =  open(ShoppingList._SHOPPING_FILEPATH, 'wb')
           
            pickle.dump(self.shopping,shopFileWrite, pickle.HIGHEST_PROTOCOL)
            shopFileWrite.close()
        except Exception as exc:
            print(exc)

        ######################################
    def emailList(self, access_token, alias):

        it = ""
        for items in shopping.shopping:
            it += (str(items.quantity) + " " + items.name + "\n")
        graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'
        send_mail_url = graph_api_endpoint.format('/Users/' +alias+ '/microsoft.graph.sendMail')	
	# Set request headers.
        headers = { 
		'User-Agent' : 'python_tutorial/1.0',
		'Authorization' : 'Bearer {0}'.format(access_token),
		'Accept' : 'application/json',
		'Content-Type' : 'application/json'
	    }						
	    # Use these headers to instrument calls. Makes it easier
	    # to correlate requests and responses in case of problems
	    # and is a recommended best practice.
        request_id = str(uuid.uuid4())
        instrumentation = { 
		    'client-request-id' : request_id,
		    'return-client-request-id' : 'true' 
	    }
        headers.update(instrumentation)

	    # Create the email that is to be sent with API.
        email = {
		    'Message': {
			    'Subject': 'Shopping List',
			    'Body': {
				    'ContentType': 'HTML',
				    'Content': it
			    },
			    'ToRecipients': [
				    {
					    'EmailAddress': {
						    'Address': emailAddress
					    }
				    }
			    ]
		    },
		    'SaveToSentItems': 'true'
	    }   

        response = requests.post(url = send_mail_url, headers = headers, data = json.dumps(email), params = None)

	    # Check if the response is 202 (success) or not (failure).
        if (response.status_code == requests.codes.accepted):
            return response.status_code
        else:
            return "{0}: {1}".format(response.status_code, response.text)
        ######################################
        ######################################
    def listItems(self):
        pass
        ######################################