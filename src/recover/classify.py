import os

CATEGORY_MAP = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".bmp": "Images", ".webp": "Images", ".tiff": "Images", ".ico": "Images",
    # Documents
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents", ".txt": "Documents",
    ".xlsx": "Documents", ".xls": "Documents", ".pptx": "Documents", ".csv": "Documents",
    ".rtf": "Documents", ".md": "Documents",
    # Archives
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives", ".7z": "Archives",
    ".rar": "Archives", ".bz2": "Archives",
    # Media (Audio / Video)
    ".mp3": "Media", ".wav": "Media", ".flac": "Media", ".mp4": "Media",
    ".avi": "Media", ".mkv": "Media", ".mov": "Media",
    # Code / System
    ".py": "Code/System", ".exe": "Code/System", ".dll": "Code/System",
    ".sh": "Code/System", ".json": "Code/System", ".xml": "Code/System"
}

def classify(filepath: str) -> str:
    """Classifies a recovered file into a human-readable category based on extension."""
    ext = os.path.splitext(filepath)[1].lower()
    return CATEGORY_MAP.get(ext, "Other")
