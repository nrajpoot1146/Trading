import dhanhq

class Order:
    def __init__(self, session):
        self.security_id = None
        self.exchange_segment = None
        self.transaction_type = None
        self.quantity = None
        self.order_type = None
        self.product_type = None
        self.price = None
        self.dhan = dhanhq("client_id","access_token")
        pass

    # NSE And BSE
    """
    # Place an order for Equity Cash
    dhan.place_order(security_id='1333',   #hdfcbank
        exchange_segment=dhan.NSE,
        transaction_type=dhan.BUY,
        quantity=10,
        order_type=dhan.MARKET,
        product_type=dhan.INTRA,
        price=0)

    dhan.place_order(security_id='500180',   #hdfcbank
        exchange_segment=dhan.BSE,
        transaction_type=dhan.BUY,
        quantity=1,
        order_type=dhan.MARKET,
        product_type=dhan.INTRA,
        price=0,)
    """
    def equityCashOrder(self, ):
        self.dhan.place_order(
            security_id='1333',   #hdfcbank
            exchange_segment=self.dhan.NSE,
            transaction_type=self.dhan.BUY,
            quantity=10,
            order_type=self.dhan.MARKET,
            product_type=self.dhan.INTRA,
            price=0)
        pass

    """
    # Place an order for Futures & Options
    dhan.place_order(security_id='52175',  #NiftyPE
        exchange_segment=dhan.FNO,
        transaction_type=dhan.BUY,
        quantity=550,
        order_type=dhan.MARKET,
        product_type=dhan.INTRA,
        price=0)
    """
    def futureAndOptionOrder(self):
        pass

    """
    # Place an order for Currency
    dhan.place_order(security_id= '10093',  #usdinr
        exchange_segment= dhan.CUR,
        transaction_type= dhan.BUY,
        quantity=1,
        order_type = dhan.MARKET,
        validity= dhan.DAY,
        product_type= dhan.INTRA,
        price=0)
    """
    def currencyOrder(self):
        pass

    """
    # Place an order for MCX Commodity    
    dhan.place_order(security_id= '114',    #gold
        exchange_segment= dhan.BSE,
        transaction_type= dhan.BUY,
        quantity=1,
        order_type=dhan.MARKET,
        product_type= dhan.INTRA,
        price=0)
    """
    def mcxCommodityOrder(self):
        pass

    """
    # Place Slice Order
    dhan.place_slice_order(security_id='52175',  #NiftyPE
        exchange_segment=dhan.FNO,
        transaction_type=dhan.BUY,
        quantity=2000,              #nifty freeze quantity is 1800
        order_type=dhan.MARKET,
        product_type=dhan.INTRA,
        price=0)
    """
    def sliceOrder(self):
        pass

    """
    # Place MTF Order
    dhan.place_order(security_id='1333',   #hdfcbank
        exchange_segment=dhan.NSE,
        transaction_type=dhan.BUY,
        quantity=100,
        order_type=dhan.MARKET,
        product_type=dhan.MTF,
        price=0)
    """
    def mtfOrder(self):
        pass
