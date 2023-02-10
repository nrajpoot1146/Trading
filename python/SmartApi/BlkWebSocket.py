from smartapi import SmartWebSocket
# from smartapi import smartWebSocketV2
import threading
import time
import Response
import Symbol
import six
import json

class WebSocket:
    def __init__(self, feedToken, clientCode):
        self.ss = SmartWebSocket(feedToken, clientCode)
        self.ss._on_open = self.on_open
        self.ss._on_message = self.on_message
        self.ss._on_error = self.on_error
        self.ss._on_close = self.on_close

        self.subscribedSymbols = dict()
    
    # def __init__(self, authtoken, apiKey, clientCode, feedToken):
    #     # self.ss2 = smartWebSocketV2()
    #     # self.ss2.on_open = on_open
    #     # self.ss2.on_data = 
    #     # self.ss2.on_error = on_error
    #     # self.ss2.on_close = on_close
    #     pass

    def printSubscribedSymbols(self):
        for s in self.subscribedSymbols:
            print(self.subscribedSymbols[s])

    def startStream(self):
        print("Start Stream")
        self.th = threading.Thread(target=self.ss.connect)
        self.th.start()

    def stopStream(self):
        self.subscribedSymbols.clear()
        self.ss.task_dict.clear()
        print("Stop Stream")
        self.ss.ws.close()

    def on_message(self, ws, message):
        Response.SocketResponce.ParseResponse(message, self.subscribedSymbols)

    def on_open(self, ws):
        print("on open")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, code, reason):
        print("On Close")

    def subscribe(self, symbol:Symbol.Symbol, task:str):
        self.ss.subscribe(task, symbol.symbolInfo.getSubToken())
        self.subscribedSymbols[symbol.symbolInfo.token] = symbol

    def unSubscribeAll(self):
        # self.subscribedSymbols.clear()
        self.ss.task_dict.clear()
        strwatchlistscrips = ""  # dynamic call
    
        try:
            request = {"task": '', "channel": '', "token": self.ss.feed_token,
                        "user": self.ss.client_code, "acctid": self.ss.client_code}
    
            self.ss.ws.send(
                six.b(json.dumps(request))
            )
            return True
        except Exception as e:
            print("Error while request sending: {}".format(str(e)))
            raise

    def unsubscribe(self, symbol:Symbol.Symbol):
        # self.ss.subscribe("mw", "")
        self.stopStream()
        self.subscribedSymbols.pop(symbol.symbolInfo.token)
        self.startStream()
        time.sleep(1)

        try:
            for s in self.subscribedSymbols:
                self.ss.subscribe('mw', self.subscribedSymbols[s].symbolInfo.getSubToken())
        except Exception:
            pass
