import datetime

class Event(object):
    """
    The class used to add events to the calander of each 'Individual'.
    It will contain the deatails of the event (date, time, location etc). 
    
    
    
    """

    def __init__(self, title, date, startTime, endTime , location, companions, reminder = False , notes = None):
        self.title = title
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.location = location
        self.companions = companions
        self.reminder = reminder
        self.notes = notes

    def editEvent(self, **options):
        if options.get("date")!= None:
            self.date = options.get("date")
        if options.get("startTime")!= None:
            self.startTime = options.get("startTime")
        if options.get("endTime")!= None:
            self.endTime = options.get("endTime")
        if options.get("location")!= None:
            self.location = options.get("location")
        if options.get("companions")!= None:
            self.companions = options.get("companions")
        if options.get("reminder")!= None:
            self.reminder = options.get("reminder")
        if options.get("notes")!= None:
            self.notes = options.get("notes")

    def delete(self):
        print ("Deleting ", self.title)
        del self