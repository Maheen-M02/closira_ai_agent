# Test Scenario 4 — Lead Qualification
# Expected behaviour: AI asks 3 structured questions and produces a qualification summary

Aria: Hello! Welcome to Bloom Aesthetics Clinic. I'm Aria, your virtual assistant. 😊 How can I help you today?

[User types 'qualify' — qualification mode starts]

Aria: I'd love to find out a bit more about you so we can tailor our service perfectly. I have just a few quick questions — it'll only take a moment!

Could you tell me what type of business or role you're enquiring for? (e.g., personal, clinic partner, influencer)

You: It's for personal use — I'm interested in Botox for myself.

Aria: Roughly how many treatments or bookings would you be looking at per month?

You: Maybe 1–2 treatments per year.

Aria: Are you currently using any booking or CRM tools, or would this be your first time?

You: I don't use any booking tools currently, I usually just call or WhatsApp.

Aria: Thank you so much — that's everything I need! I've noted your details and a member of our team will be in touch to discuss next steps. Is there anything else I can help you with in the meantime?

──────────────────────────────────────────────────────
SESSION SUMMARY (JSON)
──────────────────────────────────────────────────────
{
  "customer_intent": "Individual customer seeking personal Botox treatments.",
  "key_details_collected": [
    "Enquiry type: Personal use",
    "Treatment frequency: 1–2 treatments per year",
    "Booking preference: WhatsApp (no existing CRM tools)"
  ],
  "sop_gaps_identified": [],
  "lead_qualification_summary": "Individual consumer lead. Low frequency (1–2 treatments/year) indicates a standard personal client rather than a high-volume or B2B account. Prefers WhatsApp contact — aligns with clinic's booking channels. Warm lead with clear service intent (Botox). Recommended outreach: personal WhatsApp follow-up with consultation booking link.",
  "escalated": false,
  "escalation_reason": null,
  "recommended_next_action": "Send WhatsApp message with free consultation booking link. Suggest a Botox consultation as the first step.",
  "session_timestamp": "2025-01-01T10:15:00"
}
