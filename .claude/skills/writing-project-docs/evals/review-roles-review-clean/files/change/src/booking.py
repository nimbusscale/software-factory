"""Room bookings."""

from datetime import timedelta

from notify import send_email

CHECK_IN_WINDOW = timedelta(minutes=15)  # FR-2


def check_in(booking, member, now):
    """Mark a booking as checked in by its member, while it's under way (FR-1)."""
    if booking.member == member and booking.start <= now < booking.end:
        booking.checked_in = True


def cancel_no_shows(bookings, now):
    """Cancel each booking that nobody checked in to in time, and email its member (FR-2, FR-3)."""
    for b in list(bookings):
        if not b.checked_in and now - b.start >= CHECK_IN_WINDOW:
            bookings.remove(b)
            send_email(b.member, "no-show")
