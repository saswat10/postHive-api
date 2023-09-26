from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
# not required anymore because of the alembic migration

app = FastAPI()

# for security purposes never use wild card
# if it is for a specific app then only add that domain name
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

