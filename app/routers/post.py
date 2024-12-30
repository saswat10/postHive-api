from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, ouath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, select

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# get all the posts
@router.get(
    "/",
    response_model=schemas.AllPostOut,
)
def get_posts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(ouath2.get_current_user),
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = "",
    published: Optional[bool] = True,
):
    # calculate offset for pagination
    offset = (page - 1) * limit
    total_posts_results = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .filter(models.Post.published == published)
        .count()
    )
    total_posts = total_posts_results

    posts_results = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .filter(models.Post.published == published)
        .offset(offset)
        .limit(limit)
    )
    posts = posts_results.all()

    response = []
    for post in posts:
        # count the likes
        likes_count = (
            db.query(models.Vote).filter(models.Vote.post_id == post.id).count()
        )

        # check if user has upvoted
        upvoted = db.query(models.Vote).filter(
            models.Vote.post_id == post.id, models.Vote.user_id == current_user.id
        )
        upvote_by_user = upvoted.first() is not None

        response.append({"Post": post, "upvoted": upvote_by_user, "votes": likes_count})

    total_pages = (total_posts + limit - 1) // limit
    metadata = {
        "count": total_posts,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }

    return {"info": metadata, "results": response}


# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get post by id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # print(post)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # don't do .all() -> waste of postgres resources
    # better to do .first() -> if you know that there will be only
    # one instance of that id.
    # results = (
    #     db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    #     .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #     .group_by(models.Post.id)
    #     .filter(models.Post.id == id)
    #     .first()
    # )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )
    
    likes_count = (
            db.query(models.Vote).filter(models.Vote.post_id == post.id).count()
        )

        # check if user has upvoted
    upvoted = db.query(models.Vote).filter(
            models.Vote.post_id == post.id, models.Vote.user_id == current_user.id
        )
    upvote_by_user = upvoted.first() is not None

    response = []
    response.append({"Post": post, "upvoted": upvote_by_user, "votes": likes_count})


    return response[0]


# delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post
@router.put(
    "/{id}",
    response_model=schemas.Post,
)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE posts  SET title = %s, content = %s ,published= %s WHERE id = %s""",
    #     (post.title, post.content, post.published, str(id)),
    # )

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_first = post_query.first()

    if not post_first:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} was not found",
        )

    if post_first.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action",
        )

    post_query.update(post.model_dump(), synchronize_session=False)  # type: ignore
    db.commit()

    return post_query.first()

