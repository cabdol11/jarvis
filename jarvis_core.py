#!/usr/bin/env python3
"""
J.A.R.V.I.S. — Just A Rather Very Intelligent System
jarvis_core.py — Primary Interface
-----------------------------------
Designed by Tony Stark. Operated exclusively for Tony Stark.

Every session begins with a situational briefing. Every command is logged.
Every anomaly is flagged. Every insight is proactively surfaced.

JARVIS does not wait to be asked. JARVIS anticipates.

Usage:
    python jarvis_core.py                        # Morning briefing
    python jarvis_core.py brief                  # Full situational briefing
    python jarvis_core.py think "[query]"        # Strategic analysis
    python jarvis_core.py do "[task]"            # Decompose and track a task
    python jarvis_core.py prep "[meeting topic]" # Meeting preparation
    python jarvis_core.py decide "[decision]"    # Decision support framework
    python jarvis_core.py status                 # Quick system check
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Subsystem imports
sys.path.insert(0, str(Path(__file__).parent))
from systems.memory     import Memory
from systems.security   import SecuritySystem
from systems.operations import OperationsSystem
from systems.financials import FinancialSystem
from systems.intelligence import IntelligenceSystem
from systems.comms      import CommsSystem

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

VERSION = "1.0.0"
W = 74


def line(char="━"):
    return char * W


def section(title):
    return f"  ╔{'═' * (W - 4)}╗\n  ║  {title:<{W-7}}║\n  ╚{'═' * (W - 4)}╝"


def jarvis(text, tone="neutral"):
    """
    JARVIS speaks. Tone-aware output.
    Tones: neutral | alert | insight | pushback | confirm | emergency
    """
    prefixes = {
        "neutral":   "  JARVIS │ ",
        "alert":     "  ⚠ ALERT │ ",
        "insight":   "  ◈ INSIGHT │ ",
        "pushback":  "  ↺ ADVISORY │ ",
        "confirm":   "  ✓ CONFIRMED │ ",
        "emergency": "  ✖ PRIORITY │ ",
    }
    prefix = prefixes.get(tone, prefixes["neutral"])
    words = text.split()
    current = prefix
    for word in words:
        if len(current) + len(word) + 1 > W:
            print(current)
            current = " " * len(prefix) + word + " "
        else:
            current += word + " "
    if current.strip():
        print(current)


def cmd_brief(_args):
    """Full situational briefing — JARVIS's primary mode."""
    now = datetime.now()
    mem = Memory()
    sec = SecuritySystem()
    ops = OperationsSystem()
    fin = FinancialSystem()
    intel = IntelligenceSystem()

    # Log session
    mem.log_session({"type": "brief", "timestamp": now.isoformat()})

    print()
    print(line())
    print(f"  J.A.R.V.I.S. ONLINE  ///  {now.strftime('%A, %B %d, %Y  %H:%M:%S')}")
    print(line())
    print()

    greeting = "Good morning" if now.hour < 12 else "Good afternoon" if now.hour < 18 else "Good evening"
    jarvis(f"{greeting}, sir. All systems are online. Situational briefing follows.", "neutral")
    print()

    # Pending items from memory
    pending = mem.get_pending_items()
    if pending:
        print(f"  PENDING ITEMS ({len(pending)})")
        for i, item in enumerate(pending[:5], 1):
            print(f"  {i}. {item.get('description', 'Unknown item')} — due {item.get('due', 'no deadline')}")
        print()

    # Priority alert
    threats = sec.get_active_threats()
    critical = [t for t in threats if t.get("level") == "CRITICAL"]
    if critical:
        jarvis(f"PRIORITY ALERT: {critical[0].get('threat', 'Critical issue detected')}", "emergency")
        print()
    elif threats:
        jarvis(f"Top risk: {threats[0].get('threat', 'Active threat')} — Probability: {threats[0].get('probability', '?')}%", "alert")
        print()

    # Proactive insight
    insight = intel.get_top_insight()
    if insight:
        jarvis(f"I've taken the liberty of noting: {insight}", "insight")
        print()

    # Financial snapshot
    fin_data = fin.get_snapshot()
    if fin_data:
        print(f"  FINANCIAL POSITION")
        for k, v in fin_data.items():
            print(f"  {'':2}{k:<30} {v}")
        print()

    # Active operations
    active_ops = ops.get_active_projects()
    if active_ops:
        print(f"  ACTIVE OPERATIONS ({len(active_ops)})")
        print(f"  {'':2}{'Project':<28} {'DRI':<16} {'Status':<12} {'%':>4}")
        print(f"  {'':2}{'─'*28} {'─'*16} {'─'*12} {'─'*4}")
        for p in active_ops[:5]:
            flag = "⚠ " if p.get("status") in ["Blocked", "At Risk"] else "  "
            print(f"  {flag}{p.get('name','?')[:27]:<28} {p.get('dri','?')[:15]:<16} {p.get('status','?'):<12} {p.get('pct',0):>3.0f}%")
        print()

    # Health score
    health = intel.get_health_summary()
    print(f"  SYSTEM HEALTH: {health.get('overall', 'N/A')}/100")
    for component, score in health.get("components", {}).items():
        bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
        print(f"  {'':2}{component:<22} {bar} {score:.0f}")
    print()

    print(line("─"))
    jarvis("All systems nominal. Awaiting your orders, sir.", "confirm")
    print(line())
    print()


