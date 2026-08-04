import re

from core.ai_programmer import AIProgrammer
from core.code_executor import CodeExecutor
from core.dependency_manager import DependencyManager


class AutoProgrammer:

    def __init__(self):

        self.ai = AIProgrammer()
        self.executor = CodeExecutor()
        self.dependencies = DependencyManager()

    ########################################################

    def clean_code(self, text):

        text = text.strip()

        match = re.search(
            r"```(?:python|cpp|c\+\+|java|javascript|js|html|css|json)?\s*(.*?)```",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

        return text

    ########################################################

    def build(self, filepath, prompt, retries=3):

        code = self.ai.generate(prompt)
        code = self.clean_code(code)

        ok, message = self.executor.create_python_file(
            filepath,
            code
        )

        if not ok:
            return False, message

        last_error = ""

        for attempt in range(retries):

            ok, output = self.executor.run_python(filepath)

            ####################################################
            # SUCCESS
            ####################################################

            if ok:

                success = (
                    f"✅ Program created successfully.\n\n"
                    f"Location : {filepath}\n\n"
                    f"Output:\n{output}"
                )

                return True, success

            ####################################################
            # AUTO INSTALL MISSING MODULE
            ####################################################

            if "ModuleNotFoundError" in output:

                installed, module = self.dependencies.auto_install(output)

                if installed:

                    print(f"[AutoProgrammer] Installed {module}")

                    ok, output = self.executor.run_python(filepath)

                    if ok:

                        success = (
                            f"✅ Program created successfully.\n\n"
                            f"Installed Module : {module}\n\n"
                            f"Location : {filepath}\n\n"
                            f"Output:\n{output}"
                        )

                        return True, success

                    last_error = output
                    continue

                last_error = output
                continue

            ####################################################
            # AI FIX
            ####################################################

            last_error = output

            ok, current_code = self.executor.read(filepath)

            if not ok:
                return False, current_code

            print(f"[AutoProgrammer] AI Fix Attempt {attempt + 1}")

            fixed_code = self.ai.fix(
                current_code,
                last_error
            )

            fixed_code = self.clean_code(fixed_code)

            ok, message = self.executor.overwrite(
                filepath,
                fixed_code
            )

            if not ok:
                return False, message

        ####################################################
        # FINAL RUN
        ####################################################

        ok, output = self.executor.run_python(filepath)

        if ok:

            success = (
                f"✅ Program created successfully.\n\n"
                f"Location : {filepath}\n\n"
                f"Output:\n{output}"
            )

            return True, success

        ####################################################
        # FINAL FAILURE
        ####################################################

        explanation = self.ai.explain_error(output)

        failure = (
            f"❌ Failed after {retries} attempts.\n\n"
            f"Location : {filepath}\n\n"
            f"Final Error:\n\n"
            f"{output}\n\n"
            f"Explanation:\n"
            f"{explanation}"
        )

        return False, failure

    ########################################################

    def improve(self, filepath):

        ok, code = self.executor.read(filepath)

        if not ok:
            return False, code

        improved = self.ai.improve(code)
        improved = self.clean_code(improved)

        ok, message = self.executor.overwrite(
            filepath,
            improved
        )

        return ok, message

    ########################################################

    def run(self, filepath):

        return self.executor.run_python(filepath)

    ########################################################

    def read(self, filepath):

        return self.executor.read(filepath)

    ########################################################

    def overwrite(self, filepath, code):

        code = self.clean_code(code)

        return self.executor.overwrite(filepath, code)