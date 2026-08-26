# OSIRIS — Empirical Validation & Test Report

**Target Proposal**: PS 26149 (NTRO)  
**Date**: August 26, 2026  
**Test Platform**: Windows 11 / Python 3.12.10

---

## 1. Summary of Empirical Test Results

| Test Scenario | Test Procedure | Result / Recorded Metric | Status |
|---|---|---|---|
| **Erase — Basic Function** | Executed 3-pass DoD 5220.22-M wipe on test binary disk target | Cryptographic certificate generated (`Wipe_Cert_*.txt`). Target zeroed and randomized. | **PASS** |
| **Erase — Verification** | Ran File Recovery immediately following Erase on wiped target | **0 recovered files** (Zero-remanence confirmed). | **PASS** |
| **Recovery — Baseline** | Populated test target with 5 files (PNG, ZIP, PDF, TXT, BIN), executed Carving | 5/5 files carved. Confidence: 3 High, 1 Medium, 1 Low. | **PASS** |
| **Recovery — Corrupted File Handling** | Intentionally truncated PNG image bytes before scoring | `scoring.py` detected broken structure and scored as **Medium/Low**, not High. | **PASS** |
| **GUI — Confirmation Guard** | Attempted wipe execution with incorrect typed confirmation string | Blocked with `ValueError` dialog. Target preserved untouched. | **PASS** |
| **Reporting & Tamper Resilience** | Ran SHA-256 chain verification on `operations_log.json` | Hash chain validated 100% authentic (`VALID`). | **PASS** |

---

## 2. Automated Test Suite Execution Log

```
Ran 5 tests in 0.235s

OK (All 5 unit & integration tests passed)
- test_log_entry_sha256_hashing_and_integrity ... OK
- test_classification_mapping ... OK
- test_confidence_scoring_image_and_zip ... OK
- test_erase_guard_confirmation_check ... OK
- test_file_recovery_and_zero_remanence_verification ... OK
```
