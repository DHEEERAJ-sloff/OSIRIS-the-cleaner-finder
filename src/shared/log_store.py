import json
import os
from typing import List, Tuple
from src.shared.models import OperationLogEntry

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "operations_log.json")

def load_all_logs(file_path: str = LOG_FILE_PATH) -> List[OperationLogEntry]:
    """Loads all operation log entries from JSON file."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [OperationLogEntry.from_dict(item) for item in data]
    except Exception as e:
        print(f"Error loading log store: {e}")
        return []

def append_log_entry(entry: OperationLogEntry, file_path: str = LOG_FILE_PATH) -> OperationLogEntry:
    """Appends a new operation log entry with cryptographic hash chaining."""
    logs = load_all_logs(file_path)
    prev_hash = logs[-1].log_hash if logs else "GENESIS_HASH_OSIRIS_PS26149"
    
    if not entry.log_hash:
        entry.log_hash = entry.compute_hash(prev_hash=prev_hash)
        
    logs.append(entry)
    
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([l.to_dict() for l in logs], f, indent=2)
        
    return entry

def verify_log_integrity(file_path: str = LOG_FILE_PATH) -> Tuple[bool, str, List[dict]]:
    """
    Verifies that no entries in operations_log.json have been tampered with or modified.
    Returns (is_valid, report_summary, detailed_checks).
    """
    logs = load_all_logs(file_path)
    if not logs:
        return True, "Audit log is empty.", []
    
    detailed_checks = []
    is_valid = True
    prev_hash = "GENESIS_HASH_OSIRIS_PS26149"
    
    for idx, entry in enumerate(logs):
        expected_hash = entry.compute_hash(prev_hash=prev_hash)
        match = (expected_hash == entry.log_hash)
        detailed_checks.append({
            "index": idx,
            "operation_id": entry.operation_id,
            "timestamp": entry.timestamp,
            "stored_hash": entry.log_hash,
            "computed_hash": expected_hash,
            "status": "VALID" if match else "TAMPERED"
        })
        if not match:
            is_valid = False
        prev_hash = entry.log_hash
        
    summary = f"Audit log verified ({len(logs)} entries). Status: {'VALID (Untampered)' if is_valid else 'TAMPERED DETECTED'}"
    return is_valid, summary, detailed_checks
