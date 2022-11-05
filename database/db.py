from typing import Dict
from pymongo import MongoClient
from database.settings import DATABASE_SETTINGS as settings


# TODO - this should be singleton
class Connection:

    def read_config(self) -> dict:
        ...

    def __init__(self) -> None:
        self.host = settings["MONGODB_HOST"]
        self.port = settings["MONGODB_PORT"]
        # TODO move credintials to env
        self._client = MongoClient(
            self.host, self.port,
            username="root", password="password"
        )

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self.client[settings["MONGODB_DB"]]

    @property
    def collection(self):
        return self.database[settings["MONGODB_COLLECTION"]]


conn = Connection()
