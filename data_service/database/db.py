import os
from typing import (
    Dict, 
    Any,
    Union
)
from pymongo import MongoClient


from database.settings import (
    DATABASE_SETTINGS,
    DATABASE_TEST_SETTINGS,
    DB_RUNTYPE
)


class Connection:

    def __init__(self) -> None:
        settings_type = DB_RUNTYPE
        current_settings = DATABASE_TEST_SETTINGS if settings_type=="test_run" else DATABASE_SETTINGS
        self.host = current_settings["HOST"]
        self.port = current_settings["PORT"]
        self.username = current_settings["USER"]
        self.password = current_settings["PASSWORD"]
        self._db_name = current_settings["DB"]
        self._client = None
        self.settings = current_settings

    @property
    def client(self):
        if self._client is None:
            self._client = MongoClient(
                self.host, self.port,
                username=self.username, 
                password=self.password
            )
            # do not keep password in memory for safety
            del self.password
        return self._client

    @property
    def database(self):
        return self.client[self._db_name]

    @property
    def raw_data(self):
        return self.database[self.settings["RAW_COLLECTION"]]

    @property
    def doccano_data(self):
        return self.database[self.settings["DOCCANO_COLLECTION"]]

    @property
    def training_data(self):
        return self.database[self.settings["TRAINING_COLLECTION"]]


conn = Connection()
