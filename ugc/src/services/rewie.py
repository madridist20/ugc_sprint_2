from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from src.core.settings import Settings
from src.db.mongo import Mongo
from src.models.rewie import Rewie

mongo = Mongo()

settings = Settings()


async def get_rewies_list(
    user_id: str,
    limit: int = settings.default_limit,
    offset: int = settings.default_offset,
) -> list[Rewie]:
    """Получить список рецензий"""
    data = await mongo.find(
        settings.mongo_collection_rewie, {"user_id": user_id}, limit=limit, offset=offset
    )
    return [Rewie(**item) async for item in data]


async def get_rewie(user_id: str, film_id: str) -> Optional[Rewie]:
    """Получить одну рецензию"""
    data = await mongo.find_one(
        settings.mongo_collection_rewie, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Rewie(**data)


async def create_rewie(user_id: str, film_id: str) -> Rewie:
    """Создать рецензию"""
    data = await mongo.find_one(
        settings.mongo_collection_rewie, {"user_id": user_id, "film_id": film_id}
    )
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = Rewie(user_id=user_id, film_id=film_id, dt=datetime.now())
    await mongo.insert(settings.mongo_collection_rewie, data.dict())
    return data


async def remove_rewie(user_id: str, film_id: str) -> None:
    """Удалить рецензию"""
    data = await mongo.find_one(
        settings.mongo_collection_rewie, {"user_id": user_id, "film_id": film_id}
    )
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(
        settings.mongo_collection_rewie, {"user_id": user_id, "film_id": film_id}
    )
