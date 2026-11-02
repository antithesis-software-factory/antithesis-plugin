# Property queries

Read `snouty runs properties --help` first. `snouty runs properties "${RUN_ID}" --detail` lists each property with its example and counterexample counts and a few sample moments. The counts on the `Examples` line cover every timeline in the run; the moments are only a sample.

Not every property has moments. Some of Antithesis's default properties (`snouty docs show /docs/reference/default_properties/`), such as `Hypervisor utilization`, `Customer output volume`, `Fault injector total packets`, `Every instrumented module has symbols`, `Assertions are present in customer code`, `Fuzzing has branches`, `Unique Edges` and `The Test Composer was used`, report a value instead: a scalar or a summary object such as `{session_id, total_output_mb, ...}`. They have no log to download. Report the counterexample value as the evidence.

## Pass/fail ratios

Use the counts on the `Examples` line to prioritize:

- **All failing (0 passing)** — likely a setup or workload bug: the property is violated in every timeline.
- **Mostly failing with rare passes** — most likely a setup or workload bug, or the system under test isn't set up for Antithesis. Check the Antithesis documentation.
- **Mostly passing with rare failures** — strong candidate for a real SUT bug. Look for rare event orderings or fault patterns in the logs.
- **Roughly even split** — the property may be sensitive to configuration or timing. Check whether failing correlates with fault intensity or with a choice made at the start of the timeline, such as which test or parameters it ran.

## Assertion types

Every property that isn't a default property comes from an assertion, and its type determines what a failure tells you:

- **`Always`**: fails if the condition is false at least once, or the assertion is never reached.
- **`AlwaysOrUnreachable`**: fails if reached and false at least once. A rare or optional path was exercised and the invariant didn't hold; that the path was reached is itself informative.
- **`Sometimes`**: fails if the condition is never true in the run, including when the assertion is never reached.
- **`Reachable`**: fails if never reached.
- **`Unreachable`**: fails if reached at least once. A forbidden path was entered.

On an `in_progress` run, only these results are final: `Always`, `AlwaysOrUnreachable` or `Unreachable` failing, and `Sometimes` or `Reachable` passing. The rest settle when the run completes.

A failing assertion with no examples and no counterexamples was never reached: the run may have been too short, the workload may not trigger the state, or a SUT bug may block it (ideally another property catches that bug).

Numeric and boolean variants (e.g. `AlwaysGreaterThan`, `SometimesAll`) follow their base type's semantics and attach the compared operands to the assertion details.
