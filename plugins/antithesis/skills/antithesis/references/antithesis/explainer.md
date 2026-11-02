# Antithesis explainer

Antithesis is a simulation platform for finding bugs that traditional testing misses. It runs software in a deterministic simulation and systematically explores its state space for property violations.

## Definitions

- **Tenant**: An organization's Antithesis instance, at `<tenant>.antithesis.com`. snouty is configured for one tenant.
- **Launcher**: An Antithesis workflow such as testing or debug.
- **Run**: A running instance of a Launcher, identified by a run ID (for example: `1d0b6331ec02e8268fee157346701f01-64-0`).
- **Compute hour**: The unit Antithesis bills by: one core running for one hour. A run's compute budget and performance tier set how long it fuzzes.
- **Virtual time (`vtime`)**: The simulated clock that orders events within a timeline.
- **Moment**: A uniquely identified instant in a run. Identified by an (`input_hash`, `vtime`) tuple, where `input_hash` identifies the branch.
- **Timeline**: The sequence of moments of one continuous simulated execution, in `vtime` order.
- **Branch**: A new Timeline branched from another timeline at a **Moment**.
- **Multiverse**: A tree of Timelines branched from each other.
- **Event**: A record logged at a moment: output from the system under test (stdout or stderr), the Antithesis SDK, or an Antithesis built-in event such as faults.
- **Fault**: A disruption Antithesis injects, such as a network partition, a killed or paused container, or a thread pause.
- **System under test (SUT)**: The system that is being tested by Antithesis.
- **Setup**: The start of a run, when the SUT and workload are deployed and made ready. It ends when the workload reports **setup complete**; Antithesis then snapshots the system, and every timeline starts from that snapshot.
- **Property**: An invariant of the SUT, expressed via the Antithesis SDK or via property definition files.
- **Assertion**: An Antithesis SDK call that checks a property. A failing assertion doesn't stop the program. Each assertion has an example (it held) or a counterexample (it failed) at a moment.
- **Default properties**: Built-in properties every run reports, such as `Software was instrumented`.
- **Workload**: Everything added to the deployment to exercise the SUT. In this skill: the driver, the client programs that run the SUT's client library, and the forwarding of the SUT's logs to the driver.
- **Driver**: The workload program that picks actions, sends them to the SUT, and checks the responses. One binary, the main process of its own container.
- **Test command**: An executable that Antithesis runs in a container, found under `/opt/antithesis/test/v1/<test>/`. Its name prefix sets when it runs; a `first_` command runs once at the start of every timeline.
- **Config image**: A Docker image which contains orchestration code (docker compose config or k8s manifests) to run the SUT and Workload in Antithesis.

## Test runs

A launcher such as `basic_test`, built into every tenant, starts a test run. It deploys the Config image to the Antithesis fuzzer, which sets up the SUT and Workload and searches for property counterexamples, generating a multiverse.

## Debugger runs

A debugger run takes a source run and moment as input and rewarms it into a deterministic virtual machine. Like any run, it can rewarm more moments from one or more source runs.

## Run readiness

Real-time commands such as `snouty runs exec`, `snouty runs search` and `snouty runs logs` work on any run while it is ready: status `in_progress:ready` in `snouty runs show`, or wait with `snouty runs wait --until ready`.

## snouty

Snouty is the official Antithesis CLI. When using it:

1. Discover commands via `snouty --help`.
2. Read a subcommand's `snouty <cmd...> --help` before using it.
3. Pass `--detail` to every command that takes it. Pass `--json` instead only when you pipe the output into `jq` or another program. JSON costs several times as many tokens and carries mostly fields you don't need, while `--detail` keeps what the default output leaves out, such as assertion details.

Read Antithesis documentation with `snouty docs search <terms>`, then `snouty docs show <path>`.
