from pydantic import HttpUrl, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongo_db_service: MongoDsn = MongoDsn("mongodb://localhost:27017/")
    crowdstrike_token: str
    crowdstrike_base_url: HttpUrl = HttpUrl("https://api.recruiting.app.silk.security/api")
    qualys_token: str
    qualys_base_url: HttpUrl = HttpUrl("https://api.recruiting.app.silk.security/api")


settings = Settings()  # type: ignore
