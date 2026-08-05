from PyQt5.QtWidgets import QApplication
import sys

from ui.setup_window import SetupWindow

app = QApplication(sys.argv)

window = SetupWindow()

window.show()

sys.exit(app.exec_())