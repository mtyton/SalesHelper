import uuid
import pytest
from fastapi.testclient import TestClient
from api.main import app

from database.models import (
    JobOfferDocument,
    DoccanoDataDocument,
    TrainingDataDocument
)
from database.db import conn


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():
    conn.raw_data.delete_many({})
    conn.doccano_data.delete_many({})
    conn.training_data.delete_many({})



def test_get_training_data_success():
    document = TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    document.insert(**data)
    response = client.get("/data/training")
    assert response.status_code == 200
    data = response.json()
    assert data[0] == ["Python", [[0, 6, "Skill"]]]


def test_get_training_data_success_no_data():
    response = client.get("/data/training")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_post_doccano_data_success():
    data = [{
       "text": "Python",
       "uuid": str(uuid.uuid4()),
       "ents": [(0, 6, "Skill"),]
    }, ]
    response = client.post("/data/doccano", json=data)
    assert response.status_code == 201
    assert response.json() == {"inserted": 1}


def test_export_doccano_data_success():
    document = DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    document.insert(**data)
    response = client.get("/data/doccano-export")
    assert response.status_code == 200
    assert response.content == b'{"text": "Python", "label": [[0, 6, "Skill"]]}\n'


def test_export_doccano_data_success_no_data():
    response = client.get("/data/doccano-export")
    assert response.status_code == 200
    assert response.content == b''


def test_get_raw_data_success():
    document = JobOfferDocument()
    data = {
        "title": "SpecificTitle",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }
    document.insert(**data)
    response = client.get("/data/raw")
    assert response.status_code == 200
    data["uuid"] = str(data["uuid"])
    assert response.json() == [data]


def test_get_raw_data_success_no_data():
    response = client.get("/data/raw")
    assert response.status_code == 200
    assert response.json() == []


def test_get_job_offers_success_no_params():
    document = JobOfferDocument()
    data = [{
        "title": "Offer1",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 1
    }, {
        "title": "Offer2",
        "skills": ["PHP", "React"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }, {
        "title": "Offer3",
        "skills": ["React", "Angular"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 2
    }]
    for d in data:
        document.insert(**d)
    response = client.get("/data/offers")
    assert response.status_code == 200
    for d in data:
        d["uuid"] = str(d["uuid"])
    assert response.json() == data


def test_get_job_offers_success_with_pagination():
    document = JobOfferDocument()
    data = [{
        "title": "Offer1",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 1
    }, {
        "title": "Offer2",
        "skills": ["PHP", "React"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }, {
        "title": "Offer3",
        "skills": ["React", "Angular"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 2
    }]
    for d in data:
        document.insert(**d)
    response = client.get("/data/offers", params={"skip": 2, "limit": 3})
    assert response.status_code == 200
    for d in data:
        d["uuid"] = str(d["uuid"])
    assert response.json() == data[2:]


def test_get_job_offers_success_with_filtering():
    document = JobOfferDocument()
    data = [{
        "title": "Offer1",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 1
    }, {
        "title": "Offer2",
        "skills": ["PHP", "React"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }, {
        "title": "Offer3",
        "skills": ["React", "Angular"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 2
    }]
    for d in data:
        document.insert(**d)
    response = client.get("/data/offers", params={"category_name": "frontend"})
    assert response.status_code == 200
    for d in data:
        d["uuid"] = str(d["uuid"])
    assert response.json() == data[2:]


def test_get_job_offers_success_with_filtering_and_pagination():
    document = JobOfferDocument()
    data = [{
        "title": "Offer1",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 1
    }, {
        "title": "Offer2",
        "skills": ["PHP", "React"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }, {
        "title": "Offer3",
        "skills": ["React", "Angular"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 2
    }]
    for d in data:
        document.insert(**d)
    response = client.get("/data/offers", params={"skip": 2, "limit": 3, "category_name": "backend"})
    assert response.status_code == 200
    for d in data:
        d["uuid"] = str(d["uuid"])
    assert response.json() == []
