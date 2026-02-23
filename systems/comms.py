"""
J.A.R.V.I.S. Communications System
-------------------------------------
Message drafting, communication intelligence, relationship CRM.

"Shall I draft a response, sir?"

Handles: executive memos, investor updates, team communications,
difficult conversations, negotiation framing, and outreach sequencing.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

COMMS_LOG_FILE = DATA_DIR / "comms_log.json"
CONTACTS_FILE  = DATA_DIR / "contacts.json"

# Cross-system
TALENT_FILE = BASE_DIR.parent / "company-os" / "data" / "talent.json"


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


class CommsSystem:
    """
    JARVIS communications engine.

    Drafts, advises, and tracks all communications.
    Maintains relationship intelligence across your network.
    Flags when important relationships are going cold.
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._log      = _load(COMMS_LOG_FILE, {"messages": []})
        self._contacts = _load(CONTACTS_FILE,  {"contacts": {}})

    def _flush(self):
        _save(COMMS_LOG_FILE, self._log)
        _save(CONTACTS_FILE,  self._contacts)

    # ─── Message drafting ──────────────────────────────────────────────────

    def draft(self, context: str, tone: str = "executive") -> str:
        """
        Draft a message given context and desired tone.
        Tones: executive | investor | team | difficult | negotiation | customer
        """
        context_lower = context.lower()

        # Auto-detect message type
        if any(w in context_lower for w in ["investor", "board", "raise", "funding", "capital"]):
            return self._draft_investor(context)
        elif any(w in context_lower for w in ["fire", "let go", "terminate", "pip", "performance"]):
            return self._draft_difficult_hr(context)
        elif any(w in context_lower for w in ["negotiate", "deal", "contract", "terms", "offer"]):
            return self._draft_negotiation(context)
        elif any(w in context_lower for w in ["customer", "client", "user", "complaint", "refund"]):
            return self._draft_customer(context)
        elif any(w in context_lower for w in ["team", "all-hands", "announce", "company-wide"]):
            return self._draft_team(context)
        elif any(w in context_lower for w in ["sorry", "apolog", "mistake", "error", "delay"]):
            return self._draft_apology(context)
        else:
            return self._draft_executive_memo(context)

    def _draft_executive_memo(self, context: str) -> str:
        return f"""EXECUTIVE MEMO
Date: {datetime.now().strftime('%B %d, %Y')}
From: [Your Name]
To:   [Recipient]
Re:   [Subject — be specific]

SITUATION
[One sentence: what is the current state of affairs?]
{context[:100]}...

COMPLICATION
[What has changed or what problem has emerged?]

RESOLUTION
[Your proposed course of action — specific, with timeline and owner]

NEXT STEP
[One concrete action with a deadline. Example: "Reply by EOD Friday to confirm."]

─────────────────────────────────────────────────
JARVIS NOTE: Lead with the ask. Busy executives read the first sentence only.
Keep total length under 200 words. Attach supporting data, don't embed it.
"""

    def _draft_investor(self, context: str) -> str:
        return f"""INVESTOR UPDATE — {datetime.now().strftime('%B %Y')}

HEADLINE: [One sentence: biggest win this month]

METRICS
  MRR:          $[X]  (+[X]% MoM)
  ARR:          $[X]
  Customers:    [X]   (+[X] net new)
  Burn:         $[X]/month
  Runway:       [X] months

WINS THIS MONTH
  ▶ [Win 1 — specific and quantified]
  ▶ [Win 2 — specific and quantified]
  ▶ [Win 3 — specific and quantified]

MISSES / LEARNING
  ▶ [What didn't go as planned and what you learned]
  Note: Investors respect honesty. Never spin a miss.

FOCUS NEXT MONTH
  ▶ [Priority 1 with measurable target]
  ▶ [Priority 2 with measurable target]

ASK (if any)
  [Be direct: intro to X, advice on Y, help with Z]

─────────────────────────────────────────────────
JARVIS NOTE: Send monthly. Never miss a month. Investors who don't hear
from you assume the worst. Include a specific ask — it keeps them engaged.
Context provided: {context[:80]}
"""

    def _draft_difficult_hr(self, context: str) -> str:
        return f"""DIFFICULT CONVERSATION FRAMEWORK
Topic: Performance / HR Matter
Context: {context[:80]}

PRE-MEETING CHECKLIST
  □ HR is informed and aligned
  □ Documentation is complete (PIPs, warnings, dates)
  □ Legal has reviewed if termination
  □ Meeting is private, in-person preferred
  □ Have tissues and water available

OPENING (do not lead with small talk)
  "I want to be direct with you because I respect you.
   This is a difficult conversation, and I want to make sure
   you have clarity on where things stand."

THE MESSAGE (be clear, do not soften to the point of confusion)
  "[Name], despite [specific support provided], [specific metric/behavior]
   has not met the bar we discussed. As a result, [decision]."

IF TERMINATION:
  "Today is your last day. You'll receive [severance details].
   [HR name] will walk you through the logistics."

AFTER
  → Do not over-explain or justify
  → Do not ask how they feel about the decision
  → Follow up in writing within 24 hours

─────────────────────────────────────────────────
JARVIS NOTE: Unclear kindness is cruelty in disguise.
Be direct. Be human. Be done.
"""

    def _draft_negotiation(self, context: str) -> str:
        return f"""NEGOTIATION BRIEF
Context: {context[:80]}

PREPARATION FRAMEWORK
  Your target:     [Best realistic outcome]
  Your BATNA:      [Best Alternative to Negotiated Agreement]
  Walk-away point: [The line you will not cross]
  Their likely BATNA: [What they do if this falls through]

OPENING POSITION
  Lead with value, not price.
  "Here's what this partnership means for both sides..."

ANCHORING
  State your number first if you have information advantage.
  Go higher than target to leave room to move.

CONCESSION STRATEGY
  Concede slowly. Each concession should get smaller.
  Never give without getting: "I can do X if you can do Y."
  Label your concessions: "That's a significant move on my part..."

CLOSING
  "If we can agree on [final term], I'm prepared to sign today."
  Create urgency without desperation.

PHRASES THAT WORK
  "Help me understand how you arrived at that number."
  "What would it take to get this done?"
  "I'm not sure I can do that, but let me see what's possible."

─────────────────────────────────────────────────
JARVIS NOTE: The party that needs the deal least has the most power.
Strengthen your BATNA before you negotiate.
"""

    def _draft_customer(self, context: str) -> str:
        return f"""CUSTOMER COMMUNICATION
Context: {context[:80]}
Date: {datetime.now().strftime('%B %d, %Y')}

Subject: [Re: specific issue they raised]

Hi [Name],

Thank you for reaching out. [Acknowledge their situation in one sentence.]

[If apologizing]: I'm sorry for [specific thing]. This should not have
happened, and I take full responsibility.

[What happened]: [Brief, honest explanation — no excuses]

[What we're doing]: [Specific actions with timeline]

[What you'll do for them]: [Make it right — concretely]

Please reply directly to this email or reach me at [direct contact].
I'll personally follow up on [specific date].

[Your name]
[Title]

─────────────────────────────────────────────────
JARVIS NOTE: Respond within 24 hours. Customers forgive mistakes.
They don't forgive silence. Escalate all refund requests over $500
to the customer success lead.
"""

    def _draft_team(self, context: str) -> str:
        return f"""TEAM COMMUNICATION
Date: {datetime.now().strftime('%B %d, %Y')}
Context: {context[:80]}

Subject: [Clear headline — no vague subjects like "Update"]

Team,

[Lead with the most important thing. No preamble.]

WHAT'S HAPPENING
[2-3 sentences max. What decision was made or what is changing.]

WHY
[The real reason. People sense when they're being managed.
 Treat them as adults who can handle the truth.]

WHAT THIS MEANS FOR YOU
[Specifics. What changes? What stays the same? What do they need to do?]

QUESTIONS
[Tell them how and when they can get answers. Don't say "feel free."
 Say: "I'll host open office hours Thursday 3-4pm. Questions before then
 → Slack #general."]

[Your name]

─────────────────────────────────────────────────
JARVIS NOTE: Communicate change before the rumor mill does.
Under-communication is the #1 cause of organizational anxiety.
"""

    def _draft_apology(self, context: str) -> str:
        return f"""APOLOGY COMMUNICATION
Context: {context[:80]}

ANATOMY OF AN EFFECTIVE APOLOGY:

1. ACKNOWLEDGE (without hedging)
   "I made a mistake." NOT "Mistakes were made."
   "I let you down." NOT "There were some challenges."

2. TAKE RESPONSIBILITY
   "This was entirely my fault." [If true.]
   Never qualify with "but" — it negates the apology.

3. EXPLAIN (briefly, if helpful)
   One sentence. No excuses. Context is acceptable, excuses are not.

4. MAKE IT RIGHT
   Specific. Tangible. On a deadline.
   "I'll have [deliverable] to you by [date]."

5. PREVENT RECURRENCE
   "I've put [specific system/change] in place so this won't happen again."

WHAT NOT TO SAY:
  ✗ "I'm sorry you feel that way"
  ✗ "I'm sorry if..."
  ✗ "I was trying to..."
  ✗ Multiple paragraphs of explanation

─────────────────────────────────────────────────
JARVIS NOTE: The best apology is changed behavior.
If you can't commit to changing, don't apologize — make a plan.
"""

    # ─── Communication intelligence ────────────────────────────────────────

    def get_communication_brief(self, contact_name: str) -> str:
        """Brief on a contact before a meeting or call."""
        contact = self._contacts.get("contacts", {}).get(contact_name, {})
        if not contact:
            return (
                f"No record for '{contact_name}' in the system, sir.\n"
                f"Recommend: search LinkedIn, mutual connections, and recent news before the call.\n"
                f"Run: jarvis think \"research [contact_name]\" for a preparation framework."
            )

        last_contact = contact.get("last_contact", "never")
        notes = contact.get("notes", [])
        last_note = notes[-1].get("note", "none") if notes else "none"

        return (
            f"CONTACT BRIEF: {contact_name}\n"
            f"  Last contact:    {last_contact[:10] if last_contact != 'never' else 'never'}\n"
            f"  Relationship:    {contact.get('relationship_strength', 5)}/10\n"
            f"  They care about: {', '.join(contact.get('what_they_care_about', ['unknown']))}\n"
            f"  You owe them:    {', '.join(contact.get('what_you_owe_them', ['nothing']))}\n"
            f"  Last note:       {last_note[:80]}\n"
        )

    def log_outreach(self, recipient: str, channel: str, subject: str, outcome: str = ""):
        entry = {
            "recipient": recipient,
            "channel": channel,
            "subject": subject,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat(),
        }
        self._log["messages"].append(entry)
        self._flush()

    def get_pending_followups(self) -> list:
        """Return outreach items that haven't had a reply logged."""
        pending = []
        cutoff  = (datetime.now() - timedelta(days=7)).isoformat()
        for msg in self._log.get("messages", []):
            if not msg.get("outcome") and msg.get("timestamp", "") > cutoff:
                days_ago = (datetime.now() - datetime.fromisoformat(msg["timestamp"])).days
                pending.append({**msg, "days_ago": days_ago})
        return sorted(pending, key=lambda x: x.get("days_ago", 0), reverse=True)

    # ─── Communication audit ───────────────────────────────────────────────

    def get_comms_audit(self) -> str:
        """Weekly communications health check."""
        pending    = self.get_pending_followups()
        total_sent = len(self._log.get("messages", []))

        lines = [
            f"COMMUNICATIONS AUDIT — {datetime.now().strftime('%B %d, %Y')}",
            "",
            f"  Total messages logged:  {total_sent}",
            f"  Pending follow-ups:     {len(pending)}",
            "",
        ]

        if pending:
            lines.append("  PENDING FOLLOW-UPS (no reply logged):")
            for f in pending[:5]:
                lines.append(f"  ▶  {f.get('recipient', '?')} | {f.get('subject', '?')[:40]} ({f['days_ago']}d ago)")
            lines.append("")

        lines.append(
            "  RECOMMENDATION: Reply to all pending items within 24 hours.\n"
            "  Unanswered messages signal unreliability."
        )

        return "\n".join(lines)

    def is_online(self) -> bool:
        return True
