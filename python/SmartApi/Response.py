import Task
import Data
import threading

threadlock = threading.Lock()

class SocketResponce:
    @staticmethod
    def ParseResponse(res):
        dResponse = dict()
        dResponse['Feed'] = list()
        # print("Tick: ")
        threadlock.acquire()
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
                    print("Script Feed Recieved")
                elif(feed.isTimeFeed()):
                    dResponse['timeFeed'] = feed
                    print("Time Feed Recieved")
                elif(feed.isIndexFeed()):
                    dResponse['Feed'].append(feed)
                    print("Index Feed Recieved")
                pass
        
        if 'timeFeed' in dResponse:
            print(dResponse['timeFeed'].tValue, end=" ")
        for f in dResponse['Feed']:
            print(f.lastUpdateTime, f.lastTradedPrice, end=" ")
        print()    
        threadlock.release()
        pass