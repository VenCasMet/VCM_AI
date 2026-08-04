import os
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton
)


def resource_path(relative_path):
    """
    Returns the correct path in both development
    and PyInstaller executable.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class CommandBar(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName("CommandBar")
        self.setFixedHeight(72)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        ################################################

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a message...")
        self.input.setObjectName("CommandInput")

        ################################################

        self.micBtn = QPushButton()
        self.sendBtn = QPushButton()

        # Load icons (Works in Python + EXE)
        self.micBtn.setIcon(QIcon(resource_path("assets/mic.png")))
        self.sendBtn.setIcon(QIcon(resource_path("assets/send.png")))

        self.micBtn.setIconSize(QSize(24, 24))
        self.sendBtn.setIconSize(QSize(24, 24))

        self.micBtn.setText("")
        self.sendBtn.setText("")

        self.micBtn.setToolTip("Voice Input")
        self.sendBtn.setToolTip("Send Message")

        ################################################

        for btn in (self.micBtn, self.sendBtn):

            btn.setObjectName("RoundButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(48, 48)

        ################################################

        layout.addWidget(self.input, 1)
        layout.addWidget(self.micBtn)
        layout.addWidget(self.sendBtn)