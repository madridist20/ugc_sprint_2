import orjson as orjson
from pydantic import UUID4, BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseUGCModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ProgressFilmModel(BaseUGCModel):
    movie_id: UUID4
    viewing_progress: int
