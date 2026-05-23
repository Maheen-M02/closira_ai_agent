# Test Scenario 5 — Conversation Summary
# Expected behaviour: Full session → structured JSON summary with intent, details, SOP gaps, next action

Aria: Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. 😊 How can I help you today?

You: Hi, I'm interested in getting fillers. What are your prices?

Aria: Our dermal filler treatments start from £250. We offer lip enhancement, cheek contouring, and nasolabial fold treatment — each session takes around 45 minutes. Some mild swelling or bruising is possible for the first 24 to 48 hours, but most clients find it very manageable. Would you like to book a free consultation to explore your options?

You: Is the initial consultation free?

Aria: Yes, absolutely — your initial consultation is completely free of charge and lasts around 20 minutes. There's no obligation at all, and it's a lovely opportunity to chat through what you're hoping to achieve. Would you like to go ahead and book one?

You: Great! How do I book?

Aria: You can book easily via WhatsApp or through our website — whichever is most convenient for you. No deposit is required, so it's completely hassle-free. Shall I help you with anything else before you book?

You: What's your cancellation policy?

Aria: We just ask for 24 hours' advance notice if you need to cancel or reschedule your appointment. That's all there is to it! Is there anything else I can help you with?

──────────────────────────────────────────────────────
SESSION SUMMARY (JSON)
──────────────────────────────────────────────────────
{
  "customer_intent": "Customer is interested in dermal filler treatments and enquired about pricing, consultation cost, how to book, and the cancellation policy.",
  "key_details_collected": [
    "Service of interest: Dermal Fillers (from £250)",
    "Customer confirmed free consultation is appealing",
    "Booking channel preference: WhatsApp or website",
    "Cancellation policy acknowledged (24 hours notice)"
  ],
  "sop_gaps_identified": [],
  "lead_qualification_summary": "No formal qualification conducted, but customer is clearly warm with purchase intent. They engaged positively with all information and asked practical booking-related questions — strong signal of readiness to book.",
  "escalated": false,
  "escalation_reason": null,
  "recommended_next_action": "Send customer a WhatsApp message with the consultation booking link. Prioritise for follow-up within 24 hours while interest is high.",
  "session_timestamp": "2025-01-01T10:20:00"
}
