import re

from click import command

from core.browser_router import BrowserRouter
from core.search_router import SearchRouter
from core.system_router import SystemRouter
from core.file_router import FileRouter
from core.ai_intent_parser import AIIntentParser


class IntentRouter:

    def __init__(self, model_name="qwen2.5:7b"):

        self.model_name = model_name
        self.session_manager = None
        self.tool_manager = None
        self.ai_parser = AIIntentParser(
            model_name
        )

    def set_session_manager(self, session_manager):

        self.session_manager = session_manager

    def set_tool_manager(self, tool_manager):

        self.tool_manager = tool_manager

    def route(self, command):

        command = command.strip()

        lower = command.lower()

        if self.session_manager:

            routed = self._route_active_session(

                lower,

                command

            )

            if routed is not None:

                return routed

        routed = self._route_tools(

            lower,

            command

        )

        if routed:

            return routed

        if BrowserRouter.matches(command):
            

            routed = BrowserRouter.route(command)

            if routed:

                return routed

        if SystemRouter.matches(command):

            routed = SystemRouter.route(command)

            if routed:

                return routed

        if FileRouter.matches(command):

            routed = FileRouter.route(command)

            if routed:

                return routed
            
        if SearchRouter.matches(command):

            routed = SearchRouter.route(command)

            if routed:

                return routed

        if self._is_programming_request(lower):

            return (

                "CREATE_PROGRAM",

                {

                    "prompt": command

                }

            )

        remember = re.match(

            r"(remember|remember that|note|save)\s+(.*)",

            lower

        )

        if remember:

            return (

                "REMEMBER",

                {

                    "fact": remember.group(2)

                }

            )

        if lower in [

            "what do you remember",

            "show memory",

            "show memories",

            "recall memory"

        ]:

            return (

                "RECALL_MEMORY",

                {}

            )

        ai_result = self.ai_parser.parse(command)

        if ai_result:

            intent = ai_result.get("intent")

            if intent:

                payload = dict(ai_result)

                payload.pop("intent", None)

                if intent == "RAG_QUERY" and "query" not in payload:
                   payload["query"] = command

            return (intent, payload)

        return (

            "RAG_QUERY",

            {

                "query": command

            }

        )
    def _route_active_session(self, lower, original):

        if self.session_manager is None:

            return None

        current = self.session_manager.current()

        if current is None:

            return None

        current_name = self.session_manager.current_name()

        if current_name == "cmd":

            if lower in [

                "exit cmd",
                "close cmd",
                "close terminal",
                "leave terminal"

            ]:

                self.session_manager.remove("cmd")

                return (

                    "ACTION_RESULT",

                    {

                        "message": "✅ CMD session closed."

                    }

                )

            if lower == "pwd":

                original = "cd"

            elif lower == "ls":

                original = "dir"

            elif lower == "clear":

                original = "cls"

            ok, output = current.execute_and_wait(original)

            return (

                "ACTION_RESULT",

                {

                    "message": output

                }

            )

        if current_name == "browser":

            if lower in [

                "close browser",

                "exit browser"

            ]:

                current.close_browser()

                self.session_manager.remove("browser")

                return (

                    "ACTION_RESULT",

                    {

                        "message": "✅ Browser closed."

                    }

                )

            return None

        return None

    def _route_tools(self, lower, original):

        if lower in [

            "open cmd",

            "open command prompt",

            "start cmd",

            "terminal"

        ]:

            return (

                "OPEN_CMD",

                {}

            )

        if lower.startswith("open brave"):

            return (

                "OPEN_BROWSER",

                {

                    "browser": "brave"

                }

            )

        if lower.startswith("open chrome"):

            return (

                "OPEN_BROWSER",

                {

                    "browser": "chrome"

                }

            )

        return None
    def _is_programming_request(self, lower):

        verbs = [

            "create",
            "make",
            "build",
            "develop",
            "generate",
            "write"

        ]

        subjects = [

            "python",
            "program",
            "script",
            "calculator",
            "game",
            "snake",
            "tic tac toe",
            "flask",
            "fastapi",
            "api",
            "server",
            "weather",
            "todo",
            "chatbot",
            "bot",
            "qr",
            "qrcode",
            "password",
            "converter",
            "ocr",
            "opencv",
            "automation",
            "scraper",
            "web scraper",
            "downloader",
            "gui",
            "tkinter",
            "pygame"

        ]

        has_verb = any(

            word in lower

            for word in verbs

        )

        has_subject = any(

            word in lower

            for word in subjects

        )

        return has_verb and has_subject