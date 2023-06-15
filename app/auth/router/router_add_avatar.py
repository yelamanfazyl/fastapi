from fastapi import Depends, Response, UploadFile
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.post("/users/avatar")
def add_avatar(
    file: UploadFile,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user_id = jwt_data.user_id

    url = svc.repository.get_avatar_url(user_id)

    if url is not None:
        svc.s3_service.delete_file(user_id, url)

    result = svc.repository.add_avatar(
        user_id,
        svc.s3_service.upload_file(file.file, user_id, file.filename),
    )

    if result.modified_count == 0:
        return Response(status_code=404)

    return Response(status_code=200)
