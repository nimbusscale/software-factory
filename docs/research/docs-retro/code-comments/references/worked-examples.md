# Worked examples

Real comments from an earlier project, a road trip planner with a coordinator agent and worker
agents, written in TypeScript. Each one is sorted with the skill's steps. They show the reasoning,
so use them for the pattern, not the details. The IDs in the rewrites, such as `FR-31`, stand in
for whatever ID the project gives the item.

Some examples show other code from the project as setup, so the verdict can be checked. That code
has comments of its own, which aren't sorted unless the example says so. Don't copy them as models.

## Contents

- A type comment that repeats the name, and a field comment a type could replace
- A field's meaning, copied onto a function
- A comment with one sentence worth keeping
- A settings type with a section number
- An example of output that a test already holds
- A pointer and history, and nothing else
- An issue number on a comment with nothing else worth keeping
- A comment written in a doc's private terms
- Comments worth keeping

## A type comment that repeats the name, and a field comment a type could replace

**Before:** the type a caller reads, and the class's own copy that it fills in:

```ts
// One worker's recorded calls.
export interface WorkerRecord {
  // The stop and stay IDs it read, in the order read, each once.
  readonly readIds: readonly string[];
  ...
}

interface MutableRecord {
  readIds: string[];
  ...
}

export class WorkerCalls {
  record(agentId, toolName, toolInput, toolResponse): void {
    const record: MutableRecord = this.#recordOf(agentId);
    ...
      // Each ID once, even when one call names it twice.
      for (const id of readIdsSchema.parse(toolInput)) {
        if (!record.readIds.includes(id)) {
          record.readIds.push(id);
        }
      }
```

`readIdsSchema` reads the tool input's `stopOrStayIds` field. The one place that reads
`WorkerRecord.readIds` lists the IDs the worker read but never filled, in a block of text for the
coordinator.

**Sorted:** the type comment says what the name says, so it goes. The field comment makes three
claims, and each is tested on its own:

- "The stop and stay IDs" says which kind of ID. A caller reads only `WorkerRecord`, not the
  schema inside `record()`, so the field's type is where that belongs. Without a type for it, the
  words stay.
- "Each once" means no repeats, but it reads just as easily as "each item is read once", so it's
  unclear as well as avoidable. A set holds the rule.
- "In the order read" matters to nothing that reads the field, since the order only decides the
  order of a list in a block of text. A JavaScript `Set` also keeps the order items were added.

So the field comment comes down to which kind of ID, and goes too if a type such as
`StopId | StayId` exists. The comment inside `record()` says what the `includes` check under it
does, so it goes.

**After,** with no ID types in the project:

```ts
export interface WorkerRecord {
  // Each is a stop's or a stay's ID.
  readonly readIds: ReadonlySet<string>;
  ...
}

interface MutableRecord {
  readIds: Set<string>;
  ...
}

      for (const id of readIdsSchema.parse(toolInput)) {
        record.readIds.add(id);
      }
```

**What it shows:** a comment on what a value is, such as no repeats, usually means a type is
missing. Test each claim in a comment on its own.

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

A service function says it again. Apart from a check for rest days, it only passes the value along
to the stop:

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
where the meaning is defined. Its opening is a fragment, so make it a full sentence:

```ts
// The stop starts no earlier than this time, such as dinner at 7. Null means it follows the
// stop before it.
get setTime(): ScheduleTime | null {
```

**What it shows:** a type comes first. Short of a type, say a thing once, where it's defined.

## A comment with one sentence worth keeping

**Before:** a trip is a user's saved plan. Most changes to a trip are refused once it has started.
The function that deletes one:

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

The project's functional spec has a requirement that says what deleting a trip removes, and that a
trip can be deleted at any time, even once it has started.

**Sorted:** each sentence is tested on its own, for a caller and for a maintainer.

- The first sentence has a section number on the end. "And everything that belongs to it" says
  more than the name, but what goes with a trip is the same requirement's rule, and `remove()`
  shows it. It goes.
- The third sentence describes the waiting and the error. Both are already written once, on
  `#selectLocked`, where they happen. `TripBusyError` is a name that explains itself, and a
  function doesn't list the errors that come up from code it calls. It goes.
- The second sentence holds a reason a maintainer needs. Most changes are refused once a trip has
  started, so a maintainer could add the same check here to match. The functional spec's
  requirement holds the reason, so the comment cites its ID. "It isn't a write" goes too, since in
  plain terms deleting is a write.

