# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot.
- **Organizer.** The member a booking is for.
- **Waitlist.** The members waiting for one room for one time slot, in the order they joined.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

## F-SEC-3. Waitlists

**FR-4.** When the app refuses a booking under FR-2, the app shall offer to add the member to the
waitlist for that room and time slot.

**FR-5.** While the waitlist for a room and time slot has a member, when the booking that holds
that room for that time slot is cancelled, the app shall make the booking for the first member on
that waitlist.

**FR-6.** When the app makes a booking under FR-5, the app shall email its organizer the room and
time slot.

**FR-7.** When a time slot is 30 minutes from starting, the app shall empty every waitlist for that
time slot.
