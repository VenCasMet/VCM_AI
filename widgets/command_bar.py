from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton
)


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

        self.micBtn = QPushButton("🎤")
        self.sendBtn = QPushButton("➤")

        self.micBtn.setToolTip("Voice Input")
        self.sendBtn.setToolTip("Send Message")

        ################################################

        for btn in [self.micBtn, self.sendBtn]:

            btn.setObjectName("RoundButton")
            btn.setCursor(Qt.PointingHandCursor)

            # Slightly bigger buttons
            btn.setFixedSize(48, 48)

            # Bigger icon/text
            btn.setStyleSheet("""
                QPushButton#RoundButton {
                    font-size:18px;
                    border-radius:24px;
                }
            """)

        ################################################

        layout.addWidget(self.input, 1)
        layout.addWidget(self.micBtn)
        layout.addWidget(self.sendBtn)