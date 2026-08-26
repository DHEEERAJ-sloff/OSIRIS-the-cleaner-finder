# OSIRIS — Technical Architecture Document

**Platform**: Integrated Secure Data Erasure & Advanced File Recovery Prototype  
**Target Proposal**: PS 26149 (NTRO)

---

## 1. Architectural Overview

OSIRIS is designed around a modular decoupled architecture comprising three distinct tiers:

```
+-------------------------------------------------------------------------+
|                         OSIRIS STREAMLIT GUI                            |
|                            (src/app.py)                                 |
+-------------------+---------------------------------+-------------------+
                    |                                 |
                    v                                 v
+-----------------------------------+ +-----------------------------------+
|      SECURE ERASE SUBSYSTEM       | |    FILE CARVING & RECOVERY      |
|    (erase_engine / SecureWipe)    | |    (recovery_tool / PhotoRec)     |
+-------------------+---------------+ +-----------------+-----------------+
                    |                                   |
                    v                                   v
+-----------------------------------+ +-----------------------------------+
|   Cryptographic Certificate Gen   | |  Structural Confidence Engine     |
|   (certificates/Wipe_Cert_*.txt)  | |      (src/recover/scoring.py)    |
+-------------------+---------------+ +-----------------+-----------------+
                    |                                   |
                    +-----------------+-----------------+
                                      |
                                      v
                    +-----------------------------------+
                    |   SHA-256 Tamper-Evident Audit Log|
                    |    (src/shared/log_store.py)      |
                    +-----------------------------------+
```

---

## 2. Integrated Engines vs. Original OSIRIS Work

### Integrated Third-Party Engines
1. **SecureWipe (Forked, Python)**:
   - Integrated under `/erase_engine/`.
   - Refactored for programmatic Python invocation (`run_wipe()`), returning structured result objects instead of interactive CLI prompts.
   - Provides multi-pass sector overwriting compliant with DoD 5220.22-M and NIST 800-88 standards.

2. **PhotoRec (Unmodified Portable Binary, C)**:
   - Integrated under `/recovery_tool/`.
   - Executed via non-interactive subprocess flags (`/log /d <output_dir> /cmd <target> search`).
   - Carves raw clusters across 480+ file extensions without altering target media.

### Original OSIRIS Contributions
1. **Unified Streamlit Dashboard (`src/app.py`)**:
   - Modern dark-themed cyber UI with live progress indicators, safety guards, category filters, and audit verification tools.

2. **Structural Confidence Scoring Engine (`src/recover/scoring.py`)**:
   - PhotoRec does not expose header/footer match confidence flags. OSIRIS builds an independent verification layer using format parsers:
     - **Images**: Verified using `PIL.Image.verify()` and full buffer loading.
     - **Archives**: Verified using `zipfile.ZipFile.testzip()`.
     - **Documents**: Header signature (`%PDF-`) and EOF boundary checks.
     - Scores each file dynamically as **High**, **Medium**, or **Low**.

3. **Tamper-Evident Audit System (`src/shared/models.py`, `src/shared/log_store.py`)**:
   - Each operation generates a SHA-256 hash incorporating entry metadata and the SHA-256 hash of the preceding entry.
   - Any manual edit or corruption in `operations_log.json` breaks hash validation and is instantly flagged.

---

## 3. Safety & Confirmation Guards

- **Strict Path Match Guard**: Data erasure operations block execution unless the user explicitly types the target device path or `CONFIRM-ERASE`.
- **Target Device Enumeration**: Cross-platform enumeration discovers physical drives and synthetic test images for safe rehearsal without risking system partitions.
