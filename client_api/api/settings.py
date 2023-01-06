import os


ALLOWED_ORIGINS = [
    "http://localhost",
    "localhost"
    "http://localhost:5001",
    "http://localhost:5173",
    "localhost:5001",
    "https://87fa-89-64-62-54.eu.ngrok.io",
    "127.0.0.1:5001",
    "127.0.0.1:5001",
    "http://127.0.0.1:5001",
    "http://127.0.0.1",
    "176.115.83.177"
]

DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")
