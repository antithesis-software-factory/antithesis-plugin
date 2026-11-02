"""How checks report: settings from the environment, and GitHub annotations.

GITHUB_ACTIONS  set: print findings as GitHub annotations
CHECK_VERBOSE   set: also say what was checked (on by default under GitHub Actions)
CHECK_OFFLINE   set: skip whatever needs the network (the Stop hook sets it)
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOTATE = bool(os.environ.get("GITHUB_ACTIONS"))
VERBOSE = bool(os.environ.get("CHECK_VERBOSE", os.environ.get("GITHUB_ACTIONS")))
OFFLINE = bool(os.environ.get("CHECK_OFFLINE"))


def _escape(value: str, *, property: bool = False) -> str:
    value = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return value.replace(":", "%3A").replace(",", "%2C") if property else value


def error(
    title: str, message: str, file: str | Path, line: int | None = None, col: int | None = None
) -> None:
    """Report one finding: a GitHub annotation under Actions, otherwise path:line:col."""
    path = Path(file)
    rel = (path.relative_to(ROOT) if path.is_absolute() else path).as_posix().removeprefix("./")
    if ANNOTATE:
        props = [f"file={_escape(rel, property=True)}"]
        props += [f"line={line}"] if line else []
        props += [f"col={col}"] if col else []
        props += [f"title={_escape(title, property=True)}"]
        print(f"::error {','.join(props)}::{_escape(message)}", flush=True)
    else:
        where = ":".join(str(p) for p in (rel, line, col) if p)
        print(f"{where}: {message}", flush=True)


def say(message: str) -> None:
    """Print only in verbose mode."""
    if VERBOSE:
        print(message, flush=True)


def run(*args: str | Path, **kwargs) -> subprocess.CompletedProcess:
    """Run a command from the repo root; output goes straight through unless captured."""
    sys.stdout.flush()
    return subprocess.run([str(a) for a in args], cwd=ROOT, text=True, check=False, **kwargs)
