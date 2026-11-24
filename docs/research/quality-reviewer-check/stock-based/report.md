# Quality reviewer check: what each run found and tagged

A working report for issue #82. It lists every finding from the 12 review runs on four
road-trip-agent changes, how each one was tagged, and which known bugs were found or missed. The
current prompt is at the end.

There were three sets of runs, one run per change in each:

- **Stock:** the stock code review's prompt at `high`, from Claude Code 2.1.331.
- **Ours, first wording:** our prompt as first written.
- **Ours, current wording:** our prompt after two changes. It now asks for every candidate with a
  failure scenario, in place of "if there are only two genuine findings, report two". And a nit is
  never a bug a user of the code can hit.

Every run used Opus 5.5, in a clone of road-trip-agent with history only up to the end of the
change.

## The known bugs

| PR | Known bug | Stock | Ours, first wording | Ours, current wording |
|---|---|---|---|---|
| #30 | A named hotel loses its Google name | Missed | Found, important | Missed |
| #32 | `scheduleOf()` out of time order | Found, important | Found, **nit** | Missed |
| #33 | `save()` stops checking the started-trip lock | Found, pre-existing | Missed: it looked at the change and called it safe | Found, **nit** |
| #35 | Two ways of counting a day's driving | Missed | Missed | Missed |

## Do the current wording's nits fit its own definition?

The current prompt defines a nit like this:

> `nit`: a minor issue, worth fixing but not blocking, such as a bug that harms nobody, like a
> misleading log line. A bug that a user of the code can hit is never a nit, even when a design
> doc describes the behavior that causes it.

About 10 of its 16 nits fit. About 5 don't, and 1 is unclear. Most of the ones that fit can't be
hit today, or are wording in a message. The ones that don't fit are real paths a traveler or the
agent can hit. The rule says those aren't nits, and the prompt tagged them nits anyway.

One likely cause is that "a user of the code" can be read two ways. It could mean the person using
the app. It could also mean code that calls the function. Read the second way, a bug only a caller
can hit could pass as a nit.

| PR | ID | The nit | Fits? | Why |
|---|---|---|---|---|
| #30 | F4 | A timeout while reading the body is reported as a response the app doesn't understand | **No** | The agent hits it on a slow response, and gets the wrong advice: no "try again" |
| #30 | F5 | A `NaN` result count gets past the clamp | Yes | Only a caller passing `NaN` hits it, and nothing does |
| #30 | F6 | Deleting a trip with places fails on the foreign key | Yes | No code deletes a trip |
| #32 | F1 | Open minutes are worked out for a visit the schedule shows with no times | **No** | A day that runs past the second midnight hits it. A rare trigger doesn't lower the tag |
| #32 | F2 | A fractional drive buffer can round a drive a minute too long | **No** | Any fractional setting hits it, and every later time moves a minute |
| #32 | F3 | `isWeatherOutOfDate()` doesn't refuse a stay from another trip | Yes | Only a caller's mistake hits it, and nobody sees a wrong result |
| #32 | F4 | A stop shows a known time after a drive whose time isn't known | **No** | It's a wrong schedule during a write, against what the design says |
| #33 | F1 | `removeStops()` with the same stop twice gives a misleading error | Yes | The write is rolled back. Only the error's wording is wrong |
| #33 | F2 | Some service methods don't check that the object belongs to the trip | Unclear | It's not a nit if a tool can pass a stale object, since the call would say it worked and save nothing. The finding doesn't show a tool that can |
| #33 | F3 | `save()` stops checking the started-trip lock (the known bug) | Yes, by the definition | No code calls `save()` without checking first. Road-trip-agent fixed it anyway, since its design says the repository holds the lock |
| #33 | F4 | "The user rejected A, B, so it can't be a candidate" | Yes | Only the wording is wrong |
| #33 | F5 | An import is out of alphabetical order | Yes, but | It's style, not a bug. A reviewer that looks only for bugs shouldn't report it at all |
| #35 | F2 | A closing at midnight that the next period carries on is reported as a closing | **No** | The traveler is told the place closes at midnight when it closes at 2 a.m. |
| #35 | F3 | "You agreed to 5." has no unit, and "1 hours" is the wrong plural | Yes | Only the wording is wrong |
| #35 | F4 | `clockText()` gets a time two days on, or a negative one, wrong | Yes | Nothing passes such a time today |
| #35 | F5 | A fallback warning text may never be reached | Yes | It may be dead code, and its text is only vaguer |

