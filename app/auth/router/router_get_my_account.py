from fastapi import Depends
from pydantic import BaseModel
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class GetMyInfoResponse(BaseModel):
    email: str
    phone: str
    name: str
    city: str


@router.patch("/users/me", status_code=200, response_model=GetMyInfoResponse)
def update_user(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user_id = jwt_data.user_id

    return svc.repository.get_user_by_id(user_id)
