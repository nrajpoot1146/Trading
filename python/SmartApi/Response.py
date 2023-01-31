import Task
import Data
class SocketResponce:
    @staticmethod
    def ParseResponse(res):
        dResponse = dict()
        dResponse['Feed'] = list()
        for r in res:
            if Task.Task.IsTask(r):
                print("Task Recieved")
                task = Task.Task.fromDict(r)
                print(task)
                pass
            elif Data.Feed.IsFeed(r):
                feed = Data.Feed.CreateFeed(r)
                if (feed.isScriptFeed()):
                    dResponse['Feed'].append(feed)
                elif(feed.isTimeFeed()):
                    dResponse['timeFeed'] = feed
                pass
        
        if 'timeFeed' in dResponse:
            print(dResponse['timeFeed'].tValue, end=" ")
            for f in dResponse['Feed']:
                print(f.lastTradedPrice, end=" ")
            print()
        pass