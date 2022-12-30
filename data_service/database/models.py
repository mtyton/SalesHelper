from typing import (
    Union, 
    Type,
    List,
    Dict,
    Any,
    Iterable
)
from dataclasses import asdict

from database.db import conn
from database.exceptions import DocumentAlreadyExistsException
from database.schemas import (
    JobOffer, 
    DoccanoData,
    TrainingData
)

class MongoDocumentBase:

    collection_name: Union[str, None] = None
    mongo_dataclass: Union[Type, None] = None

    @property
    def collection(self):
        if not hasattr(conn, self.collection_name):
            raise ValueError(f"Unknown collection name: {self.collection_name} for MongoDB")
        return getattr(conn, self.collection_name)

    # TODO - add skip, limit test
    def find(
        self, query: Dict[str, Any], find_one: bool = False,
        skip: int = None, limit: int = None
    ) -> Union[List[mongo_dataclass], mongo_dataclass]:
        if find_one:
            data = self.collection.find_one(query)
        else:
            data = self.collection.find(query)
        if skip is not None and not find_one:
            data = data.skip(skip)
        if limit is not None and not find_one:
            data = data.limit(limit)    
        # if nothing has been found, return None
        if data is None:
            return
        
        if isinstance(data, Iterable) and not isinstance(data, dict):
            return [self.mongo_dataclass.from_db_instance(**d) for d in data]
        return self.mongo_dataclass.from_db_instance(**data)

    def aggregate(self, query: List[Dict[str, Any]]) -> Union[List[mongo_dataclass], mongo_dataclass]:
        data = self.collection.aggregate(query)
        if data is None:
            return
        return [self.mongo_dataclass.from_db_instance(**d) for d in data]

    def validate(self, instance: mongo_dataclass):
        """
        This method has to be implemented for each subclass seprately.
        """
        ...

    def update(
        self, query: Union[Dict[str, Any], List[Dict[str, Any]]], 
        update: Union[Dict[str, Any], List[Dict[str, Any]]], update_one:bool = False
    ) -> Union[List[mongo_dataclass], mongo_dataclass]:
        if update_one:
            self.collection.update_one(query, update)
        else:
            self.collection.update(query, update)

        return self.find(query, find_one=update_one)
        
    def insert(self, **kwargs) -> mongo_dataclass:
        instance = self.mongo_dataclass(**kwargs)
        self.validate(instance)
        self.collection.insert_one(instance.get_database_dict())
        return instance

    def count_documents(self, query: Dict[str, Any]):
        return self.collection.count_documents(query)


class JobOfferDocument(MongoDocumentBase):

    collection_name: Union[str, None] = "raw_data"
    mongo_dataclass: Union[Type, None] = JobOffer

    def validate(self, instance):
        data = instance.get_database_dict()
        existing_entry = self.collection.find_one({"uuid": data["uuid"]})
        if existing_entry:
            raise DocumentAlreadyExistsException(
                f"Record with uuid: {instance.uuid} already exists"
            )


class DoccanoDataDocument(MongoDocumentBase):
    collection_name: Union[str, None] = "doccano_data"
    mongo_dataclass: Union[Type, None] = DoccanoData


class TrainingDataDocument(MongoDocumentBase):
    collection_name: Union[str, None] = "training_data"
    mongo_dataclass: Union[Type, None] = TrainingData
