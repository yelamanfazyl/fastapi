from fastapi import Depends

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateShanyrakResponse(AppModel):
    id: str


@router.post("/", response_model=CreateShanyrakResponse, status_code=200)
def create_shanyrak(
    input: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    shanyrak_id = svc.repository.create_shanyrak(
        {
            "user_id": user_id,
            "type": input.type,
            "price": input.price,
            "address": input.address,
            "area": input.area,
            "rooms_count": input.rooms_count,
            "description": input.description,
        }
    )

    print(shanyrak_id)

    return CreateShanyrakResponse(id=shanyrak_id)
