"""
OSIRIS — Demo Environment Setup Script
=======================================
Creates all necessary demo input files and resets state for a clean assessor demo.

Run this ONCE before starting the demo:
    python demo_setup.py

This will:
  1. Create demo_workspace/recovery_source/ with 8 sample files across
     different categories and confidence levels.
  2. Create/recreate demo_disk_target.bin (1 MB) for the erase demo.
  3. Clear operations_log.json for a fresh audit trail.
  4. Clear old certificates for a clean certificate viewer.
  5. Remove old recovery output directories.
"""

import os
import sys
import json
import shutil
import zipfile
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_DIR = os.path.join(BASE_DIR, "demo_workspace")
RECOVERY_SOURCE = os.path.join(DEMO_DIR, "recovery_source")
DEMO_TARGET = os.path.join(BASE_DIR, "demo_disk_target.bin")
LOG_FILE = os.path.join(BASE_DIR, "operations_log.json")
CERT_DIR = os.path.join(BASE_DIR, "certificates")
RECOVERY_OUTPUT = os.path.join(BASE_DIR, "recovery_output")
RECOVERY_OUTPUT_WIPE = os.path.join(BASE_DIR, "recovery_output_wipe")


# ──────────────────────────────────────────────────────────────────────────────
# 1. RECOVERY SOURCE FILES (8 files across all categories & confidence tiers)
# ──────────────────────────────────────────────────────────────────────────────

