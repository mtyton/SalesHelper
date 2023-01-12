from dataclasses import (
    dataclass,
    asdict
)
from sqlalchemy.orm import Session
from sqlalchemy import update

from database.db import Base


class ValidationException(Exception):
    ...


@dataclass
class DatabaseResponseBase:
    
    @classmethod
    def special_field_mappings(cls, instance: Base) -> dict:
        return {}

    @classmethod
    def from_db_instance(cls, instance: Base) -> object:
        special_mappings = cls.special_field_mappings(instance)
        data = {}
        for field in cls.__dataclass_fields__:
            if field in special_mappings:
                continue
            data[field] = getattr(instance, field)
        data.update(special_mappings)
        return cls(**data)


class DatabaseRequestBase:
    _model: Base = None
    _id_kwarg_name: str = "id"
    _id_lookup_name: str = "id"

    def map_to_database_fields(self, db: Session, **kwargs):
        ...

    def get_existing_entry(self, db: Session, **kwargs) -> Base:
        primary_key = kwargs.pop(self._id_kwarg_name, None)
        if not primary_key:
            return primary_key
        return db.query(self._model).filter(
            getattr(self._model, self._id_lookup_name).like(primary_key)
        ).first()

    def is_valid(self, db: Session, operation="insert", **kwargs, ):
        existing_entry = self.get_existing_entry(db, **kwargs)
        if operation == "insert":
            return not bool(existing_entry)
        elif operation == "update":
            return bool(existing_entry)

    def update(self, db: Session, **kwargs):
        data = self.map_to_database_fields(db=db, **kwargs)
        if not self.is_valid(db, operation="update", **kwargs):
            raise ValidationException(
                f"No existing record for model: {self._model} for primary_key: \
                {kwargs.get(self._id_kwarg_name)}"
        )
        instance = self.get_existing_entry(db, **kwargs)
        instance.update(**data)
        db.execute(
            update(instance).
            where(id=instance.id).
            values(asdict(instance))
        )
        db.commit()
        db.refresh(instance)
        return instance


    def insert(self, db: Session, **kwargs):
        data = self.map_to_database_fields(db=db, **kwargs)
        if not self.is_valid(db, operation="insert", **kwargs):
            raise ValidationException(f"Record already exists for model: {self._model}")
            
        instance = self._model(**data)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
