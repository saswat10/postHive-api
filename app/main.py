from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .posts.controller import post_router
from .auth.controller import auth_router
from .comments.controller import comments_router
from .votes.controller import vote_router
from .communities.controller import community_router
from .errors import register_all_errors


version = "v2"
version_prefix = f"/api/{version}"

app = FastAPI(
    title="PostHive API",
    version=version,
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
    description=""
)

origins = ["*"]

register_all_errors(app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router, prefix=f"{version_prefix}/posts", tags=["posts"])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(comments_router, prefix=f"{version_prefix}/comments", tags=["comments"])
app.include_router(vote_router, prefix=f"{version_prefix}/vote", tags=["vote"])
app.include_router(community_router, prefix=f"{version_prefix}/communities", tags=["community"])