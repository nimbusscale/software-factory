# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account and an email address in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one or more time slots in a row.

## F-SEC-2. Checking in

**FR-1.** While a booking is under way, the app shall let only the member the booking is for check
in to it, not other members.

**FR-2.** While nobody has checked in to a booking, when 15 minutes have passed since it started,
the app shall cancel the booking.

**FR-3.** When the app cancels a booking under FR-2, the app shall email the member the booking was
for to say that the booking was cancelled because nobody checked in.