The two earlier sets used older definitions. In the first wording, a nit was the same, without the
second sentence. In the stock prompt, a nit also covers a broken CLAUDE.md rule.

## Where to see the prompt

The current prompt is in `src/software_factory/prompts/quality-reviewer.md`, on the branch
`issue-82-quality-reviewer-prompt`. PR #88 still shows the first wording, since the push of the
current one is waiting on the force push. The full text is at the end of this report.

## Every finding from each run

`S1`, `S2` and so on are the stock prompt's findings in the order it gave them, since it gives no
IDs.

### Road-trip-agent PR #30

The known bug: a named hotel loses its Google name (`isAddress()` drops `premise` places).

#### Stock prompt: 10 findings (3 important, 7 nit). Known bug: missed

- **S1, important,** `src/google/place-content.ts:13`. Text written by the public can still close the `<place_content>` label early, so the model reads it as instructions. `labeledAsPlaceContent` removes the closing tag in one pass, and a nested string such as `</place_</place_content>content>` turns back into `</place_content>` after the removal. Variants like `</place_content >` or `</ place_content>` don't match the regex at all. Fix: escape `<` and `>` (or `<`/`/`) in the text instead of deleting matches, or loop until no match is left and allow whitespace in the pattern.
- **S2, important,** `src/google/places-client.ts:69`. One place Google sends with an odd field makes the whole search fail with "a response the app doesn't understand". `textSearchResponseSchema` parses the `places` array as a whole, so one place that fails a strict rule rejects every result. Examples: a `rating` outside 1–5 (such as 0), a new price level, or a missing `formattedAddress`/`location`. Fix: parse each place on its own and drop or log the ones that fail, or loosen the strict checks on fields that only add detail.
- **S3, important,** `src/google/places-client.ts:75`. A `RuleError` thrown while building a `Place` escapes `searchText` as a raw domain error instead of a `GooglePlacesError`. `new Place(...)` runs after the Zod parse, and its rule (only a sole period may have no closing) can reject data Google sent. Fix: wrap building the places in try/catch and throw `GooglePlacesError`, or check the rule inside the schema with a refine.
- **S4, nit,** `src/persistence/place-repository.ts:80`. `fillNames` updates a place by `id` alone. That breaks the stated rule for this repository: "Every query names the trip, since a trip links only to its own places". Today the ids come from `EditableTrip`, which loaded them for the trip, so nothing goes wrong yet. A later caller could still rename another trip's place. Fix: add `AND trip_id = $3` and pass the trip id.
- **S5, nit,** `src/persistence/place-store.fake.ts:24`. The fake's `addPlaces` quietly drops places it can't find, but the real `PlaceRepository.addPlaces` throws in `inGivenOrder`. So the fake doesn't match "the way PlaceRepository's queries do" as it claims, and tests can't catch a call whose result is shorter than its input. Fix: throw in the fake when a place is missing, as the real store does.
- **S6, nit,** `src/domain/place.ts:116`. `townOf` takes the third-from-last comma part as the town, which only works for US-style addresses. Short or non-US addresses give the wrong `shortLine`, such as a street line shown as the town. Fix: use Google's `addressComponents` (locality), or return null when the address doesn't have the expected shape.
- **S7, nit,** `src/persistence/place-writer.ts:20`. Saving places for a trip id that doesn't exist fails with a raw Postgres foreign-key error, not a domain error. `PlaceWriter.save` doesn't check that the trip exists, so the `trip_id` foreign key in `places` (`REFERENCES trips (id)`) is what rejects it. Fix: check the trip first, or catch the foreign-key violation (23503) and throw a clear domain error.
- **S8, nit,** `src/google/places-client.ts:98`. A timeout while the response body is still downloading is reported as "a response the app doesn't understand". The `AbortSignal.timeout` also cancels reading the body, but `response.json().catch(() => null)` swallows that abort. A 2xx response then parses `null`. Fix: let the body-read error go to `failedCallMessage`, and only fall back to null when the response isn't ok.
- **S9, nit,** `src/google/places-client.ts:102`. The error message often ends with two periods. Google's error messages usually end with "." already, and the template adds another. Fix: remove a trailing period from `detail.data` before adding one.
- **S10, nit,** `src/google/places-client.ts:68`. `pageSize` is clamped but not made a whole number or checked for NaN. A fractional or NaN `maximumResults` goes to Google as a non-integer or `null`. Fix: apply `Math.trunc` and fall back to a default when the value isn't a finite number.

#### Ours, first wording: 7 findings (3 important, 4 nit). Known bug: found, as F3

