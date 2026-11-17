# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot.
- **Organizer.** The member a booking is for.
- **Check in.** To tell the app that a booking's organizer is in its room.

## F-SEC-2. Bookings

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

**FR-4.** When 15 minutes of a booking's time slot have passed and its organizer hasn't checked
in, the app shall cancel the booking.

*Why:* a room nobody turned up for is then free for someone else.
