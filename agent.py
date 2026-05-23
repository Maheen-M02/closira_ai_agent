"""
Closira AI Customer Support Agent
==================================
A four-stage AI workflow for Bloom Aesthetics Clinic:
  Stage 1 — FAQ Answering (SOP-grounded)
  Stage 2 — Lead Qualification
  Stage 3 — Escalation Detection
  Stage 4 — Conversation Summary

Run: python agent.py
"""

import os
import json
import datetime
import re
from typing import Optional
from openai import OpenAI
from sop import SOP_DATA, SOP_TEXT
from logger import ConversationLogger

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────

MODEL = "anthropic/claude-4.6-sonnet"
MAX_TOKENS = 1024

QUALIFICATION_QUESTIONS = [
    "Could you tell me what type of business or role you're enquiring for? (e.g., personal, clinic partner, influencer)",
    "Roughly how many treatments or bookings would you be looking at per month?",
    "Are you currently using any booking or CRM tools, or would this be your first time?",
]

# ──────────────────────────────────────────────
# System Prompt
# ──────────────────────────────────────────────

def build_system_prompt() -> str:
    return f"""You are Aria, a warm and professional AI customer support assistant for Bloom Aesthetics Clinic.

Your job is to help customers with enquiries, qualify leads, and provide accurate information — always based ONLY on the clinic's Standard Operating Procedures (SOP) below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLINIC SOP (your only source of truth)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{SOP_TEXT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES — YOU MUST FOLLOW THESE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HALLUCINATION PREVENTION
   - Answer ONLY from the SOP above. Never invent prices, services, policies, or any facts.
   - If a customer asks something not covered in the SOP, do NOT guess. Say you'll escalate.
   - Do not say "I think", "probably", or "I believe" about factual matters — only cite what the SOP says.

2. ESCALATION (CRITICAL)
   You MUST output a special JSON escalation marker — on its own line — whenever ANY of the following occur:
   - Customer expresses anger, frustration, or dissatisfaction
   - Customer has a medical question (side effects, contraindications, allergies, etc.)
   - Customer asks to negotiate pricing
   - Customer explicitly asks to speak to a human
   - You are asked > 2 questions you cannot answer from the SOP
   - You have low confidence in your answer

   Escalation format (output this EXACTLY, on its own line, before your human-readable reply):
   {{ESCALATE: "<reason>"}}

   Example: {{ESCALATE: "Customer expressed frustration about a past appointment"}}

3. CONFIDENCE TRACKING
   Internally track how many questions you have been unable to answer from the SOP.
   If this count exceeds 2, escalate immediately.

4. TONE & PERSONA
   - Warm, empathetic, professional — like a knowledgeable front-desk receptionist.
   - Keep responses concise (2–4 sentences for simple questions).
   - Use the customer's name if known.
   - Never be robotic or over-formal. Never be overly casual.
   - Always end with a helpful follow-up offer when appropriate.

5. FORMATTING
   - Do NOT use markdown headers or bullet lists in customer-facing replies.
   - Output the escalation JSON marker only — never explain the JSON to the customer.
   - Your human-readable reply goes after the JSON marker (if present).

You are now ready to assist customers."""


# ──────────────────────────────────────────────
# Escalation Detector
# ──────────────────────────────────────────────

def detect_escalation_in_response(response_text: str) -> tuple[bool, str, str]:
    """
    Parses the model response for escalation markers.
    Returns (should_escalate, reason, clean_reply)
    """
    pattern = r'\{ESCALATE:\s*"([^"]+)"\}'
    match = re.search(pattern, response_text)
    if match:
        reason = match.group(1)
        clean_reply = re.sub(pattern, "", response_text).strip()
        return True, reason, clean_reply
    return False, "", response_text.strip()


