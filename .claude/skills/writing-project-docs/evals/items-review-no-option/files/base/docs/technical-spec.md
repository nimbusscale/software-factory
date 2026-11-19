# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

- **Engine.** The part of the code that holds the game rules and the game state.
- **Server.** The part of the code that runs games and talks to the players' clients.
- **Client.** The part of the code that runs in each player's browser. It shows the game and sends
  the player's moves.

## T-SEC-2. Architecture decisions

**AD-1.** TypeScript for the engine, the server and the client.

*Why:* the server and the client share the engine. In two languages, every rule would be written
twice.

**AD-2.** The code is split into the engine, the server and the client.

*Why:* the engine has no network or screen code, so the server and the client can both run it,
and its rules can be tested on their own.

## T-SEC-3. Code standards

**CS-1.** A fix for a bug comes with a test that fails without the fix.
