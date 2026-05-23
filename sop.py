"""
SOP Data for Bloom Aesthetics Clinic
=====================================
Single source of truth for the AI agent. The model is instructed never
to answer outside the boundaries of this data.
"""

SOP_DATA = {
    "business": {
        "name": "Bloom Aesthetics Clinic",
        "type": "Aesthetics / Medical Beauty Clinic",
    },
    "hours": {
        "open": "Monday to Saturday",
        "hours": "9:00 AM – 7:00 PM",
        "closed": "Sunday and UK Public Holidays",
    },
    "services": {
        "botox": {
            "name": "Botox (Botulinum Toxin) Treatments",
            "starting_price": 200,
            "currency": "GBP",
            "description": "Wrinkle relaxing injections for forehead lines, crow's feet, frown lines.",
            "duration_minutes": 30,
            "downtime": "Minimal. Results visible within 3–14 days.",
        },
        "fillers": {
            "name": "Dermal Fillers",
            "starting_price": 250,
            "currency": "GBP",
            "description": "Lip enhancement, cheek contouring, nasolabial fold treatment.",
            "duration_minutes": 45,
            "downtime": "Mild swelling or bruising possible for 24–48 hours.",
        },
        "consultation": {
            "name": "Initial Consultation",
            "price": 0,
            "currency": "GBP",
            "description": "A free, no-obligation consultation with one of our aesthetic practitioners.",
            "duration_minutes": 20,
        },
    },
    "booking": {
        "channels": ["WhatsApp", "Website"],
        "cancellation_policy": "24 hours advance notice required for all cancellations.",
        "deposit_required": False,
        "walk_ins": "Not available. Appointment only.",
    },
    "escalation_triggers": [
        "complaint or dissatisfaction",
        "medical question (side effects, contraindications, allergies, medications)",
        "pricing negotiation request",
        "more than 2 unanswered questions",
        "explicit request to speak to a human or manager",
    ],
    "contact": {
        "whatsapp": "Available via website link",
        "email": "Not listed in SOP",
        "phone": "Not listed in SOP",
    },
}

# Plain-text version embedded in the system prompt
SOP_TEXT = """
Business: Bloom Aesthetics Clinic
Operating Hours: Monday to Saturday, 9:00 AM – 7:00 PM (Closed Sundays & UK Public Holidays)

SERVICES:
- Botox (Botulinum Toxin): Starting from £200. Treats forehead lines, crow's feet, frown lines. Sessions ~30 minutes. Minimal downtime. Results appear within 3–14 days.
- Dermal Fillers: Starting from £250. Lip enhancement, cheek contouring, nasolabial folds. Sessions ~45 minutes. Mild swelling or bruising for 24–48 hours possible.
- Initial Consultation: FREE. 20 minutes. No obligation.

BOOKING:
- Bookings via WhatsApp or Website only.
- Appointment only — no walk-ins accepted.
- Cancellation Policy: 24 hours advance notice required.
- No deposit required to book.

ESCALATION RULES (when you must hand off to a human):
1. Customer makes a complaint or expresses dissatisfaction.
2. Any medical question (side effects, contraindications, allergies, medications, health conditions).
3. Customer attempts to negotiate pricing.
4. You have been unable to answer more than 2 questions from this SOP.
5. Customer explicitly requests to speak to a human, manager, or supervisor.
""".strip()
