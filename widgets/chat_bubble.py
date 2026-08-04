from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy
)
from PyQt5.QtCore import Qt


class ChatBubble(QWidget):

    def __init__(self, title, message, user=False):
        super().__init__()

        root = QHBoxLayout(self)
        root.setContentsMargins(12, 4, 12, 4)

        if user:
            root.addStretch()

        bubble = QFrame()
        bubble.setObjectName("userBubble" if user else "aiBubble")

        bubble.setMinimumWidth(220)
        bubble.setMaximumWidth(620)
        bubble.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Minimum
        )

        layout = QVBoxLayout(bubble)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        header = QLabel(title)
        header.setObjectName("bubbleHeader")

        body = QLabel(message)
        body.setWordWrap(True)
        body.setTextFormat(Qt.RichText)
        body.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        layout.addWidget(header)
        layout.addWidget(body)

        root.addWidget(bubble)

        if not user:
            root.addStretch()