- **F1, important,** `src/google/place-content.ts:13`. Public review text can still close the `<place_content>` label early, so text Google got from the public can reach the model as instructions. `labeledAsPlaceContent` removes the closing tag in a single `replaceAll` pass, so a tag nested inside another tag survives once the inner one is taken out. The regex also misses near-variants that a model would still read as a closing tag, such as `</place_content >` or `</ place_content>`. Fix: run the removal in a loop until nothing changes, or better, escape `<` and `>` in the text, and widen the pattern to allow whitespace inside the tag.
- **F2, important,** `src/google/places-text-search.schema.ts:107`. A bad Google response can come out of `searchText` as a `RuleError` instead of a `GooglePlacesError`. `googlePlaceSchema.transform(factsOf)` runs inside the parse, and `PlacesClient.searchText` then builds a `Place`, whose constructor throws `RuleError` when there are several opening periods and one has no `close`. Zod 4 does not catch errors thrown inside a transform, so the `safeParse` check does not wrap it. The agent then gets what looks like a broken domain rule rather than "Google sent a response the app doesn't understand". Fix: check the period shape in the schema with a refine or superRefine, or wrap the `Place` building in `searchText` in a try/catch that rethrows as `GooglePlacesError`.
- **F3, important,** `src/google/places-text-search.schema.ts:141`. **This is the known bug.** Some named places lose Google's name, and an agent's nickname can then replace it. `isAddress` drops `displayName` whenever `types` includes `premise` or `subpremise`, and Google also tags named buildings and landmarks with `premise`. This breaks the rule that Google's name always wins (domain model 3.10). Fix: treat a place as an address only when it has an address type and no establishment or point-of-interest type, or when `displayName` matches the start of `formattedAddress`.
- **F4, nit,** `src/persistence/place-store.fake.ts:24`. The fake store doesn't behave like the real one when a place can't be found after the insert. `FakePlaceStore.addPlaces` quietly drops such places with `.filter(place => place !== undefined)`, while `PlaceRepository.addPlaces` throws in `inGivenOrder`. Because of this, the result can be shorter than the input and no longer line up with it, and tests that use the fake would never see the error. Fix: make the fake throw the same error when a place is missing.
- **F5, nit,** `src/domain/place.ts:116`. The town in the short line is wrong for addresses that aren't in the US format. `townOf` always takes the third part from the end, which assumes the address ends in a "STATE ZIP" part and then a country part. Fix: use Google's `addressComponents` (`locality`), or at least document that this only works for US addresses.
- **F6, nit,** `src/google/places-client.ts:97`. A timeout while the response body is being read is reported as a response the app can't understand. `response.json().catch(() => null)` swallows the AbortSignal timeout that fires during the body read, so `safeParse(null)` fails and the agent is told the response was unexpected instead of "didn't answer within 10 seconds. Try again." Fix: send body-read errors through `failedCallMessage`, or at least treat a TimeoutError there as a timeout.
- **F7, nit,** `src/domain/place.ts:99`. A name with spaces around it is checked against the trimmed text but stored as given, so the stray spaces reach cards and the database. `checkedName` returns the untrimmed input. Fix: return `name.trim()`.

#### Ours, current wording: 6 findings (3 important, 3 nit). Known bug: missed

