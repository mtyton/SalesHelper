from database.db import get_db
from database.models import User
from database.hasher import hash_password


if __name__ == "__main__":
    db = next(get_db)
    