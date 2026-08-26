# OSIRIS — Integrated Secure Data Erasure & Advanced File Recovery Platform

**Integrated Secure Data Erasure & Advanced File Recovery Prototype**  
**Built for PS 26149 (NTRO)**

OSIRIS is a unified forensic security platform combining standards-compliant data sanitization (forked **SecureWipe** engine), deep file carving (unmodified **PhotoRec** binary), and an original layer providing a dark-mode Streamlit dashboard, structural format confidence scoring, extension classification, and SHA-256 tamper-evident audit log chaining.

---

## Key Features

- **🔥 Secure Data Erasure Engine**:
  - DoD 5220.22-M / NIST 800-88 3-pass sector overwriting (Zero -> Ones -> Cryptographic Random).
  - Safety-typed confirmation guard preventing accidental drive destruction.
  - Automatic generation of cryptographic sanitization certificates.

- **🔍 Advanced File Carving & Recovery Subsystem**:
  - Subprocess integration with PhotoRec portable binary for deep sector carving across 480+ file extensions.
  - **Original Confidence Scoring**: Validates file integrity using Python libraries (`PIL.Image`, `zipfile`, header checks) to assign **High**, **Medium**, or **Low** confidence badges.
  - Automatic category grouping (Images, Documents, Archives, Media, Code/System).

- **📜 Tamper-Evident Audit Logging**:
  - Cryptographic SHA-256 hash chaining of all operations saved to `operations_log.json`.
  - Built-in audit verification tool to detect log file tampering.

---

## Quick Start & Setup

### Prerequisites
- Python 3.10+
- Git (Windows / Linux)

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd d:\sih_prooject\OSIRIS
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the OSIRIS Streamlit Platform:
   ```bash
   streamlit run src/app.py
   ```
   *(Note: Raw physical disk wiping or raw physical drive carving requires running your command prompt / terminal as Administrator on Windows or `sudo` on Linux.)*

4. Run the Automated Test Suite:
   ```bash
   python -m unittest tests/test_osiris.py
   ```

---

## System Architecture & Attribution

| Layer / Component | Implementation | Attribution & License |
|---|---|---|
| **GUI Dashboard** | Custom Streamlit App (`src/app.py`) | Original OSIRIS Work (GPL-3.0) |
| **Erase Engine** | Forked `SecureWipe` (`erase_engine/`) | GPL-3.0 (See `erase_engine/MODIFICATIONS.md`) |
| **Recovery Engine** | PhotoRec Portable Executable (`recovery_tool/`) | GPL-2.0+ (Unmodified Binary, CGSecurity) |
| **Confidence Scoring** | Original Structural Parser (`src/recover/scoring.py`) | Original OSIRIS Work |
| **Audit Logger** | SHA-256 Hash Chain Manager (`src/shared/`) | Original OSIRIS Work |

See `NOTICE.md` for full open-source license details.
