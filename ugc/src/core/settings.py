from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    jwt_secret_key: str = "top_secret"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "ugc_db"
    MONGO_COLLECTION_LIKE: str = "likedFilms"
    MONGO_COLLECTION_REWIE: str = "rewieFilms"
    MONGO_COLLECTION_BOOKMARK: str = "bookmarkFilms"
    DEFAULT_LIMIT: int = 10
    DEFAULT_OFFSET: int = 0
    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
