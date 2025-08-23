from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .db.main import init_db
from .posts.controller import post_router
from .auth.controller import auth_router

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server has been stopped")

version = "v2"
version_prefix = f"/api/{version}"

app = FastAPI(
    title="PostHive API",
    lifespan=life_span,
    version=version,
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router, prefix=f"{version_prefix}/posts", tags=["posts"])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])