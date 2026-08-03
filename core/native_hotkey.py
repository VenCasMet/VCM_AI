import ctypes

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QAbstractNativeEventFilter


user32 = ctypes.windll.user32

WM_HOTKEY = 0x0312

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002

VK_SPACE = 0x20


class NativeHotkeyFilter(

    QAbstractNativeEventFilter

):

    def __init__(

        self,

        callback

    ):

        super().__init__()

        self.callback = callback

    def nativeEventFilter(

        self,

        eventType,

        message

    ):

        msg = ctypes.wintypes.MSG.from_address(

            int(message)

        )

        if msg.message == WM_HOTKEY:

            self.callback()

            return True, 0

        return False, 0


class NativeHotkey(QObject):

    def __init__(

        self,

        app,

        callback

    ):

        super().__init__()

        self.app = app

        self.filter = NativeHotkeyFilter(

            callback

        )

    def register(self):

        ok = user32.RegisterHotKey(

            None,

            1,

            MOD_CONTROL | MOD_ALT,

            VK_SPACE

        )

        if not ok:

            raise RuntimeError(

                "Failed to register Ctrl+Alt+Space."

            )

        self.app.installNativeEventFilter(

            self.filter

        )

    def unregister(self):

        try:

            user32.UnregisterHotKey(

                None,

                1

            )

        except:

            pass

        try:

            self.app.removeNativeEventFilter(

                self.filter

            )

        except:

            pass