from fastapi import Depends, Response
from pydantic import BaseModel
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class UpdateUserRequest(BaseModel):
    phone: str
    name: str
    city: str


@router.patch("/users/me")
def update_user(
    input: UpdateUserRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    print(input.dict())
    svc.repository.update_user(user_id, input.dict())
    return Response(status_code=200)
