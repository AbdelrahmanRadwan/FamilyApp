from queue import priorityqueue

priorities = [ 'high' :1,
              'medium' :2,
              'low' :3]

class Todo(object):

    def __init__(self, content: str, priority: int32 ):
        self.content = content
        self.priority = priority

class TodoList(object):

    def __init__(self):
        q = priorityqueue(0)

    def addTodo(self, todo: Todo):
        q.put(todo.priority, todo)

    def finishedTodo(self, todo:Todo):
        q.get(todo)