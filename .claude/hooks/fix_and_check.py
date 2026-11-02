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
# A finding: `path:line[:col]: message` or `path:line[:col] error ...`.
LOCATION = re.compile(r"^\S+:\d+(:\d+)?[: ]")


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

    # Report only each failed check's findings (`path:line: message` lines), not its full
    # output. Claude can run the check itself for more context.
    # `mise run check` prefixes each subtask's lines with `[check] `.
    output = "\n".join(
        line.removeprefix("[check] ") for line in (checked.stdout + checked.stderr).splitlines()
    )
    failed = sorted(set(FAILED_TASK.findall(output)))
    sections = []
    for task in failed:
        prefix = f"[{task}] "
        lines = [line.removeprefix(prefix) for line in output.splitlines() if line.startswith(prefix)]
        findings = [line for line in lines if LOCATION.match(line)]
        if not findings:
            findings = [line for line in lines if not line.startswith(("$ ", "ERROR"))][-5:]
        sections.append(f"{task}:\n" + "\n".join(f"  {line}" for line in findings))
    report = "\n".join(sections) or "\n".join(output.splitlines()[-10:])
    rerun = " or ".join(f"`mise run {task}`" for task in failed) or "`mise run check`"
    report += f"\n\nRun {rerun} for the full output."

    if hook_input.get("stop_hook_active"):
        return tell_user(f"`mise run check` still fails after Claude's attempt to fix it:\n\n{report}")
    print(
        f"`mise run check` failed after `mise run fix`. Fix these, then run `mise run check` again.\n\n{report}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
