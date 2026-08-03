import re


class SystemRouter:

    @staticmethod
    def matches(command):

        lower = command.lower().strip()

        patterns = [

            r"^brightness",

            r"^brightness up",

            r"^wifi",

            r"^turn on wifi",

            r"^turn off wifi",

            r"^brightness down",

            r"^volume",

            r"^mute",

            r"^unmute",

            r"^brightness",

            r"^battery",

            r"^cpu",

            r"^ram",

            r"^disk",

            r"^lock",

            r"^sleep",

            r"^hibernate",

            r"^shutdown",

            r"^restart",

            r"^logoff",

            r"^logout",

            r"^settings",

            r"^task manager",

            r"^control panel",

            r"^device manager",

            r"^explorer",

            r"^ip"

        ]

        return any(

            re.match(

                pattern,

                lower

            )

            for pattern in patterns

        )

    @staticmethod
    def route(command):

        lower = command.lower().strip()

        if lower == "volume up":

            return (

                "VOLUME_UP",

                {}

            )

        if lower == "volume down":

            return (

                "VOLUME_DOWN",

                {}

            )

        m = re.match(

            r"volume\s+(\d+)",

            lower

        )

        if m:

            return (

                "SET_VOLUME",

                {

                    "value": int(

                        m.group(1)

                    )

                }

            )

        if lower == "mute":

            return (

                "MUTE",

                {}

            )

        if lower == "unmute":

            return (

                "UNMUTE",

                {}

            )

        if lower == "toggle mute":

            return (

                "TOGGLE_MUTE",

                {}

            )

        if lower == "brightness":

            return (

                "GET_BRIGHTNESS",

                {}

            )

        if lower == "brightness up":

            return (

                "BRIGHTNESS_UP",

                {}

            )

        if lower == "brightness down":

            return (

                "BRIGHTNESS_DOWN",

                {}

            )

        if lower == "wifi":

            return (

                "WIFI_STATUS",

                {}

            )

        if lower in [

            "wifi on",

            "turn on wifi",

            "enable wifi"

        ]:

            return (

                "WIFI_ON",

                {}

            )

        if lower in [

            "wifi off",

            "turn off wifi",

            "disable wifi"

        ]:

            return (

                "WIFI_OFF",

                {}

            )
        
        m = re.match(

            r"brightness\s+(\d+)",

            lower

        )

        if m:

            return (

                "SET_BRIGHTNESS",

                {

                    "value": int(

                        m.group(1)

                    )

                }

            )

        if lower == "battery":

            return (

                "BATTERY",

                {}

            )

        if lower == "cpu":

            return (

                "CPU_USAGE",

                {}

            )

        if lower == "ram":

            return (

                "RAM_USAGE",

                {}

            )

        if lower == "disk":

            return (

                "DISK_USAGE",

                {}

            )

        if lower == "lock":

            return (

                "LOCK_PC",

                {}

            )

        if lower == "sleep":

            return (

                "SLEEP_PC",

                {}

            )

        if lower == "hibernate":

            return (

                "HIBERNATE_PC",

                {}

            )

        if lower == "shutdown":

            return (

                "SHUTDOWN_PC",

                {}

            )

        if lower == "restart":

            return (

                "RESTART_PC",

                {}

            )

        if lower in [

            "logoff",

            "logout"

        ]:

            return (

                "LOGOFF_PC",

                {}

            )

        if lower == "settings":

            return (

                "OPEN_SETTINGS",

                {}

            )

        if lower == "task manager":

            return (

                "OPEN_TASK_MANAGER",

                {}

            )

        if lower == "control panel":

            return (

                "OPEN_CONTROL_PANEL",

                {}

            )

        if lower == "device manager":

            return (

                "OPEN_DEVICE_MANAGER",

                {}

            )

        if lower == "explorer":

            return (

                "OPEN_EXPLORER",

                {}

            )

        if lower == "ip":

            return (

                "IP_ADDRESS",

                {}

            )

        return None

