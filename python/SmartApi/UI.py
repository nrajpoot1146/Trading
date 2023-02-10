import sys
import os
from pathlib import Path
# from System import MainSystem
sys.path.append('E:/Trading/python/')
import threading
import Symbol
import Data

currDir = os.path.dirname(__file__)
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic, QtWidgets, QtGui, QtCore

lock = threading.Lock()

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)
    def write(self, text):
        self.newText.emit(str(text))

class MainUi(QtWidgets.QMainWindow):
    def __init__(self, system):
        self.app = QApplication([])
        self.app.setStyleSheet(Path(currDir+r"\..\ui\StyleSheet.css").read_text())
        self.mainWindow = MainWindow(system)
        self.mainWindow.show()
        self.system = system

    def run(self):
        self.app.exec()

class MainWindow(QtWidgets.QMainWindow):
    updateSymbolSignal = QtCore.pyqtSignal(list)
    IndexPriceUpdateSignal = QtCore.pyqtSignal(Symbol.Symbol, Data.ScriptFeed)

    def __init__(self, system):
        super(MainWindow, self).__init__()
        uic.load_ui.loadUi(currDir + r'\..\ui\MainWindow.ui', self)
        self.system = system
        self.selectedOptionChains = []

        self.actionLogin.triggered.connect(self.onActionLoginClick)
        self.actionLogout.triggered.connect(self.onActionLogoutClick)
        self.start.clicked.connect(self.onStartClick)
        self.stop.clicked.connect(self.onStopClick)
        self.IndexPriceUpdateSignal.connect(self.onPriceUpdate)

        self.stop.setEnabled(False)
        sys.stdout = Stream(newText=self.addInConsole)
        self.teConsole.setReadOnly(True)
        self.indexWatchList = self.system.getIndexSymbolsInfo()

        for i in self.indexWatchList:
            self.cbIndices.addItem(i.symbol)

        self.cbIndices.activated[int].connect(self.onActivated)
        self.onFlagUpdate = False
        self.updateSymbolSignal.connect(self.updateSymbols)

    def onActivated(self, index):
        try:
            self.system.subscribe(self.indexWatchList[index].getSymbolInstance())
            for i in range(len(self.indexWatchList)):
                if (i != index):
                    self.indexWatchList[i].getSymbolInstance().unSubscribeOnFeedRecived(self.IndexPriceUpdateSignal.emit)
            self.indexWatchList[index].getSymbolInstance().subscribeOnFeedRecived(self.IndexPriceUpdateSignal.emit)
            self.cbIndices.setEnabled(False)
            self.stop.setEnabled(True)
        except Exception as e:
            pass

    def onPriceUpdate(self, symbol, data):
        prevPrice = 0.0
        newPrice = 0.0
        try:
            prevPrice = float(self.lindexltp.text())
        except Exception as e:
            pass

        try:
            newPrice = float(data.lastTradedPrice)
        except Exception as e:
            pass
        
        if newPrice != prevPrice:
            colorEffect = QtWidgets.QGraphicsColorizeEffect()
            if newPrice > prevPrice:
                colorEffect.setColor(QtCore.Qt.GlobalColor.darkGreen)
            elif newPrice < prevPrice:
                colorEffect.setColor(QtCore.Qt.GlobalColor.red)
            self.lindexltp.setGraphicsEffect(colorEffect)
            self.lindexltp.setText(data.lastTradedPrice)

        if self.onFlagUpdate == False:
            self.selectedOptionChains = self.system.symbolsInfo.getSymbolNearCurrentPrice(symbol.symbolInfo.name, float(data.lastTradedPrice), '15FEB2023')
            self.onFlagUpdate = True
            self.updateSymbolSignal.emit(self.selectedOptionChains)

    def addInConsole(self, text):
        self.teConsole.insertPlainText(text)
        self.teConsole.moveCursor(QtGui.QTextCursor.MoveOperation.End)
    
    def updateSymbols(self, symbols):
        while self.verticalLayout.count():
            item = self.verticalLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        tempres = dict()
        for r in symbols:
            if r.getStrikePrice() not in tempres:
                tempres[r.getStrikePrice()] = list()
                tempres[r.getStrikePrice()].append(r)
            else:
                tempres[r.getStrikePrice()].append(r)
        for s in tempres:
            r = Row(s, tempres[s][0], tempres[s][1])
            self.verticalLayout.addWidget(r)

        self.system.subscribe(self.selectedOptionChains)

    def onActionLoginClick(self):
        self.system.login()
        self.system.ws.startStream()
        pass

    def onActionLogoutClick(self):
        self.system.ws.stopStream()
        self.system.logout()
        pass

    def onStartClick(self):
        try:
            self.system.subscribe(self.selectedOptionChains)
        except Exception as e:
            print(e.__traceback__.tb_frame)

    def onStopClick(self):
        self.system.ws.stopStream()
        self.system.ws.startStream()
        # self.system.ws.unSubscribeAll()
        self.cbIndices.setEnabled(True)
        self.stop.setEnabled(False)
        self.onFlagUpdate = False
     
