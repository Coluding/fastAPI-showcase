from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas, oauth
from sqlalchemy import func

router = APIRouter(prefix="/posts",
                   tags=["Posts"])


@router.get("/",  response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    posts = db.query(models.PostModel).filter(models.PostModel.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.PostModel, func.count(models.Vote.post_id).label("votes")).filter(models.PostModel.title.contains(search))\
        .join(models.Vote, models.Vote.post_id == models.PostModel.id, isouter=True)\
        .group_by(models.PostModel.id).limit(limit).offset(skip).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    new_post = models.PostModel(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: Session=Depends(oauth.get_current_user)):

    post = db.query(models.PostModel, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.PostModel.id, isouter=True)\
        .group_by(models.PostModel.id).filter(models.PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found!")

    if post.PostModel.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized for this request!")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: Session = Depends(oauth.get_current_user)):
    del_post = db.query(models.PostModel).filter(models.PostModel.id == id)

    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    if del_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")

    del_post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: Session = Depends(oauth.get_current_user)):


    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    #post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    if post_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
