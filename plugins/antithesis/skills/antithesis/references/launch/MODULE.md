# Launch an Antithesis run

Input: a workload to run in Antithesis, and optionally the launcher, compute budget or other parameters to use.

## Steps

1. **Pick the workload.** Work out from context which workload to launch and where its config directory is. If it's unclear, ask.
2. **Build it.** For a Docker Compose workload, run `docker compose build` in the config directory.
3. **Validate it.** Run `snouty validate <config_dir>` and continue only once it passes.
4. **Pick the launcher.** Use the launcher named in context, such as `advanced_test`. If none is named, use `basic_test` for Docker Compose and `basic_k8s_test` for Kubernetes.
5. **Pick the launcher's parameters.** Use the parameters from context. For the compute budget and tier, see `--max-compute-hours` and `--performance-tier` in `snouty launch --help`.
6. **Launch it** with `snouty launch`, and report the run ID from its output to the user. To follow the run, use the triage module.

## Setup timeout

Fuzzing starts only once the workload reports setup complete, so keep setup fast. Raise `--setup-timeout` only if setup genuinely can't finish within the default.
