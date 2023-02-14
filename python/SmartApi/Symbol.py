import requests
from abc import ABC, abstractmethod
import Data
import json
import LocThread

from enum import Enum


class SymbolTypes(Enum):
    CE = 0
    PE = 1
    FUT = 2
    Equity = 3
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

        self._symbolInstance = None

    def getSubToken(self):
        return Exchange[self.exch_seg] + "|" + self.token

    def isDerivative(self):
        return "OPT" in self.instrumenttype

    def getSymbolType(self):
        if (self.isDerivative()):
            if 'PE' in self.symbol:
                return SymbolTypes.PE
            elif 'CE' in self.symbol:
                return SymbolTypes.CE
            elif 'FUT' in self.symbol:
                return SymbolTypes.FUT
            elif 'EQ' in self.symbol:
                return SymbolTypes.Equity
        return SymbolTypes.NA

    def getStrikePrice(self):
        return float(self.strike) / 100
    
    def getSymbolInstance(self):
        self._symbolInstance = Symbol(self) if self._symbolInstance == None else self._symbolInstance
        return self._symbolInstance

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

## Equity, FUTURE, OPTION, INDICES
# can have future and option

# can have options
class SymbolInfoFuture(SymbolInfo):
    pass

# can have future and options
class SymbolInfoIndexAndEquity(SymbolInfo):
    def __init__(self):
        super().__init__()

        # key (Expiry) value SymbolInfoFuture
        self.__futures = dict()

        # key (Expiry) value SymbolInfoOption
        self.__options = dict()
    
    @staticmethod
    def createFromSymbolInfo(symbolInfo:SymbolInfo, symbolsInfo:list):
        symbolInfoIndexAndEquity = SymbolInfoIndexAndEquity()
        symbolInfoIndexAndEquity.token = symbolInfo.token
        symbolInfoIndexAndEquity.symbol = symbolInfo.symbol
        symbolInfoIndexAndEquity.name = symbolInfo.name
        symbolInfoIndexAndEquity.expiry = symbolInfo.expiry
        symbolInfoIndexAndEquity.strike = symbolInfo.strike
        symbolInfoIndexAndEquity.lotsize = symbolInfo.lotsize
        symbolInfoIndexAndEquity.instrumenttype = symbolInfo.instrumenttype
        symbolInfoIndexAndEquity.exch_seg = symbolInfo.exch_seg
        symbolInfoIndexAndEquity.tick_size = symbolInfo.tick_size

        symbolInfoIndexAndEquity._symbolInstance = symbolInfo._symbolInstance

        # symbolInfoIndexAndEquity.__futures = [fut for fut in symbolsInfo if fut.name == symbolInfoIndexAndEquity.name and fut.getSymbolType() == SymbolTypes.FUT]
        symbolInfoIndexAndEquity.__options = [op for op in symbolsInfo if op.name == symbolInfoIndexAndEquity.name and (op.getSymbolType() == SymbolTypes.PE or op.getSymbolType() == SymbolTypes.CE)]
        return symbolInfoIndexAndEquity
    
    def addFuture(self, symbolInfo:SymbolInfo):
        if symbolInfo.expiry not in self.__futures:
            self.__futures[symbolInfo.expiry] = list()
        self.__futures[symbolInfo.expiry].append(symbolInfo)

    def addOption(self, symbolInfo:SymbolInfo):
        if symbolInfo.expiry not in self.__options:
            self.__options[symbolInfo.expiry] = list()
        self.__options[symbolInfo.expiry].append(symbolInfo)

class SymbolsInfo:
    URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

    def __init__(self):
        self.ss = None
        self.indices = []
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
        self.seprateIndices()

    def seprateIndices(self):
        if self.ss != None:
            self.indices = [SymbolInfoIndexAndEquity.createFromSymbolInfo(si, self.ss) for si in self.ss if si.symbol == si.name and si.token in WatchList]

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
                    # f(self, data)
                    self.lcw = LocThread.SymbolOnFeedRecievedThread(threadList=self.threads,target=f, args=[self, data])
                    self.lcw.start()
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
    
class InstrumentType:
    def __init__(self, name):
        self.name = name
        pass
    
class Exchange:
    def __init__(self, name):
        self.name = name

        self.equity = None
        self.indices = None
        self.futureOptions = None
        pass
    
def hello():
    pass

if __name__ == '__main__':
    symbol = SymbolsInfo()
    symbol.load()
    print()
