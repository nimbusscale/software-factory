# Worked examples

Real comments from an earlier project, a road trip planner with a coordinator agent and worker
agents, written in TypeScript. Each one is sorted with the skill's steps. They show the reasoning,
so use them for the pattern, not the details. The IDs in the rewrites, such as `FR-31`, stand in
for whatever ID the project gives the item.

## Contents

- A type comment that repeats the name, and field comments a type could replace
- A field's meaning, copied onto a function
- A behavior the caller already gets right
- A settings type with a section number
- An example of output that a test already holds
- A pointer and history, and nothing else
- A good reason with an issue number on the end
- A reason written in a doc's private terms
- Comments worth keeping

## A type comment that repeats the name, and field comments a type could replace

**Before:**

```ts
// One worker's recorded calls.
export interface WorkerRecord {
  // The stop and stay IDs it read, in the order read, each once.
  readonly readIds: readonly string[];
  ...
}

export class WorkerCalls {
  record(agentId, toolName, toolInput, toolResponse): void {
    ...
      // Each ID once, even when one call names it twice.
      for (const id of readIdsSchema.parse(toolInput)) {
        if (!record.readIds.includes(id)) {
          record.readIds.push(id);
        }
      }
```

**Sorted:** the type comment says what the name says, so it goes. "Each once" on `readIds` means
no repeats, but it reads just as easily as "each item is read once", so it's unclear as well as
avoidable. Make the field a `ReadonlySet<string>` and the type holds the rule. The comment inside
`record()` says what the `includes` check under it does, so it goes too.

**What it shows:** a comment on what a value is, such as no repeats, usually means a type is
missing. A short comment above a declaration is the most common kind that says nothing.

## A field's meaning, copied onto a function

**Before:** a stop is one place in a day's schedule, such as dinner. Its `setTime` field says what
null means:

```ts
class Stop {
  // "Not before", such as dinner at 7. Null means it follows the stop before it.
  get setTime(): ScheduleTime | null {
    return this.#setTime;
  }
  ...
}
```

A service function that only passes the value along to the stop says it again:

```ts
// Null means it follows the stop before it.
setStopTime(itinerary: Itinerary, stop: Stop, setTime: ScheduleTime | null): void {
  refuseUntimedOnRestDay(this.#calendar.dayOf(itinerary, stop), stop, setTime);
  stop[VIA_SERVICE].setSetTime(setTime);
}
```

**Sorted:** the second comment is a copy. If what null means changes, one of the two will likely be
missed. Delete the one on the function. Better still, a type such as
`{ kind: "notBefore"; time: ScheduleTime } | { kind: "afterPrevious" }` says what null meant, and
the field's comment can go too. Without that type, keep only the field's comment, since that's
where the meaning is defined.

**What it shows:** a type comes first. Short of a type, say a thing once, where it's defined.

## A behavior the caller already gets right

**Before:** a trip is a user's saved plan, and other code writes to it while the user plans. Most
changes are refused once the trip has started. The function that deletes it:

```ts
// Removes the trip and everything that belongs to it (persistence design, section 6).
// It isn't a write, so it runs on a started trip too. It waits for a write in
// progress, and refuses once that takes longer than the lock wait.
async deleteTrip(tripId: string): Promise<void> {
  await inTransaction(pool, (client) => storeFor(client).remove(tripId));
}
```

The store's `remove()` takes the trip's row lock through this function:

```ts
// Refuses with TripBusyError when another write holds the lock for longer than
// LOCK_WAIT.
async #selectLocked(tripId: string, lock: "FOR NO KEY UPDATE" | "FOR UPDATE"): Promise<TripRow> {
  await this.connection.query("SELECT set_config('lock_timeout', $1, true)", [LOCK_WAIT]);
  try {
    ...
  } catch (error) {
    if (lockNotAvailableSchema.safeParse(error).success) {
      throw new TripBusyError();
    }
    throw error;
  }
}
```

And the web API's shared error handler, which every route's errors go through, already maps that
error to a refusal:

```ts
if (
  error instanceof ChatClosedError ||
  error instanceof TurnRunningError ||
  error instanceof TripBusyError
) {
  return 409;
}
```

**Sorted:** imagine the comment on `deleteTrip` gone, and ask what a caller would get wrong. The
first sentence says what the name says, with a section number on the end. Nothing in
`deleteTrip` checks whether the trip has started, so a reader assumes it runs on any trip. The
waiting is already written once, on `#selectLocked`, where it happens. When the trip is busy, the
caller gets `TripBusyError`, a name that explains itself, and a web route needs no code of its own
for it. Delete the comment.

**What it shows:** a comment can look like it tells the caller something, and still fail the test.
A clearly named error and a comment where the behavior lives can cover it.

## A settings type with a section number

**Before:**

```ts
// The leg scout's own model and effort settings (technical spec section 10).
export interface LegScoutDefinitionGiven {
  model: string;
  effort: EffortLevel;
}
```

**Sorted:** the fields are named `model` and `effort`, and the type's name says whose they are. The
section number gives no reason, and it breaks when the spec is reorganized. Delete the comment. If
there's a reason the definition takes these rather than reading the settings itself, write that
reason. First find where it came from, such as a spec item's Why or the task that made the choice.
The code shows that the definition takes them, but not why.

