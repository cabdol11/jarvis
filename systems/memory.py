"""
J.A.R.V.I.S. Memory System
---------------------------
Persistent intelligence layer. JARVIS remembers everything.

Short-term:  Current session context
Medium-term: Last 90 days of activity
Long-term:   All major decisions, outcomes, learned patterns

"Based on 18 months of data, sir, here's what I've learned
about how you make your best decisions."
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

MISSION_LOG_FILE  = DATA_DIR / "mission_log.json"
MEMORY_FILE       = DATA_DIR / "memory.json"
PREFERENCES_FILE  = DATA_DIR / "preferences.json"


def _load(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        try:
            return json.load(f)
        except Exception:
            return default


def _save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


class Memory:
    """
    JARVIS persistent memory engine.

    Architecture:
    - mission_log:  Every action, decision, task logged chronologically
    - memory:       Structured memory with sessions, decisions, patterns, preferences
    - preferences:  Learned preferences and behavioral patterns
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._log   = _load(MISSION_LOG_FILE, {"entries": []})
        self._mem   = _load(MEMORY_FILE, {
            "sessions": [],
            "decisions": [],
            "patterns": [],
            "pending_items": [],
            "relationships": {},
            "lessons_learned": [],
        })
        self._prefs = _load(PREFERENCES_FILE, {
            "communication_style": "direct",
            "risk_tolerance": "moderate",
            "decision_speed": "deliberate",
            "peak_hours": "morning",
            "recurring_mistakes": [],
        })

    def _flush(self):
        _save(MISSION_LOG_FILE, self._log)
        _save(MEMORY_FILE, self._mem)
        _save(PREFERENCES_FILE, self._prefs)

    # ─── Session tracking ──────────────────────────────────────────────────

    def log_session(self, data: dict):
        """Record a JARVIS session."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "session",
            **data
        }
        self._mem["sessions"].append(entry)
        self._log["entries"].append(entry)
        # Keep medium-term: 90 days
        cutoff = (datetime.now() - timedelta(days=90)).isoformat()
        self._mem["sessions"] = [
            s for s in self._mem["sessions"] if s.get("timestamp", "") > cutoff
        ]
        self._flush()

    def get_session_count(self) -> int:
        return len(self._mem.get("sessions", []))

    # ─── Decision tracking ─────────────────────────────────────────────────

    def log_decision(self, data: dict):
        """Log a major decision for institutional memory."""
        entry = {
            "id": f"D-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "status": "open",
            **data
        }
        self._mem["decisions"].append(entry)
        self._log["entries"].append({"type": "decision", **entry})
        self._flush()
        return entry["id"]

    def close_decision(self, decision_id: str, outcome: str, lesson: str = ""):
        """Record the outcome of a decision. Builds institutional memory."""
        for d in self._mem["decisions"]:
            if d.get("id") == decision_id:
                d["status"] = "closed"
                d["outcome"] = outcome
                d["outcome_date"] = datetime.now().isoformat()
                if lesson:
                    d["lesson"] = lesson
                    self._mem["lessons_learned"].append({
                        "date": datetime.now().isoformat(),
                        "decision_id": decision_id,
                        "lesson": lesson,
                        "context": d.get("decision", "")
                    })
        self._flush()

    def get_similar_decisions(self, query: str) -> list:
        """Surface past decisions relevant to current query."""
        query_words = set(query.lower().split())
        similar = []
        for d in self._mem["decisions"]:
            text = (d.get("decision", "") + " " + d.get("query", "")).lower()
            overlap = len(query_words & set(text.split()))
            if overlap >= 2 and d.get("status") == "closed":
                similar.append({
                    "decision": d.get("decision", d.get("query", "?")),
                    "outcome": d.get("outcome", "No outcome logged"),
                    "lesson": d.get("lesson", ""),
                    "date": d.get("timestamp", "")[:10],
                    "overlap_score": overlap
                })
        return sorted(similar, key=lambda x: x["overlap_score"], reverse=True)[:3]

    # ─── Pending items ─────────────────────────────────────────────────────

    def add_pending_item(self, description: str, due: str = "", priority: int = 2):
        """Add an item to the pending queue."""
        item = {
            "id": f"P-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "description": description,
            "due": due,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "status": "open"
        }
        self._mem["pending_items"].append(item)
        self._flush()
        return item["id"]

    def resolve_pending(self, item_id: str):
        for item in self._mem["pending_items"]:
            if item.get("id") == item_id:
                item["status"] = "resolved"
                item["resolved_at"] = datetime.now().isoformat()
        self._flush()

    def get_pending_items(self) -> list:
        items = [i for i in self._mem.get("pending_items", []) if i.get("status") == "open"]
        return sorted(items, key=lambda x: x.get("priority", 99))

    # ─── Relationship intelligence ─────────────────────────────────────────

    def upsert_contact(self, name: str, data: dict):
        """Update or create a contact record."""
        if name not in self._mem["relationships"]:
            self._mem["relationships"][name] = {
                "name": name,
                "created": datetime.now().isoformat(),
                "last_contact": None,
                "relationship_strength": 5,
                "what_they_care_about": [],
                "what_you_owe_them": [],
                "notes": [],
            }
        self._mem["relationships"][name].update(data)
        self._mem["relationships"][name]["last_updated"] = datetime.now().isoformat()
        self._flush()

    def get_cold_relationships(self, days_threshold: int = 30) -> list:
        """Return relationships with no contact in threshold days."""
        cutoff = (datetime.now() - timedelta(days=days_threshold)).isoformat()
        cold = []
        for name, contact in self._mem.get("relationships", {}).items():
            last = contact.get("last_contact")
            if not last or last < cutoff:
                cold.append({
                    "name": name,
                    "last_contact": last or "never",
                    "strength": contact.get("relationship_strength", 5)
                })
        return sorted(cold, key=lambda x: x["strength"], reverse=True)

    def log_contact(self, name: str, notes: str = ""):
        """Record a touchpoint with a contact."""
        if name in self._mem["relationships"]:
            self._mem["relationships"][name]["last_contact"] = datetime.now().isoformat()
            if notes:
                self._mem["relationships"][name]["notes"].append({
                    "date": datetime.now().isoformat(),
                    "note": notes
                })
            self._flush()

    # ─── Pattern recognition ───────────────────────────────────────────────

    def log_pattern(self, pattern: str, context: str, confidence: float):
        self._mem["patterns"].append({
            "pattern": pattern,
            "context": context,
            "confidence": confidence,
            "date": datetime.now().isoformat()
        })
        self._flush()

    def get_lessons_learned(self) -> list:
        return self._mem.get("lessons_learned", [])[-10:]

    # ─── Preference engine ─────────────────────────────────────────────────

    def update_preference(self, key: str, value):
        self._prefs[key] = value
        self._flush()

    def get_preference(self, key: str, default=None):
        return self._prefs.get(key, default)

    def get_all_preferences(self) -> dict:
        return self._prefs.copy()

    def add_recurring_mistake(self, mistake: str):
        if mistake not in self._prefs.get("recurring_mistakes", []):
            self._prefs.setdefault("recurring_mistakes", []).append(mistake)
            self._flush()

    # ─── Memory summary ────────────────────────────────────────────────────

    def get_memory_summary(self) -> dict:
        """High-level summary of what JARVIS knows."""
        decisions = self._mem.get("decisions", [])
        open_decisions = [d for d in decisions if d.get("status") == "open"]
        closed_decisions = [d for d in decisions if d.get("status") == "closed"]

        return {
            "sessions": len(self._mem.get("sessions", [])),
            "total_decisions": len(decisions),
            "open_decisions": len(open_decisions),
            "closed_decisions": len(closed_decisions),
            "pending_items": len(self.get_pending_items()),
            "relationships_tracked": len(self._mem.get("relationships", {})),
            "lessons_learned": len(self._mem.get("lessons_learned", [])),
            "patterns_detected": len(self._mem.get("patterns", [])),
        }

    def is_online(self) -> bool:
        return True
