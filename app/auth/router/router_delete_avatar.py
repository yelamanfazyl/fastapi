from fastapi import Depends, Response
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.delete("/users/avatar")
def delete_avatar(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user_id = jwt_data.user_id

    url = svc.repository.get_avatar_url(user_id)

    if url is None:
        return Response(status_code=404)

    result = svc.repository.delete_avatar(user_id)

    if result.modified_count == 0:
        return Response(status_code=404)

    svc.s3_service.delete_file(user_id, url)

    return Response(status_code=200)
