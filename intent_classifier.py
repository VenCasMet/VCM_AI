import json
import ollama


SYSTEM_PROMPT = """
You are an AI Intent Classifier.

Return ONLY valid JSON.

Available intents:

OPEN_APP

SEARCH_GOOGLE

SEARCH_YOUTUBE

OPEN_WEBSITE

SEARCH_FILE

SYSTEM_STATUS

REMEMBER

RECALL_MEMORY

RAG_QUERY

---------------------------------

Examples

User:
Open notepad

Output

{
"intent":"OPEN_APP",
"app":"notepad"
}

------------------------

User

Open VS Code

Output

{
"intent":"OPEN_APP",
"app":"vscode"
}

------------------------

User

Search Virat Kohli

Output

{
"intent":"SEARCH_GOOGLE",
"query":"Virat Kohli"
}

------------------------

User

Search Virat Kohli in Brave

Output

{
"intent":"SEARCH_GOOGLE",
"browser":"brave",
"query":"Virat Kohli"
}

------------------------

User

Search YouTube for WWE

Output

{
"intent":"SEARCH_YOUTUBE",
"query":"WWE"
}

------------------------

User

Search YouTube for WWE in Brave

Output

{
"intent":"SEARCH_YOUTUBE",
"browser":"brave",
"query":"WWE"
}

------------------------

User

Open ChatGPT

Output

{
"intent":"OPEN_WEBSITE",
"site":"chatgpt"
}

------------------------

User

Open Github

Output

{
"intent":"OPEN_WEBSITE",
"site":"github"
}

------------------------

User

Find resume.pdf

Output

{
"intent":"SEARCH_FILE",
"filename":"resume.pdf"
}

------------------------

User

Remember my favourite team is Real Madrid

Output

{
"intent":"REMEMBER",
"fact":"my favourite team is Real Madrid"
}

------------------------

User

What do you remember

Output

{
"intent":"RECALL_MEMORY"
}

------------------------

User

Tell me about Lionel Messi

Output

{
"intent":"RAG_QUERY"
}

Return JSON ONLY.

No markdown.

No explanation.

"""


class IntentClassifier:

    def __init__(self, model="qwen2.5:7b"):

        self.model = model

    def classify(self, query):

        response = ollama.chat(

            model=self.model,

            messages=[

                {

                    "role": "system",

                    "content": SYSTEM_PROMPT

                },

                {

                    "role": "user",

                    "content": query

                }

            ]

        )

        answer = response["message"]["content"]

        try:

            return json.loads(answer)

        except Exception:

            return {

                "intent": "RAG_QUERY"

            }