import os
import shutil
import subprocess
import sys
import time


class Installer:

    ########################################################
    # Generic Command Runner
    ########################################################

    @staticmethod
    def run_command(command, callback=None):

        try:

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True
            )

            while True:

                line = process.stdout.readline()

                if not line and process.poll() is not None:
                    break

                if line:

                    line = line.strip()

                    if callback:
                        callback(line)

            process.wait()

            if process.returncode == 0:

                return True, "Success"

            return False, f"Command failed ({process.returncode})"

        except Exception as e:

            return False, str(e)

    ########################################################
    # Ollama
    ########################################################

    @staticmethod
    def install_ollama(callback=None):

        import os
        import shutil
        import subprocess
        import time

    #######################################################
    # Already Installed
    #######################################################

        if shutil.which("ollama"):

            if callback:
                callback("✅ Ollama already installed.")

            return True, "Already Installed"

    #######################################################
    # Installer Path
    #######################################################

        installer = os.path.join(

            os.getcwd(),

            "installers",

            "OllamaSetup.exe"

        )

        if not os.path.exists(installer):

            return False, "OllamaSetup.exe not found."

    #######################################################
    # Silent Install
    #######################################################

        if callback:

            callback("Installing Ollama...")

        try:

            process = subprocess.Popen(

                [

                    installer,

                    "/VERYSILENT",

                    "/SUPPRESSMSGBOXES",

                    "/NORESTART"

            ]

            )

            process.wait()

        except Exception as e:

            return False, str(e)

    #######################################################
    # Wait Until PATH Updates
    #######################################################

        if callback:

            callback("Verifying installation...")

        for _ in range(60):

            if shutil.which("ollama"):

                if callback:

                    callback("✅ Ollama Installed.")

                return True, "Installed"

            time.sleep(2)

        return False, "Unable to verify Ollama installation."
    ########################################################
    # Verify Model
    ########################################################

    @staticmethod
    def has_model(model):

        try:

            output = subprocess.check_output(

                ["ollama", "list"],

                text=True

            )

            return model.lower() in output.lower()

        except Exception:

            return False

    ########################################################
    # qwen2.5
    ########################################################

    @staticmethod
    def install_qwen(callback=None):

        if Installer.has_model("qwen2.5:7b"):

            if callback:
                callback("qwen2.5:7b already installed.")

            return True, "Already installed."

        if callback:

            callback("Downloading qwen2.5:7b...")

        return Installer.run_command(

            [

                "ollama",

                "pull",

                "qwen2.5:7b"

            ],

            callback

        )

    ########################################################
    # nomic embedding
    ########################################################

    @staticmethod
    def install_embedding(callback=None):

        if Installer.has_model("nomic-embed-text"):

            if callback:
                callback("nomic-embed-text already installed.")

            return True, "Already installed."

        if callback:

            callback("Downloading nomic-embed-text...")

        return Installer.run_command(

            [

                "ollama",

                "pull",

                "nomic-embed-text"

            ],

            callback

        )

    ########################################################
    # Playwright
    ########################################################

    @staticmethod
    def has_playwright():

        try:

            subprocess.check_output(

                [

                    sys.executable,

                    "-m",

                    "playwright",

                    "--version"

                ],

                stderr=subprocess.STDOUT,

                text=True

            )

            return True

        except Exception:

            return False

    ########################################################
    # Chromium
    ########################################################

    @staticmethod
    def install_playwright(callback=None):

        if callback:

            callback("Checking Playwright...")

        if not Installer.has_playwright():

            if callback:

                callback("Installing Playwright...")

            ok, msg = Installer.run_command(

                [

                    sys.executable,

                    "-m",

                    "pip",

                    "install",

                    "playwright"

                ],

                callback

            )

            if not ok:

                return False, msg

        if callback:

            callback("Installing Chromium...")

        ok, msg = Installer.run_command(

            [

                sys.executable,

                "-m",

                "playwright",

                "install",

                "chromium"

            ],

            callback

        )

        if not ok:

            return False, msg

        if callback:

            callback("Chromium installed successfully.")

        return True, "Playwright ready."