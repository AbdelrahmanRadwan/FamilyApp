class ShoppingList(object):
    """description of class"""

    def __init__(self):
        pass

    def addItem(self, **itemList):
        for items in itemList:
            shopping.append(items)

    def deleteItem(self, **itemList):
        for items in itemList:
            shopping.remove(shopping.index(items))

    def deleteList(self):
        del self