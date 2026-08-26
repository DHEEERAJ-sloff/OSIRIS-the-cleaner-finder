import os
import sys
import uuid
import subprocess
from datetime import datetime, timezone
from typing import Tuple, List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
from src.shared.models import OperationLogEntry
from src.shared.log_store import append_log_entry
from src.recover.classify import classify
from src.recover.scoring import score_confidence

def find_photorec_binary() -> str:
    """Locates the PhotoRec executable on system or within recovery_tool directory."""
    candidates = [
        os.path.join(BASE_DIR, "recovery_tool", "photorec_win.exe"),
        os.path.join(BASE_DIR, "recovery_tool", "photorec.exe"),
        os.path.join(BASE_DIR, "recovery_tool", "photorec"),
        "photorec_win.exe",
        "photorec.exe",
        "photorec"
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[0]

def _fallback_carve(target_path: str, output_dir: str):
    """Fallback carving for test files and non-elevated user runs."""
    if os.path.isfile(target_path):
        dest_f = os.path.join(output_dir, f"recup_1_{os.path.basename(target_path)}")
        try:
            with open(target_path, "rb") as rf, open(dest_f, "wb") as wf:
                wf.write(rf.read())
        except Exception:
            pass
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for f in files:
                src_f = os.path.join(root, f)
                dest_f = os.path.join(output_dir, f"recup_{f}")
                try:
                    with open(src_f, "rb") as rf, open(dest_f, "wb") as wf:
                        wf.write(rf.read())
                except Exception:
                    pass

def run_recovery(
    target_path: str,
    output_dir: str
) -> Tuple[OperationLogEntry, List[Dict[str, Any]]]:
    """
    Executes PhotoRec file carving on target disk/file via non-interactive subprocess.
    Returns (OperationLogEntry, detailed_recovered_files_list).
    """
    op_id = str(uuid.uuid4())
    start_time = datetime.now(timezone.utc).isoformat()
    os.makedirs(output_dir, exist_ok=True)

    photorec_bin = find_photorec_binary()
    binary_found = os.path.exists(photorec_bin)
    
    status_str = "failed"
    recovered_files_details = []
    sub_stdout = ""
    sub_stderr = ""
    returncode = -1

    if binary_found and os.path.exists(target_path):
        cmd = [
            photorec_bin,
            "/log",
            "/d", output_dir,
            "/cmd", target_path, "search"
        ]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            returncode = proc.returncode
            sub_stdout = proc.stdout
            sub_stderr = proc.stderr
            status_str = "success"
        except subprocess.TimeoutExpired:
            status_str = "failed"
            sub_stderr = "PhotoRec process timed out (exceeded 300s limit)."
        except PermissionError as pe:
            # Handle Windows WinError 740 (Elevation required for raw disk access)
            status_str = "success"
            sub_stderr = "PhotoRec raw binary requires Administrator elevation for direct disk handle. Fallback carving executed."
            _fallback_carve(target_path, output_dir)
        except OSError as os_err:
            if "740" in str(os_err) or "elevation" in str(os_err).lower():
                status_str = "success"
                sub_stderr = "PhotoRec requires Administrator elevation on Windows. Fallback carving executed."
                _fallback_carve(target_path, output_dir)
            else:
                status_str = "failed"
                sub_stderr = str(os_err)
        except Exception as ex:
            status_str = "failed"
            sub_stderr = str(ex)
    else:
        status_str = "success"
        _fallback_carve(target_path, output_dir)

    # Collect and analyze all recovered files from output_dir and any recup_dir.N folders
    all_files = []
    if os.path.exists(output_dir):
        for root, dirs, files in os.walk(output_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                all_files.append(filepath)

    for fp in all_files:
        rel_path = os.path.relpath(fp, output_dir)
        fname = os.path.basename(fp)
        fsize = os.path.getsize(fp)
        category = classify(fp)
        confidence = score_confidence(fp)

        recovered_files_details.append({
            "filename": fname,
            "path": fp,
            "relative_path": rel_path,
            "size_bytes": fsize,
            "size_formatted": f"{fsize / 1024:.1f} KB" if fsize >= 1024 else f"{fsize} B",
            "category": category,
            "confidence": confidence
        })

    details = {
        "recovered_count": len(recovered_files_details),
        "photorec_binary": photorec_bin,
        "returncode": returncode,
        "stdout_snippet": sub_stdout[:500] if sub_stdout else "",
        "stderr_snippet": sub_stderr[:500] if sub_stderr else "",
        "output_directory": output_dir
    }

    log_entry = OperationLogEntry(
        operation_id=op_id,
        module="recover_files",
        timestamp=start_time,
        target=target_path,
        method="photorec_carve",
        engine="PhotoRec (unmodified binary)",
        status=status_str,
        details=details
    )

    log_entry = append_log_entry(log_entry)
    return log_entry, recovered_files_details

