import json
import re

import ollama


class AIIntentParser:

    def __init__(

        self,

        model="qwen2.5:7b"

    ):

        self.model = model

    def parse(

        self,

        command

    ):

        prompt = self.build_prompt(

            command

        )

        try:

            response = ollama.chat(

                model=self.model,

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ]

            )

            text = response["message"]["content"]

            return self.extract_json(

                text

            )

        except Exception:

            return None

    def build_prompt(

        self,

        command

    ):

        return f"""
You are an AI Intent Parser.

Your job is to convert a natural language command into JSON.

Rules:

1. Return ONLY JSON.
2. No markdown.
3. No explanation.
4. No extra text.
5. Never answer the user's question.
6. If unsure return:
{{"intent":"RAG_QUERY"}}

Supported intents:

OPEN_BROWSER
OPEN_CMD

GOOGLE_SEARCH
YOUTUBE_SEARCH
GITHUB_SEARCH
WIKIPEDIA_SEARCH

SEARCH_GOOGLE_BOX
SEARCH_YOUTUBE_BOX

BROWSER_BACK
BROWSER_FORWARD
BROWSER_REFRESH

BROWSER_NEW_TAB
BROWSER_CLOSE_TAB

PRESS_ENTER

WAIT

VOLUME_UP
VOLUME_DOWN
SET_VOLUME
MUTE
UNMUTE

GET_BRIGHTNESS
BRIGHTNESS_UP
BRIGHTNESS_DOWN
SET_BRIGHTNESS

BATTERY
CPU_USAGE
RAM_USAGE
DISK_USAGE

LOCK_PC
SLEEP_PC
HIBERNATE_PC
SHUTDOWN_PC
RESTART_PC
LOGOFF_PC

OPEN_SETTINGS
OPEN_EXPLORER
OPEN_TASK_MANAGER
OPEN_CONTROL_PANEL
OPEN_DEVICE_MANAGER

OPEN_FILE
OPEN_FOLDER

CREATE_FILE
CREATE_FOLDER

DELETE_FILE
DELETE_FOLDER

RENAME_FILE
RENAME_FOLDER

COPY_FILE
MOVE_FILE

COPY_FOLDER
MOVE_FOLDER

SEARCH_FILE
SEARCH_FOLDER

ZIP_FOLDER
UNZIP_FILE

Examples:

User:
Open Brave

Output:
{{"intent":"OPEN_BROWSER","browser":"brave"}}

User:
Search Google for Python

Output:
{{"intent":"GOOGLE_SEARCH","query":"python"}}

User:
Search YouTube for Real Madrid

Output:
{{"intent":"YOUTUBE_SEARCH","query":"Real Madrid"}}

User:
Go back

Output:
{{"intent":"BROWSER_BACK"}}

User:
Volume 30

Output:
{{"intent":"SET_VOLUME","value":30}}

User:
Brightness 70

Output:
{{"intent":"SET_BRIGHTNESS","value":70}}

User:
Create folder C:\\Temp

Output:
{{"intent":"CREATE_FOLDER","path":"C:\\\\Temp"}}

User:
Open file C:\\notes.txt

Output:
{{"intent":"OPEN_FILE","path":"C:\\\\notes.txt"}}

User command:

{command}

JSON:
"""
    def extract_json(

        self,

        text

    ):

        text = text.strip()

        text = text.replace(

            "```json",

            ""

        )

        text = text.replace(

            "```",

            ""

        ).strip()

        try:

            return json.loads(

                text

            )

        except:

            pass

        m = re.search(

            r"\{.*\}",

            text,

            re.DOTALL

        )

        if not m:

            return None

        try:

            return json.loads(

                m.group()

            )

        except:

            return None