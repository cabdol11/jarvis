"""
J.A.R.V.I.S. Operations System
--------------------------------
Task decomposition, project tracking, priority scoring, dependency mapping.

"Allow me to handle the logistics, sir."

Transforms vague intent into structured execution plans.
Tracks every task, flags blockers, surfaces the critical path.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

TASKS_FILE    = DATA_DIR / "tasks.json"
PROJECTS_FILE = DATA_DIR / "projects.json"

# Cross-system
COMPANY_PROJECTS_FILE = BASE_DIR.parent / "company-os" / "data" / "projects.json"


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


# Priority labels
PRIORITY_LABELS = {1: "CRITICAL", 2: "HIGH", 3: "MEDIUM", 4: "LOW", 5: "SOMEDAY"}

# Effort labels (hours)
EFFORT_LABELS = {
    "xs": "< 30 min",
    "s":  "1-2 hours",
    "m":  "half day",
    "l":  "1-2 days",
    "xl": "3-5 days",
}


class OperationsSystem:
    """
    JARVIS task and project management engine.

    Capabilities:
    - Task decomposition: break any goal into executable steps
    - Priority scoring: ICE framework (Impact × Confidence × Ease)
    - Dependency mapping: surface critical path blockers
    - Project tracking: status, DRI, milestones, budget
    - Time blocking: schedule high-priority tasks into available slots
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._tasks    = _load(TASKS_FILE,    {"tasks": [], "completed": []})
        self._projects = _load(PROJECTS_FILE, {"projects": {}})

    def _flush(self):
        _save(TASKS_FILE,    self._tasks)
        _save(PROJECTS_FILE, self._projects)

    # ─── Task decomposition ────────────────────────────────────────────────

    def decompose_task(self, goal: str) -> list:
        """
        Break a high-level goal into a structured work breakdown.
        Returns list of formatted strings for display.
        """
        lines = []

        # Classify the task type
        goal_lower = goal.lower()

        if any(w in goal_lower for w in ["hire", "recruit", "headcount", "interview"]):
            steps = self._decompose_hiring(goal)
        elif any(w in goal_lower for w in ["launch", "ship", "release", "deploy"]):
            steps = self._decompose_launch(goal)
        elif any(w in goal_lower for w in ["raise", "fundrais", "investor", "capital", "series"]):
            steps = self._decompose_fundraise(goal)
        elif any(w in goal_lower for w in ["partner", "deal", "negotiat", "contract"]):
            steps = self._decompose_partnership(goal)
        elif any(w in goal_lower for w in ["build", "create", "develop", "implement", "code"]):
            steps = self._decompose_build(goal)
        elif any(w in goal_lower for w in ["research", "analyz", "audit", "review", "assess"]):
            steps = self._decompose_research(goal)
        else:
            steps = self._decompose_generic(goal)

        # Format output
        lines.append(f"WORK BREAKDOWN: {goal.upper()}")
        lines.append("─" * 60)
        lines.append("")

        for i, step in enumerate(steps, 1):
            effort = step.get("effort", "m")
            priority = step.get("priority", 2)
            owner = step.get("owner", "DRI")
            lines.append(f"  [{i:02d}] {step['action']}")
            lines.append(f"        Effort: {EFFORT_LABELS.get(effort, effort)}  |  "
                         f"Priority: {PRIORITY_LABELS.get(priority, priority)}  |  "
                         f"Owner: {owner}")
            if step.get("dependency"):
                lines.append(f"        Depends on: Step {step['dependency']}")
            if step.get("output"):
                lines.append(f"        Output: {step['output']}")
            lines.append("")

        # Log tasks
        for step in steps:
            self.add_task(
                description=step["action"],
                priority=step.get("priority", 3),
                effort=step.get("effort", "m"),
                project=goal[:50],
            )

        lines.append(f"  {len(steps)} tasks logged to mission tracker.")
        return lines

    def _decompose_hiring(self, goal: str) -> list:
        return [
            {"action": "Define role: write job description with leveling, comp band, and 5 must-have requirements",
             "effort": "s", "priority": 1, "output": "JD doc"},
            {"action": "Source: post on LinkedIn, AngelList, and activate 3 warm referrals from network",
             "effort": "m", "priority": 2, "dependency": 1, "output": "10+ qualified applicants"},
            {"action": "Screen: 30-min culture fit call. Filter to top 5 candidates",
             "effort": "m", "priority": 2, "dependency": 2, "output": "Top 5 shortlist"},
            {"action": "Interview loop: 4-person panel (technical, values, case, Bar Raiser)",
             "effort": "l", "priority": 1, "dependency": 3, "output": "Ranked scorecard"},
            {"action": "Reference checks: 3 references, focus on working style and growth trajectory",
             "effort": "s", "priority": 2, "dependency": 4, "output": "Reference report"},
            {"action": "Offer: prepare comp package with base, equity, bonus. Allow 48-hour decision window",
             "effort": "s", "priority": 1, "dependency": 5, "output": "Signed offer letter"},
            {"action": "Onboarding: 30-60-90 day plan, assign buddy, schedule stakeholder intros",
             "effort": "m", "priority": 2, "dependency": 6, "output": "Onboarding plan"},
        ]

    def _decompose_launch(self, goal: str) -> list:
        return [
            {"action": "Define launch scope: MVF (minimum viable feature set), success metrics, kill criteria",
             "effort": "s", "priority": 1, "output": "Launch brief"},
            {"action": "Internal dogfood: run with team for 1 week, collect structured feedback",
             "effort": "m", "priority": 1, "dependency": 1, "output": "Dogfood report"},
            {"action": "Fix P0 issues from dogfood. Freeze scope. No new features",
             "effort": "l", "priority": 1, "dependency": 2, "output": "Release candidate"},
            {"action": "Prepare go-to-market: messaging, landing page copy, outreach list",
             "effort": "m", "priority": 2, "dependency": 1, "output": "GTM kit"},
            {"action": "Beta: invite 20-50 trusted users, monitor retention and NPS daily",
             "effort": "l", "priority": 1, "dependency": 3, "output": "Beta metrics"},
            {"action": "Launch comms: email sequence, social posts, PR if warranted",
             "effort": "s", "priority": 2, "dependency": 4, "output": "Sent communications"},
            {"action": "Post-launch: monitor key metrics for 72 hours, stand by for rapid response",
             "effort": "m", "priority": 1, "dependency": 6, "output": "Launch report"},
        ]

    def _decompose_fundraise(self, goal: str) -> list:
        return [
            {"action": "Prepare data room: financials (12 months), cap table, team bios, product demo, pipeline",
             "effort": "l", "priority": 1, "output": "Data room"},
            {"action": "Narrative: craft 10-slide deck answering why now, why us, why this market",
             "effort": "m", "priority": 1, "dependency": 1, "output": "Investor deck"},
            {"action": "Target list: 25 investors. Tier 1 (dream), Tier 2 (likely), Tier 3 (backup)",
             "effort": "s", "priority": 2, "dependency": 2, "output": "Investor CRM"},
            {"action": "Warm intros: activate network for Tier 1. Aim for 5+ warm intros in week 1",
             "effort": "m", "priority": 1, "dependency": 3, "output": "Intro emails sent"},
            {"action": "First meetings: run 15+ partner-level meetings. Refine pitch after each",
             "effort": "xl", "priority": 1, "dependency": 4, "output": "Term sheets or passes"},
            {"action": "Due diligence: reference calls, legal review, final negotiations",
             "effort": "l", "priority": 1, "dependency": 5, "output": "Signed term sheet"},
            {"action": "Close: legal docs, wire transfers, cap table update, investor announcement",
             "effort": "l", "priority": 1, "dependency": 6, "output": "Funding closed"},
        ]

    def _decompose_partnership(self, goal: str) -> list:
        return [
            {"action": "Define the deal: what do we want, what do we offer, BATNA, walk-away point",
             "effort": "s", "priority": 1, "output": "Deal brief"},
            {"action": "Research counterparty: their priorities, pain points, decision-maker, org structure",
             "effort": "s", "priority": 1, "dependency": 1, "output": "Intel report"},
            {"action": "Initial contact: executive-to-executive intro, 30-min exploratory call",
             "effort": "xs", "priority": 2, "dependency": 2, "output": "Call scheduled"},
            {"action": "Proposal: draft term sheet or LOI. Focus on mutual value, not just your ask",
             "effort": "m", "priority": 1, "dependency": 3, "output": "Draft proposal"},
            {"action": "Negotiation: iterate on terms. Log every change and rationale",
             "effort": "m", "priority": 1, "dependency": 4, "output": "Agreed terms"},
            {"action": "Legal review: standard + custom clauses. IP, exclusivity, exit rights",
             "effort": "l", "priority": 1, "dependency": 5, "output": "Signed contract"},
            {"action": "Activation: assign DRI, set 90-day milestones, schedule monthly partnership sync",
             "effort": "s", "priority": 2, "dependency": 6, "output": "Partnership live"},
        ]

    def _decompose_build(self, goal: str) -> list:
        return [
            {"action": "Define requirements: user story, acceptance criteria, non-functional requirements",
             "effort": "s", "priority": 1, "output": "PRD"},
            {"action": "Technical design: architecture decision, API contracts, data model, edge cases",
             "effort": "m", "priority": 1, "dependency": 1, "output": "Tech spec"},
            {"action": "Scope sprint: break into 2-week deliverables. Identify critical path",
             "effort": "s", "priority": 2, "dependency": 2, "output": "Sprint plan"},
            {"action": "Build: implement, write tests, maintain ≥80% code coverage",
             "effort": "xl", "priority": 1, "dependency": 3, "output": "Working code"},
            {"action": "Code review: peer review, security review, performance check",
             "effort": "m", "priority": 1, "dependency": 4, "output": "Approved PR"},
            {"action": "QA: test all acceptance criteria, edge cases, load test if user-facing",
             "effort": "m", "priority": 1, "dependency": 5, "output": "QA sign-off"},
            {"action": "Deploy: staging → production. Monitor error rates for 24 hours post-deploy",
             "effort": "s", "priority": 1, "dependency": 6, "output": "Live in production"},
        ]

    def _decompose_research(self, goal: str) -> list:
        return [
            {"action": "Scope the question: define what a successful answer looks like, who needs it, deadline",
             "effort": "xs", "priority": 1, "output": "Research brief"},
            {"action": "Primary sources: interviews, surveys, or direct data collection",
             "effort": "l", "priority": 1, "dependency": 1, "output": "Raw data"},
            {"action": "Secondary sources: industry reports, competitor analysis, academic research",
             "effort": "m", "priority": 2, "dependency": 1, "output": "Source library"},
            {"action": "Synthesis: identify patterns, outliers, and key insights across sources",
             "effort": "m", "priority": 1, "dependency": 3, "output": "Insights doc"},
            {"action": "Recommendations: translate insights into 3-5 specific, actionable recommendations",
             "effort": "s", "priority": 1, "dependency": 4, "output": "Recommendation memo"},
            {"action": "Present findings to key stakeholders. Get decision or next action committed",
             "effort": "s", "priority": 2, "dependency": 5, "output": "Decision logged"},
        ]

    def _decompose_generic(self, goal: str) -> list:
        return [
            {"action": f"Define success: what does '{goal}' look like when complete? Write it down",
             "effort": "xs", "priority": 1, "output": "Success criteria"},
            {"action": "Identify blockers and dependencies before starting any execution",
             "effort": "xs", "priority": 1, "dependency": 1, "output": "Dependency map"},
            {"action": "Assign DRI and set deadline. No owner = no progress",
             "effort": "xs", "priority": 1, "dependency": 1, "output": "Ownership assigned"},
            {"action": "Execute phase 1: minimum viable action to generate signal",
             "effort": "m", "priority": 2, "dependency": 3, "output": "Phase 1 complete"},
            {"action": "Review: did we get the expected output? Adjust scope or approach if not",
             "effort": "xs", "priority": 2, "dependency": 4, "output": "Course-corrected plan"},
            {"action": "Complete remaining execution phases per updated plan",
             "effort": "l", "priority": 2, "dependency": 5, "output": "Goal achieved"},
            {"action": "Post-mortem: what worked, what didn't, what would we do differently?",
             "effort": "xs", "priority": 3, "dependency": 6, "output": "Lessons learned"},
        ]

    # ─── Task management ───────────────────────────────────────────────────

    def add_task(self, description: str, priority: int = 3, effort: str = "m",
                 due: str = "", project: str = "", dri: str = "") -> str:
        task = {
            "id": f"T-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "description": description,
            "priority": priority,
            "effort": effort,
            "due": due,
            "project": project,
            "dri": dri,
            "status": "open",
            "created": datetime.now().isoformat(),
        }
        self._tasks["tasks"].append(task)
        self._flush()
        return task["id"]

    def complete_task(self, task_id: str, outcome: str = ""):
        for task in self._tasks["tasks"]:
            if task.get("id") == task_id:
                task["status"] = "complete"
                task["completed_at"] = datetime.now().isoformat()
                task["outcome"] = outcome
                self._tasks["completed"].append(task)
        self._tasks["tasks"] = [t for t in self._tasks["tasks"] if t.get("status") != "complete"]
        self._flush()

    def get_open_tasks(self, project: str = "") -> list:
        tasks = [t for t in self._tasks.get("tasks", []) if t.get("status") == "open"]
        if project:
            tasks = [t for t in tasks if project.lower() in t.get("project", "").lower()]
        return sorted(tasks, key=lambda x: (x.get("priority", 99), x.get("due", "9999")))

    # ─── Project tracking ──────────────────────────────────────────────────

    def get_active_projects(self) -> list:
        """Return active projects from both JARVIS and company-os data."""
        projects = []

        # Local JARVIS projects
        local = self._projects.get("projects", {})
        for p in local.values():
            if p.get("status") not in ["Complete", "Cancelled"]:
                projects.append({
                    "name":    p.get("name", "?"),
                    "dri":     p.get("dri", "TBD"),
                    "status":  p.get("status", "Active"),
                    "pct":     p.get("pct_complete", 0),
                    "source":  "jarvis",
                })

        # Company OS projects
        co_proj = _load(COMPANY_PROJECTS_FILE, {})
        for p in co_proj.get("projects", {}).values():
            if p.get("status") not in ["Complete", "Cancelled"]:
                projects.append({
                    "name":    p.get("name", "?"),
                    "dri":     p.get("dri", "TBD"),
                    "status":  p.get("status", "Active"),
                    "pct":     p.get("pct_complete", 0),
                    "source":  "company-os",
                })

        return sorted(projects, key=lambda x: (
            0 if x["status"] == "Blocked" else
            1 if x["status"] == "Off Track" else
            2 if x["status"] == "At Risk" else 3
        ))

    def add_project(self, name: str, dri: str, due: str = "", budget: float = 0,
                    description: str = "") -> str:
        pid = f"P-{datetime.now().strftime('%Y%m%d')}-{name[:8].upper().replace(' ', '')}"
        self._projects["projects"][pid] = {
            "id": pid,
            "name": name,
            "dri": dri,
            "due": due,
            "budget": budget,
            "actual_spend": 0,
            "description": description,
            "status": "Active",
            "pct_complete": 0,
            "created": datetime.now().isoformat(),
            "milestones": [],
        }
        self._flush()
        return pid

    def update_project_status(self, project_id: str, status: str, pct: float = None):
        if project_id in self._projects["projects"]:
            self._projects["projects"][project_id]["status"] = status
            if pct is not None:
                self._projects["projects"][project_id]["pct_complete"] = pct
            self._projects["projects"][project_id]["last_updated"] = datetime.now().isoformat()
            self._flush()

    # ─── Priority scoring (ICE) ────────────────────────────────────────────

    def score_ice(self, impact: float, confidence: float, ease: float) -> dict:
        """
        ICE scoring: Impact × Confidence × Ease
        Each dimension: 1-10
        Returns score and recommended tier.
        """
        score = (impact * confidence * ease) / 10
        tier = (
            "Priority 1 — Pursue immediately" if score >= 50 else
            "Priority 2 — Schedule this quarter" if score >= 25 else
            "Priority 3 — Backlog candidate" if score >= 10 else
            "Priority 4 — Deprioritize"
        )
        return {
            "impact": impact,
            "confidence": confidence,
            "ease": ease,
            "score": round(score, 1),
            "tier": tier,
        }

    # ─── Critical path ─────────────────────────────────────────────────────

    def get_blockers(self) -> list:
        """Surface all blocked tasks and projects."""
        blockers = []

        for task in self._tasks.get("tasks", []):
            if task.get("status") == "blocked":
                blockers.append({
                    "type": "task",
                    "item": task.get("description", "?"),
                    "blocked_since": task.get("blocked_at", "?"),
                })

        co_proj = _load(COMPANY_PROJECTS_FILE, {})
        for p in co_proj.get("projects", {}).values():
            if p.get("status") == "Blocked":
                blockers.append({
                    "type": "project",
                    "item": p.get("name", "?"),
                    "dri": p.get("dri", "?"),
                })

        return blockers

    # ─── Overdue tracking ──────────────────────────────────────────────────

    def get_overdue_tasks(self) -> list:
        today = datetime.now().date().isoformat()
        overdue = []
        for task in self._tasks.get("tasks", []):
            due = task.get("due", "")
            if due and due < today and task.get("status") == "open":
                days_over = (datetime.now().date() - datetime.fromisoformat(due).date()).days
                overdue.append({**task, "days_overdue": days_over})
        return sorted(overdue, key=lambda x: x.get("days_overdue", 0), reverse=True)

    # ─── Weekly ops summary ────────────────────────────────────────────────

    def get_weekly_summary(self) -> str:
        open_tasks  = self.get_open_tasks()
        overdue     = self.get_overdue_tasks()
        blockers    = self.get_blockers()
        projects    = self.get_active_projects()

        lines = [
            f"OPERATIONS SUMMARY — Week of {datetime.now().strftime('%B %d, %Y')}",
            "",
            f"  Active projects:   {len(projects)}",
            f"  Open tasks:        {len(open_tasks)}",
            f"  Overdue tasks:     {len(overdue)}",
            f"  Active blockers:   {len(blockers)}",
            "",
        ]

        blocked_projects = [p for p in projects if p.get("status") == "Blocked"]
        if blocked_projects:
            lines.append("  BLOCKED PROJECTS — requires immediate attention:")
            for p in blocked_projects:
                lines.append(f"  ▶  {p['name']} — DRI: {p['dri']}")
            lines.append("")

        if overdue:
            lines.append("  OVERDUE TASKS:")
            for t in overdue[:5]:
                lines.append(f"  ▶  {t['description'][:55]} ({t['days_overdue']}d overdue)")
            lines.append("")

        high_priority = [t for t in open_tasks if t.get("priority") <= 2]
        if high_priority:
            lines.append("  HIGH-PRIORITY OPEN TASKS:")
            for t in high_priority[:5]:
                lines.append(f"  ▶  [{PRIORITY_LABELS.get(t['priority'], '?')}] {t['description'][:55]}")
            lines.append("")

        return "\n".join(lines)

    def is_online(self) -> bool:
        return True
