import os


DATABASE_SETTINGS =  {
    "HOST": os.environ.get("MONGODB_HOST", "mongodb"),
    "PORT": os.environ.get("MONGODB_PORT", 27017),
    "DB": os.environ.get("MONGODB_DB", "job_matcher"),
    "RAW_COLLECTION": os.environ.get("RAW_COLLECTION", "offers"),
    "DOCCANO_COLLECTION": os.environ.get("RAW_COLLECTION", "doccano_offers"),
    "TRAINING_COLLECTION": os.environ.get("RAW_COLLECTION", "training_offers"),
    "USER": os.environ.get("MONGODB_USER", "root"),
    "PASSWORD": os.environ.get("PASSWORD", "password")
}
