from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import post, user, auth, vote, comments
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from .db.main import init_db


# uncomment the code below if you plan to use SQLalchemy
# instead of Alembic
# models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server has been stopped")

app = FastAPI(
    title="PostHive API",
    lifespan=life_span
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vote.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comments.router)
