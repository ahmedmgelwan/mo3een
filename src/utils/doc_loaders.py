import os
from pypdf import PdfReader
from src.config import config


def _load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _load_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() for page in reader.pages]
    return "\n\n".join(pages).strip()

def load_docs() -> list[dict]:
    docs = []
    print(f"Loading documents from {config.DOCS_DIR}...")
    if not os.path.exists( config.DOCS_DIR):
        print(f"Warning: {config.DOCS_DIR} does not exist.")
        return docs

    for file_name in os.listdir(config.DOCS_DIR):
        print(f"Processing file: {file_name}")
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in config.SUPPORTED_FILE_TYPES:
            print(f"Warning: {file_name} has unsupported file type {ext}. Skipping.")
            continue

        if ext == '.pdf':
            text = _load_pdf(os.path.join(config.DOCS_DIR, file_name))

        else:
            text = _load_txt(os.path.join(config.DOCS_DIR, file_name))

        if not text.strip():
            print(f"Warning: {file_name} is empty or could not be read.")

        docs.append({
            "file_name": file_name,
            "text ": text,
        })

    return docs
            
