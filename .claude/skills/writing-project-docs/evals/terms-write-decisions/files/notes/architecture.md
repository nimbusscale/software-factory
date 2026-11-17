# Room booking app: architecture notes

Notes from a meeting about how to build the room booking app. What the app does is in
docs/functional-spec.md. Nothing is built yet.

We'll write all the code in TypeScript, so the server and the browser code share one definition of
a booking.

The app is split in two: a web server, which answers everything members' browsers send, and a
worker, which runs jobs at set times, such as cancelling a booking nobody checked in to. All timed
jobs run on the worker and never on the web server. That way a job runs at its time whether or not
anyone is using the app, and a slow job never holds up a member's request.

All data lives in PostgreSQL, since two members booking the same room at once need a transaction.

Each job is a row in the database with the time it's due. When the worker starts after being
stopped, it runs every job whose time passed while it was down. Otherwise a restart could skip a
cancellation, and a room nobody turned up for would stay held.

When a job fails, the worker tries it again, up to three times, five minutes apart. Most failures
are the database being out of reach for a moment. A job that still fails after its last try is
what we call a dead job. The worker stores the error from a dead job's last try with the job, so
someone can find out what went wrong.

The web server only cancels a booking for the member FR-3 lets cancel it, whatever the browser
sends.
