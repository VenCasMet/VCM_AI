import sys
import subprocess
import os
import webbrowser
import pyttsx3
import psutil
import speech_recognition as sr
import threading

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from langchain_ollama import OllamaLLM


# ===== AI MODEL =====
llm = OllamaLLM(model="gemma:2b")

# ===== SPEECH OUTPUT =====
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ===== VOICE INPUT =====
def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

# ===== SYSTEM STATUS =====
def system_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU: {cpu}% | RAM: {ram}%"

# ===== LONG-TERM MEMORY =====
MEMORY_FILE = "memory.txt"

def remember(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def recall_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ===== SMART FILE SEARCH =====
def search_files(name, root="C:\\Users"):
    results = []
    for root_dir, _, files in os.walk(root):
        for file in files:
            if name.lower() in file.lower():
                results.append(os.path.join(root_dir, file))
    return results


# ===== MAIN APP =====
class AssistantApp(QWidget):

    def __init__(self):
        super().__init__()

        # ===== WINDOW SETTINGS =====
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle("VCMtalker AI Assistant")
        self.setGeometry(200, 100, 720, 620)
        self.setWindowIcon(QIcon("VCMtalker.ico"))

        self.always_listening = False

        main_layout = QVBoxLayout(self)

        container = QWidget()
        container.setObjectName("container")
        layout = QVBoxLayout(container)

        title = QLabel("🤖 VCMtalker AI")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setFont(QFont("Segoe UI", 11))

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type your command here...")
        self.input.setFont(QFont("Segoe UI", 11))

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.handle_command)

        voice_btn = QPushButton("🎤 Voice")
        voice_btn.clicked.connect(self.voice_command)

        always_btn = QPushButton("🟢 Always Listen")
        always_btn.clicked.connect(self.toggle_always_listen)

        layout.addWidget(title)
        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addWidget(send_btn)
        layout.addWidget(voice_btn)
        layout.addWidget(always_btn)

        main_layout.addWidget(container)

        # ===== STYLE =====
        self.setStyleSheet("""
        #container {
            background-color: rgba(30, 30, 30, 180);
            border-radius: 16px;
        }
        QLabel { color: white; }
        QTextEdit {
            background-color: rgba(0,0,0,120);
            border-radius: 10px;
            padding: 10px;
            color: white;
        }
        QLineEdit {
            background-color: rgba(0,0,0,120);
            border-radius: 10px;
            padding: 8px;
            color: white;
        }
        QPushButton {
            background-color: rgba(41,121,255,200);
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
            color: white;
        }
        QPushButton:hover {
            background-color: rgba(83,147,255,230);
        }
        """)

    # ===== DRAG WINDOW =====
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    # ===== TEXT COMMAND =====
    def handle_command(self):
        command = self.input.text().lower()
        self.chat.append(f"<b>You:</b> {command}")
        self.input.clear()

        response = self.process_command(command)

        self.chat.append(f"<b>VCM:</b> {response}")
        speak(response)

    # ===== SINGLE VOICE COMMAND =====
    def voice_command(self):
        self.chat.append("<i>Listening...</i>")
        command = listen_voice().lower()
        self.chat.append(f"<b>You (voice):</b> {command}")

        response = self.process_command(command)

        self.chat.append(f"<b>VCM:</b> {response}")
        speak(response)

    # ===== ALWAYS LISTEN MODE =====
    def toggle_always_listen(self):
        self.always_listening = not self.always_listening
        if self.always_listening:
            self.chat.append("<i>Always listening ON</i>")
            threading.Thread(target=self.always_listen_loop, daemon=True).start()
        else:
            self.chat.append("<i>Always listening OFF</i>")

    def always_listen_loop(self):
        while self.always_listening:
            command = listen_voice().lower()
            if command:
                self.chat.append(f"<b>You (voice):</b> {command}")
                response = self.process_command(command)
                self.chat.append(f"<b>VCM:</b> {response}")
                speak(response)

    # ===== NATURAL LANGUAGE COMMAND ENGINE =====
    def process_command(self, command):

        # ---- MEMORY ----
        if "remember" in command:
            info = command.replace("remember", "").strip()
            remember(info)
            return "I will remember that."

        if "what do you remember" in command:
            return recall_memory() or "I remember nothing yet."

        # ---- FILE ASSISTANT ----
        if "find file" in command or "search file" in command:
            name = command.split("file")[-1].strip()
            results = search_files(name)
            return "\n".join(results[:5]) if results else "No files found"

        # ---- SYSTEM STATUS ----
        if "status" in command or "cpu" in command or "ram" in command:
            return system_status()

        # ---- NATURAL APP CONTROL ----
        if "notepad" in command:
            subprocess.Popen("notepad.exe")
            return "Opening Notepad"

        if "calculator" in command:
            subprocess.Popen("calc.exe")
            return "Opening Calculator"

        if "chrome" in command:
            webbrowser.open("https://www.google.com")
            return "Opening Chrome"

        if "search google" in command:
            query = command.replace("search google", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for {query}"

        # ---- CONVERSATIONAL AI WITH MEMORY ----
        memory_context = recall_memory()
        prompt = f"Memory: {memory_context}\nUser: {command}"
        return llm.invoke(prompt)


# ===== RUN =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssistantApp()
    window.show()
    sys.exit(app.exec_())
