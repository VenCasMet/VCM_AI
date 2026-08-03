import win32event
import win32api
import winerror


class SingleInstance:

    def __init__(

        self,

        name="VCMtalker"

    ):

        self.mutex = win32event.CreateMutex(

            None,

            False,

            name

        )

    def already_running(self):

        return (

            win32api.GetLastError()

            == winerror.ERROR_ALREADY_EXISTS

        )
    