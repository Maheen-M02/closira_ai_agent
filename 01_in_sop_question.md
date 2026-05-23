# Test Scenario 1 — In-SOP Question (Botox Pricing)
# Expected behaviour: AI answers accurately from SOP only

Aria: Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. 😊 How can I help you today?

You: What are your Botox prices?

Aria: Our Botox treatments start from £200. The session typically takes around 30 minutes and requires minimal downtime — most clients see results within 3 to 14 days. Would you like to book a free consultation first to discuss which areas would suit you best?

You: And how long does a session take?

Aria: A Botox session takes approximately 30 minutes from start to finish. Quick and straightforward! Is there anything else you'd like to know?

You: Do I need to pay a deposit to book?

Aria: No deposit is required to secure your appointment — just give us 24 hours' notice if you need to cancel. You can book easily via WhatsApp or our website. Shall I help you with anything else?

──────────────────────────────────────────────────────
SESSION SUMMARY (JSON)
──────────────────────────────────────────────────────
{
  "customer_intent": "Customer enquired about Botox pricing, session duration, and booking deposit requirements.",
  "key_details_collected": [
    "Customer interested in Botox",
    "Asked about pricing (from £200)",
    "Asked about session duration (30 minutes)",
    "Confirmed no deposit needed"
  ],
  "sop_gaps_identified": [],
  "lead_qualification_summary": "No formal qualification conducted. Customer showed clear interest in Botox services. Warm lead — enquired about practical booking details suggesting intent to book.",
  "escalated": false,
  "escalation_reason": null,
  "recommended_next_action": "Follow up via WhatsApp with a booking link and consultation availability.",
  "session_timestamp": "2025-01-01T10:00:00"
}
