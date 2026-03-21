from pathlib import Path

import typer


app = typer.Typer()


@app.command()
def runserver(reload: bool = False):
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        env_file=".env",
        reload=reload,
        reload_dirs=[
            str(Path(__file__).parent)
        ]
    )


@app.command()
def resetdb():
    from backend.database import engine
    from backend.tables import metadata
    metadata.drop_all(engine)
    metadata.create_all(engine)


def main():
    app()


if __name__ == "__main__":
    main()