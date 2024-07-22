from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Assist(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Assist")
        self.setWindowIcon(QIcon("images/icon.png"))
        self.setMinimumSize(200, 300)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QGridLayout()
        centralWidget.setLayout(layout)
        bottomLayout = QGridLayout()
        buttonsLayout = QHBoxLayout()
        layout.addLayout(bottomLayout, 1, 0)
        bottomLayout.addLayout(buttonsLayout, 0, 1)

        self.chatListbox = QListView(self)
        layout.addWidget(self.chatListbox, 0, 0, 1, 2)
        
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Write your query")
        bottomLayout.addWidget(self.input, 0, 0, 1, 1)
        self.input.returnPressed.connect(self.send)
        
        self.voiceButton = QPushButton(self)
        self.voiceButton.setIcon(QIcon("images/voice.png"))
        buttonsLayout.addWidget(self.voiceButton)
        self.voiceButton.clicked.connect(self.voice)
        
        self.sendButton = QPushButton(self)
        self.sendButton.setIcon(QIcon("images/send.png"))
        buttonsLayout.addWidget(self.sendButton)
        self.sendButton.clicked.connect(self.send)
        
    def send(self):
        return
        
    def voice(self):
        return
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Assist()
    window.show()
    sys.exit(app.exec_())