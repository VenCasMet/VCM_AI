import os
import subprocess
import urllib.parse
import webbrowser
import psutil


class ActionExecutor:

    APP_PATHS = {

        "notepad": "notepad.exe",

        "calculator": "calc.exe",

        "paint": "mspaint.exe",

        "cmd": "cmd.exe",

        "powershell": "powershell.exe",

        "explorer": "explorer.exe",

        "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",

        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        "vscode": r"C:\Users\Piyush\AppData\Local\Programs\Microsoft VS Code\Code.exe"

    }

    WEBSITE_MAP = {

        "chatgpt": "https://chat.openai.com",

        "github": "https://github.com",

        "gmail": "https://mail.google.com",

        "linkedin": "https://linkedin.com",

        "youtube": "https://youtube.com",

        "google": "https://google.com",

        "stackoverflow": "https://stackoverflow.com",

        "leetcode": "https://leetcode.com"

    }

    @staticmethod
    def execute(data):

        intent = data.get("intent", "")

        try:

            if intent == "OPEN_APP":

                return ActionExecutor.open_app(data)

            elif intent == "SEARCH_GOOGLE":

                return ActionExecutor.search_google(data)

            elif intent == "SEARCH_YOUTUBE":

                return ActionExecutor.search_youtube(data)

            elif intent == "OPEN_WEBSITE":

                return ActionExecutor.open_website(data)

            elif intent == "SYSTEM_STATUS":

                return ActionExecutor.system_status()

            elif intent == "SEARCH_FILE":

                return ActionExecutor.search_file(data)

            return False, "Unknown action."

        except Exception as e:

            return False, str(e)

    @staticmethod
    def open_app(data):

        app = data.get("app", "").lower()

        path = ActionExecutor.APP_PATHS.get(app)

        if not path:
            return False, f"Unsupported application '{app}'."

        subprocess.Popen(path)

        return True, f"✅ Opening {app.title()}..."

    @staticmethod
    def search_google(data):

        query = urllib.parse.quote(data.get("query", ""))

        browser = data.get("browser", "default").lower()

        url = f"https://www.google.com/search?q={query}"

        if browser == "brave":

            brave = ActionExecutor.APP_PATHS["brave"]

            if os.path.exists(brave):

                subprocess.Popen([brave, url])

            else:

                webbrowser.open(url)

        else:

            webbrowser.open(url)

        return True, f"🔍 Searching Google for '{data.get('query')}'..."

    @staticmethod
    def search_youtube(data):

        query = urllib.parse.quote(data.get("query", ""))

        browser = data.get("browser", "default").lower()

        url = f"https://www.youtube.com/results?search_query={query}"

        if browser == "brave":

            brave = ActionExecutor.APP_PATHS["brave"]

            if os.path.exists(brave):

                subprocess.Popen([brave, url])

            else:

                webbrowser.open(url)

        else:

            webbrowser.open(url)

        return True, f"▶ Searching YouTube for '{data.get('query')}'..."

    @staticmethod
    def open_website(data):

        site = data.get("site", "").lower()

        url = ActionExecutor.WEBSITE_MAP.get(site)

        if not url:

            return False, "Unknown website."

        webbrowser.open(url)

        return True, f"🌐 Opening {site.title()}..."

    @staticmethod
    def system_status():

        cpu = psutil.cpu_percent(interval=0.5)

        ram = psutil.virtual_memory().percent

        disk = psutil.disk_usage("C:\\").percent

        return (

            True,

            f"""💻 SYSTEM STATUS

CPU Usage : {cpu} %

RAM Usage : {ram} %

Disk Usage : {disk} %
"""

        )

    @staticmethod
    def search_file(data):

        target = data.get("filename", "").lower()

        results = []

        home = os.path.expanduser("~")

        for root, _, files in os.walk(home):

            for file in files:

                if target in file.lower():

                    results.append(os.path.join(root, file))

                if len(results) >= 10:

                    break

            if len(results) >= 10:

                break

        if not results:

            return True, f"No file named '{target}' found."

        msg = "📁 Found Files\n\n"

        for path in results:

            msg += path + "\n"

        return True, msg