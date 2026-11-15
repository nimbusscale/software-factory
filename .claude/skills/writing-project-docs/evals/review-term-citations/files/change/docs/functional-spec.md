# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot (F-SEC-3).
- **Organizer.** The member a booking is for (FR-3).
- **Waitlist.** The members waiting for a room and time slot that a booking holds, in the order
  they joined (FR-4).
- **No-show.** A booking the app cancelled because nobody checked in in time (FR-8).

## F-SEC-2. Limits

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

## F-SEC-3. Making a booking

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** When the app makes a booking, the app shall make the member it's for the booking's
organizer.

**FR-4.** When a member asks for a booking of a room for a time slot that another booking holds,
the app shall offer to add the member to the waitlist for that room and time slot.

**FR-5.** While a booking hasn't started, the app shall let its organizer cancel it.

**FR-6.** When an organizer cancels a booking, the app shall make a booking of the same room and
time slot for the member who joined its waitlist first, and take that member off the waitlist.

## F-SEC-4. Checking in

**FR-7.** While a booking is under way, the app shall let its organizer check in.

**FR-8.** While nobody has checked in to a booking, when 15 minutes have passed since it started,
the app shall cancel the booking.

**FR-9.** When the app cancels a booking under FR-8, the app shall email its organizer the number
of no-shows they've had in the last 30 days, counting this one.
