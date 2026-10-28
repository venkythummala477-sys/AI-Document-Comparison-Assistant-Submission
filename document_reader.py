
from pypdf import PdfReader

MAX_CHARS = 60000

def extract_pdf_text(uploaded_file):
    if uploaded_file is None:
        raise ValueError("Please upload a PDF file.")

    if uploaded_file.size == 0:
        raise ValueError("The uploaded PDF is empty.")

    try:
        reader = PdfReader(uploaded_file)

        if reader.is_encrypted:
            raise ValueError("Password-protected PDFs are not supported.")

        pages = []
        for number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                pages.append(f"[Page {number}]\n{text.strip()}")

        full_text = "\n\n".join(pages).strip()

    except ValueError:
        raise
    except Exception as error:
        raise ValueError("Unable to read this PDF.") from error

    if not full_text:
        raise ValueError(
            "No readable text found. Scanned PDFs require OCR."
        )

    if len(full_text) > MAX_CHARS:
        raise ValueError(
            f"PDF is too long. Maximum allowed: {MAX_CHARS} characters."
        )

    return {
        "text": full_text,
        "pages": len(reader.pages)
    }
