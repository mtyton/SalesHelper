from typing import Dict
from pymongo import MongoClient


class Connection:

    def read_config(self) -> dict:
        ...

    def __init__(self) -> None:
        self.host = "localhost"
        self.port = 27017
        self._client = MongoClient(self.host, self.port)

    @property
    def client(self):
        return self._client

conn = Connection()
print(conn.client)
