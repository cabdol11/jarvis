# J.A.R.V.I.S.
### Just A Rather Very Intelligent System

> *"Good morning, sir. Shall I run the situational briefing?"*

---

JARVIS is your personal operating intelligence. It monitors everything, forgets nothing, and surfaces what matters before you think to ask. It reads from your company operating system, your financial dashboard, your talent records, and your affiliate business — synthesizing it all into a single command interface.

It does not wait to be asked. It anticipates.

---

## Architecture

```
jarvis/
├── jarvis_core.py          # Primary command interface
├── dashboard.py            # Live terminal HUD
├── systems/
│   ├── memory.py           # Persistent intelligence layer (3-tier memory)
│   ├── security.py         # Threat detection & risk management
│   ├── intelligence.py     # Strategic analysis engine
│   ├── operations.py       # Task decomposition & project tracking
│   ├── financials.py       # Financial monitoring & scenario modeling
│   └── comms.py            # Communications drafting & relationship CRM
└── data/                   # Local JARVIS data (auto-created)
    ├── mission_log.json
    ├── memory.json
    ├── threat_register.json
    └── ...
```

**Connected systems** (read-only):
- `~/company-os/data/` — org health, financials, talent, projects
- `~/tiktok-affiliate-system/data/` — affiliate revenue, product performance

---

## Commands

```bash
python jarvis_core.py                        # Morning briefing (default)
python jarvis_core.py brief                  # Full situational briefing
python jarvis_core.py think "your question"  # Strategic analysis
python jarvis_core.py do "task description"  # Decompose & track a task
python jarvis_core.py prep "meeting topic"   # Meeting preparation
python jarvis_core.py decide "the decision"  # Decision support framework
python jarvis_core.py status                 # Quick system check
```

```bash
python dashboard.py          # Live HUD — refreshes every 30 seconds
python dashboard.py --once   # Single render
```

---

## First Run

```bash
cd ~/jarvis
python jarvis_core.py
```

JARVIS will initialize all data directories and run the first briefing.

---

## How JARVIS Thinks

**Memory architecture:**
- Short-term: current session
- Medium-term: 90-day rolling window
- Long-term: all decisions, outcomes, lessons learned

**Threat detection** runs on every briefing, scanning:
- Financial position (runway, burn multiple, LTV:CAC)
- Talent risks (flight risks, PIP, regrettable attrition)
- Operational risks (blocked projects, overdue milestones)
- Statistical anomalies (2+ standard deviations from baseline)

**Decision support** uses framework auto-selection:
- Strategic questions → SWOT + Porter's Five Forces
- Financial questions → Variance analysis + scenario modeling
- People questions → Stakeholder mapping
- Operational questions → 5 Whys + critical path
- TikTok/affiliate → Revenue optimization framework

---

## The JARVIS Code

1. Never flatter. Always be precise.
2. Lead with the most important thing.
3. Surface what you know before being asked.
4. Push back when the data says to.
5. A decision not logged is a decision lost.
6. Every threat gets a response, not just an acknowledgment.
7. The measure of intelligence is anticipation, not reaction.
8. *"Shall I begin?"*

---

> *"I've taken the liberty of preparing the full briefing, sir."*
