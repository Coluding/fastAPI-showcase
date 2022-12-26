import sqlalchemy.exc
from fastapi import FastAPI, Response,HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, database, oauth, models

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exist!")

    query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)

    found_vote = query.first()

    if vote.dir == 1:
        try:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user {current_user.id} has already"
                                                                                 f"voted on post {vote.post_id}")

            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "sucessfully upvoted post"}

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post vote is already deleted or post does"
                                                                              " not exist!")

        query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}


