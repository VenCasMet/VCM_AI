from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout
)


class TitleBar(QWidget):

    def __init__(

        self,

        parent=None,

        icon_path=None

    ):

        super().__init__(parent)

        self.parent = parent

        self.setFixedHeight(48)

        self.setObjectName("TitleBar")

        layout = QHBoxLayout(self)

        layout.setContentsMargins(14, 6, 10, 6)

        layout.setSpacing(10)

        ################################################

        self.icon = QLabel()

        if icon_path:

            self.icon.setPixmap(

                QIcon(icon_path).pixmap(

                    24,

                    24

                )

            )

        ################################################

        self.title = QLabel(

            "VCM AI"

        )

        self.title.setObjectName(

            "WindowTitle"

        )

        ################################################

        self.status = QLabel(

            "● ONLINE"

        )

        self.status.setObjectName(

            "StatusOnline"

        )

        ################################################

        layout.addWidget(

            self.icon

        )

        layout.addWidget(

            self.title

        )

        layout.addStretch()

        layout.addWidget(

            self.status

        )

        ################################################

        self.btnMin = QPushButton("—")

        self.btnMax = QPushButton("□")

        self.btnClose = QPushButton("✕")

        for b in [

            self.btnMin,

            self.btnMax,

            self.btnClose

        ]:

            b.setFixedSize(

                38,

                32

            )

        layout.addWidget(

            self.btnMin

        )

        layout.addWidget(

            self.btnMax

        )

        layout.addWidget(

            self.btnClose

        )

        ################################################

        self.btnMin.clicked.connect(

            self.parent.showMinimized

        )

        self.btnMax.clicked.connect(

            self.toggleMax

        )

        self.btnClose.clicked.connect(

            self.parent.close

        )

        ################################################

        self.start = None

        ################################################

    def toggleMax(self):

        if self.parent.isMaximized():

            self.parent.showNormal()

            self.btnMax.setText("□")

        else:

            self.parent.showMaximized()

            self.btnMax.setText("❐")

    ################################################

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.start = event.globalPos()

    ################################################

    def mouseMoveEvent(self, event):

        if not self.start:

            return

        if event.buttons() == Qt.LeftButton:

            delta = event.globalPos() - self.start

            self.parent.move(

                self.parent.pos() + delta

            )

            self.start = event.globalPos()

    ################################################

    def mouseReleaseEvent(self, event):

        self.start = None

    ################################################

    def set_status(

        self,

        text,

        color="#00FF88"

    ):

        self.status.setText(text)

        self.status.setStyleSheet(

            f"""

            color:{color};

            font-weight:700;

            """

        )