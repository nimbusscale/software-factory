# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Meeting room.** A space in the office that holds up to 12 people.
- **Phone room.** A booth in the office for one person.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A meeting room or phone room held for one member for one time slot.
- **Organizer.** The member a booking is for.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a meeting room or phone room for a time slot,
the app shall make the booking only if no other booking holds it for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.
