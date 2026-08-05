from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QProgressBar,
)

from core.setup_manager import SetupManager
from core.installer import Installer


############################################################
# Worker Thread
############################################################

class SetupWorker(QThread):

    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):

        setup = SetupManager()

        ################################################
        # Internet
        ################################################

        self.progress.emit(10)
        self.status.emit("Checking Internet...")

        deps = setup.check_dependencies()

        if not deps["internet"]:
            self.status.emit("❌ No Internet Connection")
            return

        ################################################
        # Ollama
        ################################################

        self.progress.emit(20)
        self.status.emit("Checking Ollama...")

        if not deps["ollama"]:

            ok, msg = Installer.install_ollama(self.status.emit)

            if not ok:
                self.status.emit(msg)
                return

        ################################################
        # Refresh
        ################################################

        deps = setup.check_dependencies()

        ################################################
        # Qwen
        ################################################

        self.progress.emit(40)
        self.status.emit("Checking qwen2.5...")

        if not deps["qwen"]:

            ok, msg = Installer.install_qwen()

            if not ok:
                self.status.emit(msg)
                return

        ################################################
        # Refresh
        ################################################

        deps = setup.check_dependencies()

        ################################################
        # Embedding
        ################################################

        self.progress.emit(65)
        self.status.emit("Checking Embedding Model...")

        if not deps["embedding"]:

            ok, msg = Installer.install_embedding()

            if not ok:
                self.status.emit(msg)
                return

        ################################################
        # Verify Everything
        ################################################

        if setup.everything_ready():

            setup.mark_completed()

            self.progress.emit(100)

            self.status.emit("✅ Setup Completed!")

        else:

            setup.mark_incomplete()

            self.status.emit("❌ Setup Failed")

            return

        self.finished.emit()


############################################################
# Setup Window
############################################################

class SetupWindow(QWidget):

    def __init__(self, launch_callback=None):

        super().__init__()

        self.launch_callback = launch_callback

        self.setWindowTitle("VCM AI Setup")

        self.resize(600, 420)

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        ################################################

        title = QLabel("Welcome to VCM AI")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:26px;
            font-weight:700;
        """)

        ################################################

        self.status = QLabel("Preparing setup...")

        self.status.setAlignment(Qt.AlignCenter)

        ################################################

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)

        self.progress.setValue(0)

        ################################################

        self.startBtn = QPushButton("Start Setup")

        self.startBtn.setFixedHeight(42)

        self.startBtn.clicked.connect(self.start_setup)

        ################################################

        layout.addStretch()

        layout.addWidget(title)

        layout.addWidget(self.status)

        layout.addWidget(self.progress)

        layout.addWidget(self.startBtn)

        layout.addStretch()

    ########################################################

    def start_setup(self):

        self.progress.setValue(0)

        self.status.setText("Starting setup...")

        self.startBtn.setEnabled(False)

        self.worker = SetupWorker()

        self.worker.progress.connect(self.progress.setValue)

        self.worker.status.connect(self.status.setText)

        self.worker.finished.connect(self.finish_setup)

        self.worker.start()

    ########################################################

    def finish_setup(self):

        self.progress.setValue(100)

        self.status.setText("✅ Everything is Ready!")

        self.startBtn.setEnabled(True)

        self.startBtn.setText("Launch VCM AI")

        try:
            self.startBtn.clicked.disconnect()
        except:
            pass

        self.startBtn.clicked.connect(self.launch_assistant)

    ########################################################

    def launch_assistant(self):

        if self.launch_callback:

            self.launch_callback()

        self.close()