from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import post, user, auth, vote, comments
from fastapi.middleware.cors import CORSMiddleware


# uncomment the code below if you plan to use SQLalchemy 
# instead of Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello world!!"}


app.include_router(vote.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comments.router)
