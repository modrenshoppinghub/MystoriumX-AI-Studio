"""
Utility functions for file handling and text parsing.
"""

import logging
from pathlib import Path
from typing import List
import docx
import pypdf

from config import LOG_FILE_PATH, LOG_FORMAT

def setup_logger(name: str) -> logging.Logger:
    """Configures structured logging across modules."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

class DocumentLoader:
    """Handles reading TXT, DOCX, and PDF document formats."""
    
    @staticmethod
    def load_document(file_path: Path) -> str:
        """Parses document based on file extension."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Script file not found: {path}")

        ext = path.suffix.lower()
        if ext == ".txt":
            return DocumentLoader._load_txt(path)
        elif ext == ".docx":
            return DocumentLoader._load_docx(path)
        elif ext == ".pdf":
            return DocumentLoader._load_pdf(path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _load_txt(path: Path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _load_docx(path: Path) -> str:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    @staticmethod
    def _load_pdf(path: Path) -> str:
        reader = pypdf.PdfReader(path)
        text_chunks = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_chunks.append(extracted)
        return "\n".join(text_chunks)
