"""Room bookings."""

from datetime import timedelta

MAX_DAYS_AHEAD = 30  # FR-1
CHECK_IN_WINDOW = timedelta(minutes=15)  # FR-4


def accept(request, today, bookings):
    """Decide whether to make a requested booking (FR-1, FR-2)."""
    if (request.start.date() - today).days > MAX_DAYS_AHEAD:
        return False
    return not any(b.room == request.room and b.overlaps(request) for b in bookings)


def check_in(booking, member, now):
    """Mark a booking as checked in by its member, while it's under way (FR-3)."""
    if booking.member == member and booking.start <= now < booking.end:
        booking.checked_in = True


def cancel_no_shows(bookings, now):
    """Cancel each booking that nobody checked in to in time (FR-4)."""
    for b in bookings:
        if not b.cancelled and not b.checked_in and now - b.start >= CHECK_IN_WINDOW:
            b.cancel()
