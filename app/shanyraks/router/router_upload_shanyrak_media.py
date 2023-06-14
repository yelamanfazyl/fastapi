from fastapi import Depends, Response, UploadFile
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from typing import List

from ..service import Service, get_service
from . import router


@router.post("/{id}/media", status_code=200)
def upload_media_shanyrak(
    id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if shanyrak is None:
        return Response(status_code=404)

    user_id = jwt_data.user_id

    if user_id != str(shanyrak["user_id"]):
        return Response(status_code=401)

    for file in files:
        url = svc.s3_service.upload_file(file.file, id, file.filename)
        svc.repository.add_shanyrak_media(id, url)

    return Response(status_code=200)
