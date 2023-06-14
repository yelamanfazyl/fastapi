from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from typing import List
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class DeleteShanyrakMediaRequest(AppModel):
    media: List[str]


@router.delete("/{id}/media", status_code=200)
def delete_media_shanyrak(
    id: str,
    input: DeleteShanyrakMediaRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if shanyrak is None:
        return Response(status_code=404)

    user_id = jwt_data.user_id

    if user_id != str(shanyrak["user_id"]):
        return Response(status_code=401)

    for file in input.media:
        svc.s3_service.delete_file(id, file)
        svc.repository.delete_shanyrak_media(id, file)

    return Response(status_code=200)
