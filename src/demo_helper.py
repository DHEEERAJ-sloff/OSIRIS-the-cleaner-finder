import os
import zipfile
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def prepare_demo_environment() -> dict:
    """
    Creates a clean, realistic test dataset (sample images, zip archives, documents)
    and packages them into a test target image file for instant live demos.
    """
    demo_dir = os.path.join(BASE_DIR, "demo_workspace")
    sample_files_dir = os.path.join(demo_dir, "sample_files")
    os.makedirs(sample_files_dir, exist_ok=True)

    # 1. Create Sample PNG Image
    img_path = os.path.join(sample_files_dir, "classified_blueprint.png")
    img = Image.new("RGB", (300, 300), color=(10, 132, 255))
    draw = ImageDraw.Draw(img)
    draw.text((30, 130), "NTRO CONFIDENTIAL", fill=(255, 255, 255))
    img.save(img_path)

    # 2. Create Sample ZIP Archive
    zip_path = os.path.join(sample_files_dir, "evidence_archive.zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("network_logs.txt", "192.168.1.1 ACCESS GRANTED AT 2026-08-26\n")

    # 3. Create Sample Document
    doc_path = os.path.join(sample_files_dir, "operation_report.pdf")
    with open(doc_path, "wb") as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<< /Title (OSIRIS Incident Report) >>\nendobj\n%%EOF\n")

    # 4. Bundle into synthetic target image
    target_img_path = os.path.join(demo_dir, "demo_disk_media.bin")
    with open(target_img_path, "wb") as target:
        target.write(b"RAW_DISK_HEADER_SECTOR_0\n" + b"\x00" * 4096)
        for fname in ["classified_blueprint.png", "evidence_archive.zip", "operation_report.pdf"]:
            fp = os.path.join(sample_files_dir, fname)
            with open(fp, "rb") as sf:
                target.write(f"\n--- FILE:{fname} ---\n".encode() + sf.read())
        target.write(b"\n" + b"\xFF" * 4096)

    return {
        "demo_dir": demo_dir,
        "sample_files_dir": sample_files_dir,
        "target_img_path": target_img_path,
        "file_count": 3
    }
