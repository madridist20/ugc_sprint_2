"""CRUD на рецензии."""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.rewie import Rewie
from services import rewie
from services.auth import Auth

router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


@router.get("/", response_model=list[Rewie], description="Список рецензий")
async def get_rewies_list(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limit: int = 10,
    offset: int = 0,
) -> Any:
    """
    Список рецензий
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    return await rewie.get_rewies_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/{film_id}", response_model=Rewie, description="Создать рецензию")
async def create_rewie(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Создать рецензию
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    return await rewie.create_rewie(user_id=user_id, film_id=film_id)


@router.get("/{film_id}", response_model=Rewie, description="Получить рецензию")
async def read_category(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Получить рецензию
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    rew = await rewie.get_rewie(user_id=user_id, film_id=film_id)
    return rew


@router.delete("/{film_id}", response_model=str, description="Удалить рецензию")
async def delete_category(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Удалить рецензию
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    await rewie.remove_rewie(user_id=user_id, film_id=film_id)
    return "DONE"
