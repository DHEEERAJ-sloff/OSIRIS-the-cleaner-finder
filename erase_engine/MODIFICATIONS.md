# SecureWipe Engine Modifications

This document records the exact modifications made to the forked SecureWipe engine (`erase_engine/`) for integration into the OSIRIS platform.

## Summary of Changes

1. **Programmatic API Surface**:
   - Refactored `securewipe.py` and `core/wipe_engine.py` to expose programmatic function signatures (`run_wipe(device_path, method, pass_count) -> WipeResult`) without requiring CLI interactive prompts.

2. **Cross-Platform Device Enumeration**:
   - Refactored `core/disk_windows.py` and `core/disk_linux.py` to return structured dictionary lists (`get_device_list() -> list[dict]`) containing device path, size, model, drive type (Fixed/Removable/Image), and status flags instead of directly printing to `sys.stdout`.

3. **Cryptographic Certificate Generation**:
   - Enhanced `cert/generator.py` to return certificate metadata and output path as structured objects for seamless GUI viewing and download.

4. **Error Handling & Exception Propagation**:
   - Modified execution loops to raise structured Python exceptions on drive lock failures, permission errors, or I/O timeouts to allow OSIRIS audit logging.
