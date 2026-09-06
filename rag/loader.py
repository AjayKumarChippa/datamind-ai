from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def load_pdf(file_path: str) -> str:
    """Load text from a PDF file and return the combined page text."""
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        reader = PdfReader(pdf_path)
    except PdfReadError as exc:
        raise PdfReadError(f"Failed to parse PDF: {file_path}") from exc

    text_parts: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_parts.append(page_text)

    return "\n\n".join(text_parts)
