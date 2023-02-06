import sys
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QTextBrowser, QVBoxLayout, QWidget

class ConsoleWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        # self.setReadOnly(True)

class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.console = ConsoleWidget()
        self.setCentralWidget(self.console)

app = QApplication(sys.argv)

app.mainWindow = MainWindow()
app.mainWindow.show()

sys.stdout = Stream(newText=app.mainWindow.console.insertPlainText)
sys.stderr = sys.stdout

print("fsdfsdf", end="", sep="")
print("fsdfsdf", end="")

app.exec()