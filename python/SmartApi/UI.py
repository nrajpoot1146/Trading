import sys
import os
from pathlib import Path
# from System import MainSystem
sys.path.append('E:/Trading/python/')
import threading

currDir = os.path.dirname(__file__)
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton
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

        self.selectedOptionChains = self.system.symbolsInfo.getSymbolNearCurrentPrice('NIFTY', 17751, '09FEB2023')
        self.mainWindow.updateSymbols(self.selectedOptionChains)

    def run(self):
        self.app.exec()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, system):
        super(MainWindow, self).__init__()
        uic.load_ui.loadUi(currDir + r'\..\ui\MainWindow.ui', self)
        self.system = system
        self.actionLogin.triggered.connect(self.onActionLoginClick)
        self.actionLogout.triggered.connect(self.onActionLogoutClick)
        self.start.clicked.connect(self.onStartClick)
        sys.stdout = Stream(newText=self.addInConsole)
        self.teConsole.setReadOnly(True)

    def addInConsole(self, text):
        self.teConsole.insertPlainText(text)
        self.teConsole.moveCursor(QtGui.QTextCursor.MoveOperation.End)
    
    def updateSymbols(self, symbols):
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
            self.system.subscribe(self.system.ui.selectedOptionChains)
        except Exception as e:
            print(e.__traceback__.tb_frame)
        
class Row(QWidget):
    calloisigna = QtCore.pyqtSignal(str)
    putoisigna = QtCore.pyqtSignal(str)
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

        self.calloisigna.connect(self.lCallOIChange.setText)
        self.putoisigna.connect(self.lPutOIChange.setText)

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
        self.pbCall.setText(data.lastTradedPrice)
        pass

    def onPELTPChange(self, symbol, data):
        self.pbPut.setText(data.lastTradedPrice)
        pass

    def onCEOIChange(self, symbol, data):
        if data.perChange != None and data.perChange != "":
            self.calloisigna.emit(data.perChange)
        # self.lCallOIChange.setText(data.volume)
        pass

    def onPEOIChange(self, symbol, data):
        if data.perChange != None and data.perChange != "":
            self.putoisigna.emit(data.perChange)
        # self.lPutOIChange.setText(data.volume)
        pass