import os


DATABASE_SETTINGS =  {
    "HOST": os.environ.get("MONGODB_HOST", "localhost"),
    "PORT": os.environ.get("MONGODB_PORT", 27017),
    "DB": os.environ.get("MONGODB_HOST", "job_matcher"),
    "COLLECTION": os.environ.get("MONGODB_HOST", "offers"),
    "USER": os.environ.get("MONGODB_USER", "root"),
    "PASSWORD": os.environ.get("PASSWORD", "password")
}
