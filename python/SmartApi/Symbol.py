import requests
from abc import ABC, abstractmethod
import Data
import json
import UI
import LocThread

from enum import Enum


class DerivativeTypes(Enum):
    CE = 0
    PE = 1
    FUT = 2
    NA = -1


Exchange = {
    "NSE": "nse_cm",
    "BSE": "bse_cm",
    "NFO": "nse_fo",
    "MCX": "mcx_fo",
    "NCDEX": "ncx_fo",
    "CDS": "cde_fo"
}


class SymbolInfo:
    """
        [{'token': '246083',
        'symbol': 'CRUDEOIL23FEBFUT',
        'name': 'CRUDEOIL',
        'expiry': '17FEB2023',
        'strike': '0.000000',
        'lotsize': '100',
        'instrumenttype': 'FUTCOM',
        'exch_seg': 'MCX',
        'tick_size': '100.000000'}]
    """

    def __init__(self):
        self.token = None
        self.symbol = None
        self.name = None
        self.expiry = None
        self.strike = None
        self.lotsize = None
        self.instrumenttype = None
        self.exch_seg = None
        self.tick_size = None

        self.__symbolInstance = None

    def getSubToken(self):
        return Exchange[self.exch_seg] + "|" + self.token

    def isDerivative(self):
        return "OPT" in self.instrumenttype

    def getDrivativeType(self):
        if (self.isDerivative()):
            if 'PE' in self.symbol:
                return DerivativeTypes.PE
            elif 'CE' in self.symbol:
                return DerivativeTypes.CE
            elif 'FUT' in self.symbol:
                return DerivativeTypes.FUT
        return DerivativeTypes.NA

    def getStrikePrice(self):
        return float(self.strike) / 100
    
    def getSymbolInstance(self):
        self.__symbolInstance = Symbol(self) if self.__symbolInstance == None else self.__symbolInstance
        return self.__symbolInstance

    @staticmethod
    def fromJSON(data: dict):
        si = SymbolInfo()
        si.token = data['token']
        si.symbol = data['symbol']
        si.name = data['name']
        si.expiry = data['expiry']
        si.strike = data['strike']
        si.lotsize = data['lotsize']
        si.instrumenttype = data['instrumenttype']
        si.exch_seg = data['exch_seg']
        si.tick_size = data['tick_size']
        return si

    def __str__(self):
        return '''{{token : {0}, symbol : {1}, name : {2}, expiry : {3}, strike : {4}, lotsize : {5}, instrumenttype : {6}, exch_seg : {7}, tick_size : {8}}}''' \
            .format(self.token, self.symbol, self.name, self.expiry, self.strike, self.lotsize, self.instrumenttype, self.exch_seg, self.tick_size)
        pass


class SymbolsInfo:
    URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

    def __init__(self, ui=None):
        self.ui: UI.MainUi = ui
        self.ss = None
        pass

    def load(self):
        print("Loading Symbols Info...")

        try:
            print("Loding from file...")
            with open('json_data.json') as json_file:
                jsonData = json.load(json_file)
                pass
        except Exception:
            print("Loding from web...")
            data = requests.get(SymbolsInfo.URL)
            jsonData = data.json()
            with open('json_data.json', 'w') as outfile:
                outfile.write(data.text)

        self.ss = [SymbolInfo.fromJSON(jd) for jd in jsonData]
        self.ss.sort(key=lambda x: x.symbol)

    def find(self, callback):
        res = list()
        for s in self.ss:
            if (callback(s) == True):
                res.append(s)
        return res

    def getSymbolNearCurrentPrice(self, name, price, expiry):
        res = list()
        res = self.find(lambda x: x.name ==
                        name and x.isDerivative() and x.expiry == expiry)
        res.sort(key=lambda x: x.getStrikePrice())
        i = 0
        for r in res:
            if r.getStrikePrice() >= price:
                break
            i += 1
        start = i-10 if i-10 >= 0 else 0
        end = start+22 if start+2 < len(res) else len(res)
        res = res[start: end]
        return res
    
WatchList = ['26009', '26000', '246083']


class ISymbol(ABC):
    @abstractmethod
    def onFeedRecieved(self, data: Data.ScriptFeed):
        pass
    pass


class Symbol(ISymbol):
    def __init__(self, symbolInfo: SymbolInfo):
        super().__init__()
        self.symbolInfo: SymbolInfo = symbolInfo
        self._onFeedRecieved = list()
        self.threads = []

    def onFeedRecieved(self, data: Data.ScriptFeed):
        if (self._onFeedRecieved != None):
            for f in self._onFeedRecieved:
                try:
                    f(self, data)
                    # self.lcw = LocThread.SymbolOnFeedRecievedThread(threadList=self.threads,target=f, args=[self, data])
                    # self.lcw.start()
                    # print(len(self.threads))
                except Exception as e:
                    print(e.args)
                    self.unSubscribeOnFeedRecived(f)
    
    def subscribeOnFeedRecived(self, callable):
        self._onFeedRecieved.append(callable)

    def unSubscribeOnFeedRecived(self, callable):
        if callable in self._onFeedRecieved:
            self._onFeedRecieved.remove(callable)

    def __onFeedRecieved(self, symbolInfo: SymbolInfo, data: Data.ScriptFeed):
        print("----------------------------------------------")
        print("Name: ", symbolInfo.name)
        print("symbol: ", symbolInfo.symbol)
        print("LTT: ", data.lastTradedPrice)
        print("----------------------------------------------")

    def __str__(self):
        return self.symbolInfo.__str__()
    
def hello():
    pass

if __name__ == '__main__':
    symbol = SymbolsInfo()
    symbol.load()
    ls = symbol.find(lambda x: x.token == '26000')
    ls[0].getSymbolInstance().subscribeOnFeedRecived(hello)
    ls[0].getSymbolInstance().unSubscribeOnFeedRecived(hello)
    print()
