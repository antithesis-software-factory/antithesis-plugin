# Properties

Express properties of the system as assertions in a workload built with `references/workload/MODULE.md`. If there is none, build it first.

- `define`: add one property the user describes. Follow "Define a property".
- `import`: add properties from a source the user points to. Follow "Import properties".

If the request names no property or source, import from the system's docs, tests and past bugs.

## Define a property

Input: a property the user wants tested, in their words. For example: "the system recovers within 500 milliseconds once faults stop."

### 1. Make it checkable

Restate the property as one condition checkable in code, and confirm the system promises it, from its docs, its API contract, what its real clients rely on, and its code. Implementations often promise less than what they imitate. Ask the user about anything the code can't answer, such as what "recovered" means or when the 500 milliseconds start.

Pick the assertion type with "Choosing the assertion" in `references/properties/checks.md`.

### 2. Add the check

Put the check where it can see the condition, following `references/properties/checks.md`:

- **A driver rule**, for what clients see. See "Responses, against the model".
- **The log thread**, for a node's internal state. See "Node state, from the logs".
- **A quiet period**, for what must hold once faults stop. See "After faults stop".
- **The system's code**, only when nothing outside it can see the condition. Tell the user, since it changes their code.

Also add a sometimes or reachable assertion for the situation the property is about, so a pass means the situation happened.

### 3. Check it locally

Run the local loop in `references/workload/local-loop.md`. The property should pass. Then break the condition on purpose, for example with a deadline of zero or a small change to the system, and confirm the property fails. Undo the change.

If it fails without a change, read the system's code. A broken promise is a real bug: keep the property. A check stricter than the property, such as treating a timed-out write as lost, needs fixing. Otherwise, ask the user whether it's a bug.

### 4. Check it in a short run

Launch a short run as `references/workload/run-loop.md` describes, and read it with the triage module. The property should pass, and its sometimes or reachable assertion should be hit.

Treat early failures as in step 3. To find a failure's cause, use the triage module's `root-cause` mode.

## Import properties

Input: a source of properties, such as a property catalog for this kind of system, the user's documents (a spec, design doc or SLA), existing tests or checks, or past bugs.

Work in batches of up to 10 properties, unless the request says otherwise.

1. List the properties the source states or implies that apply to this system. For a past bug, confirm its cause from the fix, not only the report.
2. Show the user the most important batch, and ask which to add, unless the request already says which.
3. Define each chosen property with steps 1 to 3 of "Define a property", then check them all in one short run (step 4).
4. If the source has more, ask the user whether to import the next batch, unless the request already says.
