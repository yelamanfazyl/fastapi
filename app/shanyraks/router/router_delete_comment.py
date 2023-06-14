from fastapi import Depends, Response
from ..service import Service, get_service
from . import router
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.delete("/{id}/comments/{comment_id}", status_code=200)
def delete_comments(
    id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    result = svc.repository.delete_comment(id, comment_id, jwt_data.user_id)

    if result is None:
        return Response(status_code=404)

    if result.modified_count == 0:
        return Response(status_code=401)

    return Response(status_code=200)
