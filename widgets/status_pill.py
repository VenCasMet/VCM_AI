from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel


class StatusPill(QLabel):

    COLORS = {

        "ONLINE": "#00FF88",

        "LISTENING": "#00D4FF",

        "THINKING": "#9D5CFF",

        "EXECUTING": "#FFB000",

        "ERROR": "#FF3355"

    }

    def __init__(self):

        super().__init__()

        self.setAlignment(

            Qt.AlignCenter

        )

        self.setFixedHeight(

            34

        )

        self.set_status(

            "ONLINE"

        )

    ################################################

    def set_status(

        self,

        state

    ):

        color = self.COLORS.get(

            state,

            "#00FF88"

        )

        self.setText(

            f"● {state}"

        )

        self.setStyleSheet(

            f"""

            QLabel{{

                background:#151B26;

                border:1px solid {color};

                border-radius:17px;

                color:{color};

                font-weight:700;

                padding-left:16px;

                padding-right:16px;

            }}

            """

        )