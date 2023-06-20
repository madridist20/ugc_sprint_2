"""CRUD на закладки."""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.bookmark import Bookmark
from services import bookmark
from services.auth import Auth

router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


@router.get("/", response_model=list[Bookmark], description="Получить список закладок")
async def get_bookmarks_list(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limit: int = 10,
    offset: int = 0,
) -> Any:
    """
    Список закладок
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    return await bookmark.get_bookmarks_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/{film_id}", response_model=Bookmark, description="Создать закладку")
async def create_bookmark(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Создать закладку
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    return await bookmark.create_bookmark(user_id=user_id, film_id=film_id)


@router.get("/{film_id}", response_model=Bookmark, description="Получить закладку")
async def read_category(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Получить закладку
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    bookm = await bookmark.get_bookmark(user_id=user_id, film_id=film_id)
    return bookm


@router.delete("/{film_id}", response_model=str, description="Удалить закладку")
async def delete_category(
    film_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Any:
    """
    Удалить закладку
    """
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    await bookmark.remove_bookmark(user_id=user_id, film_id=film_id)
    return "DONE"
