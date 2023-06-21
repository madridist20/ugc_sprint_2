from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    jwt_secret_key: str = "top_secret"
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "ugc_db"
    mongo_collection_like: str = "likedFilms"
    mongo_collection_rewie: str = "rewieFilms"
    mongo_collection_bookmark: str = "bookmarkFilms"
    default_limit: int = 10
    default_offset: int = 0
    sentry_dsn: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