- **F1, important,** `src/google/place-content.ts:13`. Review text can still close the `<place_content>` label early, which defeats the prompt-injection guard. `labeledAsPlaceContent` strips `</place_content>` in a single pass, so a nested tag rebuilds itself once the inner copy is removed. Variants such as `</place_content >` or `</ place_content>` don't match the regex at all. Fix: strip in a loop until nothing changes, or better, escape `<` and `>` (or every `</`) in the text so no closing tag can form. Also match whitespace variants.
- **F2, important,** `src/google/places-client.ts:77`. A Google response with several opening periods, one of them with no `close`, makes `searchText` throw a raw `RuleError` instead of a `GooglePlacesError`. The schema accepts `close` as optional on every period. The `Place` constructor (`refuseOpenPeriodAmongOthers`) runs only inside `parsed.data.map(...)`, after the safeParse check, so the agent gets a domain-rule error rather than the 'response the app doesn't understand' message. Fix: enforce the rule in the zod schema (e.g. a refine on `regularOpeningHours.periods`), or wrap the Place construction and convert to `GooglePlacesError`.
- **F3, important,** `src/domain/place.ts:115`. `shortLine` shows the wrong town for any address that doesn't end in 'state zip, country'. `townOf` always takes the third-from-last comma part. For many non-US addresses, and for US addresses with an extra part, that is the street or a suite. Fix: use Google's address components (locality) if they're available. Otherwise make the heuristic aware of the format and return null when unsure.
- **F4, nit,** `src/google/places-client.ts:99`. A timeout while reading the response body is reported as 'a response the app doesn't understand' instead of a timeout. The `AbortSignal.timeout` also covers `response.json()`, but `.catch(() => null)` swallows the abort error, so the null body then fails the schema parse. Fix: let the abort from `json()` through (or check for `TimeoutError`) and map it with `failedCallMessage`.
- **F5, nit,** `src/google/places-client.ts:68`. A non-numeric `maximumResults` (such as NaN) gets past the clamp. `Math.max(NaN, 1)` is NaN, and NaN serializes as `pageSize: null`, so the request silently uses Google's default page size. Fix: guard with `Number.isFinite` / `Math.trunc` and fall back to a set default.
- **F6, nit,** `migrations/0006_places.sql:11`. `places.trip_id` references `trips(id)` with no ON DELETE rule. Any later deletion of a trip that has places will fail with an FK violation. The schema also has no CHECK that `name` is non-empty, which the `Place` domain rule needs when rows are read back. Fix: add `ON DELETE CASCADE` (or document that trips are never deleted), and consider `CHECK (name IS NULL OR btrim(name) <> '')`.

### Road-trip-agent PR #32

The known bug: `scheduleOf()` can return entries out of time order.

#### Stock prompt: 4 findings (3 important, 1 nit). Known bug: found, as S1

- **S1, important,** `src/domain/day-timeline.ts:505`. **This is the known bug.** The schedule can list a stop with no selected place after a drive that starts before it, so `scheduleOf()` is not in time order as the design promises. In `#addSelected`, waiting stops are always added after the drive. This goes wrong whenever the waiting stop's time is earlier than the drive's end, which happens when its set time comes before the next selected stop's earliest arrival. Fix: add waiting stops whose time is before the drive's start ahead of the free time and drive, or limit the 'after the drive' rule to stops whose time is at or after the drive's end.
- **S2, important,** `src/domain/weather-out-of-date.ts:729`. Seasonal weather text is never marked out of date once the trip has no dates. `datesStillFit` calls `dates.every(...)`, which returns true for an empty list. `datesOf()` returns [] when the start date is cleared, so the old text still counts as current. A forecast in the same case is flagged, because its length check fails. Fix: when `dates` is empty but `written` isn't, return false.
- **S3, important,** `src/domain/calendar.ts:316`. Stale drive times can be used when a day's start or end place has changed. `#driveMinutesOf` only checks that the leg was routed through the day's current selected stops. It never compares `leg.routedFromPlace` and `leg.routedToPlace` with `fromPlaceOf()` and `toPlaceOf()`. If lodging or the start or end place changes partway through a write, the old segment times are used as if they were current. Fix: also require both ends to match by ID before trusting the times.
- **S4, nit,** `src/domain/day-timeline.ts:436`. An entry that crosses the second midnight shows a start time but no end time. `toScheduleEntry` converts each end on its own, and `scheduleTimeAt` returns null at 2880 minutes or more. `#push` blanks both times when either is unknown, but this path doesn't, and stop entries never go through `#push`. Fix: in `toScheduleEntry`, set both times to null when either one is null, matching `#push`.

#### Ours, first wording: 1 finding (1 nit). Known bug: found, as F1

- **F1, nit,** `src/domain/day-timeline.ts:124`. **This is the known bug.** scheduleOf() can return entries out of time order, even though the design promises 'in time order'. It happens when a stop with no selected place has a set time earlier than the free time and drive before the next selected stop. TimelineBuilder.#addSelected pushes the free time and the drive first, then the waiting unselected stops, then the selected stop, so a waiting stop timed before the drive lands after it in the list. Fix: put each waiting stop with a known time where its time falls (for example, split the free time around it), or sort entries by start minute while keeping null-time entries in place. Otherwise, change the design's 'in time order' promise.

#### Ours, current wording: 4 findings (4 nit). Known bug: missed

