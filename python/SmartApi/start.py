import System
import sys

clientCode = "N491170"
pin = "1273"

if __name__ == "__main__":
    temp = sys.stdout
    system = System.MainSystem(clientCode, pin)
    system.run()
    sys.stdout = temp
    system.exit()
    # symbolInfo:Symbol.SymbolInfo = symbolsInfo.find(lambda x : x.token == '246083' or x.token =='249780')
    # symbolInfo:Symbol.SymbolInfo = symbolsInfo.find(lambda x : x.token == '26000' or x.token =='42337')