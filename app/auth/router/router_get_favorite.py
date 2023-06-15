from fastapi import Depends, Response
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.utils import AppModel
from typing import Any, List
from pydantic import Field
from app.auth.router.dependencies import parse_jwt_user_data
from app.shanyraks.repository.repository import ShanyrakRepository
from app.config import database


class ShanyrakSchema(AppModel):
    id: Any = Field(alias="_id")
    address: str


class GetFavoritesResponse(AppModel):
    shanyraks: List[ShanyrakSchema]


@router.get(
    "/users/favorites/shanyraks", response_model=GetFavoritesResponse, status_code=200
)
def get_favorites(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    result = svc.repository.get_favorite_shanyraks(user_id)

    if result is None:
        return Response(status_code=404)

    shanyraks = []

    shanyrak_rep = ShanyrakRepository(database)

    for shanyrak_id in result:
        shanyrak = shanyrak_rep.get_shanyrak_by_id(shanyrak_id)
        shanyraks.append(ShanyrakSchema(**shanyrak))

    return GetFavoritesResponse(shanyraks=shanyraks)
