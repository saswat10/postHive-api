from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import post, user, auth, vote, comments
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


description = """
**PostHive** is a dynamic social platform that enables users to share posts, comment, and vote in an interactive and community-driven environment. The name reflects the collaborative and buzzing activity, akin to a hive of ideas and discussions.

Core features include:

- User Management: User authentication (login and registration) with hashed passwords.
- Posting: Users can create, read, update, and delete text posts.
- Commenting: Users can comment on posts.
- Voting: Users can upvote or downvote posts.
- Sorting: Posts can be retrieved based on popularity or creation time.

"""

# uncomment the code below if you plan to use SQLalchemy
# instead of Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PostHive API",
    description=description,
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://github.com/saswat10/postHive-api?tab=MIT-1-ov-file",
        "identifier": "MIT"
    },
    docs_url="/docs",
    redoc_url=None,
)

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
    content = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/simpledotcss/2.3.3/simple.min.css">
    <title>PostHive - API</title>
    </head>

    <body>
    <header>
        <h1>PostHive</h1>
    </header>
    <main>

        <p>PostHive is a dynamic social platform that enables users to share posts, comment, and vote in an interactive and
        community-driven environment. The name reflects the collaborative and buzzing activity, akin to a hive of ideas
        and discussions.</p>
        <article>
        <h2>Core Features</h2>
        <ul>
            <li>User Management: User authentication (login and registration) with hashed passwords.</li>
            <li>Posting: Users can create, read, update, and delete text posts.</li>
            <li>Commenting: Users can comment on posts.</li>
            <li>Voting: Users can upvote or downvote posts.</li>
            <li>Sorting: Posts can be retrieved based on popularity or creation time.</li>
        </ul>

        </article>



        <button onclick="window.location.href='https://posthive-api.onrender.com/docs';">
        API Documentation
        </button>
        <button onclick="window.location.href='https://github.com/saswat10/postHive-api';">
        GitHub Repository
        </button>
        <button onclick="window.location.href='https://github.com/saswat10/postHive-app';">
        Android App Under Development
        </button>
    </body>

    </main>

    </html>
    """
    return HTMLResponse(content=content)


app.include_router(vote.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comments.router)
