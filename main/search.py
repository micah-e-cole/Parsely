# search.py
import re
from pathlib import Path
import openpyxl
import pdfplumber
import docx


def run(pattern, target, ignore_case=True, extension="", pdf_mode="text"):
    """
    Generator yielding lines or cells matching pattern in a file or directory.
    Supports plain text, PDF, DOCX, and Excel (.xlsx).
    Used by both CLI and GUI.
    """

    # Normalize flags and paths (cross-OS safe)
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)

    # Expand "~" and resolve any relative path (macOS-safe)
    path = Path(target).expanduser().resolve()

    if not path.exists():
        yield f"Error: {target} does not exist."
        return

    # Normalize extension
    if extension and not extension.startswith("."):
        extension = "." + extension

    # FILE SEARCH
    if path.is_file():
        yield from _search_file(path, regex, pdf_mode)
        return

    # DIRECTORY SEARCH (NAME MATCH ONLY)
    if path.is_dir():

        # Search both files and subfolders by *name only*
        for item in path.rglob("*"):
            if regex.search(item.name):
                # Return relative path from the searched folder
                rel = item.relative_to(path)
                yield str(rel)

        return

    yield f"Error: {target} is not a file or directory."


def _search_file(file_path, regex, pdf_mode="text"):
    """Call correct search backend depending on file suffix."""
    suffix = file_path.suffix.lower()

    if suffix == ".xlsx":
        yield from _search_excel(file_path, regex)
    elif suffix == ".pdf":
        yield from _search_pdf(file_path, regex)
    elif suffix == ".docx":
        yield from _search_docx(file_path, regex)
    else:
        yield from _search_text(file_path, regex)


# ----------------------------------
# TEXT FILE SEARCH
# ----------------------------------
def _search_text(file_path, regex):
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f, start=1):
                if regex.search(line):
                    yield f"{i} {line.strip()}"
    except Exception as e:
        yield f"Error reading {file_path}: {e}"


# ----------------------------------
# EXCEL SEARCH
# ----------------------------------
def _search_excel(file_path, regex):
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            for r_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
                for c_idx, cell in enumerate(row, start=1):
                    if cell and isinstance(cell, str) and regex.search(cell):
                        cell_ref = f"{openpyxl.utils.get_column_letter(c_idx)}{r_idx}"
                        yield f"Sheet: {sheet} | Cell {cell_ref} | {cell}"
        wb.close()
    except Exception as e:
        yield f"Error reading Excel file {file_path}: {e}"


# ----------------------------------
# PDF SEARCH
# ----------------------------------
def _search_pdf(file_path, regex):
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):

                text = page.extract_text()
                if not text:
                    continue  # skip blank pages

                text = re.sub(r"\s+", " ", text)

                for match in regex.finditer(text):
                    start, end = match.span()
                    extracted = text[start:]

                    period_index = extracted.find(".")
                    if period_index != -1:
                        extracted = extracted[:period_index + 1]

                    yield f"Page {page_num}: {extracted.strip()}"

    except Exception as e:
        yield f"Error reading {file_path}: {e}"


# ----------------------------------
# DOCX SEARCH
# ----------------------------------
def _search_docx(file_path, regex):
    try:
        document = docx.Document(file_path)

        # PARAGRAPHS
        for i, para in enumerate(document.paragraphs, start=1):
            text = para.text.strip()
            if text and regex.search(text):
                yield f"Paragraph {i}: {text}"

        # TABLES
        seen = set()  # de-duplicate merged table cells
        for t_idx, table in enumerate(document.tables, start=1):
            for r_idx, row in enumerate(table.rows, start=1):
                for c_idx, cell in enumerate(row.cells, start=1):
                    text = cell.text.strip()
                    if text and text not in seen and regex.search(text):
                        seen.add(text)
                        yield f"Table {t_idx}, Row {r_idx}, Col {c_idx}: {text}"

    except Exception as e:
        yield f"Error reading {file_path}: {e}"
