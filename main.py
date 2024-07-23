from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cohere
import pyttsx3
import sys

class Assist(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initAPI()
        self.initTTS()

    def initUI(self):
        
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

        self.chatListbox = QListWidget(self)
        layout.addWidget(self.chatListbox, 0, 0, 1, 2)
        
        self.chatListbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chatListbox.customContextMenuRequested.connect(self.showContextMenu)
                
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
        
    def initAPI(self):
        self.api_key = 'DL3ttePi3LvY2QuUTgWNfURVeKgh762KRjXZ3ACh'
        self.client = cohere.Client(self.api_key)
        
    def initTTS(self):
        self.engine = pyttsx3.init()
        
    def send(self):
        userText = self.input.text()
        self.chatListbox.addItem(f"You:\n\n{str(userText)}")
        
        try:
            response = self.client.generate(
                model='command-xlarge-nightly',
                prompt=userText,
                max_tokens=1000
            )
            assistText = response.generations[0].text.strip()
            self.chatListbox.addItem(f"Assist:\n\n{assistText}")
        except Exception as e:
            self.chatListbox.addItem(f"Assist:\n\nError: {str(e)}")
        
        self.input.clear()
        
    def voice(self):
        return
    
    def showContextMenu(self, position):
        contextMenu = QMenu(self)
        copyAction = QAction("Copy", self)
        listAction = QAction("List", self)
        
        contextMenu.addAction(copyAction)
        contextMenu.addAction(listAction)
        
        copyAction.triggered.connect(self.copyItem)
        listAction.triggered.connect(self.sayItem)
        
        contextMenu.exec_(self.chatListbox.viewport().mapToGlobal(position))
        
    def copyItem(self):
        selectedItems = self.chatListbox.selectedItems()
        if selectedItems:
            clipboard = QApplication.clipboard()
            clipboard.setText(selectedItems[0].text())
    
    def sayItem(self):
        selectedItems = self.chatListbox.selectedItems()
        if selectedItems:
            text = selectedItems[0].text()
            self.engine.say(text)
            self.engine.runAndWait()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Assist()
    window.show()
    sys.exit(app.exec_())
