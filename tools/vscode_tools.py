import subprocess
import os
import pyautogui
import pyperclip
import time


class VSCodeTools:

    def __init__(self):

        self.process = None

        self.started = False

        self.code_path = self.find_vscode()

    ########################################################

    def find_vscode(self):

        paths = [

            r"C:\Users\Piyush\AppData\Local\Programs\Microsoft VS Code\Code.exe",

            r"C:\Program Files\Microsoft VS Code\Code.exe",

            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"

        ]

        for path in paths:

            if os.path.exists(path):
                return path

        return "code"

    ########################################################

    def open_vscode(self, folder=None):

        try:

            if folder:

                self.process = subprocess.Popen(

                    [self.code_path, folder]

                )

            else:

                self.process = subprocess.Popen(

                    [self.code_path]

                )

            self.started = True

            time.sleep(3)

            return True, "VS Code opened."

        except Exception as e:

            return False, str(e)

    ########################################################

    def open_folder(self, folder):

        try:

            subprocess.Popen(

                [self.code_path, folder]

            )

            self.started = True

            time.sleep(3)

            return True, f"Opened {folder}"

        except Exception as e:

            return False, str(e)

    ########################################################

    def close(self):

        if self.process:

            self.process.terminate()

        self.started = False

        return True, "VS Code closed."

        ########################################################

    def create_file(self, filepath):

        try:

            folder = os.path.dirname(filepath)

            if folder:
                os.makedirs(folder, exist_ok=True)

            if not os.path.exists(filepath):

                with open(filepath, "w", encoding="utf-8"):
                    pass

            subprocess.Popen(

                [self.code_path, filepath]

            )

            time.sleep(2)

            return True, f"Opened {filepath}"

        except Exception as e:

            return False, str(e)

    ########################################################

    def write_file(self, filepath, content):

        try:

            with open(filepath, "w", encoding="utf-8") as f:

                f.write(content)

            return True, "File written."

        except Exception as e:

            return False, str(e)

    ########################################################

    def append_file(self, filepath, content):

        try:

            with open(filepath, "a", encoding="utf-8") as f:

                f.write(content)

            return True, "Content appended."

        except Exception as e:

            return False, str(e)

    ########################################################

    def read_file(self, filepath):

        try:

            with open(filepath, "r", encoding="utf-8") as f:

                return True, f.read()

        except Exception as e:

            return False, str(e)