# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot.
- **Free.** A room is free for a time slot when no booking holds that room for that slot.
- **Organizer.** The member a booking is for.
- **Waitlist.** The members waiting for a room and time slot that a booking holds.
- **Check-in.** Telling the app that a booking is in use (F-SEC-3).
- **No-show.** A booking the app cancelled under FR-7.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if the room is free for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

**FR-4.** When a member asks for a booking of a room for a time slot the room isn't free for,
the app shall offer to add the member to the waitlist for that room and time slot.

**FR-5.** While a room and time slot's waitlist has a member, when an organizer cancels the
booking that holds that room and time slot, the app shall move the member who joined the waitlist
first from it to a new booking of that room and time slot.

**FR-9.** When the app makes a booking, the app shall show the member that the booking is free of
charge.

## F-SEC-3. Checking in

**FR-6.** While a booking is under way, the app shall let its organizer check in.

**FR-7.** While nobody has checked in to a booking, when 15 minutes have passed since it started,
the app shall cancel the booking.

**FR-8.** When the app cancels a booking under FR-7, the app shall email its organizer the number
of no-shows they've had in the last 30 days, counting this one.
