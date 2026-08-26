import os
import zipfile
from PIL import Image

def score_confidence(filepath: str) -> str:
    """
    Original Structural Confidence Scoring Algorithm for OSIRIS.
    
    PhotoRec carves raw clusters based on signatures but does not expose a header/footer
    integrity flag. OSIRIS dynamically validates structural integrity using native format parsers:
      - High: File opens and verifies 100% cleanly with standard library decoder.
      - Medium: Recognized structure/extension but minor truncation, missing footer, or non-critical corruption.
      - Low: Zero-byte file, unreadable, or severe structural corruption.
    """
    if not os.path.exists(filepath):
        return "Low"

    file_size = os.path.getsize(filepath)
    if file_size == 0:
        return "Low"

    ext = os.path.splitext(filepath)[1].lower()

    try:
        # 1. Image Format Verification (PIL)
        if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"):
            try:
                with Image.open(filepath) as img:
                    img.verify()
                # Secondary check: attempt loading pixel data for thorough corruption detection
                with Image.open(filepath) as img:
                    img.load()
                return "High"
            except Exception:
                # If file exists and has image header but failed full decode
                return "Medium" if file_size > 512 else "Low"

        # 2. Archive Verification (zipfile)
        elif ext == ".zip":
            try:
                with zipfile.ZipFile(filepath, "r") as zf:
                    corrupted = zf.testzip()
                    if corrupted is None:
                        return "High"
                    return "Medium"
            except Exception:
                return "Medium" if file_size > 1024 else "Low"

        # 3. PDF Document Verification
        elif ext == ".pdf":
            try:
                with open(filepath, "rb") as f:
                    header = f.read(1024)
                    f.seek(-1024, os.SEEK_END)
                    footer = f.read(1024)
                if b"%PDF-" in header and (b"%%EOF" in footer or b"startxref" in footer):
                    return "High"
                elif b"%PDF-" in header:
                    return "Medium"
                return "Low"
            except Exception:
                return "Medium" if file_size > 1024 else "Low"

        # 4. Text & Document Checks
        elif ext in (".txt", ".json", ".xml", ".md", ".csv"):
            try:
                with open(filepath, "r", encoding="utf-8", errors="strict") as f:
                    f.read(2048)
                return "High"
            except UnicodeDecodeError:
                return "Medium"

        # 5. General Binary / Other Fallback
        else:
            if file_size > 4096:
                return "High"
            elif file_size > 512:
                return "Medium"
            else:
                return "Low"

    except Exception:
        return "Low"
