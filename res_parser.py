from pdfminer.high_level import extract_text # type: ignore

def extract_text_from_pdf(uploaded_file):
    return extract_text(uploaded_file)