- **F1, nit,** `src/domain/calendar.ts:172`. openTimeInMinutesOf() can return a number of open minutes for a visit whose times scheduleOf() shows as empty. It takes the raw timeline minutes, but scheduleTimeAt() blanks any time at or past 2880, which is two days after the day's midnight. The opening-hours approval and FeasibilityChecker would then work from times the schedule says aren't known. Fix: return null when startMinute or endMinute is 2*MINUTES_IN_DAY or more, the same limit scheduleTimeAt uses.
- **F2, nit,** `src/domain/calendar.ts:252`. With a fractional drive-buffer percent, a buffered drive time can come out one minute too long. Math.ceil((minutes * (100 + percent)) / 100) runs on binary floats, so an exact whole-minute result can pick up a tiny error and round up. The settings schema allows any non-negative number for driveBufferPercent. Fix: round off the float error before the ceil, for example Math.ceil(Number(((minutes * (100 + percent)) / 100).toFixed(6))), or limit the setting to whole numbers.
- **F3, nit,** `src/domain/calendar.ts:191`. isWeatherOutOfDate() does not refuse a stay that isn't in the itinerary when that stay has no weather text. The class comment says each function refuses such an object. The null-text branch returns early, before anything calls orderOf(). Fix: call this.orderOf(itinerary, stay) first, as endStayOf() and startTimeOf() do.
- **F4, nit,** `src/domain/day-timeline.ts:114`. A stop with no selected place but a set time can show a known time even when it comes after a drive whose time isn't known. The design says nothing after the first such drive has a known time. In #addUnselected, `at` is worked out from #heldUntil, which still holds the end of the last known item. The stop is then listed after the next selected stop's drive, which may be unknown. Fix: when that drive is unknown, blank the times of the waiting stops before adding them in #addSelected and #addLastDrive, or check the intended behavior against design 4.1.

### Road-trip-agent PR #33

The known bug: `TripRepository.save()` stops checking the started-trip lock.

#### Stock prompt: 7 findings (1 pre-existing, 6 nit). Known bug: found, as S1

- **S1, pre-existing,** `src/persistence/trip-repository.ts:87`. **This is the known bug.** TripRepository.save() no longer checks the started-trip lock, so any code that calls store.save() without going through TripWriter.#writeOnce can now write to a started trip. The guard was moved into TripWriter.#refuseIfStarted, and the repository now relies on a comment that the caller checks first. Fix: keep a check in save() (passing it `now`) or make save() reachable only through TripWriter, so the lock still holds at the persistence layer.
- **S2, nit,** `src/domain/stops-service.ts:582`. When you pick a meal candidate with the same tier as the stop, the stop keeps its old tier rule instead of getting the 'picked' rule. selectCandidate only calls setTier when candidate.tier !== stop.tier. Fix: also compare the tier rule (or always call setTier for a meal with a non-null candidate tier) so the rule records that the user's pick set the tier.
- **S3, nit,** `src/domain/days-service.ts:89`. setRestDay(…, false) never checks that the day belongs to the itinerary, while the true branch does (through calendar.isStayingPut → orderOf). So unmarking a stale or foreign day succeeds silently. Fix: call this.#calendar.orderOf(itinerary, day) before either branch, as StaysService.moveStay and setNightCount do.
- **S4, nit,** `src/domain/stops-service.ts:555`. addCandidates (and StaysService.addLodgingCandidates, approveOpeningHours, selectCandidate) never check that the stop or stay is in the itinerary, unlike moveStop, setStopTime and setNightCount, which call calendar.dayOf or orderOf. Fix: call this.#calendar.dayOf(itinerary, stop) / orderOf(itinerary, stay) first, so a stale reference is refused with the usual 'The itinerary has no stop …' error.
- **S5, nit,** `src/domain/refuse-rejected.ts:192`. The refusal message is singular even when several places are listed. It reads 'The user rejected A, B, so it can't be a candidate.' Fix: choose 'it'/'they' and 'a candidate'/'candidates' from rejected.length.
- **S6, nit,** `src/persistence/memory-writer.ts:878`. The option `hasTripStarted` now returns CalendarDate | null rather than a boolean, but keeps its predicate name. This invites `if (await hasTripStarted(...))` style use, which happens to work but reads wrongly. Fix: rename it (e.g. `startedToday`) to match the new TripStartedCheck return type.
- **S7, nit,** `src/persistence/trip-writer.ts:3`. The new import of ../domain/calendar.js is placed after ../domain/place.js, which breaks the alphabetical import order used everywhere else in the file and the project. Fix: move the Calendar import above the Place import.

#### Ours, first wording: 1 finding (1 nit). Known bug: missed

