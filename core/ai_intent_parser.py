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
6. If the command is normal conversation or a question:

Return:

{{"intent":"RAG_QUERY","query":"<original user command>"}}

Never remove the user's original query.

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

BROWSER_READ_PAGE
BROWSER_READ_LINKS
BROWSER_READ_BUTTONS
BROWSER_READ_INPUTS
BROWSER_READ_IMAGES
BROWSER_READ_HEADINGS
BROWSER_READ_TABLES

BROWSER_CLICK
BROWSER_CLICK_FIRST_LINK
BROWSER_CLICK_LINK_INDEX
BROWSER_CLICK_FIRST_BUTTON
BROWSER_CLICK_BUTTON_INDEX

BROWSER_FILL
BROWSER_SELECT
BROWSER_CHECK
BROWSER_UNCHECK

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
Give me links

Output:
{{"intent":"BROWSER_READ_LINKS"}}

User:
Show all links

Output:
{{"intent":"BROWSER_READ_LINKS"}}

User:
Read links

Output:
{{"intent":"BROWSER_READ_LINKS"}}

User:
Read page

Output:
{{"intent":"BROWSER_READ_PAGE"}}

User:
Show buttons

Output:
{{"intent":"BROWSER_READ_BUTTONS"}}

User:
Show inputs

Output:
{{"intent":"BROWSER_READ_INPUTS"}}

User:
Click Login

Output:
{{"intent":"BROWSER_CLICK","target":"Login"}}

User:
Type Piyush in username

Output:
{{"intent":"BROWSER_FILL","target":"username","value":"Piyush"}}

User:
Select India from country

Output:
{{"intent":"BROWSER_SELECT","target":"country","value":"India"}}

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