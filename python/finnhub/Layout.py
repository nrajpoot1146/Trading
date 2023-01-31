import PyQt6.QtWidgets as qw
from PyQt6 import QtCore, QtGui, uic

class CELayout(qw.QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(CELayout, self).__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
        self.addSpacing(0)
        self.addStretch(1)
        #self.setGeometry(QtCore.QRect(0, 0, 100, 100))
        
        for i in range(10):
            label = qw.QLabel()
            label.setStyleSheet("background-color: black; margin: 0; padding: 0; color: white")
            label.setText("hellofjsdfjsdfj "+str(i))
            self.addWidget(label)
        
    @staticmethod
    def getFixedSizeWidget(width:int):
        widget = qw.QWidget()
        widget.setLayout(CELayout())
        widget.setFixedWidth(width)
        return widget
    pass

class MainLayout(qw.QGridLayout):
    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        self.topLayout = qw.QHBoxLayout()
        self.topLayout.addWidget(CELayout.getFixedSizeWidget(200))
        self.addLayout(self.topLayout, 0, 0)
    pass