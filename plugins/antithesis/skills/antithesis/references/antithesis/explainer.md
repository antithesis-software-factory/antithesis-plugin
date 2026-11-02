# Antithesis explainer

Antithesis is a simulation platform for finding bugs that traditional testing misses. It runs software in a deterministic simulation and systematically explores its state space for property violations.

## Definitions

- **Tenant**: An organization's Antithesis instance, at `<tenant>.antithesis.com`. snouty is configured for one tenant.
- **Launcher**: An Antithesis workflow such as testing or debug.
- **Run**: A running instance of a Launcher, identified by a run ID (for example: `1d0b6331ec02e8268fee157346701f01-64-0`).
- **Compute hour**: The unit Antithesis bills by: one core running for one hour. A run's compute budget and performance tier set how long it fuzzes.
- **System under test (SUT)**: The system that is being tested by Antithesis.
- **Fault**: A disruption Antithesis injects, such as a network partition, a killed or paused container, or a thread pause.
- **Timeline**: One continuous simulated execution of the system.
- **Virtual time (`vtime`)**: The simulated clock of a timeline.
- **Moment**: An instant on a timeline, identified by an (`input_hash`, `vtime`) pair. `input_hash` is a hash of every input Antithesis sent up to that point.
- **Branch**: A timeline that splits off another timeline at a moment.
- **Multiverse**: A tree of timelines branched from each other.
- **Event**: A record logged at a moment: output from the SUT (stdout or stderr), the Antithesis SDK, or an Antithesis built-in event such as faults.
- **Driver**: The program that picks actions, sends them to the SUT, and checks the responses. One binary, the main process of its own container.
- **Workload**: Everything added to the deployment to exercise the SUT. In this skill: the driver, the client programs that run the SUT's client library, and the forwarding of the SUT's logs to the driver.
- **Property**: A guarantee about the system, as in property-based testing. Antithesis evaluates each property by searching the multiverse, then judging what it found, and reports it as passing or failing with examples (where it held) and counterexamples (where it didn't). Antithesis defines all properties; users can't write one directly.
- **Default properties**: Built-in properties every run reports, such as `Software was instrumented`.
- **Assertion**: An Antithesis SDK call, placed in the workload or the SUT. Each assertion type defines a generic property, and each assertion, identified by its message, is one instance of it. For example, an `Always` assertion's property passes if the assertion is hit at least once and its condition is true on every hit. Assertions are the only way to define a property, indirectly. A failing assertion doesn't stop the program.
- **Test command**: An executable that Antithesis runs in a container, found under `/opt/antithesis/test/v1/<test>/`. Its name prefix sets when it runs; a `first_` command runs once at the start of every timeline.
- **Setup**: The start of a run, when the SUT and workload are deployed and made ready. It ends when the workload reports **setup complete**; Antithesis then snapshots the system, and every timeline starts from that snapshot.
- **Config image**: A Docker image which contains orchestration code (docker compose config or k8s manifests) to run the SUT and workload in Antithesis.

## Test runs

A launcher such as `basic_test`, built into every tenant, starts a test run. It deploys the Config image to the Antithesis fuzzer, which sets up the SUT and Workload and searches for property counterexamples, generating a multiverse.

## Debugger runs

A debugger run takes a source run and moment as input and rewarms it into a deterministic virtual machine. Like any run, it can rewarm more moments from one or more source runs.

## Run readiness

Real-time commands such as `snouty runs exec`, `snouty runs search` and `snouty runs logs` work on any run while it is ready: status `in_progress:ready` in `snouty runs show`, or wait with `snouty runs wait --until ready`.

## snouty

Snouty is the official Antithesis CLI. When using it:

1. Discover commands via `snouty --help`.
2. Read a subcommand's `snouty <cmd...> --help` before using it. When you hand work to a subagent, tell it to read the `--help` of the snouty commands it will use.
3. Pass `--detail` to every command that takes it. Pass `--json` instead only when you pipe the output into `jq` or another program. JSON costs several times as many tokens and carries mostly fields you don't need, while `--detail` keeps what the default output leaves out, such as assertion details.

Read Antithesis documentation with `snouty docs search <terms>`, then `snouty docs show <path>`.