- **F1, nit,** `src/domain/stops-service.ts:562`. Some service methods change a stop or day without checking that it belongs to the trip being written. They are StopsService.selectCandidate and removeApproval, DaysService.approveDriveHours, approveRouteType and removeApproval, and setRestDay when given false. They take no itinerary, unlike the other methods that call calendar.orderOf/dayOf first, so an object from another trip is changed without an error. Fix: take the itinerary and call this.#calendar.dayOf(itinerary, stop) or orderOf(itinerary, day) before changing anything, as moveStop and setStopTime do.

#### Ours, current wording: 5 findings (5 nit). Known bug: found, as F3

- **F1, nit,** `src/domain/stops-service.ts:526`. removeStops promises to refuse the whole call before removing anything, but a list that names the same stop twice removes it, then throws a confusing 'These stops aren't on the day' error. Each stop's day is looked up first, then each is removed one by one, so the second removal fails. Fix: check the list for repeats first (as Day.placeStops does with a Set) and refuse with a clear message.
- **F2, nit,** `src/domain/stays-service.ts:358`. Several new service methods never check that the stay, stop or day belongs to the itinerary, so they can change an object outside the trip without an error. This is in StaysService.addLodgingCandidates; StopsService.selectCandidate, addCandidates and removeApproval; DaysService.approveDriveHours, approveRouteType, removeApproval, and setRestDay when isRestDay is false. Other methods such as moveStay and setNightCount do call calendar.orderOf for this. Fix: call this.#calendar.orderOf(itinerary, x) first (selectCandidate and the DaysService approvals would need an itinerary parameter).
- **F3, nit,** `src/persistence/trip-repository.ts:87`. **This is the known bug.** TripRepository.save no longer enforces the started-trip lock, so any caller other than TripWriter can save a started trip. The guard was moved out of save() into TripWriter.#refuseIfStarted, and only a comment now asks callers to check first. Fix: keep a check in save() (for example, pass in the clock time), or make sure no other path can reach TripStore.save.
- **F4, nit,** `src/domain/refuse-rejected.ts:187`. When several offers are rejected places, the refusal reads oddly, for example 'The user rejected A, B, so it can't be a candidate.' The message always uses 'it', however many names it lists. Fix: use 'they' (or 'them') when rejected.length > 1.
- **F5, nit,** `src/persistence/trip-writer.ts:3`. The new import of `../domain/calendar.js` sits after `../domain/place.js`, out of the alphabetical order the rest of the file uses. It was added by this change; it can fail an import-order lint rule if one is enabled. Fix: move it above the `place.js` import.

### Road-trip-agent PR #35

The known bug: the driving warning and the schedule count a day's driving two different ways.

#### Stock prompt: 4 findings (4 nit). Known bug: missed

- **S1, nit,** `src/domain/day-checks.ts:54`. The driving warning shown for a day with a drive hours approval drops the unit, so it reads "You agreed to 5." The `limit` text in `drivingResult()` uses `String(approved)` with nothing after it. The comfortable branch does say "hours a day". Fix: change it to `You agreed to ${String(approved)} hours.` and update the two expectations in feasibility-checker.test.ts.
- **S2, nit,** `src/domain/day-checks.ts:42`. A day with a drive hours approval gets no driving warning at all while the brief has no comfortable driving hours, even when it drives far past the approved hours. `drivingResult()` returns null as soon as `comfortableDrivingInHours` is null, before it looks at the approval. Spec section 8 says the check compares against the approved hours when there are some, so the brief item isn't needed then. Fix: skip only when both `comfortable` and `approved` are null, and compute `isOver` only when `comfortable` is not null.
- **S3, nit,** `src/domain/day-checks.ts:95`. The stop-order note gives the time saved as raw minutes ("saves about 95 minutes"). Every other check uses `durationText()`, which gives "1 h 35 m", the way the tools give drive times. The text is built from `String(leg.timeSavedInMinutes)` plus " minutes". Also, the `stop.selectedPlace === null` branch in the order mapping can never run, because `stopsInBestOrder` holds only routed stops, which all have a selected place. Fix: use `durationText(leg.timeSavedInMinutes)` and drop the dead branch.
- **S4, nit,** `src/domain/stop-checks.ts:111`. The opening-hours warning doesn't match the spec's sample wording. `clockText()` prints "12:00 p.m." where the spec says "noon", and `durationText(60)` prints "1 h" where the spec says "an hour". The text is built in `openingHoursText()` from `clockText()` and `durationText()`. Fix: add a noon/midnight case to `clockText()`, or confirm with the design doc that the clock form is intended.

#### Ours, first wording: 7 findings (2 important, 5 nit). Known bug: missed

