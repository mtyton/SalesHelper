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

    # TODO - there should be multiple collections
    @property
    def raw_data(self):
        return self.database[settings["RAW_COLLECTION"]]

    @property
    def doccano_data(self):
        return self.database[settings["DOCCANO_COLLECTION"]]

    @property
    def training_data(self):
        return self.database[settings["TRAINING_COLLECTION"]]


conn = Connection()
