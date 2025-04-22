import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
settings = Settings()
