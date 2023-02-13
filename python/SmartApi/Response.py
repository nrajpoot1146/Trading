import Task
import Data
import threading

threadlock = threading.Lock()

class SocketResponce:
    @staticmethod
    def ParseResponse(res, subscribedSymbol:dict, subscribedForTimeFeed:list):
        for r in res:
            if Task.Task.IsTask(r):
                print("Task Recieved")
                task = Task.Task.fromDict(r)
                print(task)
                pass
            elif Data.Feed.IsFeed(r):
                # print("Feed Recieved", r)
                feed = Data.Feed.CreateFeed(r)
                if (feed.isScriptFeed()):
                    print("Script Feed Recieved")
                    subscribedSymbol[feed.token].onFeedRecieved(feed)
                elif(feed.isTimeFeed()):
                    print("Time Feed Recieved")
                    for f in subscribedForTimeFeed:
                        f(feed)
                    pass
                elif(feed.isIndexFeed()):
                    print("Index Feed Recieved")
                    pass