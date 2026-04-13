import os
from pathlib import Path
from urllib.parse import urlparse

import typer
from dotenv import load_dotenv

from backend.schemas.user import UserCreate
from backend.config import settings


BACKEND_URL = settings.backend_url


app = typer.Typer()


@app.command()
def runserver(reload: bool = False):
    import uvicorn
    url = BACKEND_URL
    host, port = urlparse(url).netloc.split(":") # Will break with real urls
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=int(port),
        env_file=".env",
        reload=reload,
        reload_dirs=[
            str(Path(__file__).parent)
        ] if reload else None
    )


@app.command()
def resetdb():
    from backend.database import engine
    from backend.tables import metadata
    metadata.drop_all(engine)
    metadata.create_all(engine)


@app.command()
def createsuperuser():
    from backend.services.user import UserService
    from backend.services.auth import AuthService
    from backend.services.mail import MailService
    from backend.database import get_conn

    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    user = UserCreate(
        name=name,
        email=email,
        password=password,
    ) 
    for conn in get_conn():
        mail_service = MailService()
        auth_service = AuthService(conn, mail_service)
        user_service = UserService(conn, auth_service)
        user_service.create_user(user, active=True)
        

def main():
    load_dotenv(".env")
    app()


if __name__ == "__main__":
    main()