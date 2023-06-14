from fastapi import Depends, Response

from app.utils import AppModel
from typing import Any, List
from pydantic import Field

from ..service import Service, get_service
from . import router


class CommentSchema(AppModel):
    id: Any = Field(alias="_id")
    content: str
    created_at: str
    author_id: str


class GetCommentResponse(AppModel):
    comments: List[CommentSchema]


@router.get("/{id}/comments", response_model=GetCommentResponse, status_code=200)
def get_comments(
    id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    comments = svc.repository.get_comments(id)

    if comments is None:
        return Response(status_code=404)

    coms = []

    for comment in comments:
        created_at = str(comment["created_at"])
        author_id = str(comment["author_id"])
        coms.append(
            CommentSchema(
                id=comment["id"],
                content=comment["content"],
                created_at=created_at,
                author_id=author_id,
            )
        )

    return GetCommentResponse(comments=coms)
