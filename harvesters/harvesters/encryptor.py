from hashlib import sha256
from uuid import UUID


def encrypt_uuid(uuid:str) -> UUID:
    hash = sha256(uuid.encode("utf-8")).hexdigest()
    return UUID(hash[::2])
