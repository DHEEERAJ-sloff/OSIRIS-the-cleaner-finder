# OSIRIS — Notice & Third-Party Attributions

This project integrates open-source forensic engines as part of the OSIRIS Integrated Secure Data Erasure & Advanced File Recovery Prototype.

## Integrated Engines

### 1. SecureWipe (Data Erasure Engine)
- **Source**: https://github.com/Grujowmi/SecureWipe
- **License**: GNU General Public License v3 (GPL v3)
- **Status**: Forked & Refactored under `/erase_engine/`. Modifications documented in `erase_engine/MODIFICATIONS.md`.

### 2. PhotoRec (File Carving & Recovery Engine)
- **Source**: https://github.com/cgsecurity/testdisk (CGSecurity / Christophe GRENIER)
- **License**: GNU General Public License v2+ (GPL v2+)
- **Status**: Included unmodified as a portable executable under `/recovery_tool/`.

---

## Original OSIRIS Components
- Streamlit Unified Interactive Dashboard (`src/app.py`)
- Programmatic Python Wrappers (`src/erase/wrapper.py`, `src/recover/wrapper.py`)
- File Extension Classification (`src/recover/classify.py`)
- Library-Based Structural Verification & Confidence Scoring (`src/recover/scoring.py`)
- Tamper-Evident SHA-256 Audit Log System (`src/shared/models.py`, `src/shared/log_store.py`)
