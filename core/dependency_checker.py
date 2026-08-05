import shutil
import subprocess
import sys


class DependencyChecker:

    @staticmethod
    def has_internet():
        try:
            subprocess.check_output(
                ["ping", "8.8.8.8", "-n", "1"],
                stderr=subprocess.STDOUT,
                timeout=5
            )
            return True
        except Exception:
            return False

    @staticmethod
    def has_ollama():
        return shutil.which("ollama") is not None

    @staticmethod
    def has_model(model_name):

        if not DependencyChecker.has_ollama():
            return False

        try:
            output = subprocess.check_output(
                ["ollama", "list"],
                text=True
            )

            return model_name.lower() in output.lower()

        except Exception:
            return False

    @staticmethod
    def has_playwright():
        """
        Checks whether the Playwright Python package is installed.
        Avoids using the broken playwright.exe launcher.
        """
        try:
            import playwright  # noqa: F401
            return True
        except ImportError:
            return False

    @staticmethod
    def has_chromium():
        """
        Checks whether Chromium is installed for Playwright.
        """
        if not DependencyChecker.has_playwright():
            return False

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "playwright",
                    "install",
                    "chromium",
                    "--dry-run"
                ],
                capture_output=True,
                text=True
            )

            return result.returncode == 0

        except Exception:
            return False