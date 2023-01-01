import os

DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")


