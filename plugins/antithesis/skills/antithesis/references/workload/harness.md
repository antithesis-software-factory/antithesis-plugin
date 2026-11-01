# Wire up the harness

Every service in `docker-compose.yaml` needs an explicit `image:`. snouty rejects services without one.

## 1. The driver container

Build the driver into its own image, and add it to `docker-compose.yaml` as a service named `driver`. The driver binary is the container's main process (`references/workload/driver.md`).

```yaml
  driver:
    container_name: driver
    hostname: driver
    platform: linux/amd64
    build:
      context: .
      dockerfile: driver/Dockerfile
    image: driver:latest
    environment:
      KV_URLS: http://kv1:8000,http://kv2:8000
```

`driver/Dockerfile`:

```dockerfile
FROM rust:1-bookworm AS build
WORKDIR /src
COPY driver/ .
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=build /src/target/release/driver /usr/local/bin/
COPY --chmod=755 driver/first_start_workload /opt/antithesis/test/v1/main/
CMD ["/usr/local/bin/driver"]
```

## 2. The test template

The driver image's test template, `/opt/antithesis/test/v1/main/`, holds exactly one test command, `first_start_workload`. No other container has a test template. The directory name `main` is the test name; any name works.

`driver/first_start_workload`, executable:

```sh
#!/bin/sh
touch /workload-active
```

Antithesis runs the first command once at the start of every timeline, after setup complete and the root snapshot, in the container that holds it. So the file appears exactly when fuzzing starts, and every timeline starts from a snapshot without it.

Test commands must be executable. `snouty validate` reports any that aren't.

## 3. Client containers

Add one service per client container (`references/workload/clients.md`), built from the client program:

```yaml
  client1:
    container_name: client1
    hostname: client1
    platform: linux/amd64
    build:
      context: .
      dockerfile: client/Dockerfile
    image: client:latest
    restart: on-failure
    environment:
      KV_URLS: http://kv1:8000,http://kv2:8000
      LOG_FORWARD_ADDR: driver:7777
      OUTCOME_ADDR: driver:7778
```

`OUTCOME_ADDR` is where the client program sends its completion events. Point the driver at the clients, for example with `CLIENT_URLS: http://client1:8080,http://client2:8080` on the driver. The driver keeps `KV_URLS` for readiness, admin setup and quiet-period reads.

## 4. Shared volumes

For out-of-band facts ("Shared volumes for out-of-band facts" in `references/workload/driver.md`), mount one named volume in the node that writes and in the driver:

```yaml
  kv1:
    volumes: [shared:/shared]
  driver:
    volumes: [shared:/shared]
volumes:
  shared:
```

## 5. Exclude the driver from faults

Launch every run of the workload with the `advanced_test` launcher, following `references/launch/MODULE.md`, and these parameters, which exclude the driver container from faults:

```bash
--param 'custom.network_fault_exclusion_patterns=^driver$'
--param custom.container_status_fault_exclusions=driver
--param custom.container_cpu_fault_exclusions=driver
```

The container and CPU exclusions take exact container names. The network exclusion is a regex: for several containers use `^a$|^b$`, without parentheses, which a bug breaks. Exclude only the driver: client containers are there to be faulted.