**What it shows:** a pointer tacked onto a "what" doesn't turn it into a "why". Agents often read a
rule like "comments say why, often by pointing to a doc" this way.

## An example of output that a test already holds

**Before:**

```ts
// Such as "Stay 1 (stay_…): Moab (place_…), City, Moab. 3 nights, Days 1 to 3, from
// Sunday, October 10, 2027 to the morning of Wednesday, October 13, 2027."
export function stayHeader(context: ReadContext, stay: Stay): string {
```

**Sorted:** a test holds the same text word for word. When the format changes, the test fails and
gets fixed, but nothing fails for the comment, so it goes stale. Delete it. If part of the format
is a choice a maintainer might undo, such as putting each ID in parentheses after its name, write
why that part is there, once you've found the reason.

**What it shows:** an example in a comment is a copy. The test is its home.

## A pointer and history, and nothing else

**Before:**

```ts
// Technical spec 6.1, settled on 2026-10-27 for #60.
export const SEARCH_AGAIN = `When the results don't fit, search again ...`;
```

**Sorted:** the date and the issue are history, so they go in the commit message. The section
number becomes the ID of the requirement the prompt text meets. Check that the requirement says
what this prompt text does before citing it.

**After:**

```ts
// Meets FR-31.
export const SEARCH_AGAIN = `When the results don't fit, search again ...`;
```

**What it shows:** a prompt is code, and its home is the prompt file. The spec says what the agent
should do, and the prompt cites the ID. Neither copies the other.

## A good reason with an issue number on the end

**Before:**

```ts
// The worker's type, from an Agent call's input. It names the worker in the judge
// input. The rest of the input is the coordinator's own writing, so it's left out
// (#282).
```

**Sorted:** the reason is good. A maintainer might add the rest of the input to the judge's view,
and the comment says why not. The issue is likely where the reason came from, but citing it is
history. Drop the number, and keep the rest as it is.

**What it shows:** history often rides on the end of a good comment. The check in step 7 finds the
pattern, and the fix is to cut the tail, not the comment.

## A reason written in a doc's private terms

**Before:** an itinerary is a trip's ordered list of stays, and each stay covers some nights. The
itinerary keeps its change methods under a symbol that only domain code may import, so services
call them and other code can't:

```ts
// The key to each object's change methods for its {viaService} properties (domain model
// section 1). An object keeps them under this key, so code reaches them only by importing
// it, and only files in src/domain/ may (via-service.test.ts checks this). There, the
// objects define the methods and the services call them.
export const VIA_SERVICE = Symbol("viaService");
```

A service method that moves a stay. Its `orderOf` call refuses a stay that isn't in the itinerary:

```ts
// Its days move with it. It needs no business rule, but stays are via service.
moveStay(itinerary: Itinerary, stay: Stay, after: Stay | null): void {
  this.#calendar.orderOf(itinerary, stay);
  itinerary[VIA_SERVICE].placeStay(stay, after);
}
```

**Sorted:** "via service" is a marker from a design doc's class diagram. Without that doc, a reader
can't tell why a method with no business rule is in a service.

**After:**

```ts
// The stay's days move with it. No business rule applies, but only a service may call
// the itinerary's change methods.
```

Both claims describe this code, so the code is their source. `VIA_SERVICE` is what keeps the change
methods for services. `moveStay` checks only that the stay is in the itinerary, which isn't a
business rule.

**What it shows:** a comment is read on its own, next to the code. Its terms are the code's names
and the functional spec's terms.

## Comments worth keeping

**A reason a maintainer would otherwise undo:**

```ts
// The same error for an ID that doesn't exist and for another user's or another trip's
// item, so it doesn't say whether someone else's item exists (persistence design, 8.8).
export const NO_SUCH_MEMORY_ITEM = "No such memory item.";
```

Without it, a maintainer would likely split this into two clearer errors and leak which items
exist. The section number goes. If a decision in the spec covers it, cite that ID.

**A measured number, with its date:**

```ts
// Claude Code cuts off a tool result over 25,000 tokens, and the coordinator has no
// tool to read the rest (tool design 2.1). The tool can't count tokens without calling
// the API, so it counts characters. Measured on 2026-10-26, reads of a 14-day trip ran
// from 1.80 to 2.13 characters a token, as the API counts them for the coordinator's
// model. At 1.80, 40,000 characters is about 22,200 tokens, still under 25,000.
export const MAXIMUM_REPLY_CHARACTERS = 40_000;
```

The date isn't history. It says when the measurement was taken, so a reader can judge whether it
still holds after a model change. The cutoff is a quirk of an outside tool, and the measurement is
the reason for the number. The section number goes.

**A quirk of the platform, with one unclear sentence:**

```ts
// Docker stops a container with SIGTERM. Node ignores it by default when it's the
// container's first process, so Docker would wait 10 seconds and then kill it. The
// spans not sent yet go first.
```

The first two sentences are the model to follow. The last one can't be read on its own: a reader
can't tell what goes first, or before what. Rewrite it once you've checked what the code does, or
delete it.
