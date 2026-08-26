# OSIRIS — Evaluator Demo Guide

Welcome to the OSIRIS integrated forensic workstation. This guide provides a step-by-step walkthrough to demonstrate the three core capabilities of the platform:

1. **Target Sanitization & Cryptographic Erasure** (NIST 800-88 / DoD 5220.22-M)
2. **Advanced Deep File Carving & Structural Confidence Scoring**
3. **Tamper-Evident SHA-256 Audit Log Chain Verification**

---

## 🛠️ Step 0: One-Time Environment Setup (Run This First)

> This only needs to be done ONCE before each demo. It resets all state and creates fresh demo files.

### On Windows:
Double-click **`start_demo.bat`** in the project root.

It will automatically:
1. Run `demo_setup.py` — creates all demo input files and resets the audit log
2. Launch the OSIRIS Streamlit dashboard in your browser

### Manual Launch (if preferred):
```bash
# Step 1 — Set up demo environment (creates files, resets log)
python demo_setup.py

# Step 2 — Launch the OSIRIS Dashboard
python -m streamlit run src/app.py
```

**What `demo_setup.py` does:**
- Creates `demo_workspace/recovery_source/` with 8 forensic sample files (Images, Archives, Documents) spanning all confidence tiers.
- Creates `demo_disk_target.bin` (1 MB) filled with a repeating `CLASSIFIED_NTRO_SECRET_DATA_BLOCK_` pattern to simulate a sensitive disk image.
- Clears `operations_log.json` for a clean audit trail.
- Removes old certificates and recovery output folders.

> **The script will print the exact path to your recovery source folder at the end.** Copy that path — you will need to paste it in Step 2.

The OSIRIS Dashboard will open automatically at **`http://localhost:8501`** in your browser.

---

## 🛡️ Step 1: Secure Data Sanitization (Erase Engine)

**Objective**: Demonstrate safety guards, NIST 800-88 3-pass sector overwriting, and certificate generation.

### Execution Flow:
1. In the Web UI, navigate to the **`01 SANITIZATION`** tab.
2. In the **"Target Device"** dropdown, the demo target is pre-selected:
   `OSIRIS Demo Target Disk Image (demo_disk_target.bin)`
3. Note the **"Sanitization Standard"** is already set to `NIST 800-88 / DoD 5220.22-M (3-Pass Sector Overwrite)`.
4. In the **"Safety & Execution"** panel, note the **DESTRUCTIVE OPERATION WARNING** box.
5. Set Execution Mode to **`LIVE OPERATION`**.
6. **Safety Guard Demo** — In the "Confirm Target Path" input box, type something random (e.g., `test`). The indicator stays **red** (`UNVERIFIED`) and the Execute button stays disabled. This proves the guard is active.
7. **Unlock Execution** — Clear the box and type: `CONFIRM-ERASE`
8. The badge turns **green** (`CONFIRMED: TARGET VERIFIED`).
9. Click **`EXECUTE SECURE ERASURE`**.
10. Watch the 3-pass execution progress (Pass 1: Zeros → Pass 2: Ones → Pass 3: Cryptographic Random).
11. **Outcome** — A green **SANITIZATION COMPLETE** banner appears. Click **`Download Sanitization Certificate`** to download the cryptographic certificate showing Operation ID, timestamp, method, and DoD/NIST compliance validation.

---

## 🔍 Step 2: Advanced File Carving (Recovery Engine)

**Objective**: Showcase OSIRIS's original Structural Confidence Scoring and the PhotoRec integration.

### Execution Flow:
1. Switch to the **`02 FILE CARVING`** tab.
2. In the **"Source Target & Carving Config"** field:
   - **To demonstrate zero-remanence verification**: Leave the path as `demo_disk_target.bin` and click Run. The system will return **0 files recovered** — proving that the wiped disk has no remanence.
   - **To demonstrate the confidence scoring feature**: Paste the recovery source path that was printed when you ran `demo_setup.py`. It will be in this format, but with your own username:
     ```
     <PROJECT_ROOT>\demo_workspace\recovery_source
     ```
     *(Tip: `demo_setup.py` printed this exact path in its output — just copy it from the terminal.)*
3. Click **`RUN DEEP FILE CARVING`**.
4. The system will analyze the folder and render the **Integrity Analysis Grid**.
5. **Highlight the Scoring Algorithm** — Scroll through the results and expand individual files:
   - `classified_blueprint.png` ✅ **High Confidence** — Passes full PIL structural validation
   - `surveillance_capture.jpg` ✅ **High Confidence** — Valid JPEG with clean pixel data
   - `evidence_archive.zip` ✅ **High Confidence** — ZIP testzip() passes with no corruption
   - `operation_report.pdf` ✅ **High Confidence** — Contains valid `%PDF-` header AND `%%EOF` footer
   - `corrupted_photo.jpg` ⚠️ **Medium Confidence** — Has a valid JPEG header but corrupted body bytes
   - `partial_document.pdf` ⚠️ **Medium Confidence** — Has valid `%PDF-` header but is missing `%%EOF` footer (truncated)
   - `fragment_0x3f.dat` 🔴 **Low / Fragment** — Tiny 128-byte unidentifiable binary fragment

---

## 📜 Step 3: Tamper-Evident Audit Verification

**Objective**: Demonstrate the cryptographically chained SHA-256 log system designed for chain-of-custody preservation.

### Execution Flow:
1. Switch to the **`03 AUDIT & CERTIFICATES`** tab.
2. Under **"Tamper-Evident Operations Log"**, you will see two entries logged from Step 1 (Erasure) and Step 2 (Recovery), each showing Operation ID, timestamp, module, target, and SHA-256 hash.
3. Click **`VERIFY HASH CHAIN INTEGRITY`**.
4. A green **INTEGRITY VALIDATED** banner confirms the hash chain is intact — OSIRIS recomputed every SHA-256 hash and verified no entries were modified.

**Optional Failure Test (impressive for the assessor!)**:
1. Open `operations_log.json` in Notepad or VS Code.
2. Change any single character in any `status` or `target` field and **Save**.
3. Go back to the OSIRIS UI and click **VERIFY HASH CHAIN INTEGRITY** again.
4. It will instantly show **INTEGRITY VIOLATION DETECTED** — proving the tamper-evidence system works.
5. Re-run `demo_setup.py` (or `start_demo.bat`) to restore the clean state.

---

## ✅ Demo Checklist Summary

| Step | Feature Demonstrated | Expected Outcome |
|------|----------------------|-----------------|
| 0 | Environment Setup | Clean state, 8 demo files created |
| 1 | Secure Erasure + Safety Guard | Certificate downloaded, pass progress shown |
| 2a | Zero-Remanence Check | 0 files from wiped disk |
| 2b | Confidence Scoring | 7 files with High/Medium/Low badges |
| 3 | Hash Chain Verification | Green INTEGRITY VALIDATED |
| 3* | Tamper Detection | Red INTEGRITY VIOLATION on modified log |

---

*This concludes the standard OSIRIS demo flow. Total estimated demo time: ~5 minutes.*
