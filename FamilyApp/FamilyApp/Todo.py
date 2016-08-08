from queue import PriorityQueue

priorities = { 'high' :1,
              'medium' :2,
              'low' :3}

class Todo(object):

    def __init__(self, content: str, date, time , priority ):
        self.content = content
        self.date = date
        self.time = time
        self.priority = priority

class TodoList(object):

    _Q_FILEPATH = "SavedFiles/q.txt"

    def __init__(self):
        self.q = PriorityQueue()
        if os.path.exists(TodoList._Q_FILEPATH) and os.path.getsize(TodoList._Q_FILEPATH) > 0:
            qfile = open(TodoList._Q_FILEPATH, 'rb')
            self.q = pickle.load(qfile)
            qfile.close()
        

    def addTodo(self, todo: Todo):
        self.q.put(todo.priority, todo)

    def finishedTodo(self, todo:Todo):
        self.q.get(todo)

    def finishing(self):
        try:
            qfile =  open(TodoList._Q_FILEPATH, 'wb')
           
            pickle.dump(self.q,qfile, pickle.HIGHEST_PROTOCOL)
            qfile.close()
        except Exception as exc:
            print(exc)

    