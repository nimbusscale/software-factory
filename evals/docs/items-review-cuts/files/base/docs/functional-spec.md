# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot.
- **Organizer.** The member a booking is for.
- **Projector.** A portable projector the office lends for a booking.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

**FR-4.** While a member is the organizer of 3 bookings that haven't started, when the member asks
for a booking for a later day, the app shall refuse it.

## F-SEC-3. Projectors

**FR-5.** When a member asks for a booking, the app shall offer to add a projector to it.

**FR-6.** When a member adds a projector to a booking, the app shall email the office manager the
room and time slot, so the projector is set up before the booking starts.
