# AGENTS.md

This repo packages the Antithesis skills as one plugin, `plugins/antithesis`, for each agent platform.

## Checks

[mise](https://mise.jdx.dev) installs the tools and runs the checks that CI runs. Run `mise run fix` to apply automatic fixes, then `mise run check` before you finish. `mise tasks` lists each `check:<tool>` and `fix:<tool>` task. In Claude Code, a Stop hook (`.claude/hooks/fix-and-check`) runs both at the end of every turn that changed files. mise only runs a `mise.toml` you trust: run `mise trust` once in each checkout, or add the repo to mise's `trusted_config_paths` setting to cover its worktrees too.
