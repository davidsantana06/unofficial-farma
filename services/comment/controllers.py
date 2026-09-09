from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import Comment
from schemas import CommentCreate, CommentUpdate

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "comment"}


@router.post("/comments", response_model=Comment, status_code=201)
def create_comment(payload: CommentCreate, session: Session = Depends(get_session)):
    comment = Comment.model_validate(payload)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.get("/comments", response_model=list[Comment])
def list_comments(
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    return session.exec(select(Comment).offset(offset).limit(limit)).all()


@router.get("/comments/{comment_id}", response_model=Comment)
def get_comment(comment_id: int, session: Session = Depends(get_session)):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment


@router.patch("/comments/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    session: Session = Depends(get_session),
):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(comment, key, value)
    comment.updated_at = datetime.now(timezone.utc)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, session: Session = Depends(get_session)):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    session.delete(comment)
    session.commit()
