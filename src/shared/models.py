import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, Any, Optional

@dataclass
class OperationLogEntry:
    operation_id: str
    module: str
    timestamp: str
    target: str
    method: str
    engine: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)
    log_hash: str = ""

    def compute_hash(self, prev_hash: str = "") -> str:
        """
        Computes SHA-256 hash over log entry fields and optional chained previous hash
        to ensure tamper-evident audit trails.
        """
        payload = {
            "operation_id": self.operation_id,
            "module": self.module,
            "timestamp": self.timestamp,
            "target": self.target,
            "method": self.method,
            "engine": self.engine,
            "status": self.status,
            "details": self.details,
            "prev_hash": prev_hash
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OperationLogEntry":
        return cls(
            operation_id=data.get("operation_id", ""),
            module=data.get("module", ""),
            timestamp=data.get("timestamp", ""),
            target=data.get("target", ""),
            method=data.get("method", ""),
            engine=data.get("engine", ""),
            status=data.get("status", ""),
            details=data.get("details", {}),
            log_hash=data.get("log_hash", "")
        )
