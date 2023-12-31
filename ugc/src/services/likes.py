from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from src.core.settings import Settings
from src.db.mongo import Mongo
from src.models.like import Like

mongo = Mongo()

settings = Settings()


async def get_likes_list(
    user_id: str,
    limit: int = settings.default_limit,
    offset: int = settings.default_offset,
) -> list[Like]:
    """Получить список лайков"""
    data = await mongo.find(
        settings.mongo_collection_like, {"user_id": user_id}, limit=limit, offset=offset
    )
    return [Like(**item) async for item in data]


async def get_like(user_id: str, film_id: str) -> Optional[Like]:
    """Получить один лайк"""
    data = await mongo.find_one(
        settings.mongo_collection_like, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Like(**data)


async def create_like(user_id: str, film_id: str) -> Like:
    """Создать лайк"""
    data = Like(user_id=user_id, film_id=film_id, dt=datetime.now())
    await mongo.upsert(settings.mongo_collection_like, data.dict())
    return data


async def remove_like(user_id: str, film_id: str) -> None:
    """Удалить лайк"""
    data = await mongo.find_one(
        settings.mongo_collection_like, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(
        settings.mongo_collection_like, {"user_id": user_id, "film_id": film_id}
    )
