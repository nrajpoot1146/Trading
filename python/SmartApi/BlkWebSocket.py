from smartapi import SmartWebSocket
import threading
import Data
import Response

class WebSocket:
    def __init__(self, feedToken, clientCode):
        self.ss = SmartWebSocket(feedToken, clientCode)
        self.ss._on_open = self.on_open
        self.ss._on_message = self.on_message
        self.ss._on_error = self.on_error
        self.ss._on_close = self.on_close

        # SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
        self.token = "nse_fo|42336&nse_cm|26000"
        # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
        self.task = "mw"   # mw|sfi|dp

    def startStream(self):
        print("Start Stream")
        self.th = threading.Thread(target=self.ss.connect)
        self.th.start()

    def stopStream(self):
        print("Stop Stream")
        self.ss.ws.close()

    def on_message(self, ws, message):
        # os.system("cls")
        Response.SocketResponce.ParseResponse(message)
        # print("Ticks: {}".format(message))
        # sf = Data.Feed.CreateFeed(message)
        # if sf != None:
        #     print(sf.name, sf.lastTradePrice)
        # pass

    def on_open(self, ws):
        print("on open")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, code, reason):
        print("On Close")

    def subscribe(self):
        self.ss.subscribe(self.task, self.token)
