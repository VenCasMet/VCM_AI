import re
import sys
import subprocess


class DependencyManager:

    ####################################################

    def extract_missing_module(self, error):

        match = re.search(

            r"No module named ['\"]([^'\"]+)['\"]",

            error

        )

        if match is None:

            return None

        return match.group(1)

    ####################################################

    def map_package(self, module):

        mapping = {

            "cv2": "opencv-python",

            "PIL": "pillow",

            "bs4": "beautifulsoup4",

            "sklearn": "scikit-learn",

            "yaml": "pyyaml",

            "Crypto": "pycryptodome",

            "fitz": "pymupdf"

        }

        return mapping.get(

            module,

            module

        )

    ####################################################

    def install(self, module):

        package = self.map_package(module)

        try:

            process = subprocess.run(

                [

                    sys.executable,

                    "-m",

                    "pip",

                    "install",

                    package

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

    ####################################################

    def auto_install(self, error):

        module = self.extract_missing_module(error)

        if module is None:

            return False, None

        ok, output = self.install(module)

        if ok:

            return True, module

        return False, output