import pytest
import uuid
from bson.binary import Binary
from copy import deepcopy

from database.db import conn
from database import models
from database.dataclasses import (
    JobOffer,
    DoccanoData,
    TrainingData
)
from database.exceptions import DocumentAlreadyExistsException


@pytest.fixture(autouse=False)
def test_connection():
    yield conn
    # clear database after each test
    conn.raw_data.delete_many({})
    conn.doccano_data.delete_many({})
    conn.training_data.delete_many({})


def test_job_offer_insert_success():
    data = {
        "title": "TestTitle",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }
    document = models.JobOfferDocument()
    instance = document.insert(**data)
    assert isinstance(instance, JobOffer)


def test_job_offer_insert_validation_error(test_connection):
    data = {
        "title": "TestTitle",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }
    new_data = deepcopy(data)
    document = models.JobOfferDocument()
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.raw_data.insert_one(data)
    # try to insert record with same uuid
    try:
        instance = document.insert(**new_data)
    except Exception as e:
        expected_uuid = new_data['uuid']
        assert type(e) == DocumentAlreadyExistsException
        assert str(e) == f"Record with uuid: {expected_uuid} already exists"


def test_update_job_offer_success(test_connection):
    data = {
        "title": "TestTitle",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }
    document = models.JobOfferDocument()
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.raw_data.insert_one(data)
    temp_uuid = data["uuid"]
    query = {"uuid": temp_uuid}
    update_data = {"title": "TextUpdate"}
    new_instance = document.update(query=query, update_one=True, update={"$set": update_data})
    assert isinstance(new_instance, JobOffer)
    assert new_instance.title == "TextUpdate"


def test_job_offer_update_not_existing_record():
    data = {
        "title": "TestTitle",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }
    document = models.JobOfferDocument()
    temp_uuid = Binary.from_uuid(data['uuid'])
    query = {"uuid": temp_uuid}
    update_data = {"title": "TextUpdate"}
    new_instance = document.update(query=query, update_one=True, update={"$set": update_data})
    assert new_instance is None


def test_job_offer_aggregate_success(test_connection):
    data = {
        "title": "TestTitle",
        "skills": ["C#", "C++"],
        "url": "https://google.com",
        "description": "SomeDescription",
        "platform": 1,
        "uuid": uuid.uuid4(),
        "lang": "EN",
        "category": 3
    }
    document = models.JobOfferDocument()
    instance = JobOffer(**data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.raw_data.insert_one(data)
    query = {"lang": "EN"}
    agg_query = [
        { "$match": query },
        { "$sample": { "size": 10}}
    ]
    results = document.aggregate(agg_query)
    assert results[0].uuid == instance.uuid


def test_job_offer_find_success(test_connection):
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
    document = models.JobOfferDocument()
    validate_data = deepcopy(data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.raw_data.insert_one(data)
    instance = document.find({"title": "SpecificTitle"}, find_one=True)
    assert instance.uuid == validate_data["uuid"]
    assert isinstance(instance, JobOffer)


def test_job_offer_find_nothing_found():
    document = models.JobOfferDocument()
    instance = document.find({"title": "NameManglingINPython"}, find_one=True)
    assert instance is None


def test_doccano_data_insert_success():
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    instance = document.insert(**data)
    assert instance.uuid == data["uuid"]
    assert isinstance(instance, DoccanoData)


def test_doccano_data_insert_fail_uuid_exists(test_connection):
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    new_data = deepcopy(data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.doccano_data.insert_one(data)
    # try to insert record with same uuid
    try:
        document.insert(**new_data)
    except Exception as e:
        expected_uuid = new_data['uuid']
        assert type(e) == DocumentAlreadyExistsException
        assert str(e) == f"Record with uuid: {expected_uuid} already exists"


def test_update_doccano_data_success(test_connection):
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.doccano_data.insert_one(data)
    update_data = {"text": "Python, Git, Linux"}
    updated_instance = document.update({"uuid": data["uuid"]}, update_one=True, update={"$set": update_data})
    assert updated_instance.text == "Python, Git, Linux"


def test_update_doccano_data_not_existing_record():
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": Binary.from_uuid(uuid.uuid4()),
       "ents": [(0, 6, "Skill"),]
    }
    update_data = {"text": "Python, Git, Linux"}
    updated_instance = document.update({"uuid": data["uuid"]}, update_one=True, update={"$set": update_data})
    assert updated_instance is None


def test_aggregate_doccano_data_success(test_connection):
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    instance = DoccanoData(**data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.doccano_data.insert_one(data)
    query = {"uuid": data["uuid"]}
    agg_query = [
        { "$match": query },
        { "$sample": { "size": 10}}
    ]
    results = document.aggregate(agg_query)
    assert results[0].uuid == instance.uuid


def test_find_doccano_data_success(test_connection):
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    instance = DoccanoData(**data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.doccano_data.insert_one(data)   
    found_instance = document.find({"uuid": data["uuid"]}, find_one=True) 
    assert instance.uuid == found_instance.uuid


def test_find_doccano_data_no_record():
    document = models.DoccanoDataDocument()
    data = {
       "text": "Python",
       "uuid": Binary.from_uuid(uuid.uuid4()),
       "ents": [(0, 6, "Skill"),]
    }
    found_instance = document.find({"uuid": data["uuid"]}, find_one=True) 
    assert found_instance is None


def test_training_data_insert_success():
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    instance = document.insert(**data)
    assert instance.uuid == data["uuid"]


def test_training_data_insert_document_already_exists(test_connection):
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    temp_data = deepcopy(data)
    temp_data["uuid"] = Binary.from_uuid(temp_data["uuid"])
    test_connection.training_data.insert_one(temp_data)
    try:
        document.insert(**data)
    except Exception as e:
        expected_uuid = data['uuid']
        assert type(e) == DocumentAlreadyExistsException
        assert str(e) == f"Record with uuid: {expected_uuid} already exists"


def test_training_data_update_success(test_connection):
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.training_data.insert_one(data)
    update_data = {"text": "Python, Git, Linux"}
    updated_instance = document.update({"uuid": data["uuid"]}, update_one=True, update={"$set": update_data})
    assert updated_instance.text == "Python, Git, Linux"


def test_training_data_update_not_existing_entry():
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    data["uuid"] = Binary.from_uuid(data['uuid'])
    update_data = {"text": "Python, Git, Linux"}
    updated_instance = document.update({"uuid": data["uuid"]}, update_one=True, update={"$set": update_data})
    assert updated_instance is None


def test_training_data_aggregate_success(test_connection):
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    instance = TrainingData(**data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.training_data.insert_one(data)
    query = {"uuid": data["uuid"]}
    agg_query = [
        { "$match": query },
        { "$sample": { "size": 10}}
    ]
    results = document.aggregate(agg_query)
    assert results[0].uuid == instance.uuid


def test_training_data_find_success(test_connection):
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    instance = TrainingData(**data)
    data["uuid"] = Binary.from_uuid(data['uuid'])
    test_connection.training_data.insert_one(data)   
    found_instance = document.find({"uuid": data["uuid"]}, find_one=True) 
    assert instance.uuid == found_instance.uuid


def test_training_data_find_no_existing_entry():
    document = models.TrainingDataDocument()
    data = {
       "text": "Python",
       "uuid": uuid.uuid4(),
       "ents": [(0, 6, "Skill"),]
    }
    data["uuid"] = Binary.from_uuid(data['uuid'])
    found_instance = document.find({"uuid": data["uuid"]}, find_one=True) 
    assert found_instance is None
