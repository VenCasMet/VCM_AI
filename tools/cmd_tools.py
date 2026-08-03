import subprocess
import threading
import queue
import os


class CMDTools:

    def __init__(self):

        self.process = None

        self.output_queue = queue.Queue()

        self.reader_thread = None

        self.running = False

        self.history = []


    ##########################################################
    # Start CMD
    ##########################################################

    def open(self):

        if self.running:

            return True, "CMD already running."

        self.process = subprocess.Popen(

            ["cmd.exe"],

            stdin=subprocess.PIPE,

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            bufsize=1,

            creationflags=subprocess.CREATE_NEW_CONSOLE

        )

        self.running = True

        self.reader_thread = threading.Thread(

            target=self._reader,

            daemon=True

        )

        self.reader_thread.start()

        return True, "CMD opened successfully."


    ##########################################################
    # Background Reader
    ##########################################################

    def _reader(self):

        while self.running:

            line = self.process.stdout.readline()

            if line:

                self.output_queue.put(line.rstrip())

        ##########################################################
    # Execute Command
    ##########################################################

    def run(self, command):

        if not self.running:

            ok, msg = self.open()

            if not ok:

                return False, msg

        try:

            self.history.append(command)

            self.process.stdin.write(command + "\n")

            self.process.stdin.flush()

            return True, f"Executed: {command}"

        except Exception as e:

            return False, str(e)


    ##########################################################
    # Read Output
    ##########################################################

    def read_output(self):

        lines = []

        while not self.output_queue.empty():

            lines.append(

                self.output_queue.get()

            )

        return "\n".join(lines)


    ##########################################################
    # Execute And Wait
    ##########################################################

    def execute_and_wait(

        self,

        command,

        wait_time=1.0

    ):

        import time

        ok, msg = self.run(command)

        if not ok:

            return False, msg

        time.sleep(wait_time)

        return True, self.read_output()
        ##########################################################
    # Get Command History
    ##########################################################

    def get_history(self):

        return self.history.copy()


    ##########################################################
    # Clear Screen
    ##########################################################

    def clear(self):

        return self.run("cls")


    ##########################################################
    # Current Working Directory
    ##########################################################

    def pwd(self):

        return self.execute_and_wait("cd")


    ##########################################################
    # Change Directory
    ##########################################################

    def cd(self, path):

        return self.execute_and_wait(f'cd /d "{path}"')


    ##########################################################
    # Make Directory
    ##########################################################

    def mkdir(self, folder):

        return self.execute_and_wait(

            f'mkdir "{folder}"'

        )


    ##########################################################
    # Remove Directory
    ##########################################################

    def rmdir(self, folder):

        return self.execute_and_wait(

            f'rmdir /S /Q "{folder}"'

        )


    ##########################################################
    # Execute Python File
    ##########################################################

    def run_python(self, filename):

        return self.execute_and_wait(

            f'python "{filename}"'

        )


    ##########################################################
    # Execute Pip
    ##########################################################

    def pip(self, command):

        return self.execute_and_wait(

            f"pip {command}"

        )


    ##########################################################
    # Execute Git
    ##########################################################

    def git(self, command):

        return self.execute_and_wait(

            f"git {command}"

        )


    ##########################################################
    # Execute NPM
    ##########################################################

    def npm(self, command):

        return self.execute_and_wait(

            f"npm {command}"

        )