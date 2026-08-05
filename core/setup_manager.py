import json
import os

from core.dependency_checker import DependencyChecker


class SetupManager:

    ########################################################
    # AppData Location
    ########################################################

    APP_NAME = "VCM AI"

    CONFIG_DIR = os.path.join(

        os.getenv("LOCALAPPDATA"),

        APP_NAME

    )

    CONFIG_PATH = os.path.join(

        CONFIG_DIR,

        "setup_complete.json"

    )

    ########################################################

    def __init__(self):

        os.makedirs(

            self.CONFIG_DIR,

            exist_ok=True

        )

        if not os.path.exists(self.CONFIG_PATH):

            self.save(

                {

                    "completed": False,

                    "version": "2.0.0"

                }

            )

    ########################################################

    def load(self):

        try:

            with open(

                self.CONFIG_PATH,

                "r",

                encoding="utf-8"

            ) as f:

                return json.load(f)

        except Exception:

            return {

                "completed": False,

                "version": "2.0.0"

            }

    ########################################################

    def save(self, data):

        with open(

            self.CONFIG_PATH,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4

            )

    ########################################################

    def is_completed(self):

        return self.load().get(

            "completed",

            False

        )

    ########################################################

    def mark_completed(self):

        data = self.load()

        data["completed"] = True

        self.save(data)

    ########################################################

    def reset(self):

        self.save(

            {

                "completed": False,

                "version": "2.0.0"

            }

        )

    ########################################################

    def check_dependencies(self):

        return {

            "internet": DependencyChecker.has_internet(),

            "ollama": DependencyChecker.has_ollama(),

            "qwen": DependencyChecker.has_model(

                "qwen2.5:7b"

            ),

            "embedding": DependencyChecker.has_model(

                "nomic-embed-text"

            ),

            "playwright": DependencyChecker.has_playwright()

        }

        ########################################################

    def everything_ready(self):

        deps = self.check_dependencies()

        return (

            deps["internet"]

            and deps["ollama"]

            and deps["qwen"]

            and deps["embedding"]

        )

    ########################################################

    def mark_incomplete(self):

        data = self.load()

        data["completed"] = False

        self.save(data)