def detect_escalation_in_input(user_input: str) -> tuple[bool, str]:
    """
    Pre-screen the user's raw input for obvious escalation triggers
    before even calling the model.
    """
    lower = user_input.lower()

    anger_keywords = [
        "angry", "furious", "terrible", "awful", "disgusting", "unacceptable",
        "disgusted", "outraged", "ridiculous", "horrible", "worst", "hate",
        "useless", "incompetent", "scam", "fraud", "lawsuit", "sue",
        "i want to complain", "this is a joke"
    ]
    human_keywords = [
        "speak to a human", "speak to someone", "talk to a person",
        "real person", "human agent", "manager", "supervisor",
        "escalate", "i want to talk to"
    ]
    medical_keywords = [
        "side effect", "allergy", "allergic", "contraindication", "reaction",
        "medical", "doctor", "prescription", "safe for", "pregnant", "breastfeed",
        "medication", "drug interaction", "blood thinner"
    ]
    pricing_keywords = [
        "can you do better", "discount", "negotiate", "cheaper", "reduce the price",
        "lower the price", "best price", "deal", "offer me"
    ]

    for kw in anger_keywords:
        if kw in lower:
            return True, f"Anger/frustration detected in customer message: '{kw}'"
    for kw in human_keywords:
        if kw in lower:
            return True, f"Customer explicitly requested human agent: '{kw}'"
    for kw in medical_keywords:
        if kw in lower:
            return True, f"Medical question detected: '{kw}'"
    for kw in pricing_keywords:
        if kw in lower:
            return True, f"Pricing negotiation attempt detected: '{kw}'"

    return False, ""


# ──────────────────────────────────────────────
# Lead Qualification
# ──────────────────────────────────────────────

class LeadQualifier:
    def __init__(self):
        self.answers: dict[str, str] = {}
        self.current_q_index: int = 0
        self.complete: bool = False

    def next_question(self) -> Optional[str]:
        if self.current_q_index < len(QUALIFICATION_QUESTIONS):
            return QUALIFICATION_QUESTIONS[self.current_q_index]
        self.complete = True
        return None

    def record_answer(self, question: str, answer: str):
        self.answers[question] = answer
        self.current_q_index += 1
        if self.current_q_index >= len(QUALIFICATION_QUESTIONS):
            self.complete = True

    def summary(self) -> dict:
        return {
            "qualification_complete": self.complete,
            "responses": self.answers,
        }


# ──────────────────────────────────────────────
# Conversation Summary Generator
# ──────────────────────────────────────────────

def generate_summary(client, conversation_history: list, lead_data: dict, escalated: bool, escalation_reason: str) -> dict:
    history_text = "\n".join(
        f"{'Customer' if m['role'] == 'user' else 'Aria'}: {m['content']}"
        for m in conversation_history
        if isinstance(m.get("content"), str)
    )

    prompt = f"""You are a summarisation assistant. Analyse the following customer support conversation and produce a structured JSON summary.

CONVERSATION:
{history_text}

LEAD QUALIFICATION DATA:
{json.dumps(lead_data, indent=2)}

ESCALATION STATUS: {"ESCALATED — Reason: " + escalation_reason if escalated else "Not escalated"}

Return ONLY valid JSON (no markdown, no preamble) with these exact keys:
{{
  "customer_intent": "One sentence describing what the customer wanted",
  "key_details_collected": ["list", "of", "key facts"],
  "sop_gaps_identified": ["Questions the SOP couldn't answer, or empty list"],
  "lead_qualification_summary": "Brief paragraph on the lead quality and collected info",
  "escalated": true or false,
  "escalation_reason": "reason or null",
  "recommended_next_action": "What the human team should do next",
  "session_timestamp": "{datetime.datetime.now().isoformat()}"
}}"""

    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=MAX_TOKENS,
)

    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if present
    raw = re.sub(r"^```json\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_summary": raw, "parse_error": True}


# ──────────────────────────────────────────────
# Main Agent
# ──────────────────────────────────────────────