class Row(QWidget):
    """
        class to represnt pair of Call and put
    """
    CEOIChangeSignal = QtCore.pyqtSignal(Symbol.Symbol, Data.ScriptFeed)
    PEOIChangeSignal = QtCore.pyqtSignal(Symbol.Symbol, Data.ScriptFeed)
    CELTPChangeSignal = QtCore.pyqtSignal(Symbol.Symbol, Data.ScriptFeed)
    PELTPChangeSignal = QtCore.pyqtSignal(Symbol.Symbol, Data.ScriptFeed)

    def __init__(self, strikePrice, ceSymbol, peSymbol):
        super(Row, self).__init__()
        uic.load_ui.loadUi(currDir + r'\..\ui\Row.ui', self)
        self.peSymbol = peSymbol
        self.ceSymbol = ceSymbol
        self.lStrikePrice.setText(str(strikePrice))

        self.pbPut.setText(peSymbol.symbol) 
        self.pbCall.setText(ceSymbol.symbol)

        self._onCELTPClick = None
        self._onPELTPClick = None
        
        self.pbPut.clicked.connect(self.onPELTPClick)
        self.pbCall.clicked.connect(self.onCELTPClick)

        # connect signals to slots
        self.CELTPChangeSignal.connect(self.onCELTPChange)
        self.PELTPChangeSignal.connect(self.onPELTPChange)
        self.PEOIChangeSignal.connect(self.onPEOIChange)
        self.CEOIChangeSignal.connect(self.onCEOIChange)

        # Register to recieve feeds from server
        self.ceSymbol.getSymbolInstance().subscribeOnFeedRecived(self.CELTPChangeSignal.emit)
        self.ceSymbol.getSymbolInstance().subscribeOnFeedRecived(self.CEOIChangeSignal.emit)
        self.peSymbol.getSymbolInstance().subscribeOnFeedRecived(self.PELTPChangeSignal.emit)
        self.peSymbol.getSymbolInstance().subscribeOnFeedRecived(self.PEOIChangeSignal.emit)

    def onCELTPClick(self, e):
        print("onCELTPClick", e)
        if(self._onCELTPClick != None):
            self._onCELTPClick(self.ceSymbol)
        pass

    def onPELTPClick(self, e):
        print("onPELTPClick", e)
        if(self._onPELTPClick != None):
            self._onPELTPClick(self.peSymbol)
        pass

    def onCELTPChange(self, symbol, data):
        prevPrice = 0.0
        newPrice = 0.0
        try:
            prevPrice = float(self.pbCall.text())
        except Exception as e:
            pass
        
        try:
            newPrice = float(data.lastTradedPrice)
        except Exception as e:
            pass

        colorEffect = QtWidgets.QGraphicsColorizeEffect()

        if (newPrice != prevPrice):

            if newPrice > prevPrice:
                colorEffect.setColor(QtCore.Qt.GlobalColor.darkGreen)
            elif newPrice < prevPrice:
                colorEffect.setColor(QtCore.Qt.GlobalColor.red)
            
            self.pbCall.setGraphicsEffect(colorEffect)
            self.pbCall.setText(str(newPrice))

    def onPELTPChange(self, symbol, data):
        prevPrice = 0.0
        newPrice = 0.0
        try:
            prevPrice = float(self.pbPut.text())
        except Exception as e:
            pass

        colorEffect = QtWidgets.QGraphicsColorizeEffect()
        try:
            newPrice = float(data.lastTradedPrice)
        except Exception as e:
            pass

        if (newPrice != prevPrice):
            if newPrice > prevPrice:
                colorEffect.setColor(QtCore.Qt.GlobalColor.darkGreen)
            elif newPrice < prevPrice:
                colorEffect.setColor(QtCore.Qt.GlobalColor.red)

            self.pbPut.setGraphicsEffect(colorEffect)
            self.pbPut.setText(str(newPrice))

    def onCEOIChange(self, symbol, data):
        prevValue = 0.0
        newValue = 0.0

        try:
            prevValue = float(self.lCallOIChange.text())
        except Exception as e:
            pass

        try:
            newValue = float(data.volume)
        except Exception as e:
            pass

        if newValue > prevValue:
            self.lCallOIChange.setStyleSheet("color: green")
        elif newValue < prevValue:
            self.lCallOIChange.setStyleSheet("color: red")
        else:
            newValue = prevValue
            
        self.lCallOIChange.setText(str(newValue))

        pass

    def onPEOIChange(self, symbol, data):
        prevValue = 0.0
        newValue = 0.0

        try:
            prevValue = float(self.lPutOIChange.text())
        except Exception as e:
            pass

        try:
            newValue = float(data.perChange)
        except Exception as e:
            pass

        if newValue > prevValue:
            self.lPutOIChange.setStyleSheet("color: green")
        elif newValue < prevValue:
            self.lPutOIChange.setStyleSheet("color: red")

        self.lPutOIChange.setText(str(newValue))
        