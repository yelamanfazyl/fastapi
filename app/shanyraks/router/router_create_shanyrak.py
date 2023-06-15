from fastapi import Depends, Response

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
    location = svc.here_service.get_coordinates(input.address)

    lat = location["lat"]
    lng = location["lng"]

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
            "location": [lat, lng],
        }
    )

    print(shanyrak_id)

    if shanyrak_id is None:
        return Response(status_code=401)

    return CreateShanyrakResponse(id=shanyrak_id)
