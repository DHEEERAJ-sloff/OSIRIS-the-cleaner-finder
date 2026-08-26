# OSIRIS — User & Operations Manual

---

## 1. Starting the Platform

1. Open Terminal or PowerShell as Administrator (recommended for physical drive access).
2. Run the application:
   ```bash
   streamlit run src/app.py
   ```
3. Open your browser at `http://localhost:8501`.

---

## 2. Tab 1: Secure Erase Drive

### Steps to Perform Drive Sanitization:
1. Select the target device or test image from the **Target Device Selection** dropdown.
2. Select your desired erasure algorithm (e.g. *NIST 800-88 / DoD 5220.22-M 3-Pass Overwrite*).
3. Under **Confirmation Guard & Safety Lock**, type the exact path of the selected target or `CONFIRM-ERASE`.
4. Click **🚀 EXECUTE SECURE WIPE**.
5. Upon completion:
   - View the live status balloon notification.
   - Preview the generated **Cryptographic Wipe Certificate**.
   - Click **💾 Download Wipe Certificate** to save the `.txt` certificate.

---

## 3. Tab 2: Recover Files

### Steps to Perform File Carving:
1. Enter the path of the target drive, image file, or folder in **Target Disk / Image / Folder Path**.
2. Specify the output folder in **Recovery Destination Directory**.
3. Click **🔎 RUN FILE CARVING & RECOVERY**.
4. Review the recovered file table:
   - Use the **Category Filter** (Images, Documents, Archives, Media, Code/System, Other) to filter results.
   - Inspect the **Confidence Score Badges**:
     - 🟩 **High**: Structurally intact file, opens cleanly.
     - 🟧 **Medium**: Recovered file with partial corruption or truncation.
     - 🟥 **Low**: Unreadable or empty file fragment.
   - Click **💾 Download File** next to any recovered file to view its contents.

---

## 4. Tab 3: Audit Log & Verification

### Verifying Chain of Custody Integrity:
1. Navigate to **📜 Tamper-Evident Audit Log & Certificates**.
2. View all past erasure and recovery operation records in the interactive table.
3. Click **🔒 VERIFY AUDIT LOG INTEGRITY**:
   - The platform verifies all SHA-256 hash chains.
   - Displays a green **INTEGRITY VERIFIED** alert if all entries are authentic.
