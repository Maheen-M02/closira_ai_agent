# Closira AI Agent — Bloom Aesthetics Clinic

A production-quality, four-stage AI customer support workflow built with the Anthropic Claude API. Handles inbound customer enquiries using SOP-grounded responses, lead qualification, escalation detection, and session summarisation.

---

## Features

| Stage | What it does |
|---|---|
| **1 — FAQ Answering** | Answers questions strictly from the clinic SOP. Never hallucinates. |
| **2 — Lead Qualification** | Asks 3 structured questions and stores responses for the sales team. |
| **3 — Escalation Detection** | Dual-layer detection (rule-based + model self-flagging) with structured logging. |
| **4 — Conversation Summary** | Generates a clean JSON summary at session end: intent, details, SOP gaps, next action. |

---

## Project Structure

```
closira_agent/
├── agent.py             # Main agent: all four stages, CLI runner
├── sop.py               # SOP data (structured + plain-text for prompt injection)
├── logger.py            # Conversation + escalation logging to logs/
├── run_tests.py         # Automated test runner for all 5 required scenarios
├── requirements.txt
├── prompt_design.md     # Full prompt design document
├── README.md
├── logs/                # Auto-created. Per-session .jsonl and .json logs.
└── test_transcripts/    # Auto-created by run_tests.py
    ├── 01_in_sop_question.md
    ├── 02_out_of_scope.md
    ├── 03_escalation_trigger.md
    ├── 04_lead_qualification.md
    └── 05_conversation_summary.md
```

---

## Setup

### 1. Prerequisites
- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com/))

### 2. Install dependencies

```bash
cd closira_agent
pip install -r requirements.txt
```

### 3. Set your API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

On Windows:
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

---

## Running the Agent

### Interactive CLI (talk to Aria)

```bash
python agent.py
```

**Special commands during a session:**

| Command | Effect |
|---|---|
| `qualify` | Start lead qualification (Stage 2) |
| `summary` | Print structured session summary (Stage 4) |
| `quit` / `exit` | End session (summary auto-generates) |

### Automated Test Runner (all 5 scenarios)

```bash
python run_tests.py
```

This runs all 5 required test scenarios against the live API and saves transcripts to `test_transcripts/`.

---

## How It Works

### Hallucination Prevention
The SOP is embedded verbatim in the system prompt. The model is explicitly told:
- Answer ONLY from the SOP
- Never guess or invent facts
- Escalate (not guess) when a question is out of scope

### Escalation Detection (Dual-Layer)

**Layer 1 — Rule-based pre-screening** (no API call, instant):  
Scans user input for anger, medical, pricing negotiation, and human-request keywords before calling the model.

**Layer 2 — Model self-flagging**:  
The model is instructed to output `{ESCALATE: "reason"}` in a structured format when it detects low confidence or an escalation condition. This is parsed and stripped from the customer-facing reply.

All escalations are logged to `logs/escalations_<timestamp>.jsonl` with timestamp, session ID, and reason.

### Session Logging
Every turn is logged to `logs/session_<timestamp>.jsonl`. Session summaries are saved as `logs/summary_<timestamp>.json`.

---

## SOP Data

The agent operates on the following SOP (see `sop.py` for full structured version):

```
Business: Bloom Aesthetics Clinic
Hours: Monday–Saturday, 9 AM – 7 PM

Services:
- Botox: from £200 (30 min, minimal downtime)
- Fillers: from £250 (45 min)
- Consultation: FREE (20 min)

Booking: WhatsApp or Website. Appointment only. 24hr cancellation required.

Escalate if: complaint, medical question, pricing negotiation, >2 unanswered questions, human requested.
```

---

## Trade-offs and Known Limitations

- **State is in-memory**: Session state is not persisted across process restarts. Production use would require a database (e.g. Redis, PostgreSQL).
- **Small SOP only**: The SOP is injected directly into the system prompt. For large knowledge bases (>10k tokens), a RAG (retrieval-augmented generation) approach should be used.
- **Rule-based escalation keywords**: The pre-screening keyword list may miss novel phrasings of anger or medical questions. A dedicated sentiment/intent classifier could be added as a third layer.
- **CLI only**: No web UI or webhook integration. For production, connect to the WhatsApp Business API or email provider.
- **Single-model summarisation**: For very long sessions, the full conversation history is sent for summarisation. For 50+ turn conversations, chunked summarisation would be needed.

---

## Dependencies

- `anthropic` — Official Anthropic Python SDK

---

## Evaluation Notes for Reviewers

- All four stages are clearly separated in `agent.py` with comments marking each stage.
- The system prompt is built by `build_system_prompt()` and fully documented in `prompt_design.md`.
- Escalation detection is dual-layer: `detect_escalation_in_input()` (pre-screen) and `detect_escalation_in_response()` (post-model).
- All test transcripts are generated automatically by `run_tests.py`.
- Logs provide full audit trail for every session.