**After:**

```ts
// A started trip can be deleted too (FR-12).
async deleteTrip(tripId: string): Promise<void> {
```

**What it shows:** ask what a maintainer would get wrong, not only a caller. When the point is a
check the code doesn't make, name it, and let the ID carry the reason.

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
section number gives no reason, and it breaks when the spec is reorganized. Delete the comment.
Write a reason only if a maintainer would otherwise change the code, such as folding these into
settings the other agents share. Then cite the spec item that says why, or find the reason and
write it as a sentence.

**What it shows:** a pointer tacked onto a "what" doesn't turn it into a "why".

## An example of output that a test already holds

**Before:**

```ts
// Such as "Stay 1 (stay_…): Moab (place_…), City, Moab. 3 nights, Days 1 to 3, from
// Sunday, October 10, 2027 to the morning of Wednesday, October 13, 2027."
export function stayHeader(context: ReadContext, stay: Stay): string {
```

**Sorted:** a test holds the same text word for word. When the format changes, the test fails and
gets fixed, but nothing fails for the comment, so it goes stale. Delete it. It needs no pointer to
the test, since a reader finds the test by searching for `stayHeader`. If part of the format is a
choice a maintainer might undo, such as putting each ID in parentheses after its name, write why
that part is there, once you've found the reason.

**What it shows:** an example in a comment is a copy. The test is its home.

## A pointer and history, and nothing else

**Before:**

```ts
// Technical spec 6.1, settled on 2026-10-27 for #60.
export const SEARCH_AGAIN = `When the results don't fit, search again ...`;
```

**Sorted:** the date and the issue are history, so they go in the commit message. The section
number becomes the ID of the item the prompt text meets. Cite the ID the item has, and check that
the item says what this prompt text does before citing it. If the item looks like it's in the wrong
doc, that's for the `project-docs` skill, not the comment.

**After:**

```ts
// Meets FR-31.
export const SEARCH_AGAIN = `When the results don't fit, search again ...`;
```

**What it shows:** when a spec item holds the reason, the ID alone is enough. Restating the item
would be a copy, and it would drift when the item changes.

## An issue number on a comment with nothing else worth keeping

**Before:** a schema for one part of the input an evaluation's judge reads:

```ts
// The worker's type, from an Agent call's input. It names the worker in the judge
// input. The rest of the input is the coordinator's own writing, so it's left out
// (#282).
export const agentInputSchema = z
  .object({ subagent_type: z.string() })
