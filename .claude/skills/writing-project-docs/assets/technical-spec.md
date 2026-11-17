# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Terms

The internal terms, the ones a user wouldn't recognize.

## T-SEC-2. Architecture decisions

**AD-1.** <The choice, in one line.>

*Why:* <why this option was chosen.>

## T-SEC-3. Code standards

How all code is written, with examples where they help. A standard gets a Why only when its reason
isn't clear from it.

**CS-1.** <The standard, in one line.>

## T-SEC-4. <An area of the system>

One section per area, such as storage or tools, holding its requirements and design decisions.

**TR-1.** <Where ...> <While ...> <When ...> The <subject> shall <behavior>.

**TD-1.** <The choice, in one line, citing the FR or TR it meets.>

*Why:* <why this option was chosen.>

## T-SEC-5. Outside services

Choices about an outside service that span files or have no code to attach to.
