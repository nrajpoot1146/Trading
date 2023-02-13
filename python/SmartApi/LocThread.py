import threading
from typing import Any, Callable, Iterable

class SymbolOnFeedRecievedThread(threading.Thread):

    def __init__(self, threadList:list | None, target: Callable[..., object] | None = ..., args: Iterable[Any] = ...):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
        self.threadList = threadList
        if self.threadList != None:
            self.threadList.append(self)

    def run(self):
        self.target(*self.args)
        if self.threadList != None:
            try:
                self.threadList.remove(self)
            except:
                pass