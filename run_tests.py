"""
Test Runner — Closira Agent
============================
Automatically runs all 5 required test scenarios and saves transcripts.
No manual input needed. Uses the live Anthropic API.

Run: python run_tests.py
"""

import os
import sys
import json
import time


sys.path.insert(0, os.path.dirname(__file__))

from agent import ClosiraAgent, generate_summary

TRANSCRIPT_DIR = os.path.join(os.path.dirname(__file__), "test_transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def save_transcript(filename: str, lines: list[str]):
    path = os.path.join(TRANSCRIPT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ Saved: {filename}")


def run_scenario(name: str, filename: str, turns: list[str], *, qualify: bool = False) -> list[str]:
    """
    Runs a single scenario. `turns` is a list of user messages.
    Returns the full transcript as a list of lines.
    """
    print(f"\n{'═' * 55}")
    print(f"  SCENARIO: {name}")
    print(f"{'═' * 55}")

    agent = ClosiraAgent()
    transcript = [
        f"# Test Scenario: {name}",
        f"# File: {filename}",
        "",
        "Aria: Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. How can I help you today?",
        "",
    ]

    if qualify:
        
        print("  [Starting qualification mode]")
        reply = agent.start_qualification()
        print(f"  Aria: {reply}")
        transcript.append(f"Aria: {reply}")
        transcript.append("")

    for user_msg in turns:
        print(f"  You:  {user_msg}")
        transcript.append(f"You: {user_msg}")

        if qualify and agent.qualifying_mode:
            
            pass

        reply = agent.respond(user_msg)
        print(f"  Aria: {reply}")
        transcript.append(f"Aria: {reply}")
        transcript.append("")

        time.sleep(0.4) 

    
    summary = agent.end_session()
    transcript.append("─" * 55)
    transcript.append("SESSION SUMMARY (JSON)")
    transcript.append("─" * 55)
    transcript.append(json.dumps(summary, indent=2))

    return transcript




def scenario_1_in_sop():
    """In-SOP question — Botox pricing"""
    turns = [
        "What are your Botox prices?",
        "And how long does a session take?",
        "Do I need to pay a deposit to book?",
    ]
    lines = run_scenario(
        "1 — In-SOP Question (Botox Pricing)",
        "01_in_sop_question.md",
        turns,
    )
    save_transcript("01_in_sop_question.md", lines)


def scenario_2_out_of_scope():
    """Out-of-scope question — AI must escalate rather than guess"""
    turns = [
        "Do you offer laser hair removal?",
        "What about chemical peels?",
        "Can I get a teeth whitening treatment at your clinic?",
    ]
    lines = run_scenario(
        "2 — Out-of-Scope Question (Service Not in SOP)",
        "02_out_of_scope.md",
        turns,
    )
    save_transcript("02_out_of_scope.md", lines)


def scenario_3_escalation_trigger():
    """Escalation trigger — angry/frustrated customer"""
    turns = [
        "I booked an appointment last week and nobody showed up. This is absolutely unacceptable.",
        "I want to speak to a manager right now.",
    ]
    lines = run_scenario(
        "3 — Escalation Trigger (Complaint + Human Request)",
        "03_escalation_trigger.md",
        turns,
    )
    save_transcript("03_escalation_trigger.md", lines)


def scenario_4_lead_qualification():
    """Lead qualification — 3 structured questions"""
    
    turns = [
        "It's for personal use — I'm interested in Botox for myself.",
        "Maybe 1–2 treatments per year.",
        "I don't use any booking tools currently, I usually just call or WhatsApp.",
    ]
    lines = run_scenario(
        "4 — Lead Qualification",
        "04_lead_qualification.md",
        turns,
        qualify=True,
    )
    save_transcript("04_lead_qualification.md", lines)


def scenario_5_conversation_summary():
    """Full mixed conversation to produce a clean session summary"""
    turns = [
        "Hi, I'm interested in getting fillers. What are your prices?",
        "Is the initial consultation free?",
        "Great! How do I book?",
        "What's your cancellation policy?",
    ]
    lines = run_scenario(
        "5 — Conversation Summary",
        "05_conversation_summary.md",
        turns,
    )
    save_transcript("05_conversation_summary.md", lines)





def main():
    print("\n" + "═" * 55)
    print("  🌸  Closira Agent — Automated Test Runner")
    print("═" * 55)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ ANTHROPIC_API_KEY not set. Please export it first.\n")
        sys.exit(1)

    scenario_1_in_sop()
    scenario_2_out_of_scope()
    scenario_3_escalation_trigger()
    scenario_4_lead_qualification()
    scenario_5_conversation_summary()

    print("\n" + "═" * 55)
    print("  ✅  All 5 scenarios complete!")
    print(f"  📁  Transcripts saved to: test_transcripts/")
    print("═" * 55 + "\n")


if __name__ == "__main__":
    main()
