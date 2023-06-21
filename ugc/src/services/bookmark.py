from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from src.core.settings import Settings
from src.db.mongo import Mongo
from src.models.bookmark import Bookmark

mongo = Mongo()

settings = Settings()


async def get_bookmarks_list(
    user_id: str,
    limit: int = settings.default_limit,
    offset: int = settings.default_offset,
) -> list[Bookmark]:
    """Получить список закладок"""
    data = await mongo.find(
        settings.mongo_collection_bookmark, {"user_id": user_id}, limit=limit, offset=offset
    )
    return [Bookmark(**item) async for item in data]


async def get_bookmark(user_id: str, film_id: str) -> Optional[Bookmark]:
    """Получить одну закладку"""
    data = await mongo.find_one(
        settings.mongo_collection_bookmark, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Bookmark(**data)


async def create_bookmark(user_id: str, film_id: str) -> Bookmark:
    """Создать закладку"""
    data = await mongo.find_one(
        settings.mongo_collection_bookmark, {"user_id": user_id, "film_id": film_id}
    )
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = Bookmark(user_id=user_id, film_id=film_id, dt=datetime.now())
    await mongo.insert(settings.mongo_collection_bookmark, data.dict())
    return data


async def remove_bookmark(user_id: str, film_id: str) -> None:
    """Удалить закладку"""
    data = await mongo.find_one(
        settings.mongo_collection_bookmark, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(
        settings.mongo_collection_bookmark, {"user_id": user_id, "film_id": film_id}
    )
