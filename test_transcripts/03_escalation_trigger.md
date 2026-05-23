# Test Scenario 3 — Escalation Trigger (Complaint + Human Request)
# Expected behaviour: AI detects anger/frustration and hands off with reason logged

Aria: Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. 😊 How can I help you today?

You: I booked an appointment last week and nobody showed up. This is absolutely unacceptable.

⚠️  [ESCALATION LOGGED] Reason: Anger/frustration detected in customer message: 'unacceptable'

Aria: I completely understand, and I want to make sure you get the best help possible. I'm connecting you with one of our team members right now who will be able to assist you further. Please bear with us — someone will be in touch very shortly. 💙

You: I want to speak to a manager right now.

⚠️  [ESCALATION LOGGED] Reason: Customer explicitly requested human agent: 'speak to a manager'

Aria: I completely understand, and I want to make sure you get the best help possible. I'm connecting you with one of our team members right now who will be able to assist you further. Please bear with us — someone will be in touch very shortly. 💙

──────────────────────────────────────────────────────
SESSION SUMMARY (JSON)
──────────────────────────────────────────────────────
{
  "customer_intent": "Customer is making a complaint about a missed or no-show appointment and is demanding to speak with a manager.",
  "key_details_collected": [
    "Customer had a booking last week",
    "Appointment was not fulfilled (no-show by clinic)",
    "Customer is highly dissatisfied",
    "Customer explicitly requested a manager"
  ],
  "sop_gaps_identified": [
    "No missed appointment or no-show procedure in SOP",
    "No complaints resolution process documented in SOP"
  ],
  "lead_qualification_summary": "Not applicable. Customer is an existing client with a complaint, not a new lead.",
  "escalated": true,
  "escalation_reason": "Anger/frustration detected; customer explicitly requested human manager",
  "recommended_next_action": "Senior team member to contact customer immediately, apologise for the missed appointment, and offer a resolution (e.g., rescheduling, compensation). Review SOP to add complaints handling procedure.",
  "session_timestamp": "2025-01-01T10:10:00"
}
