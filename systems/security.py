"""
J.A.R.V.I.S. Security & Risk System
-------------------------------------
Threat detection, anomaly alerts, risk response protocols.

"Sir, we have a situation."

Monitors: all active projects, financial commitments, relationships,
competitive landscape — flagging early warning signals before problems
materialize into crises.
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

THREAT_REGISTER_FILE = DATA_DIR / "threat_register.json"
ASSET_REGISTRY_FILE  = DATA_DIR / "asset_registry.json"

# Cross-system data
FINANCIALS_FILE = BASE_DIR.parent / "company-os" / "data" / "financials_dashboard.json"
TALENT_FILE     = BASE_DIR.parent / "company-os" / "data" / "talent.json"
PROJECTS_FILE   = BASE_DIR.parent / "company-os" / "data" / "projects.json"
HEALTH_FILE     = BASE_DIR.parent / "company-os" / "data" / "health_history.json"


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


THREAT_LEVELS = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3, "MONITOR": 4}


class SecuritySystem:
    """
    JARVIS threat detection and risk management.

    Continuously monitors:
    - Financial position (runway, burn, variances)
    - Talent risks (flight risks, PIP, attrition)
    - Operational risks (blocked projects, overdue milestones)
    - Anomalies (2+ std dev from baseline on any metric)
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._register = _load(THREAT_REGISTER_FILE, {"threats": [], "incidents": [], "resolved": []})

    def _flush(self):
        _save(THREAT_REGISTER_FILE, self._register)

    # ─── Live threat scanning ──────────────────────────────────────────────

    def scan_all(self) -> list:
        """Full threat scan across all subsystems. Returns sorted threat list."""
        threats = []
        threats.extend(self._scan_financial())
        threats.extend(self._scan_talent())
        threats.extend(self._scan_operations())
        threats.extend(self._scan_anomalies())
        # Persist
        self._register["threats"] = threats
        self._register["last_scan"] = datetime.now().isoformat()
        self._flush()
        return sorted(threats, key=lambda t: THREAT_LEVELS.get(t["level"], 99))

    def _scan_financial(self) -> list:
        threats = []
        fin = _load(FINANCIALS_FILE, {})
        if not fin:
            return threats

        runway = fin.get("runway_months")
        if isinstance(runway, (int, float)):
            if runway < 6:
                threats.append(self._threat("CRITICAL", "Financial", f"Runway {runway:.0f} months — existential", 95,
                    "Initiate emergency fundraise or cost reduction immediately."))
            elif runway < 12:
                threats.append(self._threat("HIGH", "Financial", f"Runway {runway:.0f} months — capital raise urgent", 80,
                    "Begin investor outreach. Target close within 6 months."))
            elif runway < 18:
                threats.append(self._threat("MODERATE", "Financial", f"Runway {runway:.0f} months — plan capital strategy", 40,
                    "Model fundraising scenarios and identify lead targets."))

        bm = fin.get("burn_multiple")
        if isinstance(bm, (int, float)) and bm > 2.0:
            threats.append(self._threat("HIGH", "Financial", f"Burn multiple {bm:.1f}x — inefficient growth", 70,
                "Audit top 3 OpEx line items. Target <1.5x within 2 quarters."))

        ltv_cac = fin.get("ltv_cac_ratio")
        if isinstance(ltv_cac, (int, float)) and ltv_cac < 2.0:
            threats.append(self._threat("HIGH", "Financial", f"LTV:CAC {ltv_cac:.1f}x — below sustainable threshold", 75,
                "Unit economics unsustainable at current rates. Reduce CAC or improve retention."))

        return threats

    def _scan_talent(self) -> list:
        threats = []
        tal = _load(TALENT_FILE, {})
        employees = tal.get("employees", {})

        flight_risks = [e for e in employees.values() if e.get("flight_risk")]
        if flight_risks:
            names = ", ".join(e.get("name", "?") for e in flight_risks)
            threats.append(self._threat("HIGH", "Talent", f"Flight risks: {names}", 60,
                "Schedule retention conversations this week. Identify root cause."))

        pip = [e for e in employees.values() if e.get("status") == "pip"]
        if pip:
            threats.append(self._threat("MODERATE", "Talent", f"{len(pip)} employee(s) on PIP", 50,
                "Review PIP milestones. Prepare for outcome either way."))

        # Check attrition
        attrition = tal.get("attrition_log", [])
        recent_cutoff = (datetime.now() - timedelta(days=90)).isoformat()
        recent_regrettable = [a for a in attrition if a.get("regrettable") and a.get("date", "") > recent_cutoff]
        if len(recent_regrettable) >= 2:
            threats.append(self._threat("HIGH", "Talent", f"{len(recent_regrettable)} regrettable departures in 90 days", 70,
                "Investigate root cause. Culture or compensation issue likely."))

        return threats

    def _scan_operations(self) -> list:
        threats = []
        proj = _load(PROJECTS_FILE, {})
        all_proj = proj.get("projects", {})

        for p in all_proj.values():
            if p.get("status") == "Blocked":
                threats.append(self._threat("HIGH", "Operations",
                    f"Project '{p.get('name')}' BLOCKED — DRI: {p.get('dri','?')}", 85,
                    "Escalate to C-Suite. Identify and remove blocker within 24 hours."))
            elif p.get("status") == "Off Track":
                threats.append(self._threat("MODERATE", "Operations",
                    f"Project '{p.get('name')}' off track — {p.get('pct_complete',0):.0f}% complete", 65,
                    "Review scope, resources, and timeline. Consider milestone reset."))

            # Check budget overrun
            budget = p.get("budget", 0)
            actual = p.get("actual_spend", 0)
            if budget > 0 and actual > budget * 1.1:
                overrun_pct = (actual - budget) / budget * 100
                threats.append(self._threat("MODERATE", "Financial",
                    f"Project '{p.get('name')}' {overrun_pct:.0f}% over budget", 80,
                    "Review remaining scope. Approve additional budget or cut scope."))

        return threats

    def _scan_anomalies(self) -> list:
        threats = []
        history = _load(HEALTH_FILE, [])
        if len(history) < 5:
            return threats

        for key in ["overall"]:
            values = [h.get(key, 0) for h in history]
            if len(values) < 5:
                continue
            baseline = values[:-1]
            current = values[-1]
            mean = sum(baseline) / len(baseline)
            std = math.sqrt(sum((v - mean) ** 2 for v in baseline) / max(1, len(baseline)))
            if std == 0:
                continue
            z = (current - mean) / std
            if z <= -2.0:
                threats.append(self._threat(
                    "CRITICAL" if z <= -3 else "HIGH",
                    "Analytics",
                    f"Health score {abs(z):.1f}σ below baseline — anomalous decline detected",
                    min(95, int(abs(z) * 30)),
                    "Investigate which subsystem drove the decline. Full audit recommended."
                ))

        return threats

    def _threat(self, level, domain, threat, probability, response):
        return {
            "level": level,
            "domain": domain,
            "threat": threat,
            "probability": probability,
            "response": response,
            "detected_at": datetime.now().isoformat()
        }

    # ─── Public interface ──────────────────────────────────────────────────

    def get_active_threats(self) -> list:
        """Return current threats, scanning live data."""
        return self.scan_all()

    def get_threats_by_level(self, level: str) -> list:
        return [t for t in self.get_active_threats() if t["level"] == level]

    def log_incident(self, title: str, description: str, severity: str = "HIGH"):
        """Manually log a security or risk incident."""
        incident = {
            "id": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": title,
            "description": description,
            "severity": severity,
            "logged_at": datetime.now().isoformat(),
            "status": "open",
            "resolution": None
        }
        self._register["incidents"].append(incident)
        self._flush()
        return incident["id"]

    def resolve_incident(self, incident_id: str, resolution: str):
        for inc in self._register["incidents"]:
            if inc.get("id") == incident_id:
                inc["status"] = "resolved"
                inc["resolution"] = resolution
                inc["resolved_at"] = datetime.now().isoformat()
                self._register["resolved"].append(inc)
        self._flush()

    def get_threat_report(self) -> str:
        """Generate a formatted threat report."""
        threats = self.get_active_threats()
        if not threats:
            return "No active threats detected. All systems within operational parameters."

        lines = [f"THREAT ASSESSMENT — {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
        for i, t in enumerate(threats, 1):
            lines.append(f"[{t['level']}] {t['domain']}: {t['threat']}")
            lines.append(f"  Probability: {t['probability']}%  |  Response: {t['response']}")
            lines.append("")
        return "\n".join(lines)

    def adversarial_model(self, competitor: str) -> str:
        """Model likely competitor strategy and predicted moves."""
        return (
            f"ADVERSARIAL ANALYSIS: {competitor}\n\n"
            f"Known capabilities: Assess from public product launches, hiring patterns, funding.\n"
            f"Likely current focus: Where are they hiring most aggressively?\n"
            f"Predicted moves (90 days): Based on their trajectory, expect moves in adjacent markets.\n"
            f"Your defensive posture: Lock in key customer relationships before they enter your market.\n"
            f"Your offensive opportunity: Attack their weakest flank before they shore it up.\n\n"
            f"Confidence: MODERATE — adversarial modeling requires current intelligence input.\n"
            f"Recommendation: Conduct customer interviews to detect any competitive inbound."
        )

    def is_online(self) -> bool:
        return True
