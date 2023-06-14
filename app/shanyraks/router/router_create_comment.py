from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateCommentRequest(AppModel):
    comment: str


@router.post("/{id}/comments", status_code=200)
def create_comment(
    id: str,
    input: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    comment = svc.repository.create_comment(id, user_id, input.comment)
    if comment is None:
        return Response(status_code=404)

    return Response(status_code=200)
