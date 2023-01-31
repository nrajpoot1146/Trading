import sys
import os
sys.path.append('E:/Trading/python/')

currDir = os.path.dirname(__file__)

import threading
import time
import ui.ui_MainWindow

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PyQt6 import uic, QtWidgets
import MainWindow

import websocket
import finnhub

def on_message(ws, message):
    print(message)
    mainWindow.setMessage(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AMZN"}')

def startWebsocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cf4ogg2ad3i7dbfht0ogcf4ogg2ad3i7dbfht0p0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    mainWindow = None
    app = None
    stop = False

    Form, Window = uic.load_ui.loadUiType(currDir + r'\..\ui\MainWindow.ui')
    FormRow, RowWidget = uic.load_ui.loadUiType(currDir + r'\..\ui\Row.ui')

    app = QApplication([])
    form = Form()
    window:QtWidgets.QMainWindow = Window()

    rowWidget:QWidget = RowWidget()
    formRow = FormRow()
    formRow.setupUi(rowWidget)

    form.setupUi(window)
    window.show()
    print(formRow.pushButton.clicked.connect(lambda x : formRow.label.setText("hello")))

    ceWidget:QWidget = window.findChildren(QWidget, "CEWidget")[0]
    ceWidget.setLayout(QtWidgets.QVBoxLayout())
    ceWidget.layout().addWidget(rowWidget)


    # window = QtWidgets.QMainWindow()
    # ui_main = ui.ui_MainWindow.Ui_MainWindow()
    # ui_main.setupUi(window)
    # window.show()

    

    sys.exit(app.exec())
    stop = True