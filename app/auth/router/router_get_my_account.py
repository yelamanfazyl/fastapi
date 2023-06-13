from fastapi import Depends
from app.utils import AppModel
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from typing import Any
from pydantic import Field


class GetMyInfoResponse(AppModel):
    id: Any = Field(alias="_id")
    email: str
    phone: str = ""
    name: str = ""
    city: str = ""


@router.get("/users/me", status_code=200, response_model=GetMyInfoResponse)
def get_user(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user_id = jwt_data.user_id

    return svc.repository.get_user_by_id(user_id)
