import requests
import json
from typing import(
    List,
    Dict,
    Any,
    Union
)

from database.models import (
    EmployeeCategory,
    Employee
)
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

    def get_job_offers_list(self, category: Union[None, str] = None, skip: int = 0, limit: int = 25):
        url = self.get_full_url("/data/offers/")
        url += f"?skip={skip}&limit={limit}"
        if category is not None:
            url += f"&category_name={category}"
        response = requests.get(url)
        return response.json()
 
    def get_exact_job_offer(self, offer_uuid):
        url = self.get_full_url(f"/data/offers/{offer_uuid}")
        response = requests.get(url)
        return response.json()

dt_client = DataServiceClient()


class MachineLearningServiceClient(Client):
    target_host = "ml_service"
    target_port = "5002"
    
    def get_match(self, employee: Employee, resume_content: str):
        url = self.get_full_url("/ml/match")
        category = EmployeeCategory(employee.category)
        url += f"?category={category.name}"
        with requests.post(url, json={"resume": resume_content}, stream=True) as r:
            r.raise_for_status()
            for item in r.iter_content(chunk_size=2048):
                yield json.loads(item)


ml_client = MachineLearningServiceClient()
