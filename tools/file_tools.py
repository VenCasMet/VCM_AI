import os
import shutil
import subprocess


class FileTools:

    def open_file(self, path):

        try:

            os.startfile(path)

            return True, f"Opened {path}"

        except Exception as e:

            return False, str(e)

    def open_folder(self, path):

        try:

            subprocess.Popen(

                [

                    "explorer",

                    path

                ]

            )

            return True, f"Opened {path}"

        except Exception as e:

            return False, str(e)

    def create_file(self, path):

        try:

            with open(

                path,

                "w",

                encoding="utf-8"

            ):

                pass

            return True, f"Created {path}"

        except Exception as e:

            return False, str(e)

    def create_folder(self, path):

        try:

            os.makedirs(

                path,

                exist_ok=True

            )

            return True, f"Created {path}"

        except Exception as e:

            return False, str(e)

    def delete_file(self, path):

        try:

            os.remove(path)

            return True, f"Deleted {path}"

        except Exception as e:

            return False, str(e)

    def delete_folder(self, path):

        try:

            shutil.rmtree(path)

            return True, f"Deleted {path}"

        except Exception as e:

            return False, str(e)

    def rename_file(self, old_path, new_path):

        try:

            os.rename(

                old_path,

                new_path

            )

            return True, f"Renamed to {new_path}"

        except Exception as e:

            return False, str(e)

    def rename_folder(self, old_path, new_path):

        try:

            os.rename(

                old_path,

                new_path

            )

            return True, f"Renamed to {new_path}"

        except Exception as e:

            return False, str(e)

    def exists(self, path):

        return os.path.exists(path)

    def copy_file(self, source, destination):

        try:

            shutil.copy2(

                source,

                destination

            )

            return True, f"Copied to {destination}"

        except Exception as e:

            return False, str(e)

    def move_file(self, source, destination):

        try:

            shutil.move(

                source,

                destination

            )

            return True, f"Moved to {destination}"

        except Exception as e:

            return False, str(e)

    def copy_folder(self, source, destination):

        try:

            shutil.copytree(

                source,

                destination,

                dirs_exist_ok=True

            )

            return True, f"Copied to {destination}"

        except Exception as e:

            return False, str(e)

    def move_folder(self, source, destination):

        try:

            shutil.move(

                source,

                destination

            )

            return True, f"Moved to {destination}"

        except Exception as e:

            return False, str(e)

    def search_files(self, keyword, root=None, limit=20):

        try:

            if root is None:

                root = os.path.expanduser("~")

            results = []

            for current_root, _, files in os.walk(root):

                for file in files:

                    if keyword.lower() in file.lower():

                        results.append(

                            os.path.join(

                                current_root,

                                file

                            )

                        )

                        if len(results) >= limit:

                            return True, results

            return True, results

        except Exception as e:

            return False, str(e)

    def search_folders(self, keyword, root=None, limit=20):

        try:

            if root is None:

                root = os.path.expanduser("~")

            results = []

            for current_root, folders, _ in os.walk(root):

                for folder in folders:

                    if keyword.lower() in folder.lower():

                        results.append(

                            os.path.join(

                                current_root,

                                folder

                            )

                        )

                        if len(results) >= limit:

                            return True, results

            return True, results

        except Exception as e:

            return False, str(e)

    def desktop(self):

        return os.path.join(

            os.path.expanduser("~"),

            "Desktop"

        )

    def documents(self):

        return os.path.join(

            os.path.expanduser("~"),

            "Documents"

        )

    def downloads(self):

        return os.path.join(

            os.path.expanduser("~"),

            "Downloads"

        )

    def pictures(self):

        return os.path.join(

            os.path.expanduser("~"),

            "Pictures"

        )

    def videos(self):

        return os.path.join(

            os.path.expanduser("~"),

            "Videos"

        )

    def zip_folder(self, source, destination):

        try:

            shutil.make_archive(

                destination,

                "zip",

                source

            )

            return True, destination + ".zip"

        except Exception as e:

            return False, str(e)

    def unzip_file(self, source, destination):

        try:

            shutil.unpack_archive(

                source,

                destination

            )

            return True, f"Extracted to {destination}"

        except Exception as e:

            return False, str(e)