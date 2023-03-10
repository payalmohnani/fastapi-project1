from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db 
from .. import models, schemas, oauth2

router = APIRouter(prefix= "/posts", tags=["Posts"])

# create a post (Create)
@router.post("",status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get all posts (Read)
@router.get("", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit:int = 10, skip: int = 0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts """) 
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result

# get a particular post by id
@router.get("/{id}", response_model=schemas.PostOut) # id represents path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user) ):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


# update a post
@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, (str(id),)) )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} does not exist.")
    
    if post.owner_id  != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = f"Not authorized to perform requested action.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post
    

# update a post partially
# @app.patch("/posts/{id}", status_code = status.HTTP_202_ACCEPTED)
# def patch_post(id: int, post: Post):
# 
    # cursor.execute("""UPDATE posts SET WHERE id = %s""",id)

    # if id == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                         detail = f"Post with id {id} does not exist.")

    # post_dict = post.dict()
    # print(post_dict)
    # for key,value in post_dict.items():
    #     # if the value is updated
    #     if value != None:
    #         my_posts[index].update({key:value})
    
    # # print(my_posts)
    # return {"message": "patched"}
        

# delete a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Not authorized to perform the requested action.")
    
    post_query.delete(synchronize_session = "fetch")
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

