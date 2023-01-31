import sys

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt6 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import Layout

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 800, 400)
        widget = QWidget()
        widget.setLayout(Layout.MainLayout())
        self.setCentralWidget(widget)
        pass

    def setMessage(self, y):
        self.label.setText(str(y))
        pass
    