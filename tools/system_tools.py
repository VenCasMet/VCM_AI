import ctypes
import subprocess
import psutil
import os

from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class SystemTools:

    def __init__(self):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(

            IAudioEndpointVolume._iid_,

            CLSCTX_ALL,

            None

        )

        self.volume = cast(

            interface,

            POINTER(IAudioEndpointVolume)

        )

    def volume_up(self, step=10):

        current = self.get_volume()

        return self.set_volume(

            min(

                100,

                current + step

            )

        )

    def volume_down(self, step=10):

        current = self.get_volume()

        return self.set_volume(

            max(

                0,

                current - step

            )

        )

    def get_volume(self):

        level = self.volume.GetMasterVolumeLevelScalar()

        return int(

            level * 100

        )

    def set_volume(self, value):

        value = max(

            0,

            min(

                100,

                int(value)

            )

        )

        self.volume.SetMasterVolumeLevelScalar(

            value / 100,

            None

        )

        return True, f"Volume set to {value}%"

    def mute(self):

        self.volume.SetMute(

            1,

            None

        )

        return True, "Muted."

    def unmute(self):

        self.volume.SetMute(

            0,

            None

        )

        return True, "Unmuted."

    def toggle_mute(self):

        state = self.volume.GetMute()

        self.volume.SetMute(

            0 if state else 1,

            None

        )

        return True, "Mute toggled."

    def lock(self):

        ctypes.windll.user32.LockWorkStation()

        return True, "PC locked."

    def shutdown(self):

        os.system(

            "shutdown /s /t 0"

        )

        return True, "Shutting down."

    def restart(self):

        os.system(

            "shutdown /r /t 0"

        )

        return True, "Restarting."

    def sleep(self):

        ctypes.windll.powrprof.SetSuspendState(

            False,

            True,

            False

        )

        return True, "Sleeping."

    def hibernate(self):

        os.system(

            "shutdown /h"

        )

        return True, "Hibernating."

    def logoff(self):

        os.system(

            "shutdown /l"

        )

        return True, "Logging off."

    def battery(self):

        battery = psutil.sensors_battery()

        if battery is None:

            return False, "Battery information unavailable."

        status = "Charging" if battery.power_plugged else "Not Charging"

        return (

            True,

            f"Battery : {battery.percent}%\nStatus : {status}"

        )

    def cpu_usage(self):

        return (

            True,

            f"CPU Usage : {psutil.cpu_percent(interval=1)}%"

        )

    def ram_usage(self):

        memory = psutil.virtual_memory()

        return (

            True,

            f"RAM Usage : {memory.percent}%"

        )

    def disk_usage(self):

        disk = psutil.disk_usage("C:\\")

        return (

            True,

            f"Disk Usage : {disk.percent}%"

        )

    def open_settings(self):

        subprocess.Popen(

            "start ms-settings:",

            shell=True

        )

        return True, "Settings opened."

    def open_task_manager(self):

        subprocess.Popen(

            "taskmgr"

        )

        return True, "Task Manager opened."

    def open_control_panel(self):

        subprocess.Popen(

            "control"

        )

        return True, "Control Panel opened."

    def open_device_manager(self):

        subprocess.Popen(

            "devmgmt.msc"

        )

        return True, "Device Manager opened."

    def open_explorer(self):

        subprocess.Popen(

            "explorer"

        )

        return True, "File Explorer opened."

    def ip_address(self):

        try:

            output = subprocess.check_output(

                "ipconfig",

                shell=True,

                text=True,

                encoding="utf-8",

                errors="ignore"

            )

            return True, output

        except Exception as e:

            return False, str(e)

    def get_brightness(self):

        try:

            value = sbc.get_brightness()[0]

            return True, f"Brightness : {value}%"

        except Exception as e:

            return False, str(e)

    def set_brightness(self, value):

        try:

            value = max(

                0,

                min(

                    100,

                    int(value)

                )

            )

            sbc.set_brightness(value)

            return True, f"Brightness set to {value}%"

        except Exception as e:

            return False, str(e)

    def brightness_up(self, step=10):

        try:

            current = sbc.get_brightness()[0]

            current = min(

                100,

                current + step

            )

            sbc.set_brightness(current)

            return True, f"Brightness : {current}%"

        except Exception as e:

            return False, str(e)

    def brightness_down(self, step=10):

        try:

            current = sbc.get_brightness()[0]

            current = max(

                0,

                current - step

            )

            sbc.set_brightness(current)

            return True, f"Brightness : {current}%"

        except Exception as e:

            return False, str(e)

    def wifi_status(self):

        try:

            output = subprocess.check_output(

                "netsh interface show interface",

                shell=True,

                text=True,

              encoding="utf-8",

                errors="ignore"

            )

            return True, output

        except Exception as e:

            return False, str(e)

    def wifi_on(self):

        try:

            process = subprocess.run(

                'netsh interface set interface name="Wi-Fi" admin=enabled',

                shell=True,

                capture_output=True,

                text=True

            )

            if process.returncode != 0:

                return False, process.stderr or process.stdout

            return True, "Wi-Fi enabled."

        except Exception as e:

            return False, str(e)

    def wifi_off(self):

        try:

            process = subprocess.run(

                'netsh interface set interface name="Wi-Fi" admin=disabled',

                shell=True,

                capture_output=True,

                text=True

            )

            if process.returncode != 0:

                return False, process.stderr or process.stdout

            return True, "Wi-Fi disabled."

        except Exception as e:

            return False, str(e)