# Room booking app: notes

These are notes from a planning meeting for a small app that lets people in our office book
meeting rooms. Nothing is built yet.

Anyone with an account can book. We call them members. Rooms are booked in time slots of half an
hour, starting on the hour or the half hour. A booking can cover several slots in a row. You can
book up to two weeks ahead, never more.

Whoever makes a booking is its organizer. A room can only be booked for a slot if nobody else has
any part of that slot already. If the slot you want is taken, the app offers to put you on that
slot's waitlist. When a booking is cancelled, each of its slots goes to the first person on that
slot's waitlist.

People book rooms and then don't show up, so we want check-ins. While a booking is under way, the
organizer can check in from the room's page. If nobody has checked in 15 minutes after the start,
the booking is cancelled. We call that a no-show. Anyone with three no-shows in the last 30 days
can't book rooms for a week.
