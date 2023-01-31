import Order
from smartapi import SmartConnect
import BlkWebSocket
import pyotp
import time
import System

totp = pyotp.TOTP("DBBAJXZ7ARJP7VBW3HJYLHCLW4")


clientCode = "N491170"
pin = "1273"

if __name__ == "__main__":
    system = System.MainSystem(clientCode, pin)
    system.login(totp.now())

    # fetch the feedtoken
    feedToken = system.obj.getfeedToken()

    # fetch User Profile
    userProfile = system.obj.getProfile(system.getRefereshToken())
    print(userProfile)

    ws = BlkWebSocket.WebSocket(feedToken, clientCode)

    q = False
    while not q:
        print("1. start stream")
        print("2. stop stream")

        ch = int(input("Enter: "))

        if(ch == 1):
            ws.startStream()
        elif(ch == 2):
            ws.stopStream()
        elif(ch == 3):
            ws.subscribe()
        elif(ch == 0):
            system.logout()
        else:
            ws.stopStream()
            system.logout()
            q = True


    # from smartapi import SmartWebSocket
    # import os

    # # feed_token=092017047
    # FEED_TOKEN=feedToken
    # CLIENT_CODE=clientCode
    # # token="mcx_fo|224395"
    # token="mcx_fo|246083"    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
    # # token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
    # task="mw"   # mw|sfi|dp

    # ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

    # def on_message(ws, message):
    #     os.system("cls")
    #     print("Ticks: {}".format(message))

    # def on_open(ws):
    #     print("on open")
    #     ss.subscribe(task,token)

    # def on_error(ws, error):
    #     print(error)

    # def on_close(ws):
    #     print("Close")

    # # Assign the callbacks.
    # ss._on_open = on_open
    # ss._on_message = on_message
    # ss._on_error = on_error
    # ss._on_close = on_close

    # ss.connect()

   # ss.connect()
    # logout=obj.terminateSession(clientCode)
    # print("Logout Successfull")
