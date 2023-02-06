from smartapi import SmartWebSocket
import threading
import time
import Response
import Symbol

class WebSocket:
    def __init__(self, feedToken, clientCode):
        self.ss = SmartWebSocket(feedToken, clientCode)
        self.ss._on_open = self.on_open
        self.ss._on_message = self.on_message
        self.ss._on_error = self.on_error
        self.ss._on_close = self.on_close

        self.subscribedSymbols = dict()

    def printSubscribedSymbols(self):
        for s in self.subscribedSymbols:
            print(self.subscribedSymbols[s])

    def startStream(self):
        print("Start Stream")
        self.th = threading.Thread(target=self.ss.connect)
        self.th.start()

    def stopStream(self):
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
