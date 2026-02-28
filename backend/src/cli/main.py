import typer


app = typer.Typer()


@app.command()
def runserver(test: bool = False):
    import uvicorn
    if test:
        uvicorn.run("api.main:app", reload=True, env_file=".env.test")
    else:
        uvicorn.run("api.main:app")


@app.command()
def resetdb():
    from api.database import engine
    from api.tables import metadata
    metadata.drop_all(engine)
    metadata.create_all(engine)


def main():
    app()


if __name__ == "__main__":
    main()