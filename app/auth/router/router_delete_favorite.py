from fastapi import Depends, Response
from . import router
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.delete(
    "/users/favorites/shanyraks/{id}",
    status_code=200,
)
def delete_favorite(
    id: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    result = svc.repository.delete_favorite_shanyrak(jwt_data.user_id, id)

    if result.modified_count == 0:
        return Response(status_code=404)

    return Response(status_code=200)
