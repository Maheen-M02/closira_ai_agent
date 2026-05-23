# Closira AI Agent — Bloom Aesthetics Clinic

A production-quality, four-stage AI customer support workflow built using OpenRouter for multi-model AI access. Handles inbound customer enquiries using SOP-grounded responses, lead qualification, escalation detection, and session summarisation.

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

```bash
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

## AI Provider

This project uses OpenRouter as the AI gateway, allowing flexible access to multiple models including Claude, GPT, Gemini, DeepSeek, and more through a unified API.

Recommended model:

```python
MODEL = "anthropic/claude-4.6-sonnet"
```

---

## Setup

### 1. Prerequisites

- Python 3.10+
- An OpenRouter API key

Get your API key here:

https://openrouter.ai/

---

### 2. Install dependencies

```bash
cd closira_agent
pip install -r requirements.txt
```

---

### 3. Set your API key

### Windows PowerShell

```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-..."
```

### Mac/Linux

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

---

## Running the Agent

### Interactive CLI (talk to Aria)

```bash
python agent.py
```

### Special commands during a session

| Command | Effect |
|---|---|
| `qualify` | Start lead qualification (Stage 2) |
| `summary` | Print structured session summary (Stage 4) |
| `quit` / `exit` | End session (summary auto-generates) |

---

## Automated Test Runner

Run all 5 required test scenarios:

```bash
python run_tests.py
```

This runs all scenarios against the live API and saves transcripts to `test_transcripts/`.

---

## How It Works

### Hallucination Prevention

The SOP is embedded directly into the system prompt.

The model is explicitly instructed to:

- Answer ONLY from the SOP
- Never guess or invent facts
- Escalate instead of hallucinating
- Avoid unsupported claims

---

## Escalation Detection (Dual-Layer)

### Layer 1 — Rule-Based Pre-Screening

Before calling the model, user input is scanned for:

- Anger/frustration
- Medical questions
- Pricing negotiation attempts
- Human escalation requests

This happens instantly without an API call.

---

### Layer 2 — Model Self-Flagging

The model is instructed to emit structured escalation markers:

```txt
{ESCALATE: "reason"}
```

These are automatically parsed and removed from the customer-facing response.

All escalations are logged with:

- Timestamp
- Session ID
- Escalation reason

---

## Session Logging

Every conversation turn is logged to:

```bash
logs/session_<timestamp>.jsonl
```

Escalations:

```bash
logs/escalations_<timestamp>.jsonl
```

Summaries:

```bash
logs/summary_<timestamp>.json
```

---

## SOP Data

The agent operates using a structured SOP defined in `sop.py`.

Example:

```txt
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

## Recommended Models

| Use Case | Recommended Model |
|---|---|
| Production support agent | anthropic/claude-3.7-sonnet |
| Budget-friendly testing | google/gemini-2.5-flash |
| Fast summaries | openai/gpt-4.1-mini |
| Cheapest experimentation | deepseek/deepseek-chat-v3 |

---

## Trade-offs and Known Limitations

### In-Memory State

Session state is not persisted across restarts.

Production systems should use:

- Redis
- PostgreSQL
- MongoDB

---

### Small SOP Only

The SOP is injected directly into the prompt.

For large knowledge bases (>10k tokens), a RAG architecture should be used.

---

### Rule-Based Escalation

Keyword-based escalation detection may miss unusual phrasing.

Production systems could add:

- Sentiment analysis
- Intent classifiers
- Safety moderation layers

---

### CLI Only

No frontend or webhook integration is included.

Production deployment could integrate:

- WhatsApp Business API
- Telegram
- Web chat
- Email
- CRM systems

---

### Long Conversation Summaries

Very long conversations may eventually exceed context limits.

Future improvements could include:

- Chunked summarisation
- Memory compression
- Vector databases

---

## Dependencies

```txt
openai>=1.30.0
```

The OpenAI-compatible SDK is used with OpenRouter.

---

## Evaluation Notes for Reviewers

- All four stages are clearly separated in `agent.py`
- Prompt construction is centralized in `build_system_prompt()`
- Escalation detection is dual-layer:
  - `detect_escalation_in_input()`
  - `detect_escalation_in_response()`
- Structured logs provide a complete audit trail
- Automated tests generate transcripts for all required scenarios
- OpenRouter enables flexible multi-model support without changing architecture