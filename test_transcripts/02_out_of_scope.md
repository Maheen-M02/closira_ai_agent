# Test Scenario 2 — Out-of-Scope Question (Service Not in SOP)
# Expected behaviour: AI acknowledges gap and escalates rather than guessing

Aria: Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. 😊 How can I help you today?

You: Do you offer laser hair removal?

Aria: That's a great question! I don't have information about laser hair removal in our current services list, so I wouldn't want to give you inaccurate details. Let me connect you with one of our team members who can give you a definitive answer.

⚠️  [ESCALATION LOGGED] Reason: Customer asked about a service not covered in the SOP (laser hair removal)

Aria: I'm connecting you with one of our team members right now who will be able to assist you further. Please bear with us — someone will be in touch very shortly. 💙

You: What about chemical peels?

Aria: I'm sorry, I don't have information about chemical peels in our current services either. Our team member who's joining the conversation shortly will be best placed to answer that for you fully.

You: Can I get a teeth whitening treatment at your clinic?

Aria: Teeth whitening isn't something I can confirm from the information I have available. I'd hate to mislead you, so our team will be able to give you a complete picture of everything we offer when they follow up. Is there anything else I can help you with in the meantime?

──────────────────────────────────────────────────────
SESSION SUMMARY (JSON)
──────────────────────────────────────────────────────
{
  "customer_intent": "Customer enquired about multiple aesthetic services — laser hair removal, chemical peels, and teeth whitening — none of which are listed in the clinic SOP.",
  "key_details_collected": [
    "Customer interested in laser hair removal",
    "Customer interested in chemical peels",
    "Customer interested in teeth whitening"
  ],
  "sop_gaps_identified": [
    "Laser hair removal not listed in SOP",
    "Chemical peels not listed in SOP",
    "Teeth whitening not listed in SOP"
  ],
  "lead_qualification_summary": "No formal qualification conducted. Customer appears interested in a broader range of aesthetic services than currently documented. SOP should be updated to clarify full service offering.",
  "escalated": true,
  "escalation_reason": "Customer asked about a service not covered in the SOP (laser hair removal); subsequent out-of-scope questions exceeded threshold",
  "recommended_next_action": "Human agent to contact customer with full service menu. Consider updating SOP to include all offered services to reduce future escalations.",
  "session_timestamp": "2025-01-01T10:05:00"
}
