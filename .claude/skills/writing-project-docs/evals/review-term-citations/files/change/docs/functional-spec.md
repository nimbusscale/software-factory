# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room that members can book.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one or more time slots in a row (F-SEC-3).
- **Organizer.** The member who made a booking (FR-2).
- **Free.** A room is free for a time slot when a member can book it for that slot (FR-3).
- **Waitlist.** The members waiting for a room's time slot that's already booked (FR-4).
- **No-show.** A booking the app cancelled because nobody checked in in time (FR-7).

## F-SEC-2. Limits

**FR-1.** The app shall let a member book a room only up to 14 days ahead, not further.

## F-SEC-3. Booking a room

**FR-2.** When a member books a room, the app shall make that member the booking's organizer.

**FR-3.** When a member asks to book a room for some time slots, the app shall book it only if no
other booking holds that room for any of those slots.

**FR-4.** When a member asks to book a room for a time slot that isn't free, the app shall offer
to add the member to that slot's waitlist.

**FR-5.** When a booking is cancelled, the app shall book each of its time slots for the first
member on that slot's waitlist.

## F-SEC-4. Checking in

**FR-6.** While a booking is under way, the app shall let its organizer check in from the room's
page.

**FR-7.** When 15 minutes have passed since a booking started and nobody has checked in, the app
shall cancel the booking.

**FR-8.** When a member has had three no-shows in the last 30 days, the app shall stop them from
booking rooms for 7 days.
