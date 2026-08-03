import re


class SearchRouter:

    @staticmethod
    def matches(command):

        lower = command.lower().strip()

        patterns = [

            r"^search google",
            r"^google ",

            r"^search youtube",
            r"^youtube ",

            r"^search github",
            r"^github ",

            r"^search wikipedia",
            r"^wikipedia ",

            r"^search current page$",
            r"^read current page$",
            r"^page html$",

            r"^search google box",
            r"^search youtube box",

            r"^press enter$",

            r"^wait "

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

        command = command.strip()

        m = re.match(

            r"search youtube for\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "YOUTUBE_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"youtube\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "YOUTUBE_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"search google for\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "GOOGLE_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"google\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "GOOGLE_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )
        m = re.match(

            r"search github for\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "GITHUB_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"github\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "GITHUB_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"search wikipedia for\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "WIKIPEDIA_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"wikipedia\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "WIKIPEDIA_SEARCH",

                {

                    "query": m.group(1).strip()

                }

            )
        m = re.match(

            r"search current page",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_CURRENT_PAGE",

                {}

            )

        m = re.match(

            r"read current page",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_CURRENT_PAGE",

                {}

            )

        m = re.match(

            r"page html",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_PAGE_HTML",

                {}

            )

        m = re.match(

            r"search google box for\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_GOOGLE_BOX",

                {

                    "query": m.group(1).strip()

                }

            )

        m = re.match(

            r"search youtube box for\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_YOUTUBE_BOX",

                {

                    "query": m.group(1).strip()

                }

            )

        if command.lower().strip() == "press enter":

            return (

                "PRESS_ENTER",

                {}

            )

        m = re.match(

            r"wait\s+(\d+)",

            command,

            re.I

        )

        if m:

            return (

                "WAIT",

                {

                    "milliseconds": int(m.group(1))

                }

            )

        return None
