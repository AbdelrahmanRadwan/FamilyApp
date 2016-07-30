class ShoppingList(object):
    """description of class"""

    def __init__(self):
        pass

    def addItems(self, **itemList):
        for items in itemList:
            shopping.append(items)

    def deleteItems(self, **itemList):
        for items in itemList:
            shopping.remove(shopping.index(items))

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