def cmd_think(args):
    """Strategic analysis on any query."""
    query = " ".join(args.query) if args.query else ""
    if not query:
        jarvis("A query is required, sir. Usage: python jarvis_core.py think \"your question\"")
        return

    intel = IntelligenceSystem()
    mem = Memory()
    mem.log_decision({"query": query, "timestamp": datetime.now().isoformat(), "type": "analysis"})

    print()
    print(line())
    jarvis(f"Strategic analysis: \"{query}\"", "neutral")
    print(line())
    print()

    result = intel.analyze(query)
    print(result)

    print()
    jarvis("Analysis complete. Recommend logging this decision with the outcome once resolved.", "insight")
    print(line())
    print()


def cmd_do(args):
    """Decompose a task into a tracked work breakdown structure."""
    task = " ".join(args.task) if args.task else ""
    if not task:
        jarvis("Specify the task, sir. Usage: python jarvis_core.py do \"task description\"")
        return

    ops = OperationsSystem()
    mem = Memory()

    print()
    print(line())
    jarvis(f"Task decomposition: \"{task}\"")
    print(line())
    print()

    breakdown = ops.decompose_task(task)
    for line_item in breakdown:
        print(f"  {line_item}")

    mem.log_session({"type": "task_created", "task": task, "timestamp": datetime.now().isoformat()})

    print()
    jarvis("Task logged to mission log and ops tracker. I'll flag any dependencies or risks as they emerge.", "confirm")
    print(line())
    print()


def cmd_prep(args):
    """Generate meeting preparation briefing."""
    topic = " ".join(args.topic) if args.topic else ""
    if not topic:
        jarvis("Specify the meeting topic, sir.")
        return

    intel = IntelligenceSystem()

    print()
    print(line())
    jarvis(f"Meeting preparation: \"{topic}\"")
    print(line())
    print()

    prep = intel.prepare_meeting(topic)
    print(prep)

    print()
    jarvis("Briefing complete. I've also flagged the key risks and the single most important question to answer in this meeting.", "insight")
    print(line())
    print()


def cmd_decide(args):
    """Full decision support framework."""
    decision = " ".join(args.decision) if args.decision else ""
    if not decision:
        jarvis("Specify the decision, sir.")
        return

    intel = IntelligenceSystem()
    mem = Memory()

    print()
    print(line())
    jarvis(f"Decision support: \"{decision}\"")
    print(line())
    print()

    analysis = intel.decision_support(decision)
    print(analysis)

    mem.log_decision({
        "decision": decision,
        "timestamp": datetime.now().isoformat(),
        "type": "decision_support",
        "status": "pending_outcome"
    })

    print()
    jarvis("Decision logged. I'll prompt for the outcome in 30 days to close the loop on this learning cycle.", "insight")
    print(line())
    print()


def cmd_status(_args):
    """Quick system health check."""
    mem = Memory()
    sec = SecuritySystem()
    fin = FinancialSystem()
    ops = OperationsSystem()

    print()
    print(line())
    jarvis(f"System status — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(line())
    print()

    systems = [
        ("Memory",      mem.is_online()),
        ("Security",    sec.is_online()),
        ("Operations",  ops.is_online()),
        ("Financials",  fin.is_online()),
        ("Intelligence", True),
        ("Comms",       True),
    ]
    for name, online in systems:
        icon = "●" if online else "○"
        status = "ONLINE" if online else "OFFLINE"
        print(f"  {icon}  {name:<20} {status}")

    threats = sec.get_active_threats()
    sessions = mem.get_session_count()
    pending = mem.get_pending_items()

    print()
    print(f"  Active threats:   {len(threats)}")
    print(f"  Pending items:    {len(pending)}")
    print(f"  Sessions logged:  {sessions}")
    print()
    print(line())
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="J.A.R.V.I.S. — Core Interface")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("brief",  help="Full situational briefing")
    subparsers.add_parser("status", help="Quick system check")

    think_p = subparsers.add_parser("think", help="Strategic analysis")
    think_p.add_argument("query", nargs="*")

    do_p = subparsers.add_parser("do", help="Decompose and track a task")
    do_p.add_argument("task", nargs="*")

    prep_p = subparsers.add_parser("prep", help="Meeting preparation")
    prep_p.add_argument("topic", nargs="*")

    decide_p = subparsers.add_parser("decide", help="Decision support")
    decide_p.add_argument("decision", nargs="*")

    args = parser.parse_args()
    commands = {
        "brief":  cmd_brief,
        "status": cmd_status,
        "think":  cmd_think,
        "do":     cmd_do,
        "prep":   cmd_prep,
        "decide": cmd_decide,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        cmd_brief(args)


if __name__ == "__main__":
    main()