```

**Sorted:** the issue number is history, even when the issue is where the reason came from. Drop
it, then test what's left like any other comment:

- "The worker's type, from an Agent call's input" says what the schema's one field already says.
- "It names the worker in the judge input" describes how other code uses the schema.
- "The rest of the input is the coordinator's own writing, so it's left out" looks like a reason,
  but a reader can't make sense of it. Nothing says why the coordinator's writing must be kept from
  the judge, so it doesn't tell a maintainer what not to change.

Nothing is left, so the whole comment goes. If the issue holds the real reason, write that as a
sentence instead.

**What it shows:** history often rides on the end of a comment, and the check in step 7 finds it.
Cutting the tail isn't the end of the job. What's left has to pass the test too, and here none of
it does.

## A comment written in a doc's private terms

**Before:** an itinerary is a trip's ordered list of stays. The itinerary keeps its change methods
under a symbol that only domain code may import, so code outside the domain can't call them:

```ts
// The key to each object's change methods for its {viaService} properties (domain model
// section 1). An object keeps them under this key, so code reaches them only by importing
// it, and only files in src/domain/ may (via-service.test.ts checks this). There, the
// objects define the methods and the services call them.
export const VIA_SERVICE = Symbol("viaService");
```

This setup comment has the same problem as the one this example sorts: a private marker,
`{viaService}`, and a section number. It's shown only for what it says about the code.

A service method that moves a stay. Its `orderOf` call refuses a stay that isn't in the itinerary:

```ts
// Its days move with it. It needs no business rule, but stays are via service.
moveStay(itinerary: Itinerary, stay: Stay, after: Stay | null): void {
  this.#calendar.orderOf(itinerary, stay);
  itinerary[VIA_SERVICE].placeStay(stay, after);
}
```

**Sorted:** "via service" is a marker from a design doc's class diagram, and "business rule" is a
term from the same doc. A reader without that doc can't tell what either means. Said in plain
words, the comment's point is that this is a service method because code outside the domain can't
reach the itinerary's change methods. But that holds for every service method that calls one, and
`VIA_SERVICE` already says it. Repeating it on each method would make copies. "Its days move with
it" describes what `placeStay` does to the itinerary. If it needs saying, it goes on `placeStay`,
once.

So the comment goes. One thing in this method does need a fix. `orderOf` returns a number that the
method throws away, so a maintainer could delete the call as dead code and lose the check. A name
that says what it does fixes that better than a comment, such as a `refuseIfNotIn(itinerary, stay)`
on the calendar.

**After:**

```ts
moveStay(itinerary: Itinerary, stay: Stay, after: Stay | null): void {
  this.#calendar.refuseIfNotIn(itinerary, stay);
  itinerary[VIA_SERVICE].placeStay(stay, after);
}
```

**What it shows:** a comment is read on its own, next to the code. Its terms are the code's names
and the functional spec's terms. Once a private term is put in plain words, test the comment again.
Here, the plain version turned out to be a copy.

## Comments worth keeping

**A reason a maintainer would otherwise undo:**

```ts
// The same error for an ID that doesn't exist and for another user's or another trip's
// item, so it doesn't say whether someone else's item exists (persistence design, 8.8).
export const NO_SUCH_MEMORY_ITEM = "No such memory item.";
```

Without it, a maintainer would likely split this into two clearer errors and leak which items
exist. Two fixes: the section number goes, and the opening becomes a full sentence.

```ts
// This is the same error for an ID that doesn't exist and for another user's or another
// trip's item, so it doesn't say whether someone else's item exists.
export const NO_SUCH_MEMORY_ITEM = "No such memory item.";
```

**A measured number, with its date:**

```ts
// Claude Code cuts off a tool result over 25,000 tokens, and the coordinator has no
// tool to read the rest (tool design 2.1). The tool can't count tokens without calling
// the API, so it counts characters. Measured on 2026-10-26, reads of a 14-day trip ran
// from 1.80 to 2.13 characters a token, as the API counts them for the coordinator's
// model. At 1.80, 40,000 characters is about 22,200 tokens, still under 25,000.
export const MAXIMUM_REPLY_CHARACTERS = 40_000;
```

The cutoff is a quirk of an outside tool, and the measurement is the reason for the number. The
date isn't history. It says when the measurement was taken, so a reader can judge whether it still
holds. Three fixes:

- "The coordinator has no tool to read the rest" is a fact about other code today. It goes stale
  the day someone adds such a tool, and nothing would flag it. The cutoff alone is the reason.
- The section number goes. Cite the decision's ID if one covers the limit.
- "The coordinator's model" doesn't say which model. Name it, since the date alone doesn't say
  what the number was measured on.

```ts
// Claude Code cuts off a tool result over 25,000 tokens, so a reply has to stay under that.
// The tool can't count tokens without calling the API, so it counts characters. Measured on
// 2026-10-26, reads of a 14-day trip ran from 1.80 to 2.13 characters a token, as the API
// counts them for <the model>. At 1.80, 40,000 characters is about 22,200 tokens, still
// under 25,000.
export const MAXIMUM_REPLY_CHARACTERS = 40_000;
```

**A quirk of the platform, with one unclear sentence:**

```ts
// Docker stops a container with SIGTERM. Node ignores it by default when it's the
// container's first process, so Docker would wait 10 seconds and then kill it. The
// spans not sent yet go first.
const stop = (): void => {
  server.close();
  void pool.end();
  void tracing.shutdown();
};
process.once("SIGTERM", stop);
process.once("SIGINT", stop);
```

The first two sentences are the model to follow. They give the reason the SIGTERM handler exists,
which no name could. But they sit on `stop`, six lines above the line they explain. Step 4 puts a
reason for one line right above that line.

The last sentence can't be read on its own, and the code doesn't match it: `tracing.shutdown()` is
called last, not first. It may mean that `tracing.shutdown()` sends the spans that haven't been
sent yet. Check what it does, then rewrite the sentence to say that, above that call, or delete it.

**After,** with the last sentence deleted until it's checked:

```ts
const stop = (): void => {
  server.close();
  void pool.end();
  void tracing.shutdown();
};
// Docker stops a container with SIGTERM. Node ignores it by default when it's the
// container's first process, so Docker would wait 10 seconds and then kill it.
process.once("SIGTERM", stop);
process.once("SIGINT", stop);
```
