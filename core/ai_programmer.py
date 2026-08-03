import ollama


class AIProgrammer:

    def __init__(self, model="qwen2.5:7b"):

        self.model = model

    ####################################################

    def _chat(self, system, prompt):

        response = ollama.chat(

            model=self.model,

            messages=[

                {
                    "role": "system",
                    "content": system
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        return response["message"]["content"].strip()

    ####################################################

    def generate(self, prompt):

        system = """
You are a senior Python software engineer.

Your task is to generate complete executable Python programs.

STRICT RULES:

1. Return ONLY Python code.
2. Do NOT use markdown.
3. Do NOT use ``` blocks.
4. Do NOT explain anything.
5. Never ask the user for input().
6. Never wait for keyboard input.
7. Use sample values whenever input is required.
8. The program must execute immediately.
9. The program must terminate automatically.
10. Print meaningful output.
11. Import every required library.
12. Write clean, production-quality code.
13. Never leave TODOs.
14. Never return partial code.
15. Always return a complete executable Python file.
"""

        return self._chat(system, prompt)

    ####################################################

    def fix(self, code, error):

        system = """
You are a senior Python debugging expert.

Your ONLY task is to repair Python code.

STRICT RULES:

1. Return ONLY corrected Python code.
2. No markdown.
3. No explanations.
4. No comments unless already present.
5. Preserve functionality.
6. Fix every syntax/runtime/import error.
7. Never use input().
8. The corrected code must execute successfully.
9. Return the COMPLETE corrected file.
"""

        prompt = f"""
Current Python code:

{code}

Execution Error:

{error}

Fix the code and return the COMPLETE corrected Python file.
"""

        return self._chat(system, prompt)

    ####################################################

    def improve(self, code):

        system = """
You are a senior software engineer.

Improve the following Python program.

Rules:

1. Return ONLY Python code.
2. No markdown.
3. Preserve functionality.
4. Improve readability.
5. Improve performance where possible.
6. Remove duplicate code.
7. Follow Python best practices.
8. Return the COMPLETE file.
"""

        return self._chat(system, code)

    ####################################################

    def explain_error(self, error):

        system = """
Explain Python errors briefly.

Maximum 3 sentences.

No code.
"""

        return self._chat(system, error)