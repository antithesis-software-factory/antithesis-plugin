# Debugging with Antithesis

Antithesis can run scripts at any Moment in the Multiverse. Start by choosing the moment(s) and run(s) to investigate.

## Finding moments

For a property failure, find its passing and failing moments with `snouty runs search` (see `snouty runs search --help`). On a live run, `snouty runs stream` reports counterexample moments as they happen. `snouty runs logs` shows the moments along a timeline.

## Choosing a run to execute commands in

Any ready run (see the explainer) can execute commands, but a run that already has the moment warm saves rewarming time:

1. Prefer a ready run that has already rewarmed the moment. Check with `snouty runs search <run_id> 'filter(ev => ev.moment.input_hash == "<hash>")' --count`; non-zero means every moment of that branch is warm.
2. Prefer reusing a ready run over starting a new one.
3. If no run is ready, start a debug run with `snouty debug` (read `snouty debug --help` first).

Executing commands doesn't keep a run alive. If the run exits while you debug, pick a new one with this policy and continue.

## Executing commands

Run a bash command at a moment with `snouty runs exec`. Read `snouty runs exec --help` first.

- The command runs inside the run, and can use only the tools installed in its images, which may differ from yours. If a tool is missing there, process the output on your machine.
- Rewarming a deep moment takes longer: a moment at vtime 10 rewarms faster than one at vtime 100.
- `--container` doesn't support k8s pods; use `kubectl` for those.
- To see how the system reacts to an action, such as killing a container, run `sleep 30` with `--events` from the action's end moment.
