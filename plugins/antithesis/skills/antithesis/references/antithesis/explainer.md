# Antithesis explainer

Antithesis is a simulation platform for finding bugs that traditional testing misses. It runs software in a deterministic simulation and systematically explores its state space for property violations.

## Definitions

- **Launcher**: An Antithesis workflow such as testing or debug.
- **Run**: A running instance of a Launcher, identified by a run ID (for example: `1d0b6331ec02e8268fee157346701f01-64-0`).
- **Moment**: A uniquely identified instant in a run. Identified by an (`input_hash`, `vtime`) tuple, where `input_hash` identifies the branch, and `vtime` identifies the virtual time.
- **Timeline**: The sequence of moments of one continuous simulated execution, in `vtime` order.
- **Branch**: A new Timeline branched from another timeline at a **Moment**.
- **Multiverse**: A tree of Timelines branched from each other.
- **Event**: A record logged at a moment: output from the system under test (stdout or stderr), the Antithesis SDK, or an Antithesis built-in event such as faults.
- **System under test (SUT)**: The system that is being tested by Antithesis.
- **Property**: An invariant of the SUT, expressed via the Antithesis SDK or via property definition files.
- **Workload**: Code that exercises the SUT so Antithesis can explore its state space and find property violations.
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
