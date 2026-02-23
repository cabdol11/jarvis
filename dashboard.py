#!/usr/bin/env python3
"""
J.A.R.V.I.S. Dashboard — Terminal HUD
----------------------------------------
Live system status, threat feed, financial pulse, ops tracker.

"All systems nominal, sir. Displaying full situational awareness."

Usage:
    python dashboard.py          # Live dashboard (refreshes every 30s)
    python dashboard.py --once   # Single render, no loop
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from systems.memory      import Memory
from systems.security    import SecuritySystem
from systems.operations  import OperationsSystem
from systems.financials  import FinancialSystem
from systems.intelligence import IntelligenceSystem

# ─── Layout constants ─────────────────────────────────────────────────────

W       = 78    # Total width
COL_L   = 36    # Left column width
COL_R   = 36    # Right column width

LEVEL_COLORS = {
    "CRITICAL": "\033[91m",   # Red
    "HIGH":     "\033[93m",   # Yellow
    "MODERATE": "\033[33m",   # Dark yellow
    "LOW":      "\033[32m",   # Green
    "MONITOR":  "\033[36m",   # Cyan
}
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BLUE   = "\033[94m"


def _bar(value: float, max_val: float = 100, width: int = 12) -> str:
    """Generate ASCII progress bar."""
    filled = int((value / max_val) * width) if max_val > 0 else 0
    filled = max(0, min(width, filled))
    color = GREEN if value >= 70 else YELLOW if value >= 40 else RED
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET}"


def _pad(text: str, width: int, align: str = "left") -> str:
    """Pad a string to fixed width, truncating if needed."""
    visible = _strip_ansi(text)
    overflow = len(visible) - width
    if overflow > 0:
        text = text[:-(overflow + 3)] + "..."
    padding = width - len(_strip_ansi(text))
    if align == "right":
        return " " * padding + text
    return text + " " * max(0, padding)


def _strip_ansi(s: str) -> str:
    """Remove ANSI escape codes for length calculations."""
    import re
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


def _divider(char="─", width=W):
    return char * width


def _box_top(width=W):
    return f"╔{'═' * (width - 2)}╗"


def _box_bottom(width=W):
    return f"╚{'═' * (width - 2)}╝"


def _box_row(content: str, width=W):
    padded = _pad(content, width - 4)
    return f"║  {padded}  ║"


def _section_header(title: str, width=W):
    inner = f"  {title}  "
    side  = (width - len(inner) - 2) // 2
    return f"╠{'─' * side}{inner}{'─' * (width - side - len(inner) - 2)}╣"


# ─── Dashboard panels ─────────────────────────────────────────────────────

def render_header(now: datetime) -> list:
    lines = []
    lines.append(f"{BOLD}{CYAN}")
    lines.append(_box_top())
    lines.append(_box_row(
        f"J.A.R.V.I.S.  ///  {now.strftime('%A, %B %d, %Y  %H:%M:%S')}  ///  ALL SYSTEMS NOMINAL"
    ))
    lines.append(_box_bottom())
    lines.append(f"{RESET}")
    return lines


def render_health(intel: IntelligenceSystem) -> list:
    lines = []
    health = intel.get_health_summary()
    overall = health.get("overall", 0)
    components = health.get("components", {})

    lines.append(f"  {BOLD}SYSTEM HEALTH{RESET}  {_bar(overall)}  {overall:.0f}/100")
    lines.append("")

    for name, score in components.items():
        label = _pad(name, 20)
        bar   = _bar(score, width=10)
        score_str = f"{score:.0f}"
        lines.append(f"  {label}  {bar}  {score_str}")

    return lines


def render_threats(sec: SecuritySystem) -> list:
    lines = []
    threats = sec.get_active_threats()

    if not threats:
        lines.append(f"  {GREEN}✓ No active threats — all systems within parameters{RESET}")
        return lines

    for t in threats[:5]:
        level = t.get("level", "MONITOR")
        color = LEVEL_COLORS.get(level, "")
        domain = t.get("domain", "?")[:10]
        threat_text = t.get("threat", "?")[:48]
        prob = t.get("probability", 0)
        lines.append(f"  {color}[{level:<8}]{RESET} {domain:<11} {threat_text}  {DIM}{prob}%{RESET}")

    if len(threats) > 5:
        lines.append(f"  {DIM}... and {len(threats) - 5} more{RESET}")

    return lines


def render_financials(fin: FinancialSystem) -> list:
    lines = []
    snap = fin.get_snapshot()

    if not snap:
        lines.append(f"  {DIM}No financial data — update company-os/data/financials_dashboard.json{RESET}")
        return lines

    for k, v in snap.items():
        label = _pad(k, 18)
        lines.append(f"  {label}  {CYAN}{v}{RESET}")

    return lines


def render_operations(ops: OperationsSystem) -> list:
    lines = []
    projects = ops.get_active_projects()
    blockers = ops.get_blockers()

    if not projects:
        lines.append(f"  {DIM}No active projects{RESET}")
        return lines

    lines.append(f"  {'Project':<22} {'DRI':<12} {'Status':<12} {'Pct':>4}")
    lines.append(f"  {'─'*22} {'─'*12} {'─'*12} {'─'*4}")

    for p in projects[:6]:
        status = p.get("status", "Active")
        flag   = f"{RED}⚠{RESET} " if status in ["Blocked", "At Risk"] else "  "
        name   = p.get("name", "?")[:20]
        dri    = p.get("dri", "?")[:11]
        pct    = p.get("pct", 0)
        status_col = (f"{RED}{status}{RESET}" if status == "Blocked"
                      else f"{YELLOW}{status}{RESET}" if status in ["Off Track", "At Risk"]
                      else f"{GREEN}{status}{RESET}")
        lines.append(f"  {flag}{name:<22} {dri:<12} {_pad(status_col, 20)} {pct:>3.0f}%")

    if blockers:
        lines.append("")
        lines.append(f"  {RED}BLOCKERS: {len(blockers)}{RESET}")
        for b in blockers[:2]:
            lines.append(f"  {RED}▶{RESET} {b.get('item', '?')[:55]}")

    return lines


def render_pending(mem: Memory) -> list:
    lines = []
    pending = mem.get_pending_items()

    if not pending:
        lines.append(f"  {GREEN}✓ No pending items{RESET}")
        return lines

    for i, item in enumerate(pending[:5], 1):
        desc = item.get("description", "?")[:52]
        due  = item.get("due", "")
        due_str = f"  {DIM}due {due}{RESET}" if due else ""
        lines.append(f"  {DIM}{i}.{RESET} {desc}{due_str}")

    if len(pending) > 5:
        lines.append(f"  {DIM}... +{len(pending) - 5} more{RESET}")

    return lines


def render_insight(intel: IntelligenceSystem) -> list:
    insight = intel.get_top_insight()
    if not insight:
        return [f"  {DIM}No insight available — check back tomorrow, sir.{RESET}"]
    return [f"  {CYAN}◈{RESET}  {insight[:W-6]}"]


# ─── Full dashboard render ────────────────────────────────────────────────

def render_dashboard(once: bool = False):
    """Render the full JARVIS HUD."""
    try:
        mem   = Memory()
        sec   = SecuritySystem()
        ops   = OperationsSystem()
        fin   = FinancialSystem()
        intel = IntelligenceSystem()
    except Exception as e:
        print(f"Error initializing JARVIS subsystems: {e}")
        return

    while True:
        now = datetime.now()

        # Clear screen
        os.system("clear" if os.name == "posix" else "cls")

        output = []
        output.extend(render_header(now))
        output.append("")

        # Row 1: Health + Threats
        output.append(f"  {BOLD}━━━ SYSTEM HEALTH {'━' * 20}  ━━━ ACTIVE THREATS {'━' * 18}{RESET}")
        health_lines   = render_health(intel)
        threat_lines   = render_threats(sec)
        max_rows = max(len(health_lines), len(threat_lines))
        for i in range(max_rows):
            hl = health_lines[i] if i < len(health_lines) else ""
            tl = threat_lines[i]  if i < len(threat_lines) else ""
            hl_stripped = _strip_ansi(hl)
            pad = max(0, 38 - len(hl_stripped))
            print(hl + " " * pad + tl)
        output = []  # flush buffer since we used direct print above

        print("")
        print(f"  {BOLD}━━━ FINANCIAL POSITION {'━' * 15}  ━━━ ACTIVE OPERATIONS {'━' * 14}{RESET}")
        fin_lines  = render_financials(fin)
        ops_lines  = render_operations(ops)
        max_rows = max(len(fin_lines), len(ops_lines))
        for i in range(max_rows):
            fl = fin_lines[i]  if i < len(fin_lines)  else ""
            ol = ops_lines[i]  if i < len(ops_lines)  else ""
            fl_stripped = _strip_ansi(fl)
            pad = max(0, 38 - len(fl_stripped))
            print(fl + " " * pad + ol)

        print("")
        print(f"  {BOLD}━━━ PENDING ITEMS {'━' * 22}{RESET}")
        for line in render_pending(mem):
            print(line)

        print("")
        print(f"  {BOLD}━━━ JARVIS INSIGHT {'━' * 21}{RESET}")
        for line in render_insight(intel):
            print(line)

        print("")
        print(_divider())
        sessions = mem.get_session_count()
        threats  = len(sec.get_active_threats())
        pending  = len(mem.get_pending_items())
        print(
            f"  {DIM}Sessions: {sessions}  │  Active Threats: {threats}  │  "
            f"Pending: {pending}  │  Last refresh: {now.strftime('%H:%M:%S')}{RESET}"
        )
        print(_divider())

        if once:
            break

        print(f"\n  {DIM}Refreshing in 30 seconds — Ctrl+C to exit{RESET}")
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print(f"\n  {DIM}Dashboard closed. JARVIS remains online.{RESET}\n")
            break


# ─── Entry point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="J.A.R.V.I.S. Dashboard")
    parser.add_argument("--once", action="store_true", help="Render once and exit")
    args = parser.parse_args()
    render_dashboard(once=args.once)


if __name__ == "__main__":
    main()
