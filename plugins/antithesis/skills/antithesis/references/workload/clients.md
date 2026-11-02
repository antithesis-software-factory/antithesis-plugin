# Client containers

## Why client containers

Client libraries often hold part of the protocol: retry numbering, sessions, leases, multi-step commits, cached routing, batching. The servers' recovery code for these runs only when a client fails partway through, and a hand-written client never runs the library's own retry and recovery code. So run the real library in client containers, faulted like the servers, and have the driver tell them what to do.

Skip client containers only when the system has no client library, or its client keeps nothing between requests. Then the driver sends requests to the servers itself, as in the example in `references/workload/driver.md`.

## The client program

A small long-running program in the library's language holds one client and exposes its operations to the driver, for example over HTTP.

- **Configure the library as production users would.** Randomness and checks belong in the driver.
- **Serve requests concurrently on one shared client,** so batching and pipelining happen. The driver tags each operation with an ID. Send every completion to the driver as an event, `{boot, op_id, outcome}`, to `OUTCOME_ADDR` over UDP, even if the request has stopped waiting. Put the boot identifier in every response too.
- **Answer a health request** that doesn't depend on the servers, for example `GET /health` returning the boot identifier. The driver's startup waits for it.
- **Run it as the container's main process with `restart: on-failure`** (`references/workload/surface.md`), so a kill brings back a fresh client. Run several client containers, since many bugs sit between clients.
- **Forward its logs** (`references/workload/system-logs.md`). Many interesting states sit inside one library call, and sometimes assertions on the logs are the only way to see them.
- **Instrument it** (`references/workload/instrumentation.md`), and measure its coverage locally (`references/workload/local-loop.md`).

How the driver uses the clients is in "Driving client containers" in `references/workload/driver.md`.

## Talking to the servers directly

A direct connection to the servers is a client that never fails. Use one only for:

- the driver's startup waits, admin setup, and other admin or metadata queries,
- read-only checks in quiet periods.

Never use one for actions.
