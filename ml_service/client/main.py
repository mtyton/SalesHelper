import requests
from typing import List
from bs4 import BeautifulSoup


class Client:
    target_host: str = None
    target_port: int = None
    
    @property
    def server_url(self) -> str:
        return f"http://{self.target_host}:{self.target_port}"

    def get_full_url(self, endpoint: str) -> str:
        if not endpoint or endpoint[0] != "/":
            raise ValueError(
                f"Endpoint must be defined and should start with /, you've passed: {endpoint}"
            )
        return f"{self.server_url}{endpoint}"


class DataServiceClient(Client):
    # TODO - change for docker
    target_host = "127.0.0.1"
    target_port = "5000"

    def get_and_preproces_raw_data(self):
        url = self.get_full_url("/data/raw")
        response = requests.get(url)
        data = response.json()
        for i, record in enumerate(data):
            text_record = record["title"] +"\n"
            text_record += " ".join(record["skills"]) + "\n"
            soup = BeautifulSoup(record["description"], features="lxml")
            description_text = soup.get_text(" ")
            text_record += description_text
            data[i] = {"text": text_record, "uuid": record["uuid"]}
        return data

    def post_doccano_data(self, data: List[dict]) -> int:
        url = self.get_full_url("/data/doccano")
        response = requests.post(url, json=data)
        if not response.status_code == 201:
            raise Exception
        return response.data["inserted"]


dt_client = DataServiceClient()
