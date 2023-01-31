from enum import Enum

class OrderVariety(Enum):
    NORMAL = 0

class ProductType(Enum):
    INTRADAY = 0

class TransactionType(Enum):
    BUY = 0
    SELL = 1

class Exchange(Enum):
    NSE = 0

class OrderType(Enum):
    LIMIT = 0

class OrderDetails:
    def __init__(self, 
        tradingsymbol:str, 
        symboltoken:str, 
        ordertype:OrderType, 
        price, 
        producttype:ProductType = ProductType.INTRADAY, 
        transactiontype:TransactionType = TransactionType.BUY, 
        exchange:Exchange = Exchange.NSE, 
        duration = "DAY", 
        squareoff = "0", 
        stoploss = "0", 
        quantity = "1", 
        variety:OrderVariety = OrderVariety.NORMAL):

        self.variety = variety
        self.tradingsymbol = tradingsymbol
        self.symboltoken = symboltoken
        self.ordertype = ordertype
        self.price = price
        self.producttype  = producttype 
        self.transactiontype = transactiontype
        self.exchange = exchange
        self.duration = duration 
        self.squareoff = squareoff 
        self.stoploss = stoploss
        self.quantity = quantity 
    
    def getJSONIFY(self):
        return {
        "variety": self.variety.name,
        "tradingsymbol": self.tradingsymbol,
        "symboltoken": self.symboltoken,
        "transactiontype": self.transactiontype.name,
        "exchange": self.exchange.name,
        "ordertype": self.ordertype.name,
        "producttype": self.producttype.name,
        "duration": self.duration,
        "price": self.price,
        "squareoff": self.squareoff,
        "stoploss": self.stoploss,
        "quantity": self.quantity
        }
        pass