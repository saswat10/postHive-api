# PostHive - API
**PostHive** is a dynamic social platform that enables users to share posts, comment, and vote in an interactive and community-driven environment. The name reflects the collaborative and buzzing activity, akin to a hive of ideas and discussions.

Core features include:

- [x] User Management: User authentication (login and registration) with hashed passwords.
- [x] Posting: Users can create, read, update, and delete text posts.
- [ ] Commenting: Users can comment on posts.
- [X] Voting: Users can upvote or downvote posts.
- [ ] Sorting: Posts can be retrieved based on popularity or creation time.

## Table of Contents

- PostHive Components
- Documentation - API

## PostHive Components

1. PostHive-api: Python API written in FastAPI
2. *PostHive-app: Mobile App written in Kotlin (TODO)*

## Documentation - API

### Tech Stack
- Backend Framework: FastAPI - High-performance Python web framework.
- Database: NeonDB - Serverless PostgreSQL.
- ORM: SQLAlchemy - For database interaction.
- Authentication: OAuth2 with JSON Web Tokens (JWT).
- Testing: Pytest.
<!-- - Dependency Management: Poetry (or pip. -->
<!-- - Containerization: Docker (optional). -->

### Project Setup

1. Clone the repository
   ```bash
   git clone https://github.com/your-repo/social-platform-api.git
   cd social-platform-api
   ```
2. Create virtual environment
    ```bash
    python -m venv env
    source env/scripts/activate # on windows: env/scripts/Activate.ps1
    ```
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables
    ```python
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_PASSWORD=# password
    DATABASE_NAME= # database-name
    DATABASE_USERNAME=# database-username
    SECRET_KEY= # Generated-Key
    ALGORITHM= # Algorithm used
    ACCESS_TOKEN_EXPIRE_MINUTES= #Time

    # use this if you do not have postgres installed
    POSTGRES_URL="<Your remote postgres url if you >" 
    ```

    > if using **neon database** or any other db url then add "+psycopg" after postgresql in the url, your url should look something like this
    postgresql+psycopg://**************@#############?sslmode=require


    ```sh
    # example generation of the key
    $ openssl rand -hex 32
    ```
5. Initialize the Database
    ```bash
    alembic revision --autogenerte -m "create tables"
    alembic upgrade head
    ```
6. Run the application
    ```bash
    uvicorn app.main:app --reload
    # or use fastapi
    fastapi dev app/main.py
    ```
7. Access the API - Visit `http://127.0.0.1:8000/docs` to explore the API with Swagger UI.

--- 
### Future Enhancements
- [ ] Adding media support (image and video uploads).
- [ ] Implementing real-time features (e.g., notifications).
- [ ] Advanced search and sorting.
  

--- 

Feel free to reach out for further clarification or support!