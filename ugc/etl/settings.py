from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str = 'localhost'
    kafka_port: int = 9092
    kafka_topic: str = 'views'
    clickhouse_host: str = 'localhost'
    clickhouse_port: str = 9000
    messages_count: int = 1
    project_name: str = 'api kafka'
    KAFKA_INSTANCE = f"{kafka_host}:{kafka_port}"

    class Config:
        env_file = ".env"
