from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

genai.configure(api_key="AIzaSyB58kpyFbG70wMQuR8PhafgF0G4u2q_06c")

def generate_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assist")
        self.setMinimumSize(300, 200)
        self.setWindowIcon(QIcon("icon.png"))
        
        main_layout = QVBoxLayout(self)
        
        self.chat_list = QListWidget(self)
        self.chat_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chat_list.customContextMenuRequested.connect(self.show_menu)
        main_layout.addWidget(self.chat_list)
        
        bottom_panel = QHBoxLayout()
        bottom_panel.setContentsMargins(0, 0, 0, 0)
        bottom_panel.setSpacing(5)
        
        self.text_input = QTextEdit(self)
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.text_input.setMaximumHeight(50)
        
        self.voice_button = QPushButton("Voice", self)
        self.voice_button.setFixedHeight(50)
        self.send_button = QPushButton("Send", self)
        self.send_button.setFixedHeight(50)
        
        bottom_panel.addWidget(self.text_input)
        bottom_panel.addWidget(self.voice_button)
        bottom_panel.addWidget(self.send_button)
        
        main_layout.addLayout(bottom_panel)
        
        self.send_button.clicked.connect(self.send_text)
        self.voice_button.clicked.connect(self.voice_input)
        
        self.tts_engine = pyttsx3.init()

    def send_text(self):
        user_text = self.text_input.toPlainText().strip()
        if user_text:
            self.chat_list.addItem(f"You: {user_text}")
            response = generate_response(user_text)
            self.chat_list.addItem(f"AI: {response}")
            self.text_input.clear()

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.chat_list.addItem("Listening...")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                self.chat_list.addItem(f"You (Voice): {text}")
                response = generate_response(text)
                self.chat_list.addItem(f"AI: {response}")
            except sr.UnknownValueError:
                self.chat_list.addItem("Could not understand audio")
            except sr.RequestError:
                self.chat_list.addItem("Speech Recognition service unavailable")

    def show_menu(self, position):
        menu = QMenu()
        copy_action = menu.addAction("Copy")
        read_action = menu.addAction("Read Selected")
        
        action = menu.exec_(self.chat_list.viewport().mapToGlobal(position))
        if action == copy_action:
            self.copy_text()
        elif action == read_action:
            self.read_selected_text()

    def copy_text(self):
        item = self.chat_list.currentItem()
        if item:
            QApplication.clipboard().setText(item.text())

    def read_selected_text(self):
        item = self.chat_list.currentItem()
        if item:
            self.tts_engine.say(item.text())
            self.tts_engine.runAndWait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatApp = App()
    chatApp.show()
    sys.exit(app.exec_())