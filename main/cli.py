import typer
from search import run  # ✅ Make sure this matches your actual filename (search.py)

app = typer.Typer(help="Parsely: Search and filter text across files and directories")

@app.command()
def find(
    pattern: str = typer.Argument(..., help="Text or regex pattern to search for"),
    path: str = typer.Option(".", "--path", "-p", help="Directory to search in"),
    ignore_case: bool = typer.Option(True, "--ignore-case", "-i", help="Ignore case when matching"),
    extension: str = typer.Option("", "--extension", "-e", help="Filter by file extension (e.g. .txt, .log)"),
):
    """
    Search for PATTERN in files under PATH.
    """
    run(pattern, path, ignore_case, extension)  # ✅ variable names must match exactly here

if __name__ == "__main__":
    app()
