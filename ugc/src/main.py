""" Основной модуль сервиса UGC """

import logging

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import progress, rewies, bookmarks
from core.settings import Settings
from db import kafka_producer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import likes

settings = Settings()


if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=settings.traces_sample_rate,
    )

app = FastAPI(
    title="API for posting user-generated content events to UGC db",
    docs_url="/ugc/openapi",
    openapi_url="/ugc/openapi.json",
    description="",
    default_response_class=ORJSONResponse,
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    """Инициализация продьюсера кафки"""
    kafka_producer.aio_producer = AIOKafkaProducer(
        **{
            "bootstrap_servers": "{}:{}".format(
                settings.kafka_host, settings.kafka_port
            )
        }
    )
    await kafka_producer.aio_producer.start()


@app.on_event("shutdown")
async def shutdown():
    """Окончание работы продьюсера."""
    await kafka_producer.aio_producer.stop()


app.include_router(progress.router, prefix="/ugc/v1", tags=["progress_film"])
app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["bookmarks"])
app.include_router(rewies.router, prefix="/api/v1/rewies", tags=["rewies"])

if __name__ == "__main__":
    logging.info("Start application")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
    )
