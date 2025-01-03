from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip_address/hostname>/<database_name>'
# postgres://fastapi_a1v1_user:YCrDxTUFYnDQVnkYgw4EXPPpTMLwj91k@dpg-ckr4gm05vl2c73ak865g-a/fastapi_a1v1
# postgres://fastapi_a1v1_user:YCrDxTUFYnDQVnkYgw4EXPPpTMLwj91k@dpg-ckr4gm05vl2c73ak865g-a.oregon-postgres.render.com/fastapi_a1v1
SQLALCHEMY_DATABASE_URL = f"{settings.postgres_url}"



# local machine
# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# for documentation pupose only
# connection made using raw sql
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="Muna@1970",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("The error was", error)
#         time.sleep(2)
