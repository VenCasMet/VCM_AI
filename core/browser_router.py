import re


class BrowserRouter:

    @staticmethod
    def matches(command):

        lower = command.lower().strip()

        patterns = [

            r"^click ",
            r"^(type|enter) ",
            r"^select ",
            r"^(check|tick) ",
            r"^(uncheck|untick) ",
            r"^(read|show|list|tell me|display) ",
            r"^scroll ",
            r"^take screenshot$",
            r"^screenshot$",
            r"^back$",
            r"^forward$",
            r"^refresh$",
            r"^new tab$",
            r"^close tab$"

        ]

        for pattern in patterns:

            if re.match(pattern, lower):

                return True

        return False

    @staticmethod
    def route(command):

        command = command.strip()

        lower = command.lower()

        if lower == "click first link":

            return ("BROWSER_CLICK_FIRST_LINK", {})

        m = re.match(

            r"click\s+(\d+)(?:st|nd|rd|th)?\s+link",

            lower

        )

        if m:

            return (

                "BROWSER_CLICK_LINK_INDEX",

                {

                    "index": int(m.group(1)) - 1

                }

            )

        if lower == "click first button":

            return ("BROWSER_CLICK_FIRST_BUTTON", {})

        m = re.match(

            r"click\s+(\d+)(?:st|nd|rd|th)?\s+button",

            lower

        )

        if m:

            return (

                "BROWSER_CLICK_BUTTON_INDEX",

                {

                    "index": int(m.group(1)) - 1

                }

            )

        m = re.match(

            r"click\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "BROWSER_CLICK",

                {

                    "target": m.group(1).strip()

                }

            )

        m = re.match(

            r"(?:type|enter)\s+(.+?)\s+(?:in|into)\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "BROWSER_FILL",

                {

                    "value": m.group(1).strip(),

                    "target": m.group(2).strip()

                }

            )

        m = re.match(

            r"select\s+(.+?)\s+(?:from|in)\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "BROWSER_SELECT",

                {

                    "value": m.group(1).strip(),

                    "target": m.group(2).strip()

                }

            )

        m = re.match(

            r"(?:check|tick)\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "BROWSER_CHECK",

                {

                    "target": m.group(1).strip()

                }

            )

        m = re.match(

            r"(?:uncheck|untick)\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "BROWSER_UNCHECK",

                {

                    "target": m.group(1).strip()

                }

            )

        if lower == "read page":

            return ("BROWSER_READ_PAGE", {})

        if lower == "read headings":

            return ("BROWSER_READ_HEADINGS", {})

        if lower == "read tables":

            return ("BROWSER_READ_TABLES", {})

        if lower == "read images":

            return ("BROWSER_READ_IMAGES", {})

        if (
            lower == "read links"
            or "all links" in lower
            or "links present" in lower
            or "show links" in lower
            or "list links" in lower
            or "display links" in lower
            or "tell me the links" in lower
            or "tell me all the links" in lower
        ):
            return ("BROWSER_READ_LINKS", {})

        if (
            lower == "read buttons"
            or "all buttons" in lower
            or "buttons present" in lower
            or "show buttons" in lower
        ):
            return ("BROWSER_READ_BUTTONS", {})
        if (
            lower == "read inputs"
            or "all inputs" in lower
            or "input fields" in lower
            or "text fields" in lower
        ):

            return ("BROWSER_READ_INPUTS", {})

        if lower == "back":

            return ("BROWSER_BACK", {})

        if lower == "forward":

            return ("BROWSER_FORWARD", {})

        if lower == "refresh":

            return ("BROWSER_REFRESH", {})

        if lower == "new tab":

            return ("BROWSER_NEW_TAB", {})

        if lower == "close tab":

            return ("BROWSER_CLOSE_TAB", {})

        if lower in [

            "take screenshot",

            "screenshot"

        ]:

            return ("BROWSER_SCREENSHOT", {})

        return None