from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from ..entities.post import Post
from .models import PostCreateModel, PostUpdateModel

class PostService:
    async def get_all_posts(self, session: AsyncSession):
        statement = select(Post).order_by(desc(Post.created_at))
        result = await session.exec(statement)
        return result.all()
    

    async def get_post(self, post_uid: str, session: AsyncSession):
        statement = select(Post).where(Post.uid == post_uid)
        result = await session.exec(statement)
        post = result.first()
        return post if post is not None else None
    
    async def get_user_posts(self, user_uid: str, session: AsyncSession):
        statement = select(Post).where(Post.user_uid == user_uid).order_by(desc(Post.updated_at))
        result = await session.exec(statement)
        return result.all()

    async def create_post(self, post_data: PostCreateModel, user_id: str, session: AsyncSession):
        post_data_dict = post_data.model_dump()
        new_post = Post(**post_data_dict)
        new_post.user_uid = user_id
        session.add(new_post)
        await session.commit()
        return new_post
    

    async def update_post(self, post_uid: str, update_post_data: PostUpdateModel, session: AsyncSession):
        post_to_update = await self.get_post(post_uid, session)
        
        if post_to_update is not None:
            update_post_dict = update_post_data.model_dump()

            for k, v in update_post_dict.items():
                setattr(post_to_update, k, v)
            
            await session.commit()
            return post_to_update
        else:
            None


    async def delete_post(self, post_uid: str, session: AsyncSession):
        post_to_delete = await self.get_post(post_uid, session)

        if post_to_delete is not None:
            await session.delete(post_to_delete)
            await session.commit()
            return {}
        else:
            None