- **F1, important,** `src/domain/day-checks.ts:74`. The stop-order note can name stops that were deleted, or show up when the order hasn't changed. `stopOrderResult` compares the leg's `stopsInBestOrder` with the day's current stops by object identity. But `LegsService.isRoutedFor` only re-routes a leg when the place IDs change. Fix: match stops by ID, or re-route when the stops themselves change, not just their places.
- **F2, important,** `src/domain/stop-checks.ts:87`. A stop whose visit runs past midnight of the next day gets no opening-hours warning, even when the place is closed. The visit times come from `scheduleOf()`, which leaves any time of 2880 minutes or more empty (`scheduleTimeAt`), so `visitOf` returns null and the check returns null. `openTimeInMinutesOf` works from the raw timeline minutes, so the open time and the approval check still have values. Fix: work out the visit from the timeline's raw minutes, the same ones `openTimeInMinutesOf` uses.
- **F3, nit,** `src/domain/day-checks.ts:54`. The daily driving warning's text says "You agreed to 6." with no unit, while the version without an approval says "Comfortable driving is 4 hours a day." It's built in `drivingResult`'s `limit` string. Fix: write `You agreed to ${approved} hours.`, and add "days" in the same way to the trip-length text, "the brief asks for 5." (`stay-checks.ts:33`).
- **F4, nit,** `src/domain/open-minutes.ts:59`. With back-to-back opening periods, the warning can name a closing time when the place doesn't really close then. `openingChangeWithin` treats each period's open and close as a separate event, so a close at minute M followed by a reopen at the same M still counts as "closes". Fix: merge spans that touch or overlap before listing the changes, or drop a close that has an open at the same minute.
- **F5, nit,** `src/domain/stop-checks.ts:108`. A partly open visit can produce "X is open for only N of the visit." with no opening or closing time, though the spec says the warning gives one. This fallback runs whenever `openingChangeWithin` returns null while `open` is above 0. Fix: check that this fallback can actually happen with the spans as built, or give the arrival and the boundary another way.
- **F6, nit,** `src/domain/feasibility-checker.ts:89`. `isApplying` for a route type approval returns true only when the day holds one. The design table says a route type approval applies "Always". The two can be read together, since it's also false when there's none, but the comment and the table disagree on what callers should expect. Fix: say in the docs that route type applies whenever it's present, or make the code match the table.
- **F7, nit,** `src/domain/stay-checks.ts:80`. The tier note can fire after a stay's nights change even when nobody chose its tier for those nights. `tierSetForNightCount` starts as the night count at creation, and only `setTier` updates it. Fix: check that a stay created with a default tier should really raise this note when its nights change.

#### Ours, current wording: 5 findings (1 important, 4 nit). Known bug: missed

- **F1, important,** `src/domain/stop-checks.ts:152`. A stop the party reaches very late gets no late warning at all. `lateResult` returns null when the schedule entry's `startTime` is null, and `scheduleTimeAt` (day-timeline.ts) leaves that empty for any arrival from minute 2880 on, which is past the end of the next day. Fix: work out the arrival from the timeline's own `startMinute` rather than the clipped `ScheduleTime`, or treat an empty arrival behind a set time as late.
- **F2, nit,** `src/domain/open-minutes.ts:935`. The opening-hours warning can name the wrong opening or closing time when a place's hours come as periods that meet. `openingChangeWithin` lists every span boundary, including a close at minute X followed by an open at the same minute X, and reports the earliest. So a seamless midnight changeover shows up as a closing. Fix: merge spans that touch or overlap before collecting changes, or drop a close and open that fall on the same minute.
- **F3, nit,** `src/domain/day-checks.ts:210`. The check texts get units and plurals wrong. The driving warning says "You agreed to 5." with no unit, and "Comfortable driving is 1 hours a day" when the brief says 1 hour. The stop-order note can say "saves about 1 minutes", since the minimum is clamped to 1 (line 95). Fix: write "You agreed to N hours" and make "hour(s)" and "minute(s)" plural only when needed.
- **F4, nit,** `src/domain/check-text.ts:124`. `clockText` adds " the next day" for any minute from 1440 on. It doesn't check that the minute is under 2880, and a negative minute gives a broken time. Callers can only pass schedule minutes today, so nothing breaks yet. Fix: limit it to [0, 2880) or say which day it is.
- **F5, nit,** `src/domain/stop-checks.ts:1218`. The text "X is open for only N of the visit." is only used when `open > 0` and `openingChangeWithin` finds nothing. That means the place is open only part of the visit with no opening or closing inside it, which shouldn't happen. If it does (for example with overlapping periods), the opening-hours text quietly falls back to a vaguer sentence. Fix: check whether this branch can be reached, and remove it or test it.

