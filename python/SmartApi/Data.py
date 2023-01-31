import json
class Feed:
    def __init__(self, name):
        self.name = name
        pass

    @staticmethod
    def CreateFeed(data):
        if (data['name'] == 'sf'):
            return ScriptFeed.CreateFromJSON(data)
        elif (data['name'] == 'tm'):
            return TimeFeed.CreateFromJSON(data)
        return None
    @staticmethod
    def IsFeed(r):
        if (type(r) == dict):
            return 'name' in r
        return False
    
    def isScriptFeed(self):
        return self.name == 'sf'

    def isTimeFeed(self):
        return self.name == 'tm'

    def isIndexFeed(self):
        return self.name == 'if'

class ScriptFeed(Feed):
    def __init__(self, name=""):
        super().__init__(name)
        self.token = None
        self.exchange = None
        self.lastTradedPrice = None
        self.prevClosePrice = None
        self.perChange = None
        self.change = None
        self.volume = None
        self.bestBuyQuantity = None
        self.bestBuyPrice = None
        self.bestSellQuantity = None
        self.bestSellPrice = None
        self.lastTradedQuantity = None
        self.lastUpdateTime = None
        self.upperCircuitLimit = None
        self.totalBuyQuantity = None
        self.marketCapitalization = None
        self.lowPrice = None
        self.yearlyHighPrice = None
        self.openPrice = None
        self.tradingSymbol = None
        self.highPrice = None
        self.lowerCircuitLimit = None
        self.totalSellQuantity = None
        self.vwapAveragePrice = None
        self.yearlyLowPrice = None
        self.yearlyLowPrice = None
        self.openInterest = None
        self.issuedCapital = None
        self.totalOpeninterest = None
        self.lowTradeExecutionRange = None
        self.highTradeExecutionRange = None
        self.settlementType = None
        self.data = None
        

    @staticmethod
    def CreateFromJSON(data):
        sf = ScriptFeed()
        sf.data = data#json.loads(str)
        sf.name = data['name']
        sf.token = data['tk']
        sf.exchange = data['e']
        sf.lastTradedPrice = data['ltp']
        sf.prevClosePrice = data['c']
        sf.perChange = data['nc']
        sf.change = data['cng']
        sf.lastUpdateTime = data['ltt']

        return sf
    pass

class TimeFeed(Feed):
    def __init__(self, name = ""):
        super().__init__(name)
        self.tValue = None

    @staticmethod
    def CreateFromJSON(data):
        tf = TimeFeed()
        tf.name = data['name']
        tf.tValue = data['tvalue']
        return tf

