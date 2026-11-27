# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person who works in the office and books rooms.
- **Room.** A meeting room that members book.
- **Booking.** A room kept for a member for a time slot.
- **Office manager.** The person who runs the office.

## F-SEC-2. Bookings

**FR-1.** When a member books a room, the app shall accept the booking only if no other booking
holds that room for any part of its time slot.

**FR-2.** When a member cancels a booking, the app shall free its room for that time slot.

**FR-3.** When the office manager asks for a booking's history, the app shall show each change to
it, who made the change and when.
