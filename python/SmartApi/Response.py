import Task
import Data
import threading

threadlock = threading.Lock()

class SocketResponce:
    @staticmethod
    def ParseResponse(res, subscribedSymbol:dict):
        dResponse = dict()
        dResponse['Feed'] = list()
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
                    dResponse['Feed'].append(feed)
                    subscribedSymbol[feed.token].onFeedRecieved(feed)
                elif(feed.isTimeFeed()):
                    dResponse['timeFeed'] = feed
                elif(feed.isIndexFeed()):
                    dResponse['Feed'].append(feed)
                pass