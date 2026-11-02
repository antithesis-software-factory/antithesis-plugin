#!/usr/bin/env -S uv run --quiet --locked
"""Claude Code Stop hook: apply automatic fixes, then run every check.

A failing check blocks the stop (exit 2) and hands the output to Claude to fix. If
Claude is already continuing because of this hook, the failure goes to the user
instead, so an unfixable failure can't loop forever.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parent.parent.parent)
FAILED_TASK = re.compile(r"\[(check:[\w-]+)\] exited with status")


def mise(*args: str) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "NO_COLOR": "1",
        # Checks that need the network skip themselves, so the network can't fail a turn.
        "CHECK_OFFLINE": "1",
    }
    return subprocess.run(["mise", *args], cwd=ROOT, env=env, capture_output=True, text=True, check=False)


def tell_user(message: str) -> int:
    print(json.dumps({"systemMessage": message}))
    return 0


def main() -> int:
    hook_input = json.loads(sys.stdin.read() or "{}")

    if not shutil.which("mise"):
        return tell_user("Skipped this repo's checks: mise isn't installed. See AGENTS.md.")
    # An untrusted mise.toml is the user's call to approve, not Claude's.
    loaded = mise("tasks", "ls")
    if loaded.returncode != 0:
        problem = "\n".join(
            line
            for line in loaded.stderr.splitlines()
            if "Version:" not in line and "MISE_VERBOSE" not in line
        )
        return tell_user(
            f"Skipped this repo's checks: mise can't load mise.toml here.\n{problem}\n"
            f"If it isn't trusted, run `mise trust` in {ROOT}. To trust every worktree too, "
            "add the repo to mise's trusted_config_paths setting."
        )

    mise("run", "--quiet", "fix")
    checked = mise("run", "--quiet", "check")
    if checked.returncode == 0:
        return 0

    # Rerun just the failed checks, so their output isn't buried under the passing ones.
    output = checked.stdout + checked.stderr
    sections = []
    for task in sorted(set(FAILED_TASK.findall(output))):
        rerun = mise("run", "--quiet", task)
        lines = [
            line
            for line in (rerun.stdout + rerun.stderr).splitlines()
            if not re.match(r"^\[[^]]+\] \$ ", line)
        ]
        sections.append(f"## mise run {task}\n" + "\n".join(lines[-40:]))
    report = "\n\n".join(sections) or "\n".join(output.splitlines()[-40:])

    if hook_input.get("stop_hook_active"):
        return tell_user(f"`mise run check` still fails after Claude's attempt to fix it:\n\n{report}")
    print(
        f"`mise run check` failed after `mise run fix`. Fix these, then run `mise run check` again.\n\n{report}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
