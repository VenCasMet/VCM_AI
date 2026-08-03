import subprocess
import os
import sys


class PythonRunner:

    def run(self, filepath):

        try:

            abs_path = os.path.abspath(filepath)

            process = subprocess.run(

                [

                    sys.executable,

                    abs_path

                ],

                capture_output=True,

                text=True

            )

            output = process.stdout + process.stderr

            return (

                process.returncode == 0,

                output

            )

        except Exception as e:

            return False, str(e)

    ########################################################

    def run_command(self, command, cwd=None):

        try:

            process = subprocess.run(

                command,

                shell=True,

                capture_output=True,

                text=True,

                cwd=cwd

            )

            output = process.stdout + process.stderr

            return (

                process.returncode == 0,

                output

            )

        except Exception as e:

            return False, str(e)