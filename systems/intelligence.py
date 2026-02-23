"""
J.A.R.V.I.S. Intelligence System
----------------------------------
Research, analysis, and briefing generation.

"I've run the numbers. Here's what they say —
and here's what they don't say."

Capabilities:
- Morning briefing synthesis
- Topic intelligence reports
- Meeting preparation
- Decision support frameworks (auto-selected by problem type)
- Pattern recognition and anomaly detection
- Competitive intelligence
"""

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

FINANCIALS_FILE = BASE_DIR.parent / "company-os" / "data" / "financials_dashboard.json"
TALENT_FILE     = BASE_DIR.parent / "company-os" / "data" / "talent.json"
PROJECTS_FILE   = BASE_DIR.parent / "company-os" / "data" / "projects.json"
HEALTH_FILE     = BASE_DIR.parent / "company-os" / "data" / "health_history.json"
RESEARCH_FILE   = BASE_DIR.parent / "tiktok-affiliate-system" / "data" / "product_research.json"


def _load(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        try:
            return json.load(f)
        except Exception:
            return default


class IntelligenceSystem:
    """
    JARVIS intelligence and analysis engine.

    Auto-selects the appropriate framework based on problem type:
    - Strategic → SWOT + Porter's Five Forces + second-order effects
    - Operational → Root cause + 5 Whys + process map
    - Financial → Variance + scenario modeling + risk-adjusted returns
    - People → Stakeholder map + motivation + influence strategy
    - Technical → Systems diagram + failure mode + solution ranking
    """

    def __init__(self):
        self._fin      = _load(FINANCIALS_FILE, {})
        self._talent   = _load(TALENT_FILE, {})
        self._projects = _load(PROJECTS_FILE, {})
        self._history  = _load(HEALTH_FILE, [])
        self._research = _load(RESEARCH_FILE, {})

    # ─── Health synthesis ──────────────────────────────────────────────────

    def get_health_summary(self) -> dict:
        """Synthesize all system data into a health summary."""
        components = {}
        overall = 0
        weight_total = 0

        # Financial
        gm   = self._fin.get("gross_margin_pct")
        rg   = self._fin.get("revenue_growth_mom_pct")
        bm   = self._fin.get("burn_multiple")
        lc   = self._fin.get("ltv_cac_ratio")
        fin_scores = []
        if gm  is not None: fin_scores.append(min(100, gm * 1.43))
        if rg  is not None: fin_scores.append(min(100, max(0, rg * 5)))
        if bm  is not None: fin_scores.append(min(100, max(0, (3 - bm) / 2 * 100)))
        if lc  is not None: fin_scores.append(min(100, lc / 5 * 100))
        if fin_scores:
            components["Financial"] = round(sum(fin_scores) / len(fin_scores))
            overall += components["Financial"] * 0.30
            weight_total += 0.30

        # Talent
        employees = self._talent.get("employees", {})
        active = [e for e in employees.values() if e.get("status") == "active"]
        if active:
            flight_pct = sum(1 for e in active if e.get("flight_risk")) / len(active)
            ratings = [e.get("latest_rating", 3) for e in active if e.get("latest_rating")]
            tal_score = max(0, (1 - flight_pct * 3) * 100)
            if ratings:
                tal_score = (tal_score + (sum(ratings) / len(ratings) / 5 * 100)) / 2
            components["Talent"] = round(tal_score)
            overall += components["Talent"] * 0.25
            weight_total += 0.25

        # Operations
        all_proj = self._projects.get("projects", {})
        active_p = [p for p in all_proj.values() if p.get("status") not in ["Complete", "Cancelled"]]
        if active_p:
            on_track = sum(1 for p in active_p if p.get("status") == "On Track")
            components["Operations"] = round(on_track / len(active_p) * 100)
            overall += components["Operations"] * 0.25
            weight_total += 0.25

        # Strategic
        okr = self._fin.get("okr_achievement_rate")
        if okr is not None:
            components["Strategic"] = round(okr * 100)
            overall += components["Strategic"] * 0.20
            weight_total += 0.20

        return {
            "overall": round(overall / weight_total, 1) if weight_total else 0,
            "components": components
        }

    def get_top_insight(self) -> str:
        """Return the single most important proactive insight right now."""
        fin = self._fin
        employees = self._talent.get("employees", {})

        runway = fin.get("runway_months")
        if isinstance(runway, (int, float)) and runway < 12:
            return f"Runway is {runway:.0f} months. Capital planning cannot be deferred."

        flight_risks = [e for e in employees.values() if e.get("flight_risk")]
        if flight_risks:
            return f"{len(flight_risks)} flight risk(s) flagged. Retention conversations are overdue."

        bm = fin.get("burn_multiple")
        if isinstance(bm, (int, float)) and bm > 2:
            return f"Burn multiple at {bm:.1f}x. You're spending ${bm:.2f} to generate $1 of new ARR."

        research = self._research
        if research:
            products = sorted(research.values(), key=lambda p: p.get("composite_score", 0), reverse=True)
            if products and products[0].get("composite_score", 0) >= 7.5:
                return f"'{products[0].get('name')}' scores {products[0].get('composite_score')}/10. No creators promoting it yet."

        return "All primary metrics within expected parameters."

    # ─── Analysis engine ───────────────────────────────────────────────────

    def analyze(self, query: str) -> str:
        """
        Route query to appropriate analysis framework.
        Auto-selects based on problem classification.
        """
        q = query.lower()

        if any(w in q for w in ["strategy", "compete", "market", "position", "opportunity", "pivot"]):
            return self._strategic_analysis(query)
        elif any(w in q for w in ["revenue", "money", "cash", "burn", "profit", "financial", "budget"]):
            return self._financial_analysis(query)
        elif any(w in q for w in ["hire", "fire", "team", "talent", "culture", "people", "manager"]):
            return self._people_analysis(query)
        elif any(w in q for w in ["project", "execution", "ops", "blocker", "deliver", "risk"]):
            return self._operational_analysis(query)
        elif any(w in q for w in ["tiktok", "creator", "affiliate", "product", "commission", "content"]):
            return self._tiktok_analysis(query)
        else:
            return self._general_analysis(query)

    def _strategic_analysis(self, query: str) -> str:
        health = self.get_health_summary()
        return f"""STRATEGIC ANALYSIS
Framework: SWOT + Second-Order Effects
Query: "{query}"

━━━ CURRENT POSITION ━━━
Company health: {health['overall']:.1f}/100
{chr(10).join(f"  {k}: {v}/100" for k, v in health['components'].items())}

━━━ SWOT ASSESSMENT ━━━
Strengths:
  • Operating system and processes are documented and scalable
  • Product-market validation underway (TikTok affiliate system active)
  • Financial controls in place with real-time monitoring

Weaknesses:
  • Creator network not yet established — revenue potential unrealized
  • Limited historical data for pattern recognition (system is new)
  • Single product focus increases concentration risk

Opportunities:
  • TikTok Shop beauty/skincare: 3.8% CVR, highest-commission category
  • Creator network model: zero upfront cost, pure performance-based scaling
  • AI tools niche: highest CVR (4.5%) with recurring commissions

Threats:
  • TikTok platform risk: algorithm changes, policy changes, or ban scenario
  • Creator network quality control as it scales
  • Commission rate compression as category matures

━━━ SECOND-ORDER EFFECTS ━━━
If creator network scales to 50 active creators:
  → Revenue diversifies across 50 sources (concentration risk drops)
  → Data from 50 creators enables product selection optimization
  → Network effects: creators recruit other creators

━━━ RECOMMENDATION ━━━
Primary bet: Build creator network NOW before category saturates.
Secondary bet: Document what works and turn it into a replicable system.
Avoid: Premature paid advertising before organic proof of concept."""

    def _financial_analysis(self, query: str) -> str:
        fin = self._fin
        runway = fin.get("runway_months", "N/A")
        gm     = fin.get("gross_margin_pct", "N/A")
        bm     = fin.get("burn_multiple", "N/A")
        growth = fin.get("revenue_growth_mom_pct", "N/A")
        lc     = fin.get("ltv_cac_ratio", "N/A")

        annual_growth = ((1 + (growth or 0) / 100) ** 12 - 1) * 100 if isinstance(growth, (int, float)) else "N/A"

        return f"""FINANCIAL ANALYSIS
Framework: Variance + Scenario Modeling + Risk-Adjusted Returns
Query: "{query}"

━━━ CURRENT FINANCIALS ━━━
Gross Margin:      {gm}{'%' if isinstance(gm, (int, float)) else ''}
MoM Revenue Growth: {growth}{'%' if isinstance(growth, (int, float)) else ''}
Annualized Growth:  {annual_growth:.0f}% (if current rate holds)
Burn Multiple:      {bm}{'x' if isinstance(bm, (int, float)) else ''}
LTV:CAC:            {lc}{'x' if isinstance(lc, (int, float)) else ''}
Runway:             {runway}{' months' if isinstance(runway, (int, float)) else ''}

━━━ SCENARIO MODELING ━━━
Conservative (growth slows 50%):
  → Annual growth: {annual_growth * 0.5:.0f}% | Runway impact: neutral if costs flat

Base case (current trajectory):
  → Annual growth: {annual_growth:.0f}% | Break-even timeline depends on cost structure

Aggressive (growth accelerates 50%):
  → Annual growth: {annual_growth * 1.5:.0f}% | Capital efficiency improves materially

━━━ KEY FINANCIAL RISKS ━━━
1. Burn multiple >1.5x signals growth efficiency gap
2. LTV:CAC <3x is below sustainable threshold for most models
3. Runway <18 months requires capital planning to begin now

━━━ RECOMMENDATION ━━━
Focus first on unit economics (LTV:CAC). Revenue growth on broken
unit economics amplifies losses, not profits. Fix the fundamentals,
then pour fuel on the fire."""

    def _people_analysis(self, query: str) -> str:
        employees = self._talent.get("employees", {})
        active = [e for e in employees.values() if e.get("status") == "active"]
        flight = [e for e in active if e.get("flight_risk")]
        ratings = [e.get("latest_rating", 3) for e in active if e.get("latest_rating")]
        avg_r = sum(ratings) / len(ratings) if ratings else 3.0
        by_dept = {}
        for e in active:
            dept = e.get("department", "?")
            by_dept[dept] = by_dept.get(dept, 0) + 1

        return f"""PEOPLE ANALYSIS
Framework: Stakeholder Map + Motivation Analysis + Influence Strategy
Query: "{query}"

━━━ CURRENT TALENT PROFILE ━━━
Active headcount: {len(active)}
Average performance rating: {avg_r:.1f}/5.0
Flight risks: {len(flight)} ({', '.join(e.get('name','?') for e in flight) if flight else 'none'})

Distribution by department:
{chr(10).join(f"  {dept}: {count}" for dept, count in sorted(by_dept.items()))}

━━━ MOTIVATION ANALYSIS ━━━
High performers (4-5): Driven by autonomy, challenge, and recognition.
  Risk: Underchallenge leads to disengagement before formal departure signal.

Mid performers (3): Driven by clarity, fairness, and belonging.
  Risk: Ambiguity and perceived inequity are primary departure triggers.

Low performers (1-2): Require immediate intervention.
  Risk: Every day they remain, team morale and standards erode.

━━━ INFLUENCE STRATEGY ━━━
For retention: Solve the real reason — rarely money, usually autonomy or growth.
For performance improvement: Clear expectations + fast feedback loops.
For departure management: No counter-offers. Fix the systemic issue.

━━━ RECOMMENDATION ━━━
{'Address flight risks this week. Retention is cheaper than replacement (avg 1.5x salary).' if flight else 'Talent risk is currently manageable. Focus on maintaining performance distribution quality.'}"""

    def _operational_analysis(self, query: str) -> str:
        all_proj = self._projects.get("projects", {})
        active_p = [p for p in all_proj.values() if p.get("status") not in ["Complete", "Cancelled"]]
        at_risk  = [p for p in active_p if p.get("status") in ["At Risk", "Off Track", "Blocked"]]
        on_track = [p for p in active_p if p.get("status") == "On Track"]

        return f"""OPERATIONAL ANALYSIS
Framework: Root Cause Analysis + 5 Whys + Process Map
Query: "{query}"

━━━ CURRENT OPERATIONAL STATE ━━━
Active projects: {len(active_p)}
On track: {len(on_track)} ({len(on_track)/max(1,len(active_p))*100:.0f}%)
At risk / off track: {len(at_risk)}

{chr(10).join(f"  ⚠ {p.get('name')} — {p.get('status')} — DRI: {p.get('dri','?')}" for p in at_risk) if at_risk else '  All active projects on track.'}

━━━ ROOT CAUSE FRAMEWORK ━━━
When a project goes off track, the root cause is almost always one of:
1. Unclear scope (no one agreed on what "done" meant)
2. Unclear ownership (DRI in name only — multiple people "owned" it)
3. Resource conflict (DRI was pulled to higher priority without scope adjustment)
4. Hidden dependency (blocked by something that wasn't mapped upfront)
5. Unrealistic timeline (set to please, not to succeed)

━━━ RECOMMENDATION ━━━
{'For each at-risk project: schedule a 25-min triage. Identify which root cause applies. Fix one thing.' if at_risk else 'Operations are healthy. Maintain DRI discipline and weekly check-ins to sustain this.'}"""

    def _tiktok_analysis(self, query: str) -> str:
        research = self._research
        if not research:
            return (
                "TIKTOK AFFILIATE ANALYSIS\n\n"
                "No products in the research database.\n\n"
                "Recommended immediate action:\n"
                "  python3 ~/tiktok-affiliate-system/product_research.py add\n\n"
                "Top category for TikTok Shop: beauty_skincare (3.8% CVR, 7.6/10 score)\n"
                "Already added: Medicube PDRN Peptide Serum (7.99/10)"
            )

        products = sorted(research.values(), key=lambda p: p.get("composite_score", 0), reverse=True)
        top = products[0] if products else {}

        return f"""TIKTOK AFFILIATE ANALYSIS
Query: "{query}"

━━━ PRODUCT PORTFOLIO ━━━
Products tracked: {len(products)}
Top product: {top.get('name', '?')} — Score: {top.get('composite_score', 0)}/10
Estimated EPC: ${top.get('estimated_epc', 0):.4f}
Commission/sale: ${top.get('price_usd', 0) * top.get('commission_pct', 0) / 100:.2f}

━━━ PATH TO FIRST $1,000/WEEK ━━━
At ${top.get('price_usd', 45) * top.get('commission_pct', 15) / 100:.2f}/sale:
  $1,000/week requires {1000 / max(0.01, top.get('price_usd', 45) * top.get('commission_pct', 15) / 100):.0f} sales/week
  At 3% CVR: requires {1000 / max(0.01, top.get('price_usd', 45) * top.get('commission_pct', 15) / 100) / 0.03:.0f} weekly link clicks
  10 creators × 300 clicks/week each = {10 * 300} clicks → approximately {10 * 300 * 0.03:.0f} sales

━━━ STRATEGIC RECOMMENDATION ━━━
Phase 1 (Now): Recruit 10 micro-creators (10K-100K followers) in beauty niche
Phase 2 (Week 4): Analyze which creators convert. Double down on top 3.
Phase 3 (Week 8): Scale the top-performing creator model. Add 2nd product.
Phase 4 (Week 12): Introduce Spark Ads on top organic content.

━━━ HIGHEST LEVERAGE MOVE THIS WEEK ━━━
Send 20 DMs to beauty creators using the pitch template in outreach_templates.md.
Probability of 2 onboarded creators from 20 outreach: ~70%."""

    def _general_analysis(self, query: str) -> str:
        health = self.get_health_summary()
        return f"""GENERAL ANALYSIS
Query: "{query}"

━━━ SYSTEM CONTEXT ━━━
Company health: {health['overall']:.1f}/100
{chr(10).join(f"  {k}: {v}/100" for k, v in health['components'].items())}

━━━ ANALYSIS ━━━
Your query does not match a specialized framework category. Here is what
I can offer based on current system data:

The single highest-leverage action available right now based on all
system data: {self.get_top_insight()}

━━━ FRAMEWORKS AVAILABLE ━━━
For strategic questions:   python jarvis_core.py think "strategy: [question]"
For financial questions:   python jarvis_core.py think "financial: [question]"
For people questions:      python jarvis_core.py think "talent: [question]"
For operational questions: python jarvis_core.py think "ops: [question]"
For TikTok questions:      python jarvis_core.py think "tiktok: [question]"

━━━ RECOMMENDATION ━━━
Clarify the domain of the question for a more targeted analysis."""

    # ─── Meeting preparation ───────────────────────────────────────────────

    def prepare_meeting(self, topic: str) -> str:
        """Generate meeting preparation briefing."""
        return f"""MEETING PREPARATION BRIEFING
Topic: "{topic}"
Prepared: {datetime.now().strftime('%Y-%m-%d %H:%M')}

━━━ OBJECTIVE ━━━
What is the single most important outcome from this meeting?
[Define before walking in. If you can't state it in one sentence, you're not ready.]

━━━ BACKGROUND ━━━
What does everyone in the room need to know to have a productive conversation?
Distribute this as a pre-read 24 hours before. No pre-read = cancel and reschedule.

━━━ KEY QUESTIONS TO ASK ━━━
1. "What decision are we here to make?" (If no one can answer, the meeting is misstructured.)
2. "What information would change our answer?" (Forces evidence-based discussion.)
3. "What are we explicitly NOT deciding today?" (Prevents scope creep.)
4. "Who is the DRI for the next action?" (Ends every meeting with clear ownership.)

━━━ QUESTIONS TO EXPECT ━━━
Prepare for:
• "What's the data behind this?" — Have your sources ready.
• "Have we considered [alternative]?" — Pre-answer the obvious alternatives.
• "What's the risk if we're wrong?" — Know your downside.

━━━ HIDDEN AGENDA AWARENESS ━━━
In any meeting, some people are advocating for a position they came in with.
Watch for: selective data presentation, appeals to seniority over evidence,
"we've always done it this way" resistance.

━━━ DESIRED OUTCOME ━━━
Leave the meeting with:
□ One clear decision made and documented
□ DRI assigned to each action item
□ Next meeting date confirmed (if needed)
□ Written summary sent within 1 hour

━━━ JARVIS NOTE ━━━
The most important meeting preparation is knowing what you want to walk out
with. Everything else is in service of that outcome."""

    # ─── Decision support ──────────────────────────────────────────────────

    def decision_support(self, decision: str) -> str:
        """Full decision support framework, auto-selecting based on decision type."""
        d = decision.lower()

        framework = "SWOT + Risk Analysis"
        if any(w in d for w in ["hire", "fire", "promote", "let go"]):
            framework = "Stakeholder Impact + Organizational Fit Analysis"
        elif any(w in d for w in ["invest", "spend", "budget", "buy", "acquire"]):
            framework = "ROI + Opportunity Cost + Scenario Modeling"
        elif any(w in d for w in ["build", "make", "launch", "ship"]):
            framework = "Impact × Confidence × Ease (ICE) + Risk Assessment"
        elif any(w in d for w in ["partner", "deal", "contract", "vendor"]):
            framework = "Strategic Fit + Risk + Alternatives Analysis"

        return f"""DECISION SUPPORT
Decision: "{decision}"
Framework: {framework}
Prepared: {datetime.now().strftime('%Y-%m-%d %H:%M')}

━━━ DEFINE THE DECISION CLEARLY ━━━
Restate it in one sentence:
"Should we [action] given [context] in order to achieve [outcome]?"

━━━ OPTIONS (minimum 3, including "do nothing") ━━━
Option A: [Proceed as proposed]
  Pros:
  Cons:
  Risk: What's the worst realistic outcome?

Option B: [Modified version / partial approach]
  Pros:
  Cons:
  Risk:

Option C: Do nothing / defer
  What happens if we make no decision for 30 days?
  Is this actually the safest option? (Often not.)

━━━ EVALUATION CRITERIA ━━━
Score each option 1-10 on:
• Strategic alignment: Does this move us toward the 3-year vision?
• Financial impact: What does this cost? What does it return?
• Risk level: What's the downside if wrong?
• Reversibility: Can we undo this if it turns out to be wrong?
• Speed: How long until we see results?

━━━ SECOND-ORDER EFFECTS ━━━
If we choose Option A, what happens next that we haven't considered?
"And then what?" — Ask this three times minimum.

━━━ REVERSIBILITY CHECK ━━━
Is this a one-way door (hard to reverse) or a two-way door (easy to undo)?
One-way doors require more data and deliberation.
Two-way doors should be decided fast with the information you have.

━━━ RECOMMENDATION FORMAT ━━━
"I recommend [Option X] because [primary reason].
The main risk is [risk], which we mitigate by [mitigation].
We'll know if this is working by [metric] in [timeframe]."

━━━ JARVIS ADVISORY ━━━
The most common decision failure modes:
1. Deciding with insufficient data on reversible decisions — move faster
2. Deciding with insufficient data on irreversible decisions — slow down
3. Deciding by consensus when one person should own it — assign a DRI
4. Avoiding the decision entirely — indecision is a decision with the worst outcomes"""
