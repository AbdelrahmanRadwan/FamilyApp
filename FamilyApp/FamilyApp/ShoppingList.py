class ShoppingList(object):
    """description of class"""

    def __init__(self):
        self.shopping = []
        

    def addItems(self, **itemList):
        for items in itemList:
            self.shopping.append(items)

    def deleteItems(self, **itemList):
        for items in itemList:
            self.shopping.remove(shopping.index(items))

    def deleteList(self):
        del self

        ######################################
    def emailList(self, recipient):
        pass
        ######################################
        ######################################
    def listItems(self):
        pass
        ######################################