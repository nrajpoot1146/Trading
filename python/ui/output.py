# Form implementation generated from reading ui file '.\MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(953, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(9, 0, 941, 271))
        self.widget.setObjectName("widget")
        self.CEWidget = QtWidgets.QWidget(self.widget)
        self.CEWidget.setGeometry(QtCore.QRect(0, 0, 313, 261))
        self.CEWidget.setStyleSheet("border: 1px solid red;")
        self.CEWidget.setObjectName("CEWidget")
        self.listView = QtWidgets.QListView(self.CEWidget)
        self.listView.setGeometry(QtCore.QRect(0, 0, 311, 192))
        self.listView.setObjectName("listView")
        self.pushButton = QtWidgets.QPushButton(self.CEWidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 40, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.CEWidget)
        self.label.setGeometry(QtCore.QRect(100, 90, 55, 16))
        self.label.setObjectName("label")
        self.PWidget = QtWidgets.QWidget(self.widget)
        self.PWidget.setGeometry(QtCore.QRect(314, 0, 313, 261))
        self.PWidget.setStyleSheet("border: 1px solid red;")
        self.PWidget.setObjectName("PWidget")
        self.PEWidget = QtWidgets.QWidget(self.widget)
        self.PEWidget.setGeometry(QtCore.QRect(628, 0, 313, 261))
        self.PEWidget.setStyleSheet("border: 1px solid red;")
        self.PEWidget.setObjectName("PEWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 953, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(MainWindow.close)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
