from fastapi import Depends, Response
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class DeleteShanyrakRequest(AppModel):
    id: str


@router.delete("/shanyraks/{id}", status_code=200)
def delete_shanyrak(
    id: str,
    input: DeleteShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.delete_shanyrak_by_id(id, jwt_data.user_id)

    print(shanyrak)

    if shanyrak is False:
        return Response(status_code=404)

    return Response(status_code=200)
