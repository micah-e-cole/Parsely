# search.py
import re
from pathlib import Path

def run(pattern, target, ignore_case=True, extension=""):
    """
    Generator that yields lines matching pattern in a file or directory.
    Compatible with both CLI and GUI frontends.
    """
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    path = Path(target)

    if not path.exists():
        yield f"Error: {target} does not exist."
        return  # ensures generator returns gracefully

    if extension and not extension.startswith("."):
        extension = "." + extension

    # Determine if target is a file or directory
    if path.is_file():
        yield from _search_file(path, regex)
    elif path.is_dir():
        for file in path.rglob(f"*{extension}" if extension else "*"):
            yield from _search_file(file, regex)
    else:
        yield f"Error: {target} is not a file or directory."

def _search_file(file_path, regex):
    """Helper function that yields matches from a single file."""
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                if regex.search(line):
                    yield f"{i} {line.strip()}"
    except Exception as e:
        yield f"Error reading {file_path}: {e}"
