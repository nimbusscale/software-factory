# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot.
- **Organizer.** The member a booking is for.
- **Check-in.** Telling the app that a booking is in use.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

## F-SEC-3. Checking in

**FR-4.** While a booking's time slot has started and hasn't ended, and the booking hasn't been
cancelled, the app shall let its organizer check in to it.

*Scenario:* Given a booking for 14:00 that nobody has checked in to, when its organizer tries to
check in at 14:20, then they can't, since the app cancelled the booking at 14:15.

**FR-5.** While nobody has checked in to a booking, when 15 minutes have passed since its time slot
started, the app shall cancel the booking.

*Scenario:* Given a booking for 14:00 that nobody has checked in to, when it's 14:15, then the
app cancels the booking.
