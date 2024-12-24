from pydantic import MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db_service: MongoDsn = MongoDsn("mongodb://localhost:27017/")


settings = Settings()
