import sys
import os
from pathlib import Path
# from System import MainSystem
sys.path.append('E:/Trading/python/')
import threading

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


tr = False
class MainWindow(QtWidgets.QMainWindow):
    updateSymbolSignal = QtCore.pyqtSignal(list)

    def __init__(self, system):
        super(MainWindow, self).__init__()
        uic.load_ui.loadUi(currDir + r'\..\ui\MainWindow.ui', self)
        self.system = system
        self.selectedOptionChains = []

        self.actionLogin.triggered.connect(self.onActionLoginClick)
        self.actionLogout.triggered.connect(self.onActionLogoutClick)
        self.start.clicked.connect(self.onStartClick)
        self.stop.clicked.connect(self.onStopClick)
        self.stop.setEnabled(False)
        # sys.stdout = Stream(newText=self.addInConsole)
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
                    self.indexWatchList[i].getSymbolInstance().unSubscribeOnFeedRecived(self.onPriceUpdate)
            self.indexWatchList[index].getSymbolInstance().subscribeOnFeedRecived(self.onPriceUpdate)
            self.cbIndices.setEnabled(False)
            self.stop.setEnabled(True)
        except Exception as e:
            pass
        # self.onFlagUpdate = False

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

        if newPrice > prevPrice:
            self.lindexltp.setStyleSheet("color: green")
        elif newPrice < prevPrice:
            self.lindexltp.setStyleSheet("color: red")

        self.lindexltp.setText(data.lastTradedPrice)

        if self.onFlagUpdate == False:
            self.selectedOptionChains = self.system.symbolsInfo.getSymbolNearCurrentPrice(symbol.symbolInfo.name, float(data.lastTradedPrice), '09FEB2023')
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
    calloisignal = QtCore.pyqtSignal(str)
    putoisignal = QtCore.pyqtSignal(str)
    putLTPsignal = QtCore.pyqtSignal(str)
    callLTPsignal = QtCore.pyqtSignal(str)

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

        self.ceSymbol.getSymbolInstance().subscribeOnFeedRecived(self.onCELTPChange)
        self.ceSymbol.getSymbolInstance().subscribeOnFeedRecived(self.onCEOIChange)
        self.peSymbol.getSymbolInstance().subscribeOnFeedRecived(self.onPELTPChange)
        self.peSymbol.getSymbolInstance().subscribeOnFeedRecived(self.onPEOIChange)

        self.calloisignal.connect(self.lCallOIChange.setText)
        self.putoisignal.connect(self.lPutOIChange.setText)
        self.putLTPsignal.connect(self.pbPut.setText)
        self.callLTPsignal.connect(self.pbCall.setText)

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

        if newPrice > prevPrice:
            self.pbCall.setStyleSheet("color: green; background-color: yellow;")
        elif newPrice < prevPrice:
            self.pbCall.setStyleSheet("color: red; background-color: yellow;")

        self.callLTPsignal.emit(str(newPrice))
        pass

    def onPELTPChange(self, symbol, data):
        prevPrice = 0.0
        newPrice = 0.0
        # try:
        #     prevPrice = float(self.pbPut.text())
        # except Exception as e:
        #     pass

        try:
            newPrice = float(data.lastTradedPrice)
        except Exception as e:
            pass

        # if newPrice > prevPrice:
        #     self.pbPut.setStyleSheet("color: green")
        # elif newPrice < prevPrice:
        #     self.pbPut.setStyleSheet("color: red")

        
        self.putLTPsignal.emit(str(newPrice))
        pass

    def onCEOIChange(self, symbol, data):
        # if data.perChange != None and data.perChange != "":
        #     self.calloisigna.emit(data.perChange)

        prevValue = 0.0
        newValue = 0.0
        # try:
        #     prevValue = float(self.lCallOIChange.text())
        # except Exception as e:
        #     pass

        try:
            newValue = float(data.perChange)
        except Exception as e:
            pass

        # if newValue > prevValue:
        #     self.lCallOIChange.setStyleSheet("color: green")
        # elif newValue < prevValue:
        #     self.lCallOIChange.setStyleSheet("color: red")
        # else:
        #     newValue = prevValue
        # self.lCallOIChange.setText(str(newValue))
        self.calloisignal.emit(str(newValue))
        pass

    def onPEOIChange(self, symbol, data):
        # if data.perChange != None and data.perChange != "":
        #     self.putoisigna.emit(data.perChange)
        prevValue = 0.0
        newValue = 0.0
        # try:
        #     prevValue = float(self.lPutOIChange.text())
        # except Exception as e:
        #     pass

        try:
            newValue = float(data.perChange)
        except Exception as e:
            pass

        # if newValue > prevValue:
        #     self.lPutOIChange.setStyleSheet("color: green")
        # elif newValue < prevValue:
        #     self.lPutOIChange.setStyleSheet("color: red")

        # self.lPutOIChange.setText(str(newValue))
        self.putoisignal.emit(str(newValue))
        pass
        