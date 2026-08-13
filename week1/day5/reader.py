from pathlib import Path
from pypdf import PdfReader
from docx import Document


def read_pdf(file_path: str) -> str:
    """
    Read text from a PDF file.
    Args:
        file_path: Path to the PDF file.
    Returns:
        Extracted text as a single string.
    """
    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text.strip())

    return "\n\n".join(pages)


def read_docx(file_path: str) -> str:
    """
    Read text from a DOCX file.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        Extracted text as a single string.
    """
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def read_document(file_path: str) -> str:
    """
    Read PDF or DOCX based on file extension.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension == ".docx":
        return read_docx(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Only PDF and DOCX are supported."
        )