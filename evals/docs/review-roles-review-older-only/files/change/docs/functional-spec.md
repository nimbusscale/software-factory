# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account and an email address in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one or more time slots in a row.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a start date up to 14 days after the day the
member asks for it, not later.

**FR-2.** When a member asks for a booking of a room, the app shall make the booking only if no
other booking holds that room for any of the same time slots.

## F-SEC-3. Checking in

**FR-3.** While a booking is under way, the app shall let the member who holds it check in
(F-SEC-5).

**FR-4.** While nobody has checked in to a booking, when 15 minutes have passed since it started,
the app shall cancel the booking.

**FR-5.** When the app cancels a booking under FR-4, the app shall email the member who held it,
naming the booking's room and start time, to say that it was cancelled because nobody checked in.
