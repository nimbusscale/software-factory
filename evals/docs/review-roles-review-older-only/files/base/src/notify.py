"""Sends emails to members."""

MESSAGES = {
    "no-show": "Your booking of {room} at {start:%H:%M on %d %B} was cancelled because nobody checked in.",
}

outbox = []


def send_email(member, message, **details):
    """Queue the message with this name, filled in with the details, to be emailed to the member."""
    outbox.append((member, MESSAGES[message].format(**details)))
