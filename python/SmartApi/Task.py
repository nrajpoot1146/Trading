class Task:
    class Type:
        CONNECT = 'cn'
        HEART_BEAT = 'hb'
        MARKET_WATCH = 'mw'
        SUBSCRIPTION_INDEX = 'sfi'
        MARKET_DEPTH = 'dp'

    def __init__(self):
        self.ak = None
        self.msg = None
        self.type = None
        pass

    def __str__(self):
        return '{{"ak" : {0}, "msg" : {1}, "task" : {2}}}'.format(self.ak, self.msg, self.type)

    @staticmethod
    def fromDict(data:dict):
        task = Task()
        task.ak = data['ak']
        task.msg = data['msg']
        task.type = data['task']
        return task

    @staticmethod
    def IsTask(r):
        if (type(r) == dict):
            return 'task' in r
        return False