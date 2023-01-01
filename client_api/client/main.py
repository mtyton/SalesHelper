import requests
from typing import(
    List,
    Dict,
    Any,
    Union
)
from uuid import UUID

from client.exceptions import ClientException
from client.adapters import (
    JobOfferListAdapter
)



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
    adapter = JobOfferListAdapter()


    def get_job_offers_list(self, category: Union[None, str] = None, skip: int = 0, limit: int = 25):
        url = self.get_full_url("/data/offers/")
        url += f"?skip={skip}&limit={limit}"
        if category is not None:
            url += f"&category_name={category}"
        response = requests.get(url)
        return self.adapt_data(response.json())

    def get_exact_job_offer(self, offer_uuid):
        url = self.get_full_url(f"/data/offers/{offer_uuid}")
        response = requests.get(url)
        return self.adapter.adapt(response.json())


dt_client = DataServiceClient()


class MachineLearningServiceClient:
    ...
