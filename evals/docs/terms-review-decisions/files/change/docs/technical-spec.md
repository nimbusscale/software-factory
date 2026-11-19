# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

The internal terms, the ones a user wouldn't recognize.

**Failed task.** A task that still fails after its last try (TD-1).

**Task.** A job the app runs at a set time, with no member asking for it.

**Web server.** The part of the app that answers members' browsers, and never runs a task.

**Worker.** The part of the app that runs tasks (AD-2).

## T-SEC-2. Architecture decisions

**AD-1.** TypeScript for all the code.

*Why:* the web server and the browser code share one definition of a booking.

**AD-2.** The app has two parts: a web server and a worker.

*Why:* a task then runs at its time whether or not any member is using the app.

**AD-3.** The worker runs every task, and the web server runs none.

*Why:* a slow task then never holds up a member's request.

**AD-4.** PostgreSQL for all stored data.

*Why:* two members asking for the same room at once need a transaction, so only one booking is
made.

## T-SEC-3. Code standards

How all code is written, with examples where they help. A standard gets a Why only when its reason
isn't clear from it.

**CS-1.** A fix for a bug comes with a test that fails without the fix.

## T-SEC-4. Requests

How the web server handles what members' browsers send.

**TR-1.** When the web server receives a request to cancel a booking, the web server shall cancel
it only if FR-3 lets the member who sent it cancel that booking.

## T-SEC-5. Tasks

How the worker runs tasks.

**TR-2.** When the worker starts after being stopped, the worker shall run every task whose time
passed while it was stopped.

*Why:* otherwise a restart could skip the cancellations FR-4 makes, and a room nobody turned up
for would stay held.

**TR-3.** When a task becomes a failed task, the worker shall store the error from its last try
with the task.

**TD-1.** A task that fails is tried again up to three times, five minutes apart, to meet FR-4.

*Why:* most failures come from the database being out of reach for a moment, and a cancellation
that never runs leaves a room held.

**TD-2.** Each task is a row in the database, with the time it's due, and the worker runs every
row whose time has passed and that hasn't run yet.

*Why:* a task kept in the database is still there after the worker stops, so the worker can find
and run it when it starts again (TR-2).
