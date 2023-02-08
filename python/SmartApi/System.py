from smartapi import SmartConnect
import zope.interface
import BlkWebSocket
import Symbol
import pyotp
import UI
import os
from multipledispatch import dispatch


currDir = os.path.dirname(__file__)

totpGenerator = pyotp.TOTP("DBBAJXZ7ARJP7VBW3HJYLHCLW4")

class MainSystem:
    ApiKeys = {
        "LiveMarket" : "l5g7IX0d",
        "Trading" : "ikEzyHy2",
        "HystoricalData" : "47ulWE5o",
        "Publisher" : "o8SSZu3k"
        }

    def __init__(self, ClientCode, Pin):
        self.ws = None
        
        self.ClientCode = ClientCode
        self.Pin = Pin

        self.liveMarket = SmartConnect(api_key=MainSystem.ApiKeys["LiveMarket"])
        self.trading = SmartConnect(api_key=MainSystem.ApiKeys["Trading"])
        self.hysData = SmartConnect(api_key=MainSystem.ApiKeys["HystoricalData"])
        self.publisher = SmartConnect(api_key=MainSystem.ApiKeys["Publisher"])

        self.symbolsInfo = Symbol.SymbolsInfo()
        self.symbolsInfo.load()

        self.ui = UI.MainUi(self)

    def getIndexSymbolsInfo(self):
        res = []
        for token in Symbol.WatchList:
            symbol = self.symbolsInfo.find(lambda x: x.token == token)
            res.extend(symbol)
        return res

    def login(self, totp: str = None):
        totp = totpGenerator.now() #if totp == None else totp
        self.liveMarketSession = self.liveMarket.generateSession(self.ClientCode, self.Pin, totp)
        # self.tradingSession = self.trading.generateSession(self.ClientCode, self.Pin, totp)

        if (self.liveMarketSession['message'] != 'SUCCESS'):
            print("login failled")
            return
        
        print("Login Success")
        
        self._createWebSocket()

        pass

    def logout(self):
        logout = self.liveMarket.terminateSession(self.ClientCode)
        print("Logout Successfull")
        pass

    def _createWebSocket(self):
        self.ws = BlkWebSocket.WebSocket(self.liveMarket.getfeedToken(), self.ClientCode)

    def getRefereshToken(self):
        return self.liveMarketSession['data']['refreshToken']
    
    def getAuthToken(self):
        return self.liveMarketSession['data']['jwtToken']
    
    @dispatch(list)
    def subscribe(self, symbols:list):
        print("Subscribe Symbol List: ")
        # token = ""
        for s in symbols:
            # if (len(token) != 0):
            #     token += '&'
            # token += s.getSubToken()
            self.ws.subscribe(s.getSymbolInstance(), "mw")
            # time.sleep(0.00)
        pass

    @dispatch(Symbol.Symbol)
    def subscribe(self, symbol:Symbol.Symbol):
        try:
            self.ws.subscribe(symbol, "mw")
        except Exception as e:
            print(e.__traceback__)
            pass
    
    @dispatch(str)
    def subscribe(self, token:str):
        symbolInfo:Symbol.SymbolInfo = self.symbolsInfo.find(lambda x : x.token == '26000')[0]
        symbol = Symbol.Symbol(symbolInfo)
        try:
            self.ws.subscribe(symbol, "mw")
        except Exception as e:
            print(e.__traceback__)
            pass
    
    def exit(self):
        try:
            self.ws.stopStream()
        except Exception:
            pass
        self.logout()

    def run(self):
        self.ui.run()


class Api(zope.interface.Interface):
    pass
