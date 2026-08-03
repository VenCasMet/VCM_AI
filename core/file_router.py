import re


class FileRouter:

    @staticmethod
    def matches(command):

        lower = command.lower().strip()

        patterns = [

            r"^open file",

            r"^open folder",

            r"^create file",

            r"^create folder",

            r"^delete file",

            r"^delete folder",

            r"^rename file",

            r"^rename folder",

            r"^copy file",

            r"^move file",

            r"^copy folder",

            r"^move folder",

            r"^search file",

            r"^search folder",

            r"^zip",

            r"^unzip"

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

            r"open file\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "OPEN_FILE",

                {

                    "path": m.group(1).strip()

                }

            )

        m = re.match(

            r"open folder\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "OPEN_FOLDER",

                {

                    "path": m.group(1).strip()

                }

            )

        m = re.match(

            r"create file\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "CREATE_FILE",

                {

                    "path": m.group(1).strip()

                }

            )

        m = re.match(

            r"create folder\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "CREATE_FOLDER",

                {

                    "path": m.group(1).strip()

                }

            )

        m = re.match(

            r"delete file\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "DELETE_FILE",

                {

                    "path": m.group(1).strip()

                }

            )

        m = re.match(

            r"delete folder\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "DELETE_FOLDER",

                {

                    "path": m.group(1).strip()

                }

            )

        m = re.match(

            r"rename file\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "RENAME_FILE",

                {

                    "old_path": m.group(1).strip(),

                    "new_path": m.group(2).strip()

                }

            )

        m = re.match(

            r"rename folder\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "RENAME_FOLDER",

                {

                    "old_path": m.group(1).strip(),

                    "new_path": m.group(2).strip()

                }

            )

        m = re.match(

            r"copy file\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "COPY_FILE",

                {

                    "source": m.group(1).strip(),

                    "destination": m.group(2).strip()

                }

            )

        m = re.match(

            r"move file\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "MOVE_FILE",

                {

                    "source": m.group(1).strip(),

                    "destination": m.group(2).strip()

                }

            )

        m = re.match(

            r"copy folder\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "COPY_FOLDER",

                {

                    "source": m.group(1).strip(),

                    "destination": m.group(2).strip()

                }

            )

        m = re.match(

            r"move folder\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "MOVE_FOLDER",

                {

                    "source": m.group(1).strip(),

                    "destination": m.group(2).strip()

                }

            )

        m = re.match(

            r"search file\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_FILE",

                {

                    "keyword": m.group(1).strip()

                }

            )

        m = re.match(

            r"search folder\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "SEARCH_FOLDER",

                {

                    "keyword": m.group(1).strip()

                }

            )

        m = re.match(

            r"zip\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "ZIP_FOLDER",

                {

                    "source": m.group(1).strip(),

                    "destination": m.group(2).strip()

                }

            )

        m = re.match(

            r"unzip\s+(.+?)\s+to\s+(.+)",

            command,

            re.I

        )

        if m:

            return (

                "UNZIP_FILE",

                {

                    "source": m.group(1).strip(),

                    "destination": m.group(2).strip()

                }

            )

        return None