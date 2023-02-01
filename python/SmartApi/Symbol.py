import json
import requests

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
    
    @staticmethod
    def fromJSON(data:dict):
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

class Symbols:
    URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    
    def __init__(self):
        self.ss = None
        pass

    def load(self):
        data = requests.get(Symbols.URL)
        jsonData = data.json()
        self.ss = [SymbolInfo.fromJSON(jd) for jd in jsonData]
    
    def find(self, callback):
        res = list()
        for s in self.ss:
            if(callback(s) == True):
                res.append(s)
        return res
        