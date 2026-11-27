# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

- **Web server.** The part of the app that answers members' requests.
- **Main database.** The database that holds the bookings.
- **Cache.** The database that holds copies of the main database's data, so the web server can
  read them quickly.
- **Audit log.** The database that holds each change to a booking.

## T-SEC-2. Architecture decisions

**AD-1.** Python for the whole app.

*Why:* the team knows Python, and the app has no part that needs another language.

**AD-2.** PostgreSQL for every database.

*Why:* the team then runs and learns one kind of database.

## T-SEC-3. Code standards

**CS-1.** A fix for a bug comes with a test that fails without the fix.

## T-SEC-4. Backups

**AD-3.** Every database is backed up each night to the backup store.

*Why:* a lost disk then loses at most a day of bookings.

**AD-4.** The cache isn't backed up.

*Why:* everything in it can be rebuilt from the main database, and restoring an old copy would
bring back bookings that were cancelled since.

**AD-5.** The audit log is backed up every hour, to a second backup store in another region.

*Why:* the audit log is the only record of who changed a booking (FR-3). An hour's loss is the most
the office will accept, and a second region keeps it safe if the first region's store is lost.
