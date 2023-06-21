"""CRUD на лайки."""
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.like import Like
from services import likes
from services.auth import Auth

router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


@router.get("/", response_model=list[Like], description="Список лайков")
async def get_likes_list(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limit: Annotated[int, Query(description='Pagination page size', ge=1)] = 10,
    offset: Annotated[int, Query(description='Pagination page offset', ge=0)] = 0,
) -> Any:
    """
    Список лайков
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    return await likes.get_likes_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/{film_id}", response_model=Like, description="Создать лайк")
async def create_like(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Создать лайк
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    return await likes.create_like(user_id=user_id, film_id=film_id)


@router.get("/{film_id}", response_model=Like, description="Получить лайк")
async def read_category(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Получить лайк
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    like = await likes.get_like(user_id=user_id, film_id=film_id)
    return like


@router.delete("/{film_id}", response_model=str, description="Удалить лайк")
async def delete_category(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Удалить лайк
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    await likes.remove_like(user_id=user_id, film_id=film_id)
    return "DONE"
