import typer

from app.application import main


def cli():
    typer.run(main)


if __name__ == "__main__":
    cli()
