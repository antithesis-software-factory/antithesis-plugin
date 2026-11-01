# Iterate locally

## 1. Build the system for coverage

Antithesis instrumentation records nothing outside Antithesis, so measure local coverage with the language's own tool. Add a `docker-compose.coverage.yaml` that overrides each system service with a coverage Dockerfile and a shared `coverage` volume, one directory per service. Client containers count as system services: the client library is code under test.

**Rust**

- In the build stage, run `rustup component add llvm-tools-preview` and build with `RUSTFLAGS="-Cinstrument-coverage -Cllvm-args=-runtime-counter-relocation"`. This overrides the Antithesis flags in `.cargo/config.toml`.
- Set `LLVM_PROFILE_FILE=/coverage/<service>/%c%m.profraw`. `%c` writes counters as they change, so the data survives a killed process. `%m` merges restarts into one file. Don't use `%p`: every container's process is PID 1, so a restart overwrites the data.

**Go**

- Build with `go build -cover -covermode=atomic -coverpkg=./...`, and set `GOCOVERDIR=/coverage/<service>`.
- Go writes counters only when `main` returns or the program calls `os.Exit`.

**Other languages**

- Use the standard tool: clang's `-fprofile-instr-generate -fcoverage-mapping` for C and C++ (same `LLVM_PROFILE_FILE` rules as Rust), JaCoCo for Java, `c8` for Node, `coverage.py` for Python.
- Check that the data survives `docker compose stop` and a container restart before trusting it.

## 2. Run the workload

In `docker-compose.coverage.yaml`, also set `ANTITHESIS_SDK_LOCAL_OUTPUT` on the driver:

```yaml
  driver:
    environment:
      ANTITHESIS_SDK_LOCAL_OUTPUT: /tmp/sdk.jsonl
```

The driver's SDK then writes everything it reports to that file: its assertions, and its setup-complete event, `{"antithesis_setup": {"status": "complete", ...}}`.

Nothing runs test commands locally, so start the workload by running the driver's first command yourself, right after `up`. That also checks the command. Running it before setup complete is fine: the driver finds the file as soon as it starts waiting.

Start the coverage build from scratch, let the workload run for a few minutes, then stop the system:

```bash
C="docker compose -f docker-compose.yaml -f docker-compose.coverage.yaml"
$C down -v && $C up -d --build
$C exec driver /opt/antithesis/test/v1/main/first_start_workload
sleep 300
$C cp driver:/tmp/sdk.jsonl .
$C stop
```

If `sdk.jsonl` has no `antithesis_setup` line, the driver never got past its readiness wait. `$C logs driver` shows which nodes it was waiting for.

## 3. Check the behavior

- **Startup.** `the workload starts` was reached.
- **Actions.** Every action reaches its intended outcome sometimes, and none is routinely slow.
- **Assertions.** Only sometimes assertions for situations that need faults are unmet. This lists every assertion that would fail in a run:
  ```bash
  jq -rs '[.[].antithesis_assert // empty] | group_by(.message)[]
    | select(if .[0].assert_type == "sometimes" then any(.hit and .condition) | not
             else any(.hit and (.condition | not)) or (.[0].must_hit and (any(.hit) | not)) end)
    | "\(.[0].display_type)\t\(.[0].message)"' sdk.jsonl
  ```
  An unmet sometimes assertion means the workload doesn't reach that situation: change the actions or their mix.
- **Quiet periods.** One forced on finds the healthy system recovered.
- **System logs.** Every kind of log line you expect arrives.
- **Shutdown.** `docker stop` on a system container shuts its process down cleanly, without a kill.

## 4. Read the coverage

After the system stops, run the language's coverage tool on the `coverage` volume, and list the functions in the system's own source that never ran: `llvm-cov` for Rust, C and C++, and `go tool cover` for Go.

Error-handling and recovery code looks unreached without faults. Leave it to the Antithesis runs.

## 5. Close the gaps

- **A request the workload never sends:** add it to the driver.
- **A rare condition** (an error path or race): act only if a different action mix would make it common.

Repeat until the remaining gaps are rare conditions or out of scope.
