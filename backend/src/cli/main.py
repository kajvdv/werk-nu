import typer
import uvicorn


app = typer.Typer()


@app.command()
def runserver():
    uvicorn.run("api.main:app", reload=True)


def main():
    app()


if __name__ == "__main__":
    main()