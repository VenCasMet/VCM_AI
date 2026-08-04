from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (

    QWidget,

    QPushButton,

    QVBoxLayout,

    QLabel,

    QSizePolicy

)


class Sidebar(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName("Sidebar")

        self.setFixedWidth(90)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(10, 20, 10, 20)

        layout.setSpacing(14)

        layout.setAlignment(Qt.AlignTop)

        ################################################

        self.logo = QLabel("VCM")

        self.logo.setAlignment(Qt.AlignCenter)

        self.logo.setObjectName("SidebarLogo")

        layout.addWidget(self.logo)

        ################################################

        self.chatBtn = self.make_button("💬", "Chat")

        self.memoryBtn = self.make_button("🧠", "Memory")

        self.browserBtn = self.make_button("🌍", "Browser")

        self.systemBtn = self.make_button("💻", "System")

        self.filesBtn = self.make_button("📁", "Files")

        self.settingsBtn = self.make_button("⚙", "Settings")

        ################################################

        layout.addWidget(self.chatBtn)

        layout.addWidget(self.memoryBtn)

        layout.addWidget(self.browserBtn)

        layout.addWidget(self.systemBtn)

        layout.addWidget(self.filesBtn)

        layout.addStretch()

        layout.addWidget(self.settingsBtn)

    ################################################

    def make_button(

        self,

        icon,

        tooltip

    ):

        btn = QPushButton(icon)

        btn.setToolTip(tooltip)

        btn.setCursor(Qt.PointingHandCursor)

        btn.setObjectName("SidebarButton")

        btn.setFixedSize(58,58)

        btn.setSizePolicy(

            QSizePolicy.Fixed,

            QSizePolicy.Fixed

        )

        return btn