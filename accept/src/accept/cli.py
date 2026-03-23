import os

import typer

from dotenv import load_dotenv


app = typer.Typer()


@app.command()
def runbrowser(user: str, port: int):
    from accept.drivers.selenium.brower import startbrowser
    driver = startbrowser(port, user)
    while True:
        try:
            _ = driver.current_url
        except Exception:
            break


def main():
    load_dotenv(".env")
    app()


if __name__ == "__main__":
    main()