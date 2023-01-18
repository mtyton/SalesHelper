from dataclasses import dataclass
from uuid import UUID

from api.schemas.base import (
    DatabaseRequestBase,
    DatabaseResponseBase
)
from database.models import User
from database.hasher import hash_password


@dataclass 
class UserCreateRequest(DatabaseRequestBase):
    username: str
    password: str
    email: str

    _model = User

    def __post_init__(self, *args, **kwargs):
        self.password = hash_password(self.password)

    def map_to_database_fields(self, db, **kwargs):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }


@dataclass
class UserTokenResponse:
    access_token: str
    refresh_token : str


@dataclass
class UserResponse(DatabaseResponseBase):
    username: str
    password: str
    email: str
    

@dataclass
class TokenPayload:
    sub: int = None
    exp: int = None
