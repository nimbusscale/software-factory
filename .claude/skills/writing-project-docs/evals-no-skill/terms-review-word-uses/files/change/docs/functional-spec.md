# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Member.** A person with an account in the app.
- **Office manager.** The member who looks after the rooms.
- **Meeting room.** A space in the office that seats up to 12 people.
- **Phone room.** A booth in the office for one person.
- **Room.** A meeting room or a phone room.
- **Time slot.** A half hour that starts on the hour or on the half hour.
- **Booking.** A room reserved for one member for one time slot.
- **Organizer.** The member a booking is for.
- **Hold.** A room and time slot kept for one member while they finish asking for a booking
  (FR-4).
- **Round.** The office manager's evening check that every room is ready for the next day.

## F-SEC-2. Making a booking

**FR-1.** The app shall make a booking only for a time slot that starts up to 14 days after the
day the member asks for it, not later.

**FR-2.** When a member asks for a booking of a room for a time slot, the app shall make the
booking only if no other booking, and no other member's hold, has that room for that time slot.

**FR-3.** While a booking hasn't started, the app shall let its organizer cancel it.

**FR-4.** When a member picks a room and a time slot, the app shall give that member a hold on
them for 10 minutes.

**FR-7.** When an organizer cancels a booking, the app shall hold it for 30 days, then delete it.

## F-SEC-3. Rounds

**FR-5.** When the office manager starts a round, the app shall list the rooms booked for the next
day.

## F-SEC-4. Room use

**FR-6.** The app shall show the office manager how many hours each room was booked in the past 7
days, rounded up to a whole hour.