def create_demo_recovery_source():
    """Creates a directory of sample files with varying integrity for confidence scoring demo."""

    if os.path.exists(RECOVERY_SOURCE):
        shutil.rmtree(RECOVERY_SOURCE)
    os.makedirs(RECOVERY_SOURCE, exist_ok=True)

    # ── FILE 1: Valid PNG Image ── (Expected: Images / High)
    print("  [1/8] classified_blueprint.png   → Images / High confidence")
    img = Image.new("RGB", (400, 300), color=(10, 20, 40))
    draw = ImageDraw.Draw(img)
    for x in range(0, 400, 40):
        draw.line([(x, 0), (x, 300)], fill=(40, 80, 120), width=1)
    for y in range(0, 300, 40):
        draw.line([(0, y), (400, y)], fill=(40, 80, 120), width=1)
    draw.rectangle([50, 50, 350, 250], outline=(0, 180, 255), width=2)
    draw.text((100, 120), "NTRO CLASSIFIED", fill=(255, 255, 255))
    draw.text((110, 150), "BLUEPRINT v2.1", fill=(100, 200, 255))
    img.save(os.path.join(RECOVERY_SOURCE, "classified_blueprint.png"))

    # ── FILE 2: Valid JPEG Photo ── (Expected: Images / High)
    print("  [2/8] surveillance_capture.jpg   → Images / High confidence")
    img2 = Image.new("RGB", (320, 240), color=(30, 30, 30))
    draw2 = ImageDraw.Draw(img2)
    draw2.ellipse([100, 60, 220, 180], fill=(60, 60, 60), outline=(0, 255, 0), width=1)
    draw2.text((80, 200), "CAM-04 2026-08-26 14:32", fill=(0, 255, 0))
    img2.save(os.path.join(RECOVERY_SOURCE, "surveillance_capture.jpg"), quality=85)

    # ── FILE 3: Valid ZIP Archive ── (Expected: Archives / High)
    print("  [3/8] evidence_archive.zip       → Archives / High confidence")
    zip_path = os.path.join(RECOVERY_SOURCE, "evidence_archive.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("access_logs.txt",
                     "2026-08-26 12:00:01 | 192.168.1.105 | ACCESS GRANTED | LEVEL-3\n" * 20)
        zf.writestr("incident_notes.md",
                     "# Incident Report IR-2026-0842\n\nClassified briefing notes.\n")

    # ── FILE 4: Valid PDF Document ── (Expected: Documents / High)
    print("  [4/8] operation_report.pdf       → Documents / High confidence")
    pdf_path = os.path.join(RECOVERY_SOURCE, "operation_report.pdf")
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n")
        f.write(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        f.write(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
        f.write(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n")
        f.write(b"xref\n0 4\n")
        f.write(b"0000000000 65535 f \n")
        f.write(b"0000000009 00000 n \n")
        f.write(b"0000000058 00000 n \n")
        f.write(b"0000000115 00000 n \n")
        f.write(b"trailer\n<< /Size 4 /Root 1 0 R >>\n")
        f.write(b"startxref\n183\n%%EOF\n")

    # ── FILE 5: Valid Text Log ── (Expected: Documents / High)
    print("  [5/8] network_intercept.txt      → Documents / High confidence")
    txt_path = os.path.join(RECOVERY_SOURCE, "network_intercept.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for i in range(50):
            f.write(f"[2026-08-26T{12 + i // 60:02d}:{i % 60:02d}:00Z] "
                    f"SRC:10.0.0.{i + 1} DST:172.16.0.1 PROTO:TCP PORT:443 STATUS:CAPTURED\n")

    # ── FILE 6: Corrupted JPEG (bad body) ── (Expected: Images / Medium)
    print("  [6/8] corrupted_photo.jpg        → Images / Medium confidence")
    corrupted_path = os.path.join(RECOVERY_SOURCE, "corrupted_photo.jpg")
    with open(corrupted_path, "wb") as f:
        f.write(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00")
        f.write(os.urandom(2048))  # Random garbage → truncated/corrupted image body

    # ── FILE 7: Truncated PDF (no %%EOF) ── (Expected: Documents / Medium)
    print("  [7/8] partial_document.pdf       → Documents / Medium confidence")
    partial_pdf = os.path.join(RECOVERY_SOURCE, "partial_document.pdf")
    with open(partial_pdf, "wb") as f:
        f.write(b"%PDF-1.4\n")
        f.write(b"1 0 obj\n<< /Title (Classified Operations Manual) >>\nendobj\n")
        f.write(os.urandom(1500))  # Truncated body, missing %%EOF footer

    # ── FILE 8: Tiny unidentifiable fragment ── (Expected: Other / Low)
    print("  [8/8] fragment_0x3f.dat          → Other / Low confidence")
    fragment_path = os.path.join(RECOVERY_SOURCE, "fragment_0x3f.dat")
    with open(fragment_path, "wb") as f:
        f.write(os.urandom(128))  # Tiny unidentifiable binary fragment

    file_count = len(os.listdir(RECOVERY_SOURCE))
    print(f"\n  ✅ Recovery source created: {RECOVERY_SOURCE}")
    print(f"     {file_count} files spanning Images, Documents, Archives, Other")
    print(f"     Confidence mix: ~4 High, ~2 Medium, ~1-2 Low")


# ──────────────────────────────────────────────────────────────────────────────
# 2. WIPE TARGET (sensitive data-filled 1 MB file)
# ──────────────────────────────────────────────────────────────────────────────

def create_demo_wipe_target():
    """Creates a 1 MB demo disk target file filled with recognizable 'sensitive' data."""
    print("\n  Creating demo wipe target...")
    total_size = 1024 * 1024  # 1 MB
    pattern = b"CLASSIFIED_NTRO_SECRET_DATA_BLOCK_"

    with open(DEMO_TARGET, "wb") as f:
        written = 0
        while written < total_size:
            chunk = pattern[:min(len(pattern), total_size - written)]
            f.write(chunk)
            written += len(chunk)

    size_kb = os.path.getsize(DEMO_TARGET) / 1024
    print(f"  ✅ Wipe target created: {DEMO_TARGET} ({size_kb:.0f} KB)")
    print(f"     Content: repeating 'CLASSIFIED_NTRO_SECRET_DATA_BLOCK_' pattern")


# ──────────────────────────────────────────────────────────────────────────────
# 3. STATE RESET (clean log, certificates, recovery output)
# ──────────────────────────────────────────────────────────────────────────────

def reset_operations_log():
    """Clears the operations log for a fresh demo."""
    print("\n  Resetting operations log...")
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)
    print(f"  ✅ Operations log cleared: {LOG_FILE}")


def reset_certificates():
    """Removes old certificates for a clean demo."""
    print("  Clearing old certificates...")
    if os.path.exists(CERT_DIR):
        certs = [c for c in os.listdir(CERT_DIR) if c.endswith(".txt")]
        for c in certs:
            os.remove(os.path.join(CERT_DIR, c))
        print(f"  ✅ Removed {len(certs)} old certificates")
    else:
        os.makedirs(CERT_DIR, exist_ok=True)
        print("  ✅ Certificates directory created (was empty)")


def clean_recovery_outputs():
    """Removes old recovery output directories."""
    print("  Cleaning recovery output directories...")
    removed = 0
    for d in [RECOVERY_OUTPUT, RECOVERY_OUTPUT_WIPE]:
        if os.path.exists(d):
            shutil.rmtree(d)
            removed += 1
    # Also clean demo_workspace outputs
    demo_out = os.path.join(DEMO_DIR, "recovery_output")
    if os.path.exists(demo_out):
        shutil.rmtree(demo_out)
        removed += 1
    print(f"  ✅ Cleaned {removed} old recovery output directories")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 70)
    print("       OSIRIS — DEMO ENVIRONMENT SETUP")
    print("       Preparing all demo inputs and resetting state")
    print("=" * 70)
    print()

    print("─── PHASE 1: Creating Recovery Source Files ───")
    create_demo_recovery_source()

    print("\n─── PHASE 2: Creating Wipe Target ───")
    create_demo_wipe_target()

    print("\n─── PHASE 3: Resetting State for Clean Demo ───")
    reset_operations_log()
    reset_certificates()
    clean_recovery_outputs()

    print()
    print("=" * 70)
    print("       ✅ DEMO ENVIRONMENT READY")
    print("=" * 70)
    print()
    print("  Created files:")
    print(f"    • {RECOVERY_SOURCE}  (8 sample files)")
    print(f"    • {DEMO_TARGET}  (1 MB wipe target)")
    print()
    print("  Cleared state:")
    print(f"    • {LOG_FILE}  (empty)")
    print(f"    • {CERT_DIR}  (empty)")
    print()
    print("  ─── NEXT STEPS ───")
    print(f"  1. Launch OSIRIS:")
    print(f"       python -m streamlit run src/app.py")
    print(f"  2. Follow DEMO_GUIDE.md for step-by-step instructions")
    print()


if __name__ == "__main__":
    main()
