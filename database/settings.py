import os


DATABASE_SETTINGS =  {
    "MONGODB_HOST": os.environ.get("MONGODB_HOST", "localhost"),
    "MONGODB_PORT": os.environ.get("MONGODB_PORT", 27017),
    "MONGODB_DB": os.environ.get("MONGODB_HOST", "job_matcher"),
    "MONGODB_COLLECTION": os.environ.get("MONGODB_HOST", "offers"),
}
