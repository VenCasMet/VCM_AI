import sys
import os
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSlot
from core.auto_programmer import AutoProgrammer
from rag_engine import RAGEngine
from intent_router import IntentRouter
from worker_threads import VoiceWorker, LLMWorker, TTSWorker
from core.tool_manager import ToolManager
from core.session_manager import SessionManager
from tools.browser_agent import BrowserAgent
from tools.browser_tools import BrowserTools
from tools.cmd_tools import CMDTools
from tools.system_tools import SystemTools
from tools.file_tools import FileTools
from core.native_hotkey import NativeHotkey
from core.tray_manager import TrayManager
from PyQt5.QtWidgets import QSystemTrayIcon
from core.single_instance import SingleInstance


class AssistantApp(QWidget):

    def __init__(self):
        super().__init__()
        self.rag_engine = RAGEngine(ollama_model="qwen2.5:7b")
        self.rag_engine.auto_index_project_docs()
        self.voice_worker = None
        self.llm_worker = None
        self.tts_worker = None
        self.voice_enabled = True
        self.busy = False
        self.tool_manager = ToolManager()

        self.session_manager = SessionManager()

        self.browser = BrowserTools()

        self.file_tools = FileTools()

        self.browser_agent = BrowserAgent(self.browser)

        self.cmd = CMDTools()

        self.hotkey = NativeHotkey(

            QApplication.instance(),

            self.hotkey_pressed

        )

        self.tray_manager = TrayManager(self)

        self.system = SystemTools()

        self.programmer = AutoProgrammer()

        self.tool_manager.register(
            "browser.google_search",
            self.browser.google_search,
            "Browser"
        )

        self.tool_manager.register(
            "browser.youtube_search",
            self.browser.youtube_search,
            "Browser"
        )

        self.tool_manager.register(
            "browser.open_url",
            self.browser.goto,
            "Browser"
        )

        self.tool_manager.register(
            "cmd.execute",
            self.cmd.execute_and_wait,
            "Terminal"
        )

        self.init_ui()
        self.intent_router = IntentRouter(
            self.model_selector.currentText()
        )
        icon_path = os.path.join(
        os.path.dirname(__file__),
        "VCMtalker.ico"
        )

        self.tray_manager.create(
            icon_path
        )
        self.tray_manager.show_action.triggered.connect(
            self.restore_window
        )

        self.tray_manager.listen_action.triggered.connect(
            self.start_voice_input
        )

        self.tray_manager.exit_action.triggered.connect(
            QApplication.quit
        )

        self.tray_manager.tray.activated.connect(
            self.tray_icon_clicked
        )
        self.intent_router.set_tool_manager(
            self.tool_manager
        )

        self.intent_router.set_session_manager(
            self.session_manager
        )

        try:

            self.hotkey.register()

        except Exception as e:

            print(e)

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("VCMtalker AI Assistant")
        self.setGeometry(200, 100, 780, 680)
        
        icon_path = os.path.join(os.path.dirname(__file__), "VCMtalker.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout(self)

        container = QWidget()
        container.setObjectName("container")
        layout = QVBoxLayout(container)
        header_layout = QHBoxLayout()

        title = QLabel("🤖 VCMtalker AI Assistant")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))

        self.model_selector = QComboBox()
        self.model_selector.addItems(["qwen2.5:7b", "gemma:2b"])
        self.model_selector.currentTextChanged.connect(
    self.change_model
)
        self.model_selector.setFont(QFont("Segoe UI", 10))
        self.voice_toggle = QPushButton("🔊 Voice ON")
        self.voice_toggle.setChecked(True)
        self.voice_toggle.setCheckable(True)
        self.voice_toggle.clicked.connect(self.toggle_voice)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setObjectName("close_btn")
        close_btn.clicked.connect(self.close)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Model:"))
        header_layout.addWidget(self.model_selector)

        header_layout.addSpacing(10)
        header_layout.addWidget(self.voice_toggle)

        header_layout.addWidget(close_btn)

        self.status_label = QLabel("🟢 Status: Ready (RAG Vector Store Active)")
        self.status_label.setFont(QFont("Segoe UI", 9, QFont.StyleItalic))
        self.status_label.setStyleSheet("color: #81c784; padding-bottom: 4px;")

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setFont(QFont("Segoe UI", 10))

        self.chat.append(
            "<div style='color: #4fc3f7; font-size: 14px;'><b>🤖 Welcome to VCMtalker AI!</b><br>"
            "I am equipped with <b>Vector Database RAG</b> for intelligent memory and document searching.<br>"
            "You can ask me questions, index files (PDF/DOCX/TXT), search local files, or manage your system.</div><br>"
        )
        self.scroll_to_bottom()

        input_layout = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type your question or command here...")
        self.input.setFont(QFont("Segoe UI", 11))
        self.input.returnPressed.connect(self.handle_command)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.handle_command)

        input_layout.addWidget(self.input)
        input_layout.addWidget(self.send_btn)

        action_layout = QHBoxLayout()

        voice_btn = QPushButton("🎤 Voice Command")
        voice_btn.clicked.connect(self.start_voice_input)

        index_btn = QPushButton("📁 Index Document")
        index_btn.clicked.connect(self.index_document_dialog)

        memory_btn = QPushButton("🧠 View Memories")
        memory_btn.clicked.connect(self.view_memories)

        clear_btn = QPushButton("🧹 Clear Chat")
        clear_btn.clicked.connect(self.clear_chat)
        

        action_layout.addWidget(voice_btn)
        action_layout.addWidget(index_btn)
        action_layout.addWidget(memory_btn)
        action_layout.addWidget(clear_btn)

        layout.addLayout(header_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.chat)
        layout.addLayout(input_layout)
        layout.addLayout(action_layout)

        main_layout.addWidget(container)

        self.setStyleSheet("""
        #container {
            background-color: rgba(25, 28, 36, 235);
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 16px;
            padding: 12px;
        }
        QLabel { color: #ffffff; }
        QTextEdit {
            background-color: rgba(15, 18, 24, 180);
            border: 1px solid rgba(255, 255, 255, 20);
            border-radius: 12px;
            padding: 12px;
            color: #e0e0e0;
        }
        QLineEdit {
            background-color: rgba(15, 18, 24, 200);
            border: 1px solid rgba(41, 121, 255, 150);
            border-radius: 10px;
            padding: 8px 12px;
            color: white;
        }
        QComboBox {
            background-color: rgba(40, 44, 56, 220);
            color: white;
            border-radius: 6px;
            padding: 4px 8px;
        }
        QPushButton {
            background-color: rgba(41, 121, 255, 200);
            border-radius: 10px;
            padding: 8px 14px;
            font-weight: bold;
            color: white;
        }
        QPushButton:hover {
            background-color: rgba(83, 147, 255, 230);
        }
        #close_btn {
            background-color: rgba(244, 67, 54, 180);
            border-radius: 15px;
            font-weight: bold;
        }
        #close_btn:hover {
            background-color: rgba(244, 67, 54, 230);
        }
        """)

    def clear_chat(self):
    
                self.chat.clear()
    
                self.chat.append(
                    "<div style='color:#4fc3f7;'>"
                    "<b>🤖 Welcome back!</b><br>"
                    "How can I help you today?"
                    "</div><br>"
                )
                self.scroll_to_bottom()
    def change_model(self, model):

        self.intent_router = IntentRouter(model)

        self.intent_router.set_tool_manager(
           self.tool_manager
        )

        self.intent_router.set_session_manager(
           self.session_manager
        )

    def toggle_voice(self):

        self.voice_enabled = self.voice_toggle.isChecked()

        if self.voice_enabled:

            self.voice_toggle.setText("🔊 Voice ON")

        else:

            self.voice_toggle.setText("🔇 Voice OFF")

            if self.tts_worker and self.tts_worker.isRunning():

                self.tts_worker.stop()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def restore_window(self):

        self.showNormal()

        self.raise_()

        self.activateWindow()

    def tray_icon_clicked(self, reason):

        from PyQt5.QtWidgets import QSystemTrayIcon

        if reason == QSystemTrayIcon.DoubleClick:

            self.restore_window()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def scroll_to_bottom(self):

        scrollbar = self.chat.verticalScrollBar()

        scrollbar.setValue(scrollbar.maximum())

    def update_status(self, text: str, color: str = "#81c784"):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color}; padding-bottom: 4px;")

    def handle_command(self):
        if self.busy:
            self.update_status("⏳ Please wait...", "#ffb74d")
            return
        command = self.input.text().strip()
        if not command:
            return

        self.chat.append(f"<div style='color: #90caf9;'><b>You:</b> {command}</div>")
        self.scroll_to_bottom()
        self.input.clear()
        self.process_command(command)

    def start_voice_input(self):
        self.update_status("🎤 Status: Listening...", "#ffb74d")
        self.chat.append("<i>🎤 Listening... speak into your microphone...</i>")
        self.scroll_to_bottom()
        
        self.voice_worker = VoiceWorker()
        self.voice_worker.result_signal.connect(self.on_voice_recognized)
        self.voice_worker.error_signal.connect(self.on_voice_error)
        self.voice_worker.start()

    @pyqtSlot(str)
    def on_voice_recognized(self, text: str):
        self.update_status("🟢 Status: Speech Recognized", "#81c784")
        self.chat.append(f"<div style='color: #90caf9;'><b>You (Voice):</b> {text}</div>")
        self.scroll_to_bottom()
        self.process_command(text)

    @pyqtSlot(str)
    def on_voice_error(self, err: str):
        self.update_status("🟢 Status: Ready", "#81c784")
        self.chat.append(f"<div style='color: #e57373;'><i>{err}</i></div>")
        self.scroll_to_bottom()


    def hotkey_pressed(self):

        self.restore_window()

        self.start_voice_input()

    def process_command(self, command: str):

        intent, payload = self.intent_router.route(command)

        if intent == "CREATE_PROGRAM":

            prompt = payload["prompt"]

            filename = "program.py"

            lower = prompt.lower()

            keywords = [

                "calculator",
                "snake",
                "tic tac toe",
                "weather",
                "flask",
                "api",
                "server",
                "todo",
                "chatbot",
                "game",
                "password",
                "qr"

            ]

            for word in keywords:

                if word in lower:

                    filename = word.replace(" ", "_") + ".py"

                    break

            self.display_and_speak_response(
                f"🧠 Creating {filename}..."
            )

            ok, output = self.programmer.build(

                f"AI_TEST/{filename}",

                prompt

            )

            self.display_and_speak_response(output)

            return

        if intent == "REMEMBER":

            response = self.rag_engine.add_memory(

                payload["fact"]

            )   

            self.display_and_speak_response(response)

            return

        if intent == "RECALL_MEMORY":

            memories = self.rag_engine.get_all_memories()

            if memories:

                text = "🧠 <b>Stored Memories</b><br><br>"

                for mem in memories:

                    text += f"• {mem}<br>"

            else:

                text = "No memories stored."

            self.display_and_speak_response(text)

            return

        if intent == "OPEN_CMD":

            ok, msg = self.cmd.open()

            if ok:

                self.session_manager.register(

                    "cmd",

                    self.cmd,

                    "terminal"

                )

                self.session_manager.activate(

                    "cmd"

                )

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_BROWSER":

            browser_name = payload.get(

                "browser",

                "brave"

            )

            ok, msg = self.browser.start_browser(

                browser_name

            )

            if ok:

                self.session_manager.register(

                    "browser",

                    self.browser,

                    "browser"

                )

                self.session_manager.activate(

                    "browser"

                )

            self.display_and_speak_response(msg)

            return
        if intent == "BROWSER_CLICK":

            ok, msg = self.browser_agent.click_best_link(

                payload["target"]

            )

            if not ok:

                ok, msg = self.browser_agent.click_best_button(

                    payload["target"]

                )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_FILL":

            ok, msg = self.browser_agent.fill_best_input(

                payload["target"],

                payload["value"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_SELECT":

            ok, msg = self.browser_agent.select_dropdown(

                payload["target"],

                payload["value"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_CHECK":

            ok, msg = self.browser_agent.check_checkbox(

                payload["target"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_UNCHECK":

            ok, msg = self.browser_agent.uncheck_checkbox(

                payload["target"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_READ_HEADINGS":

            ok, data = self.browser.read_headings()

            if ok:

                msg = "\n".join(data)

            else:

                msg = data

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_READ_TABLES":

            ok, data = self.browser.read_tables()

            self.display_and_speak_response(str(data))

            return

        if intent == "BROWSER_READ_IMAGES":

            ok, data = self.browser.read_images()

            self.display_and_speak_response(str(data))

            return

        if intent == "BROWSER_BACK":

            ok, msg = self.browser.back()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_FORWARD":

            ok, msg = self.browser.forward()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_REFRESH":

            ok, msg = self.browser.refresh()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_NEW_TAB":

            ok, msg = self.browser.new_tab()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_CLOSE_TAB":

            ok, msg = self.browser.close_tab()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_SCREENSHOT":

            ok, msg = self.browser.screenshot()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_CLICK_FIRST_LINK":

            ok, msg = self.browser_agent.click_first_link()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_CLICK_LINK_INDEX":

            ok, msg = self.browser_agent.click_link_index(

                payload["index"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_CLICK_FIRST_BUTTON":

            ok, msg = self.browser_agent.click_first_button()

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_CLICK_BUTTON_INDEX":

            ok, msg = self.browser_agent.click_button_index(

                payload["index"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "BROWSER_READ_PAGE":

            ok, data = self.browser_agent.read_page()

            self.display_and_speak_response(

                data if ok else str(data)

            )

            return

        if intent == "BROWSER_READ_LINKS":

            ok, data = self.browser_agent.read_links()

            if ok:

                text = ""

                for i, item in enumerate(data, 1):

                    label = item.get("text") or item.get("href") or "(empty)"

                    text += f"{i}. {label}\n"

            else:

                text = str(data)

            self.display_and_speak_response(text)

            return

        if intent == "BROWSER_READ_BUTTONS":

            ok, data = self.browser_agent.read_buttons()

            if ok:

                text = ""

                for i, item in enumerate(data, 1):

                    label = item.get("text") or "(no text)"

                    text += f"{i}. {label}\n"

            else:

                text = str(data)

            self.display_and_speak_response(text)

            return

        if intent == "BROWSER_READ_INPUTS":

            ok, data = self.browser_agent.read_inputs()

            if ok:

                text = ""

                for i, item in enumerate(data, 1):

                    name = item.get("name") or ""

                    placeholder = item.get("placeholder") or ""

                    text += f"{i}. {name} {placeholder}\n"

            else:

                text = str(data)

            self.display_and_speak_response(text)

            return

        if intent == "GOOGLE_SEARCH":

            ok, msg = self.browser.google_search(

                payload["query"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "YOUTUBE_SEARCH":

            ok, msg = self.browser.youtube_search(

                payload["query"]

            )

            self.display_and_speak_response(msg)

            return
        if intent == "GITHUB_SEARCH":

            url = (

                "https://github.com/search?q=" +

                payload["query"].replace(

                    " ",

                    "+"

                )

            )

            ok, msg = self.browser.goto(

                url

            )

            if not ok:

                msg = f"Opened {url}"

            self.display_and_speak_response(

                msg

            )

            return

        if intent == "WIKIPEDIA_SEARCH":

            url = (

                "https://en.wikipedia.org/wiki/Special:Search?search=" +

                payload["query"].replace(

                    " ",

                    "+"

                )

            )

            ok, msg = self.browser.goto(

                url

            )

            if not ok:

                msg = f"Opened {url}"

            self.display_and_speak_response(

                msg

            )

            return
        if intent == "SEARCH_CURRENT_PAGE":

            ok, text = self.browser.current_page_text()

            if ok:

                self.display_and_speak_response(text[:4000])

            else:

                self.display_and_speak_response(text)

            return

        if intent == "SEARCH_PAGE_HTML":

            ok, html = self.browser.current_page_html()

            if ok:

                self.display_and_speak_response(html[:4000])

            else:

                self.display_and_speak_response(html)

            return

        if intent == "SEARCH_GOOGLE_BOX":

            ok, msg = self.browser.search_google_box(

                payload["query"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "SEARCH_YOUTUBE_BOX":

            ok, msg = self.browser.search_youtube_box(

                payload["query"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "PRESS_ENTER":

            ok, msg = self.browser.press_enter()

            self.display_and_speak_response(msg)

            return

        if intent == "WAIT":

            ok, msg = self.browser.wait(

                payload.get(

                    "milliseconds",

                    1000

                )

            )

            self.display_and_speak_response(msg)

            return

        if intent == "ACTION_RESULT":

            self.display_and_speak_response(

                payload["message"]

            )

            return

        if intent == "VOLUME_UP":

            ok, msg = self.system.volume_up()

            self.display_and_speak_response(msg)

            return

        if intent == "VOLUME_DOWN":

            ok, msg = self.system.volume_down()

            self.display_and_speak_response(msg)

            return

        if intent == "SET_VOLUME":

            ok, msg = self.system.set_volume(

                payload["value"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "MUTE":

            ok, msg = self.system.mute()

            self.display_and_speak_response(msg)

            return

        if intent == "UNMUTE":

            ok, msg = self.system.unmute()

            self.display_and_speak_response(msg)

            return

        if intent == "TOGGLE_MUTE":

            ok, msg = self.system.toggle_mute()

            self.display_and_speak_response(msg)

            return

        if intent == "GET_BRIGHTNESS":

            ok, msg = self.system.get_brightness()

            self.display_and_speak_response(msg)

            return

        if intent == "BRIGHTNESS_UP":

            ok, msg = self.system.brightness_up()

            self.display_and_speak_response(msg)

            return

        if intent == "BRIGHTNESS_DOWN":

            ok, msg = self.system.brightness_down()

            self.display_and_speak_response(msg)

            return

        if intent == "SET_BRIGHTNESS":

            ok, msg = self.system.set_brightness(

                payload["value"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "WIFI_ON":

            ok, msg = self.system.wifi_on()

            self.display_and_speak_response(msg)

            return

        if intent == "WIFI_OFF":

            ok, msg = self.system.wifi_off()

            self.display_and_speak_response(msg)

            return

        if intent == "WIFI_STATUS":

            ok, msg = self.system.wifi_status()

            self.display_and_speak_response(msg)

            return

        if intent == "BATTERY":

            ok, msg = self.system.battery()

            self.display_and_speak_response(msg)

            return

        if intent == "CPU_USAGE":

            ok, msg = self.system.cpu_usage()

            self.display_and_speak_response(msg)

            return

        if intent == "RAM_USAGE":

            ok, msg = self.system.ram_usage()

            self.display_and_speak_response(msg)

            return

        if intent == "DISK_USAGE":

            ok, msg = self.system.disk_usage()

            self.display_and_speak_response(msg)

            return

        if intent == "LOCK_PC":

            ok, msg = self.system.lock()

            self.display_and_speak_response(msg)

            return

        if intent == "SLEEP_PC":

            ok, msg = self.system.sleep()

            self.display_and_speak_response(msg)

            return

        if intent == "HIBERNATE_PC":

            ok, msg = self.system.hibernate()

            self.display_and_speak_response(msg)

            return

        if intent == "SHUTDOWN_PC":

            ok, msg = self.system.shutdown()

            self.display_and_speak_response(msg)

            return

        if intent == "RESTART_PC":

            ok, msg = self.system.restart()

            self.display_and_speak_response(msg)

            return

        if intent == "LOGOFF_PC":

            ok, msg = self.system.logoff()

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_SETTINGS":

            ok, msg = self.system.open_settings()

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_TASK_MANAGER":

            ok, msg = self.system.open_task_manager()

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_CONTROL_PANEL":

            ok, msg = self.system.open_control_panel()

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_DEVICE_MANAGER":

            ok, msg = self.system.open_device_manager()

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_EXPLORER":

            ok, msg = self.system.open_explorer()

            self.display_and_speak_response(msg)

            return

        if intent == "IP_ADDRESS":

            ok, msg = self.system.ip_address()

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_FILE":

            ok, msg = self.file_tools.open_file(

                payload["path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "OPEN_FOLDER":

            ok, msg = self.file_tools.open_folder(

                payload["path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "CREATE_FILE":

            ok, msg = self.file_tools.create_file(

                payload["path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "CREATE_FOLDER":

            ok, msg = self.file_tools.create_folder(

                payload["path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "DELETE_FILE":

            ok, msg = self.file_tools.delete_file(

                payload["path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "DELETE_FOLDER":

            ok, msg = self.file_tools.delete_folder(

                payload["path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "RENAME_FILE":

            ok, msg = self.file_tools.rename_file(

                payload["old_path"],

                payload["new_path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "RENAME_FOLDER":

            ok, msg = self.file_tools.rename_folder(

                payload["old_path"],

                payload["new_path"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "COPY_FILE":

            ok, msg = self.file_tools.copy_file(

                payload["source"],

                payload["destination"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "MOVE_FILE":

            ok, msg = self.file_tools.move_file(

                payload["source"],

                payload["destination"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "COPY_FOLDER":

            ok, msg = self.file_tools.copy_folder(

                payload["source"],

                payload["destination"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "MOVE_FOLDER":

            ok, msg = self.file_tools.move_folder(

                payload["source"],

                payload["destination"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "SEARCH_FILE":

            ok, data = self.file_tools.search_files(

                payload["keyword"]

            )

            if ok:

                if data:

                    msg = "\n".join(data)

                else:

                    msg = "No files found."

            else:

                msg = data

            self.display_and_speak_response(msg)

            return

        if intent == "SEARCH_FOLDER":

            ok, data = self.file_tools.search_folders(

                payload["keyword"]

            )

            if ok:

                if data:

                    msg = "\n".join(data)

                else:

                    msg = "No folders found."

            else:

                msg = data

            self.display_and_speak_response(msg)

            return

        if intent == "ZIP_FOLDER":

            ok, msg = self.file_tools.zip_folder(

                payload["source"],

                payload["destination"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "UNZIP_FILE":

            ok, msg = self.file_tools.unzip_file(

                payload["source"],

                payload["destination"]

            )

            self.display_and_speak_response(msg)

            return

        if intent == "RAG_QUERY":

            self.update_status(

                "🧠 Thinking...",

                "#64b5f6"

            )

            prompt = self.rag_engine.build_rag_prompt(

                command

            )

            self.busy = True

            self.send_btn.setEnabled(False)

            self.send_btn.setText(

                "Thinking..."

            )

            self.input.setEnabled(False)

            self.llm_worker = LLMWorker(

                prompt=prompt,

                model_name=self.model_selector.currentText()

            )

            self.llm_worker.result_signal.connect(

                self.on_llm_success

            )

            self.llm_worker.error_signal.connect(

                self.on_llm_error

            )
            self.llm_worker.start()

    @pyqtSlot(str)
    def on_llm_success(self, response: str):
        self.busy = False
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send")
        self.input.setEnabled(True)
        self.update_status("🟢 Status: Ready", "#81c784")
        formatted_resp = response.replace("\n", "<br>")
        self.chat.append(f"<div style='color: #a5d6a7;'><b>VCMtalker:</b><br>{formatted_resp}</div><br>")
        self.scroll_to_bottom()
        self.speak_bg(response)

    @pyqtSlot(str)
    def on_llm_error(self, err: str):
        self.busy = False
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send")
        self.input.setEnabled(True)
        self.update_status("🔴 Status: LLM Error", "#e57373")
        self.chat.append(f"<div style='color: #e57373;'><b>Error:</b> {err}</div><br>")
        self.scroll_to_bottom()

    def display_and_speak_response(self, text: str, speak_text: str = None):
        formatted_text = text.replace("\n", "<br>")
        self.chat.append(f"<div style='color: #a5d6a7;'><b>VCMtalker:</b> {formatted_text}</div><br>")
        self.scroll_to_bottom()
        self.speak_bg(speak_text or text)

    def speak_bg(self, text: str):

        if not self.voice_enabled:
            return

        self.update_status("🔊 Speaking...", "#ba68c8")

        self.tts_worker = TTSWorker(text=text)
        self.tts_worker.finished_signal.connect(
            lambda: self.update_status("🟢 Ready", "#81c784")
        )
        self.tts_worker.start()
    def index_document_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Document to Index into Vector DB", "", "Documents (*.txt *.md *.docx *.pdf)"
        )
        if file_path:
            self.update_status("📁 Status: Indexing Document into Vector DB...", "#ffb74d")
            success, msg = self.rag_engine.index_document(file_path)
            if success:
                self.update_status("🟢 Status: Document Indexed", "#81c784")
                self.chat.append(f"<div style='color: #81c784;'><b>System:</b> {msg}</div><br>")
                self.scroll_to_bottom()
            else:
                self.update_status("🔴 Status: Indexing Failed", "#e57373")
                self.chat.append(f"<div style='color: #e57373;'><b>System:</b> {msg}</div><br>")
                self.scroll_to_bottom()

    def view_memories(self):
        memories = self.rag_engine.get_all_memories()
        if memories:
            msg = "\n".join([f"• {m}" for m in memories])
        else:
            msg = "No memories stored yet."
        QMessageBox.information(self, "Stored Vector Memories", msg)

    def closeEvent(self, event):

        event.ignore()

        self.hide()

        self.tray_manager.tray.showMessage(

            "VCMtalker",

            "Running in System Tray.",

            QSystemTrayIcon.Information,

            2000

        )
    
    def __del__(self):

        try:

            self.hotkey.unregister()

        except:

            pass




if __name__ == "__main__":

    single = SingleInstance()

    if single.already_running():

        print("VCMtalker is already running.")

        sys.exit(0)

    app = QApplication(sys.argv)

    window = AssistantApp()

    window.show()

    sys.exit(app.exec_())