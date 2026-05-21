import os
import re
from dotenv import load_dotenv

load_dotenv()

# Central config variables
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")

# Shared memory database
MEMORIES = {
    "sarah": [
        "Call Jan 15: Sarah mentioned Q3 budget freeze initially blocking deal. Needs CFO approval from James Lee.",
        "Call Feb 3: $200K budget officially approved. June 30 go-live deadline is NON-NEGOTIABLE.",
        "Email Feb 20: Sarah raised Salesforce integration as a blocker. HubSpot migration risk.",
        "Call March 5: COMPETITIVE THREAT -- Gong.io pitching at $165K vs our $200K proposal.",
        "Internal note March 10: James Lee attending next demo. Needs ROI one-pager."
    ],
    "mark": [
        "Intro call Feb 28: Mark is CEO of TechStart (18-person SaaS). No formal sales process.",
        "Call March 8: Budget tight -- $45K upper limit. Needs ROI within 60 days.",
        "Demo March 14: Mark loved Before/After email comparison."
    ],
    "priya": [
        "First contact Feb 10: Priya is Head of Ops at GlobalEdge.",
        "Call March 1: $85K approved. Main concern: GDPR compliance for EU clients.",
        "Call March 18: Proposal sent. Legal reviewing data retention limits (max 24 months)."
    ]
}


def prospect_id(name: str) -> str:
    """Generate a clean prospect ID."""
    clean = re.sub(r"[^a-z0-9_]", "", name.lower().replace(" ", "_"))
    return f"dealmind_{clean}"


def get_memories(prospect_name: str, query: str = "overview") -> str:
    """Retrieve formatted memory context for a prospect."""
    memories = MEMORIES.get(
        prospect_name.lower().strip(),
        ["No previous records found."]
    )

    formatted = [
        f"{idx}. {memory}"
        for idx, memory in enumerate(memories, start=1)
    ]

    return "REMEMBERED CONTEXT:\n" + "\n".join(formatted)


def store_memory(prospect_name: str, user_msg: str, ai_response: str) -> bool:
    """
    Placeholder memory storage function.
    Replace with database or API logic if needed.
    """
    return True


def get_memories_list(prospect_name: str) -> list:
    """Return raw memory list for a prospect."""
    return MEMORIES.get(
        prospect_name.lower().strip(),
        []
    )


# CascadeFlow Routing Logic
COMPLEX_KEYWORDS = [
    "strategy",
    "negotiat",
    "proposal",
    "objection",
    "competitor",
    "pricing",
    "contract",
    "close",
    "discount",
    "legal",
    "compliance",
    "budget",
    "timeline",
    "deadline",
    "decision",
    "authority"
]


def route_query(message: str) -> dict:
    """
    Route requests to the appropriate model based on
    complexity and keyword analysis.
    """
    word_count = len(message.split())

    has_complex_keyword = any(
        keyword in message.lower()
        for keyword in COMPLEX_KEYWORDS
    )

    is_complex = word_count > 35 or has_complex_keyword

    if is_complex:
        return {
            "model": "llama-3.3-70b-versatile",
            "cost": 0.008,
            "reason": f"Complex query ({word_count} words) -- premium model",
            "is_complex": True
        }

    return {
        "model": "llama-3.1-8b-instant",
        "cost": 0.001,
        "reason": f"Simple query ({word_count} words) -- efficient model",
        "is_complex": False
    }
