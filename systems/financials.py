"""
J.A.R.V.I.S. Financial System
--------------------------------
Real-time financial monitoring, scenario modeling, weekly briefings.

"Your burn rate is accelerating, sir. I thought you should know."

Monitors: runway, burn, revenue growth, unit economics, budget variances.
Models: fundraising scenarios, growth projections, break-even analysis.
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Cross-system
FINANCIALS_FILE  = BASE_DIR.parent / "company-os" / "data" / "financials_dashboard.json"
PROJECTS_FILE    = BASE_DIR.parent / "company-os" / "data" / "projects.json"
TIKTOK_FILE      = BASE_DIR.parent / "tiktok-affiliate-system" / "data" / "financials.json"


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


class FinancialSystem:
    """
    JARVIS financial intelligence engine.

    Synthesizes financial data from all connected systems.
    Flags anomalies. Models scenarios. Provides executive-grade briefings.
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._fin = _load(FINANCIALS_FILE, {})

    def _reload(self):
        """Re-read from disk in case data was updated."""
        self._fin = _load(FINANCIALS_FILE, {})

    # ─── Snapshot ──────────────────────────────────────────────────────────

    def get_snapshot(self) -> dict:
        """Return key financial metrics formatted for display."""
        self._reload()
        fin = self._fin
        if not fin:
            return {}

        snapshot = {}

        mrr = fin.get("mrr")
        arr = fin.get("arr") or (mrr * 12 if mrr else None)
        if mrr:
            snapshot["MRR"] = f"${mrr:,.0f}"
        if arr:
            snapshot["ARR"] = f"${arr:,.0f}"

        burn = fin.get("monthly_burn") or fin.get("burn_rate")
        if burn:
            snapshot["Monthly burn"] = f"${burn:,.0f}"

        runway = fin.get("runway_months")
        if runway:
            snapshot["Runway"] = f"{runway:.0f} months"

        cash = fin.get("cash_on_hand") or fin.get("cash")
        if cash:
            snapshot["Cash on hand"] = f"${cash:,.0f}"

        bm = fin.get("burn_multiple")
        if bm:
            snapshot["Burn multiple"] = f"{bm:.1f}x"

        ltv_cac = fin.get("ltv_cac_ratio")
        if ltv_cac:
            snapshot["LTV:CAC"] = f"{ltv_cac:.1f}x"

        growth = fin.get("mom_growth") or fin.get("revenue_growth_mom")
        if growth:
            snapshot["MoM growth"] = f"{growth:.1f}%"

        return snapshot

    # ─── Runway analysis ───────────────────────────────────────────────────

    def analyze_runway(self) -> str:
        self._reload()
        fin = self._fin

        cash  = fin.get("cash_on_hand") or fin.get("cash", 0)
        burn  = fin.get("monthly_burn")  or fin.get("burn_rate", 0)
        mrr   = fin.get("mrr", 0)

        if not burn:
            return "Insufficient data to compute runway. Update financials_dashboard.json."

        net_burn = max(burn - mrr, 0) if mrr else burn
        runway   = cash / net_burn if net_burn > 0 else float("inf")

        lines = [
            "RUNWAY ANALYSIS",
            "",
            f"  Cash on hand:     ${cash:,.0f}",
            f"  Gross burn/month: ${burn:,.0f}",
            f"  MRR:              ${mrr:,.0f}",
            f"  Net burn/month:   ${net_burn:,.0f}",
            f"  Runway:           {runway:.1f} months",
            "",
        ]

        if runway < 6:
            lines.append("  STATUS: CRITICAL — Initiate emergency fundraise or cost reduction now.")
        elif runway < 12:
            lines.append("  STATUS: HIGH RISK — Begin investor outreach immediately.")
        elif runway < 18:
            lines.append("  STATUS: MODERATE — Start fundraise planning this quarter.")
        else:
            lines.append("  STATUS: HEALTHY — Runway supports current strategy.")

        # Break-even projection
        if mrr and burn:
            months_to_be = None
            growth = fin.get("mom_growth", 0)
            if growth and growth > 0:
                current_mrr = mrr
                for m in range(1, 61):
                    current_mrr *= (1 + growth / 100)
                    if current_mrr >= burn:
                        months_to_be = m
                        break
            if months_to_be:
                be_date = (datetime.now() + timedelta(days=months_to_be * 30)).strftime("%B %Y")
                lines.append(f"\n  Break-even projected: {be_date} (at {growth:.1f}% MoM growth)")

        return "\n".join(lines)

    # ─── Scenario modeling ─────────────────────────────────────────────────

    def model_fundraise(self, target_raise: float, valuation_cap: float = None,
                        discount: float = 0.20) -> str:
        """Model fundraising scenarios: dilution, runway extension."""
        self._reload()
        fin = self._fin

        burn    = fin.get("monthly_burn") or fin.get("burn_rate", 0)
        mrr     = fin.get("mrr", 0)
        cash    = fin.get("cash_on_hand") or fin.get("cash", 0)
        net_burn = max(burn - mrr, 0) if mrr else burn

        lines = [
            f"FUNDRAISE SCENARIO MODEL",
            f"  Target raise: ${target_raise:,.0f}",
            "",
        ]

        if net_burn:
            additional_runway = target_raise / net_burn
            new_runway = (cash + target_raise) / net_burn
            lines.append(f"  Runway extension:   +{additional_runway:.0f} months")
            lines.append(f"  New total runway:   {new_runway:.0f} months")
            lines.append("")

        if valuation_cap:
            dilution_safe = target_raise / valuation_cap
            lines.append(f"  SAFE at ${valuation_cap/1e6:.1f}M cap:")
            lines.append(f"    Approximate dilution: {dilution_safe*100:.1f}%")
            lines.append("")

        # Model scenarios
        scenarios = [
            ("Bear",   target_raise * 0.5,  "Slower growth, bridge only"),
            ("Base",   target_raise,         "Plan case — meets target"),
            ("Bull",   target_raise * 1.5,  "Strong interest, oversubscribed"),
        ]

        lines.append("  SCENARIOS:")
        for name, amount, description in scenarios:
            if net_burn:
                runway = (cash + amount) / net_burn
                lines.append(f"  {name:<6} ${amount:>12,.0f} → {runway:.0f}mo runway  ({description})")

        lines.append("")
        lines.append("  RECOMMENDATION:")
        lines.append(f"  Raise for 24 months runway at minimum. Close within 6 months of start.")

        return "\n".join(lines)

    def model_growth(self, target_arr: float, current_mrr: float = None) -> str:
        """Model months to ARR target at various growth rates."""
        self._reload()
        if current_mrr is None:
            current_mrr = self._fin.get("mrr", 0)

        if not current_mrr:
            return "No MRR data available. Update financials_dashboard.json."

        target_mrr = target_arr / 12
        lines = [
            f"GROWTH MODEL — Target: ${target_arr/1e6:.1f}M ARR",
            f"  Current MRR: ${current_mrr:,.0f}",
            f"  Target MRR:  ${target_mrr:,.0f}",
            "",
            f"  {'Growth Rate':<14} {'Months':<10} {'Arrival Date'}",
            f"  {'─'*14} {'─'*10} {'─'*15}",
        ]

        for growth_pct in [5, 10, 15, 20, 25, 30]:
            mrr = current_mrr
            months = 0
            while mrr < target_mrr and months < 120:
                mrr *= (1 + growth_pct / 100)
                months += 1
            if months < 120:
                arrival = (datetime.now() + timedelta(days=months * 30)).strftime("%b %Y")
                lines.append(f"  {growth_pct}% MoM          {months:<10} {arrival}")
            else:
                lines.append(f"  {growth_pct}% MoM          >10 years   Not feasible at this rate")

        return "\n".join(lines)

    # ─── Unit economics ────────────────────────────────────────────────────

    def analyze_unit_economics(self) -> str:
        self._reload()
        fin = self._fin

        cac      = fin.get("cac")
        ltv      = fin.get("ltv")
        arpu     = fin.get("arpu")
        churn    = fin.get("monthly_churn_rate") or fin.get("churn_rate")
        payback  = fin.get("cac_payback_months")

        if not cac and not ltv:
            return "No unit economics data found. Update financials_dashboard.json."

        lines = ["UNIT ECONOMICS ANALYSIS", ""]

        if cac:
            lines.append(f"  CAC:             ${cac:,.0f}")
        if ltv:
            lines.append(f"  LTV:             ${ltv:,.0f}")
        if cac and ltv:
            ratio = ltv / cac
            flag  = "✓" if ratio >= 3.0 else "⚠" if ratio >= 2.0 else "✗"
            lines.append(f"  LTV:CAC:         {ratio:.1f}x  {flag}")
            lines.append(f"  Benchmark:       3.0x+ for healthy SaaS")
        if payback:
            flag = "✓" if payback <= 12 else "⚠" if payback <= 18 else "✗"
            lines.append(f"  CAC payback:     {payback} months  {flag}")
        if churn:
            annual = (1 - (1 - churn) ** 12) * 100
            flag = "✓" if annual < 5 else "⚠" if annual < 10 else "✗"
            lines.append(f"  Monthly churn:   {churn:.1f}%  ({annual:.0f}% annual)  {flag}")
        if arpu:
            lines.append(f"  ARPU:            ${arpu:,.0f}")

        lines.append("")
        lines.append("  GRADE:")
        if cac and ltv:
            if ratio >= 3.0 and (not payback or payback <= 12):
                lines.append("  EXCELLENT — Unit economics support aggressive growth investment.")
            elif ratio >= 2.0:
                lines.append("  ACCEPTABLE — Improve CAC efficiency or increase retention.")
            else:
                lines.append("  CRITICAL — Growing at current unit economics accelerates losses.")

        return "\n".join(lines)

    # ─── Budget variance ───────────────────────────────────────────────────

    def get_budget_variances(self) -> list:
        """Return projects with budget overruns."""
        proj = _load(PROJECTS_FILE, {})
        variances = []
        for p in proj.get("projects", {}).values():
            budget = p.get("budget", 0)
            actual = p.get("actual_spend", 0)
            if budget > 0 and actual > 0:
                variance_pct = (actual - budget) / budget * 100
                if abs(variance_pct) > 5:
                    variances.append({
                        "project": p.get("name", "?"),
                        "budget":  budget,
                        "actual":  actual,
                        "variance_pct": round(variance_pct, 1),
                        "status":  "over" if variance_pct > 0 else "under",
                    })
        return sorted(variances, key=lambda x: abs(x["variance_pct"]), reverse=True)

    # ─── TikTok revenue tracking ───────────────────────────────────────────

    def get_affiliate_revenue(self) -> dict:
        """Pull TikTok affiliate revenue from connected system."""
        tiktok = _load(TIKTOK_FILE, {})
        if not tiktok:
            return {}

        return {
            "Total revenue":    f"${tiktok.get('total_revenue', 0):,.2f}",
            "This month":       f"${tiktok.get('monthly_revenue', 0):,.2f}",
            "Active products":  tiktok.get("active_products", 0),
            "Conversion rate":  f"{tiktok.get('avg_cvr', 0):.1f}%",
        }

    # ─── Weekly financial briefing ─────────────────────────────────────────

    def get_weekly_briefing(self) -> str:
        self._reload()
        snapshot  = self.get_snapshot()
        variances = self.get_budget_variances()
        affiliate = self.get_affiliate_revenue()

        lines = [
            f"FINANCIAL BRIEFING — Week of {datetime.now().strftime('%B %d, %Y')}",
            "",
        ]

        if snapshot:
            lines.append("  KEY METRICS:")
            for k, v in snapshot.items():
                lines.append(f"  {'':2}{k:<25} {v}")
            lines.append("")

        if affiliate:
            lines.append("  TIKTOK AFFILIATE:")
            for k, v in affiliate.items():
                lines.append(f"  {'':2}{k:<25} {v}")
            lines.append("")

        if variances:
            over_budget = [v for v in variances if v["status"] == "over"]
            if over_budget:
                lines.append("  BUDGET OVERRUNS:")
                for v in over_budget[:3]:
                    lines.append(f"  ▶  {v['project'][:35]} +{v['variance_pct']:.0f}% over budget")
                lines.append("")

        # Runway alert
        runway = self._fin.get("runway_months")
        if isinstance(runway, (int, float)):
            if runway < 12:
                lines.append(f"  ⚠  RUNWAY WARNING: {runway:.0f} months remaining.")
                lines.append("     Capital raise should be active or initiated.")

        return "\n".join(lines)

    def is_online(self) -> bool:
        return True
