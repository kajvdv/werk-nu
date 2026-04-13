import os

from sqlalchemy import create_engine

from backend.config import settings


DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=False)


def get_conn():
    with engine.connect() as conn:
        yield conn
        conn.commit()
