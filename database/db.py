from typing import Dict
from pymongo import MongoClient
from database.settings import DATABASE_SETTINGS as settings


class Connection:

    def __init__(self) -> None:
        self.host = settings["HOST"]
        self.port = settings["PORT"]
        self._client = MongoClient(
            self.host, self.port,
            username=settings["USER"], 
            password=settings["PASSWORD"]
        )

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self.client[settings["DB"]]

    @property
    def collection(self):
        return self.database[settings["COLLECTION"]]


conn = Connection()
