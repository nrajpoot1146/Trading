import threading
from typing import Any, Callable, Iterable, Mapping

class SymbolOnFeedRecievedThread(threading.Thread):

    def __init__(self, threadList:list, target: Callable[..., object] | None = ..., args: Iterable[Any] = ...):
        threading.Thread.__init__(self)
        self.target = target
        self.args = args
        self.threadList = threadList
        self.threadList.append(self)

    def run(self):
        self.target(*self.args)
        self.threadList.remove(self)