from tools.vscode_tools import VSCodeTools
from tools.python_runner import PythonRunner


class CodeExecutor:

    def __init__(self):

        self.vscode = VSCodeTools()
        self.runner = PythonRunner()

    ####################################################

    def create_python_file(self, filepath, code):

        ok, message = self.vscode.create_file(filepath)

        if not ok:
            return False, message

        return self.vscode.write_file(
            filepath,
            code
        )

    ####################################################

    def write(self, filepath, code):

        return self.vscode.write_file(
            filepath,
            code
        )

    ####################################################

    def overwrite(self, filepath, code):

        return self.vscode.write_file(
            filepath,
            code
        )

    ####################################################

    def append(self, filepath, code):

        return self.vscode.append_file(
            filepath,
            code
        )

    ####################################################

    def read(self, filepath):

        return self.vscode.read_file(
            filepath
        )

    ####################################################

    def run_python(self, filepath):

        return self.runner.run(
            filepath
        )

    ####################################################

    def run_command(self, command, cwd=None):

        return self.runner.run_command(
            command,
            cwd
        )

    ####################################################

    def open_in_vscode(self, filepath):

        return self.vscode.create_file(
            filepath
        )