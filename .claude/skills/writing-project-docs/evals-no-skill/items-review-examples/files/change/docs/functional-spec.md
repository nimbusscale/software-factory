# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Room.** A meeting room in the office.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room held for one member for one time slot.
- **Organizer.** The member a booking is for.
- **Upcoming booking.** A booking whose time slot hasn't started, and that hasn't been cancelled.
- **Check-in.** Telling the app that a booking is in use.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-4.** The app shall make a new booking for a member only while they have fewer than 3
upcoming bookings, not while they have 3.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking holds that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

## F-SEC-3. Checking in

**FR-5.** While a booking's time slot has started and hasn't ended, the app shall let its organizer
check in to it.

## F-SEC-4. Confirmation emails

**FR-6.** When the app makes a booking, the app shall email its organizer a confirmation of it.

No confirmation goes to an organizer who has turned emails off in their settings.