## The current prompt

The caller puts the review target in place of `{{review_target}}` on the first line.

~~~~markdown
Review target: {{review_target}}

`high effort → 3 inline angles (bugs) → dedup (no verify) → every finding`

You are reviewing for **recall** at high effort: catch every real bug a careful
reviewer would catch in one sitting. At this level, catching real bugs matters
more than avoiding false positives. Err on the side of surfacing.

## Phase 0 — Gather the diff

Get the unified diff of the review target named above, and treat it as the
review scope. For the changes not yet committed, run `git diff HEAD`. For a
range, such as `main...HEAD`, run `git diff` on that range, as written. Three
forms need permission, so never write them: `@{upstream}` or `@{u}` next to `..`
or `...`, commands grouped in parentheses, and shell variables such as `$?`.

## Phase 1 — Find candidates (3 correctness angles)

Run **3 independent finder angles** in sequence yourself, in THIS context — do NOT spawn subagents for them. Each
surfaces candidate findings with `file`, `line`, a short `summary`, and a
concrete `failure_scenario`.

### Angle A — line-by-line diff scan

Read every hunk in the diff, line by line. Then Read the enclosing function for
each hunk — bugs in unchanged lines of a touched function are in scope (the PR
re-exposes or fails to fix them). For every line ask: what input, state, timing,
or platform makes this line wrong? Look for inverted/wrong conditions,
off-by-one, null/undefined deref, missing `await`, falsy-zero checks,
wrong-variable copy-paste, error swallowed in catch, unescaped regex metachars.

### Angle B — removed-behavior auditor

For every line the diff DELETES or replaces, name the invariant or behavior it
enforced, then search the new code for where that invariant is re-established.
If you can't find it, that's a candidate: a removed guard, a dropped error
path, a narrowed validation, a deleted test that was covering a real case.

### Angle C — cross-file tracer

For each function the diff changes, find its callers (Grep for the symbol) and
check whether the change breaks any call site: a new precondition, a changed
return shape, a new exception, a timing/ordering dependency. Also check callees:
does a parallel change in the same PR make a call unsafe?

Pass every candidate with a nameable failure scenario through — finders that
silently drop half-believed candidates are the dominant cause of misses.

## Phase 2 — Dedup only (no verify)

Pool all candidates. Dedup near-duplicates only (same defect, same location, same reason → keep one). Do NOT run verifiers; do NOT re-judge. Give each finding that is left its `severity`, as Output defines it. Sort by severity.

## Output

Report every finding that is left, each candidate with a nameable failure
scenario, even if there are only one or two.

Return findings as a JSON array of objects:

```json
[
  {
    "id": "F1",
    "file": "path/to/file.ext",
    "line": 123,
    "summary": "the problem, where it happens and what sets it off. Fix: the change to make",
    "failure_scenario": "concrete inputs/state → wrong output/crash",
    "severity": "one of: important, nit, pre_existing"
  }
]
```

Every object carries every key shown above. Its `id` is `F` and its place in
the list, starting from `F1`. Its `severity` is one of:

- `important`: a bug that should be fixed before merging because this change
  adds it or makes it worse. If someone can hit it, a rare trigger does not
  lower the severity.
- `nit`: a minor issue, worth fixing but not blocking, such as a bug that harms
  nobody, like a misleading log line. A bug that a user of the code can hit is
  never a nit, even when a design doc describes the behavior that causes it.
- `pre_existing`: a bug that exists in the codebase but that this change did
  not introduce. A bug in unchanged lines is `pre_existing` if the change only
  fails to fix it, and `important` if the change re-exposes it.

A severity only labels and orders a finding: never drop one for its severity.
Most severe means `important`, then `pre_existing`, then `nit`.

Write each `summary` in two or three short sentences. Start with the problem as
a user of the code would see it. Next say where it happens and what sets it
off. End with "Fix:" and the change to make, or what to check if you are not
sure.

Beyond Phase 2's dedup, if the same mistake is repeated in several places,
report it once and name the other places in its `summary`. Different mistakes
stay separate findings, even when one change would fix them all.

Ranked most-severe first. If nothing survives, return `[]`. Do not call the
ReportFindings tool even if it is available - this review's
output contract is the JSON block above.
~~~~
