from fastapi import APIRouter , Depends, HTTPException

from crud.games import get_game_by_id
from crud.users import get_user_by_id
from crud.lfgPosts import get_lfg_post_by_id

from database import get_db

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas import LFG_Post , Join_Request
from models import LFGPostModel , LFGPostResponseModel , JoinRequestModel , JoinRequestUpdateModel

router = APIRouter(prefix="/lfg", tags=["LFG_Posts"])

@router.post("",response_model=LFGPostResponseModel)
def create_lfgPost(post : LFGPostModel ,db : Session = Depends(get_db)):
    user = get_user_by_id(post.user_id)

    game = get_game_by_id(post.game_id)

    new_lfg_post = LFG_Post(
        user_id = user.id,
        game_id = game.id,
        title = post.title,
        players_needed = post.players_needed,
        message = post.message
    )

    db.add(new_lfg_post)
    db.commit()

    return LFGPostResponseModel.model_validate(new_lfg_post)

@router.get("",response_model=List[LFGPostResponseModel])
def get_lfg_posts(db : Session = Depends(get_db), game_id : int = None):
    stmt = select(LFG_Post)

    if game_id is None:
        lfg_posts = db.scalars(stmt)
        return lfg_posts.all()
    else:
        requested_lfg_posts = db.scalars(select(LFG_Post).where(LFG_Post.game_id == game_id))
        return requested_lfg_posts.all()

    
@router.get("/{post_id}", response_model=LFGPostResponseModel)
def get_lfg_post(post_id : int, db: Session = Depends(get_db)):
    requested_lfg_post = get_lfg_post_by_id(post_id, db)
    return LFGPostResponseModel.model_validate(requested_lfg_post)

@router.post("/{post_id}/join",response_model=JoinRequestModel)
def create_join_request(post_id : int , usr_id : int , db : Session = Depends(get_db)):
    lfg_post = get_lfg_post_by_id(post_id,db)

    requesting_user = get_user_by_id(usr_id,db)

    if lfg_post.user_id == requesting_user.id:
        raise HTTPException(
            status_code=409,
            detail="User cannot request to his/her own lfg_post"
        )

    existing_request = db.scalar(
        select(Join_Request).where(
            Join_Request.lfg_post_id == post_id,
            Join_Request.user_id == usr_id
        )
    )

    if existing_request is not None:
        raise HTTPException(
            status_code=409,
            detail="User has already requested to join this LFG"
        )

    
    new_join_request = Join_Request(
        lfg_post_id = lfg_post.id,
        user_id = requesting_user.id,
        status = "pending"
    )

    db.add(new_join_request)
    db.commit()

    return JoinRequestModel.model_validate(new_join_request)


@router.get("/{post_id}/requests", response_model=List[JoinRequestModel])
def get_join_requests(post_id : int, db : Session = Depends(get_db)):
    lfg_post = get_lfg_post_by_id(post_id,db)

    requests = lfg_post.join_requests

    return requests

@router.patch("/{post_id}/requests/{user_id}",response_model=JoinRequestModel)
def approve_request(post_id:int , user_id:int, request : JoinRequestUpdateModel ,db : Session = Depends(get_db), ):
    lfg_post = get_lfg_post_by_id(post_id,db)

    user = get_user_by_id(user_id,db)

    join_request = db.scalar(
        select(Join_Request).where(
            Join_Request.lfg_post_id == lfg_post.id,
            Join_Request.user_id == user.id
        )
    )

    if join_request is None:
        raise HTTPException(
            status_code=404,
            detail="Join Request Not Found"
        )


    if join_request.status != "pending":
        raise HTTPException(
            status_code=409,
            detail="Join Request Already Processed"
        )
    
    if request.status not in ["accepted", "rejected"]:  
        raise HTTPException(
            status_code=409,
            detail="Invalid Request"
        )

    join_request.status = request.status
    db.commit() 

    return JoinRequestModel.model_validate(join_request)
    
