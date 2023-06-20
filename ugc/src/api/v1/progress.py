from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from db.kafka_producer import get_producer
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.progress_film import ProgressFilmModel
from services.auth import Auth

router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


@router.post("/progress_film/")
async def post_event(
    progress_film: ProgressFilmModel,
    producer: AIOKafkaProducer = Depends(get_producer),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    try:
        await producer.send(
            topic="views",
            value=progress_film.json().encode(),
            key=f"{user_id}+{progress_film.movie_id}".encode(),
        )
        return {"msg": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e.args[0].str()
        )
