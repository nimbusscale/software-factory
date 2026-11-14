# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), and the
architecture (`AD`) and design (`TD`) decisions that new code could follow or break from anywhere,
each with its reason. Decisions carried out in one place in the code are comments there instead.

## T-SEC-1. Terms

The internal terms, the ones a user wouldn't recognize.

## T-SEC-2. Architecture decisions

**AD-1.** <The choice, in one line.>

*Why:* <why this option was chosen.>

## T-SEC-3. <An area of the system>

One section per area, such as storage or tools, holding its requirements and design decisions.

**TR-1.** <Where ...> <While ...> <When ...> The <subject> shall <behavior>.

**TD-1.** <The choice, in one line.>

*Why:* <why this option was chosen.>

## T-SEC-4. Code standards

Design decisions about how all code is written, each with its reason, and examples where they help.

## T-SEC-5. Outside services

Choices about an outside service that span files or have no code to attach to.

## T-SEC-6. Commands

Where commands are defined, and the one command that says work is done.
