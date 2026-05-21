import os
import re
from dotenv import load_dotenv

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")

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
    clean = re.sub(r"[^a-z0-9_]", "", name.lower().replace(" ", "_"))
    return f"dealmind_{clean}"


def get_memories(prospect_name: str, query: str = "overview") -> str:
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
    prospect = prospect_name.lower().strip()

    if prospect not in MEMORIES:
        MEMORIES[prospect] = []

    short_memory = (
        f"User asked: {user_msg[:60]} | "
        f"AI replied: {ai_response[:80]}"
    )

    MEMORIES[prospect].append(short_memory)

    if len(MEMORIES[prospect]) > 10:
        MEMORIES[prospect] = MEMORIES[prospect][-10:]

    return True


def get_memories_list(prospect_name: str) -> list:
    return MEMORIES.get(
        prospect_name.lower().strip(),
        []
    )


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
    word_count = len(message.split())

    has_complex_keyword = any(
        keyword in message.lower()
        for keyword in COMPLEX_KEYWORDS
    )

    is_complex = (
        word_count > 35
        or has_complex_keyword
    )

    if is_complex:
        return {
            "model": "llama-3.3-70b-versatile",
            "cost": 0.008,
            "reason": f"Complex query ({word_count} words) - premium model",
            "is_complex": True
        }

    return {
        "model": "llama-3.1-8b-instant",
        "cost": 0.001,
        "reason": f"Simple query ({word_count} words) - efficient model",
        "is_complex": False
    }
    GROQ_API_KEY = st.secrets.get(
    "GROQ_API_KEY",
    os.getenv("GROQ_API_KEY", "")
)
    if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
messages = [
    {
        "role": "system",
        "content": system_prompt
    }
]

for msg in st.session_state["chat_history"][-6:]:
    messages.append(
        {
            "role": msg["role"],
            "content": msg["content"]
        }
    )

response = client.chat.completions.create(
    model=route["model"],
    messages=messages,
    max_tokens=300,
    temperature=0.7
)

ai_reply = response.choices[0].message.content
