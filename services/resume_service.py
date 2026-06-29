import fitz


def extract_pdf_text(uploaded_file) -> str:
    """Extract readable text from an uploaded PDF file."""
    if uploaded_file is None:
        return ""

    try:
        pdf_bytes = uploaded_file.getvalue()
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages = [page.get_text("text") for page in document]
        document.close()
        return "\n\n".join(page for page in pages if page).strip()
    except Exception as exc:
        raise ValueError(f"Unable to read the PDF resume: {exc}") from exc
