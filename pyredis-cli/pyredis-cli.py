import typer
from typing_extensions import Annotated


DEFAULT_PORT = 6379
DEFAULT_SERVER = "127.0.0.1"


def main(
    server: Annotated[str, typer.Argument()] = DEFAULT_SERVER,
    port: Annotated[int, typer.Argument()] = DEFAULT_PORT,
):
    while True:
        command = input(f"{server}:{port}>")

        if command == 'quit':
            break



if __name__ == "__main__":
    typer.run(main)