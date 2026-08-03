from typing import Any


class SessionManager:

    def __init__(self):

        self.active_session = None

        self.active_type = None

        self.sessions = {}

    #########################################################
    # Register Session
    #########################################################

    def register(

        self,

        name: str,

        session: Any,

        session_type: str

    ):

        self.sessions[name] = {

            "object": session,

            "type": session_type

        }

    #########################################################
    # Activate Session
    #########################################################

    def activate(

        self,

        name: str

    ):

        if name not in self.sessions:

            return False, f"{name} session not found."

        self.active_session = name

        self.active_type = self.sessions[name]["type"]

        return True, f"{name} is now active."

    #########################################################
    # Current Session
    #########################################################

    def current(self):

        if self.active_session is None:

            return None

        return self.sessions[self.active_session]["object"]

    #########################################################
    # Current Session Name
    #########################################################

    def current_name(self):

        return self.active_session

    #########################################################
    # Current Session Type
    #########################################################

    def current_type(self):

        return self.active_type

    #########################################################
    # Check Active
    #########################################################

    def is_active(self, name):

        return self.active_session == name

    #########################################################
    # Remove Session
    #########################################################

    def remove(self, name):

        if name in self.sessions:

            del self.sessions[name]

            if self.active_session == name:

                self.active_session = None

                self.active_type = None

    #########################################################
    # List Sessions
    #########################################################

    def list_sessions(self):

        return list(self.sessions.keys())

    #########################################################
    # Clear
    #########################################################

    def clear(self):

        self.sessions.clear()

        self.active_session = None

        self.active_type = None

    #########################################################
    # String
    #########################################################

    def __str__(self):

        out = []

        out.append("===== Session Manager =====")

        for name in self.sessions:

            mark = ""

            if name == self.active_session:

                mark = "  <-- ACTIVE"

            out.append(

                f"{name} ({self.sessions[name]['type']}){mark}"

            )

        return "\n".join(out)