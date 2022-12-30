import requests
from typing import (
    List,
    Dict, 
    Any
)

from client.adapters import JobOfferAdapter
from client.exceptions import ClientException


class Client:
    target_host: str = None
    target_port: int = None
    adapter = None

    @property
    def server_url(self) -> str:
        return f"http://{self.target_host}:{self.target_port}"

    def get_full_url(self, endpoint: str) -> str:
        if not endpoint or endpoint[0] != "/":
            raise ValueError(
                f"Endpoint must be defined and should start with /, you've passed: {endpoint}"
            )
        return f"{self.server_url}{endpoint}"

    def adapt_data(self, data: List[Dict[str, Any]]):
        if not self.adapter:
            raise ClientException("adapter variable has not been defined")
        for i, record in enumerate(data):
            data[i] = self.adapter.adapt(record)
        return data


class DataServiceClient(Client):
    target_host = "data_service"
    target_port = "5000"
    adapter = JobOfferAdapter()

    def get_filtered_raw_data(self, number_of_records:int = 10):
        url = self.get_full_url("/data/offers")
        response = requests.get(url, kwargs={"number_of_records": number_of_records})
        return self.adapt_data(response.json())

    def get_and_preproces_raw_data(self):
        url = self.get_full_url("/data/raw")
        response = requests.get(url)
        return self.adapt_data(response.json())

    def post_doccano_data(self, data: List[dict]) -> int:
        url = self.get_full_url("/data/doccano")
        response = requests.post(url, json=data)
        if not response.status_code == 201:
            raise ClientException(
                "Client was unable to create doccano_data instance in data_service"
            )
        return response.json()["inserted"]

    def get_training_data(self):
        url = self.get_full_url("/data/training")
        response = requests.get(url)
        return response.json()


dt_client = DataServiceClient()
