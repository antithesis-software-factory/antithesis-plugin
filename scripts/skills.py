"""Where skills live, and how a skill file names the other files it bundles."""

import re
from collections.abc import Iterator
from pathlib import Path

from report import ROOT

SKILL_GLOBS = ["plugins/*/skills/*/SKILL.md", ".agents/skills/*/SKILL.md"]
BUNDLED_DIRS = ("references", "scripts", "assets")
# A path from the skill root, in backticks or as a Markdown link target.
_REFERENCE = re.compile(rf"(?:`|\]\()((?:{'|'.join(BUNDLED_DIRS)})/[^`)\s#]+)")
_PLACEHOLDER = re.compile(r"[<>{}*]")


def skills() -> list[Path]:
    """Every SKILL.md in the repo."""
    return sorted(p for g in SKILL_GLOBS for p in ROOT.glob(g))


def references(text: str) -> Iterator[tuple[int, str]]:
    """Yield (line number, path from the skill root) for each file the text names."""
    for number, line in enumerate(text.splitlines(), 1):
        for match in _REFERENCE.finditer(line):
            target = match.group(1).rstrip(".,:;")
            if not _PLACEHOLDER.search(target):
                yield number, target
