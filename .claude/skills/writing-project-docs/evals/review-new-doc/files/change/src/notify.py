"""Sends emails to members."""

MESSAGES = {
    "no-show": "Your booking was cancelled because nobody checked in.",
}

outbox = []


def send_email(member, message):
    """Queue the message with this name to be emailed to the member."""
    outbox.append((member, MESSAGES[message]))
