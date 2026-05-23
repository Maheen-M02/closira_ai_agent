"""
Conversation Logger
====================
Logs all turns, escalations, and session summaries to timestamped files.
"""

import os
import json
import datetime


LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


class ConversationLogger:
    def __init__(self):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = ts
        self.log_path = os.path.join(LOG_DIR, f"session_{ts}.jsonl")
        self.escalation_path = os.path.join(LOG_DIR, f"escalations_{ts}.jsonl")
        self.summary_path = os.path.join(LOG_DIR, f"summary_{ts}.json")

    def _write(self, path: str, record: dict):
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def log_turn(self, role: str, content: str):
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "role": role,
            "content": content,
        }
        self._write(self.log_path, record)

    def log_escalation(self, reason: str):
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "ESCALATION",
            "reason": reason,
        }
        self._write(self.escalation_path, record)
        print(f"\n⚠️  [ESCALATION LOGGED] Reason: {reason}\n")

    def log_summary(self, summary: dict):
        with open(self.summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
