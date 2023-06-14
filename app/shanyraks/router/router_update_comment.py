from fastapi import Depends, Response
from ..service import Service, get_service
from . import router
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel


class UpdateShanyrakRequest(AppModel):
    content: str


@router.patch("/{id}/comments/{comment_id}", status_code=200)
def update_comments(
    id: str,
    comment_id: str,
    input: UpdateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    result = svc.repository.update_comment(
        id, comment_id, jwt_data.user_id, input.content
    )

    if result is None:
        return Response(status_code=404)

    if result.modified_count == 0:
        return Response(status_code=401)

    return Response(status_code=200)
