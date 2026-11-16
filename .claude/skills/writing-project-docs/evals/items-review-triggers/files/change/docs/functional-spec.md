# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Admin.** A member who manages the office's rooms.
- **Board member.** A member who sits on the company's board.
- **Time slot.** A half hour that starts on the hour or on the half hour.

## F-SEC-2. Limits

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-9.** The app shall give a booking only one organizer, not more.

**FR-11.** Where an admin has closed a room, the app shall book the room only for an admin, not
for other members.

**FR-12.** Where a room is kept for the board, the app shall book the room only for a board
member, not for other members.

## F-SEC-3. Making a booking

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

**FR-4.** When a member asks for a booking of a room for a time slot that another booking holds,
the app shall offer to add the member to the waitlist for that room and time slot.

**FR-5.** When an organizer cancels a booking, the app shall move the member who joined that
room and time slot's waitlist first from the waitlist to a new booking of that room and time slot.

**FR-10.** When a time slot starts, the app shall remove every member from the waitlist for each
room and that time slot.

**FR-13.** When a member who isn't an admin asks for a booking of a room an admin has closed, or a
member who isn't a board member asks for a booking of a room kept for the board, the app shall
offer them another room they may book for the same time slot.

**FR-14.** When an organizer cancels a booking, or a member joins a waitlist, the app shall email
a confirmation to the member who did it.

## F-SEC-4. Checking in

**FR-6.** While a booking is under way, the app shall let its organizer check in.

**FR-7.** While nobody has checked in to a booking, when 15 minutes have passed since it started,
the app shall cancel the booking.

**FR-8.** When the app cancels a booking under FR-7, the app shall email its organizer the number
of no-shows they've had in the last 30 days, counting this one.
