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

    """   
        | 1	 |   name	    |               |   sf - If value comes as sf it's a script feed
        | 2	 |   tk	        |               |   script token
        | 3	 |   e	        |               |   Exchange
        | 4	 |   ltp	    |               |   Last traded price
        | 5	 |   c	        |               |   Previous close price
        | 6	 |   nc	        |               |   % change
        | 7	 |   cng	    |               |   Change
        | 8	 |   v	        |               |   Volume
        | 9	 |   bq	        |               |   Best buy quantity
        | 10 |   bp	        |               |   Best buy price
        | 11 |   bs	        |               |   Best sell quantity
        | 12 |   sp	        |               |   Best sell price
        | 13 |   ltq	    |               |   Last traded quantity
        | 14 |   ltt	    |               |   Last update time
        | 15 |   ucl	    |               |   Upper circuit limit
        | 16 |   tbq	    |               |   Total buy quantity
        | 17 |   mc	        |               |   Market Capitalization ( issued capital * previous close)
        | 18 |   lo	        |               |   Low price
        | 19 |   yh	        |               |   Yearly high price
        | 20 |   op	        |               |   Open price
        | 21 |   ts	        |               |   Trading symbol
        | 22 |   h	        |               |   High price
        | 23 |   lcl	    |               |   Lower circuit limit
        | 24 |   tsq	    |               |   Total Sell quantity
        | 25 |   ap	        |               |   Vwap Average Price
        | 26 |   yl	        |               |   Yearly Low price
        | 27 |   h	        |               |   High price
        | 28 |   oi	        |               |   Open interest
        | 29 |   isdc	    |               |   Issued capital
        | 30 |   to	        |               |   Issued capital
        | 31 |   toi	    |               |   total open interest
        | 32 |   lter	    |               |   Low trade execution range
        | 33 |   hter	    |               |   High trade execution range
        | 34 |   setltyp    |               |	Settlement type
    """
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
        self.to = None # Need to check
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
        sf.name = data['name'] if 'name' in data else None
        sf.token = data['tk'] if 'tk' in data else None
        sf.exchange = data['e'] if 'e' in data else None
        sf.lastTradedPrice = data['ltp'] if 'ltp' in data else None
        sf.prevClosePrice = data['c'] if 'c' in data else None
        sf.perChange = data['nc'] if 'nc' in data else None
        sf.change = data['cng'] if 'cng' in data else None
        sf.volume = data['v'] if 'v' in data else None
        sf.bestBuyQuantity = data['bq'] if 'bq' in data else None
        sf.bestBuyPrice = data['bp'] if 'bp' in data else None
        sf.bestSellQuantity = data['bs'] if 'bs' in data else None
        sf.bestSellPrice = data['sp'] if 'sp' in data else None
        sf.lastTradedQuantity = data['ltq'] if 'ltq' in data else None
        sf.lastUpdateTime = data['ltt'] if 'ltt' in data else None
        sf.upperCircuitLimit = data['ucl'] if 'ucl' in data else None
        sf.totalBuyQuantity = data['tbq'] if 'tbq' in data else None
        sf.marketCapitalization = data['mc'] if 'mc' in data else None
        sf.lowPrice = data['lo'] if 'lo' in data else None
        sf.yearlyHighPrice = data['yh'] if 'yh' in data else None
        sf.openPrice = data['op'] if 'op' in data else None
        sf.tradingSymbol = data['ts'] if 'ts' in data else None
        sf.highPrice = data['h'] if 'h' in data else None
        sf.lowerCircuitLimit = data['lcl'] if 'lcl' in data else None
        sf.totalSellQuantity = data['tsq'] if 'tsq' in data else None
        sf.vwapAveragePrice = data['ap'] if 'ap' in data else None
        sf.yearlyLowPrice = data['yl'] if 'yl' in data else None
        sf.openInterest = data['oi'] if 'oi' in data else None
        sf.to = data['to'] if 'to' in data else None # Need to check
        sf.issuedCapital = data['isdc'] if 'isdc' in data else None
        sf.totalOpeninterest = data['toi'] if 'toi' in data else None
        sf.lowTradeExecutionRange = data['lter'] if 'lter' in data else None
        sf.highTradeExecutionRange = data['hter'] if 'hter' in data else None
        sf.settlementType = data['setltyp'] if 'setltyp' in data else None
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

