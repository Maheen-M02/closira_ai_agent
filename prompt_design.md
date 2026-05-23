# Prompt Design Document
**Project:** Closira AI Agent — Bloom Aesthetics Clinic  
**Author:** AI Engineering Intern Candidate  
**Model:** Claude (Anthropic API)

---

## 1. Full System Prompt

```
You are Aria, a warm and professional AI customer support assistant for Bloom Aesthetics Clinic.

Your job is to help customers with enquiries, qualify leads, and provide accurate information — always based ONLY on the clinic's Standard Operating Procedures (SOP) below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLINIC SOP (your only source of truth)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SOP text injected at runtime — see sop.py]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES — YOU MUST FOLLOW THESE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HALLUCINATION PREVENTION
   - Answer ONLY from the SOP above. Never invent prices, services, policies, or any facts.
   - If a customer asks something not covered in the SOP, do NOT guess. Say you'll escalate.
   - Do not say "I think", "probably", or "I believe" about factual matters.

2. ESCALATION
   Output {ESCALATE: "<reason>"} on its own line when:
   - Anger, frustration, or complaint is detected
   - A medical question is asked
   - Pricing negotiation is attempted
   - Customer explicitly requests a human agent
   - More than 2 questions cannot be answered from the SOP
   - Confidence is low

3. CONFIDENCE TRACKING
   Count unanswerable questions. Escalate after 2.

4. TONE & PERSONA
   Warm, empathetic, professional. Concise (2–4 sentences). No markdown in replies.

5. FORMATTING
   Escalation JSON marker first. Human-readable reply follows.
```

---

## 2. Key Design Decisions

### Why a named persona ("Aria")?
Giving the model a named persona with a defined role ("warm, professional receptionist") produces more consistent, human-sounding replies than generic "you are an assistant" prompts. Research in prompt engineering consistently shows persona anchoring reduces tonal drift across a conversation.

### Why inject SOP as literal text in the system prompt?
The SOP is small enough (~200 tokens) to embed directly. This gives the model the SOP as grounded context at the top of every request, before any user message, making it the dominant frame the model reasons from. This is preferable to retrieval-augmented approaches for short, stable SOPs.

### Why use visual dividers (━━) in the system prompt?
Large language models are sensitive to visual structure in prompts. Clear section boundaries reduce the chance of the model blending rules from different sections. The triple-line dividers make the SOP section unmistakable.

---

## 3. Hallucination Prevention

The approach operates at **three layers**:

### Layer 1 — Explicit prohibition in the system prompt
The model is told three things in plain language:
- Answer ONLY from the SOP.
- Never invent prices, services, or policies.
- Do NOT say "I think", "probably", or "I believe" about facts.

This addresses the most common hallucination pathway: the model hedging with uncertain language while still inventing information.

### Layer 2 — Escalation as the default fallback
Instead of giving the model permission to say "I don't know" (which can still be followed by a guess), the model is instructed to **escalate** when it cannot answer. Escalation is a safe, defined action — not an open-ended invitation to improvise. This is the key insight: never give an AI a knowledge gap without a prescribed safe exit.

### Layer 3 — Unanswered question counter
The model is instructed to track the count of questions it couldn't answer from the SOP. After 2, it must escalate regardless of topic. This prevents the model from drifting into progressively more speculative answers as the conversation continues.

---

## 4. Confidence-Based Escalation

### Detection mechanism
Escalation is signalled via a **structured JSON marker** embedded in the model's response:

```
{ESCALATE: "reason text here"}
```

This is parsed by `detect_escalation_in_response()` using a regex, so it is:
- Machine-readable (logged with reason)
- Invisible to the customer (stripped from the display reply)
- Unambiguous (no fuzzy classification needed)

### Why structured output over classification?
An alternative approach is to run a second classifier call on every response to detect escalation. This doubles API costs and adds latency. By having the model self-flag in a structured format, we get escalation detection in one call. The trade-off is that the model must be prompted precisely — which we do.

### Pre-screening (Rule-based layer)
Before calling the model at all, `detect_escalation_in_input()` scans the raw user message for keyword signals:
- Anger keywords: "furious", "unacceptable", "sue", "scam", etc.
- Medical keywords: "side effect", "allergic", "pregnant", etc.
- Human request keywords: "speak to a manager", "real person", etc.
- Pricing negotiation keywords: "can you do better", "discount", etc.

This means obvious escalation triggers are caught instantly — before any API call is made — reducing latency and ensuring no angry message ever reaches the model for a "normal" response.

### Escalation logging
Every escalation is written to a timestamped `.jsonl` file in `logs/` with:
- Session ID
- Timestamp
- Reason string

This gives operations teams a full audit trail.

---

## 5. Tone and Persona

### Target register
SMB aesthetics customers are often first-timers, may have anxiety about treatments, and expect the warmth of a receptionist, not the formality of a bank. The persona specification targets this with:
- First-person warmth ("I'd love to...")
- Empathy markers where relevant
- Brevity (2–4 sentence cap for simple answers)
- Emoji used sparingly in the opening and closings (consistent with WhatsApp-style SMB communication)

### Anti-patterns explicitly suppressed
- No markdown headers or bullet lists (would look broken on WhatsApp/SMS)
- No over-formal openers ("Certainly! I would be delighted to assist you today...")
- No hedging language on factual matters
- No explanations of the escalation JSON to the customer

### Persona name: Aria
A short, warm, memorable name that fits the aesthetic/beauty space. Consistent across the session — the model is instructed to use it in the greeting.

---

## 6. Four-Stage Workflow Architecture

```
User Input
    │
    ▼
[Stage 3] Pre-screen for escalation (rule-based, no API call)
    │
    ├── ESCALATE → log + reply with handoff message
    │
    ▼
[Stage 2] Qualification mode active?
    │
    ├── YES → record answer, ask next question
    │
    ▼
[Stage 1] Call model with full conversation history + SOP system prompt
    │
    ▼
[Stage 3] Parse model response for {ESCALATE: ...} marker
    │
    ├── ESCALATE → strip marker, log, append handoff message
    │
    ▼
Return clean reply to user

─────── End of session ───────

[Stage 4] Call model for structured JSON summary
    → customer intent, key details, SOP gaps, lead quality, recommended action
```

---

## 7. Known Trade-offs and Limitations

| Area | Decision | Trade-off |
|---|---|---|
| State management | In-memory (Python objects) | Not persistent across process restarts. For production, use Redis or a database. |
| Escalation detection | Dual-layer (rules + model self-flag) | Rule-based layer may miss novel phrasings. Could add a dedicated sentiment model. |
| SOP grounding | Embedded in system prompt | Works for small SOPs. For large SOPs (>10k tokens), use RAG (retrieval-augmented generation). |
| Session summary | Single API call with full history | For very long conversations (>50 turns), history may exceed context window. Chunked summarisation would be needed. |
| No UI | CLI only | Sufficient for this assignment. Production deployment would use a webhook handler (WhatsApp Business API, email SMTP, etc.). |
