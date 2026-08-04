from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (

    QWidget,

    QLabel,

    QVBoxLayout,

    QHBoxLayout

)


class ToolCard(QWidget):

    def __init__(

        self,

        title,

        message,

        status="SUCCESS",

        icon="⚡"

    ):

        super().__init__()

        self.setObjectName(

            "ToolCard"

        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(

            18,

            14,

            18,

            14

        )

        layout.setSpacing(8)

        ################################################

        header = QHBoxLayout()

        ################################################

        self.icon = QLabel(icon)

        self.icon.setObjectName(

            "ToolIcon"

        )

        ################################################

        self.title = QLabel(title)

        self.title.setObjectName(

            "ToolTitle"

        )

        ################################################

        self.status = QLabel(status)

        self.status.setObjectName(

            "ToolStatus"

        )

        ################################################

        header.addWidget(

            self.icon

        )

        header.addWidget(

            self.title

        )

        header.addStretch()

        header.addWidget(

            self.status

        )

        ################################################

        layout.addLayout(

            header

        )

        ################################################

        self.message = QLabel(message)

        self.message.setWordWrap(True)

        self.message.setObjectName(

            "ToolMessage"

        )

        layout.addWidget(

            self.message
        )