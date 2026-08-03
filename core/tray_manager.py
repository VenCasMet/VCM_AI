from PyQt5.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QAction
)

from PyQt5.QtGui import QIcon


class TrayManager:

    def __init__(self, app):

        self.app = app

        self.tray = None

    def create(self, icon_path):

        self.tray = QSystemTrayIcon(

            QIcon(icon_path),

            self.app

        )

        menu = QMenu()

        self.show_action = QAction(

            "Open",

            self.app

        )

        self.listen_action = QAction(

            "Start Listening",

            self.app

        )

        self.exit_action = QAction(

            "Exit",

            self.app

        )

        menu.addAction(

            self.show_action

        )

        menu.addAction(

            self.listen_action

        )

        menu.addSeparator()

        menu.addAction(

            self.exit_action

        )

        self.tray.setContextMenu(menu)

        self.tray.show()
        