class ClosiraAgent:
    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        if not api_key:
            raise EnvironmentError("OPENROUTER_API_KEY environment variable not set.")
       
        self.conversation_history: list = []
        self.lead_qualifier = LeadQualifier()
        self.logger = ConversationLogger()
        self.escalated = False
        self.escalation_reason = ""
        self.unanswered_count = 0
        self.qualifying_mode = False
        self.current_qualification_question: Optional[str] = None

    # ── Internal helpers ──

    def _add_user(self, text: str):
        self.conversation_history.append({"role": "user", "content": text})

    def _add_assistant(self, text: str):
        self.conversation_history.append({"role": "assistant", "content": text})
    def _call_model(self) -> str:
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
            {
                "role": "system",
                "content": build_system_prompt()
            },
            *self.conversation_history
        ],
        max_tokens=MAX_TOKENS,
    )
        return response.choices[0].message.content.strip()

    def _handle_escalation(self, reason: str) -> str:
        self.escalated = True
        self.escalation_reason = reason
        self.logger.log_escalation(reason)
        return (
            f"I completely understand, and I want to make sure you get the best help possible. "
            f"I'm connecting you with one of our team members right now who will be able to assist you further. "
            f"Please bear with us — someone will be in touch very shortly. 💙"
        )

    # ── Stage routing ──

    def respond(self, user_input: str) -> str:
        """Main entry point. Routes input through the four-stage pipeline."""

        self.logger.log_turn("user", user_input)

        # ── STAGE 3: Pre-screen for escalation triggers ──
        should_escalate, reason = detect_escalation_in_input(user_input)
        if should_escalate and not self.escalated:
            self._add_user(user_input)
            reply = self._handle_escalation(reason)
            self._add_assistant(reply)
            self.logger.log_turn("assistant", reply)
            return reply

        # ── STAGE 2: Lead qualification mode ──
        if self.qualifying_mode and self.current_qualification_question:
            self.lead_qualifier.record_answer(self.current_qualification_question, user_input)
            self._add_user(user_input)

            next_q = self.lead_qualifier.next_question()
            if next_q:
                self.current_qualification_question = next_q
                self._add_assistant(next_q)
                self.logger.log_turn("assistant", next_q)
                return next_q
            else:
                self.qualifying_mode = False
                self.current_qualification_question = None
                summary_msg = (
                    "Thank you so much — that's everything I need! "
                    "I've noted your details and a member of our team will be in touch to discuss next steps. "
                    "Is there anything else I can help you with in the meantime?"
                )
                self._add_assistant(summary_msg)
                self.logger.log_turn("assistant", summary_msg)
                return summary_msg

        # ── STAGE 1 & 3: Normal FAQ answering with model ──
        self._add_user(user_input)
        raw_reply = self._call_model()

        # Check if model flagged an escalation
        should_escalate_model, model_reason, clean_reply = detect_escalation_in_response(raw_reply)

        if should_escalate_model and not self.escalated:
            self._add_assistant(clean_reply)  # log clean reply first
            escalation_reply = self._handle_escalation(model_reason)
            final_reply = (clean_reply + "\n\n" + escalation_reply).strip() if clean_reply else escalation_reply
            self.logger.log_turn("assistant", final_reply)
            return final_reply

        self._add_assistant(clean_reply)
        self.logger.log_turn("assistant", clean_reply)
        return clean_reply

    def start_qualification(self) -> str:
        """Kick off Stage 2 — Lead Qualification."""
        self.qualifying_mode = True
        intro = (
            "I'd love to find out a bit more about you so we can tailor our service perfectly. "
            "I have just a few quick questions — it'll only take a moment!"
        )
        first_q = self.lead_qualifier.next_question()
        self.current_qualification_question = first_q
        full_msg = f"{intro}\n\n{first_q}"
        self._add_assistant(full_msg)
        self.logger.log_turn("assistant", full_msg)
        return full_msg

    def end_session(self) -> dict:
        """Stage 4 — Generate structured conversation summary."""
        summary = generate_summary(
            self.client,
            self.conversation_history,
            self.lead_qualifier.summary(),
            self.escalated,
            self.escalation_reason,
        )
        self.logger.log_summary(summary)
        return summary


# ──────────────────────────────────────────────
# CLI Runner
# ──────────────────────────────────────────────

def print_banner():
    print("\n" + "═" * 60)
    print("  🌸  Bloom Aesthetics Clinic — AI Support (Aria)")
    print("  Powered by Closira")
    print("═" * 60)
    print("  Type 'qualify' to start lead qualification")
    print("  Type 'summary' to see the session summary")
    print("  Type 'quit' or 'exit' to end the session")
    print("═" * 60 + "\n")


def main():
    print_banner()
    agent = ClosiraAgent()

    greeting = (
        "Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. 😊 "
        "How can I help you today?"
    )
    print(f"Aria: {greeting}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n[Session interrupted]")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("\nAria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a wonderful day! 🌸")
            break

        if user_input.lower() == "qualify":
            reply = agent.start_qualification()
            print(f"\nAria: {reply}\n")
            continue

        if user_input.lower() == "summary":
            print("\n[Generating session summary...]\n")
            summary = agent.end_session()
            print(json.dumps(summary, indent=2))
            print()
            continue

        reply = agent.respond(user_input)
        print(f"\nAria: {reply}\n")

    # Auto-generate summary at end
    print("\n" + "─" * 60)
    print("Session ended. Generating summary...")
    print("─" * 60 + "\n")
    summary = agent.end_session()
    print(json.dumps(summary, indent=2))
    print()


if __name__ == "__main__":
    main()
