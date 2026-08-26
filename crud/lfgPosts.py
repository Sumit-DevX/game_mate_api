from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas import LFG_Post

from fastapi import HTTPException

def get_lfg_post_by_id(post_id : int, db: Session ):
    requested_lfg_post = db.scalar(select(LFG_Post).where(LFG_Post.id == post_id))

    if requested_lfg_post is None:
        raise HTTPException(
            status_code = 404,
            detail="Post Not Found"
        )
    else:
        return requested_lfg_post