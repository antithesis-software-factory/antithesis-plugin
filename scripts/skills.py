"""What scripts/check-references and scripts/token-report share: where skills live, and
how a skill file names the other files it bundles."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_GLOBS = ["plugins/*/skills/*/SKILL.md", ".agents/skills/*/SKILL.md"]
BUNDLED_DIRS = ("references", "scripts", "assets")
# A path from the skill root, in backticks or as a Markdown link target.
_REFERENCE = re.compile(r"(?:`|\]\()((?:%s)/[^`)\s#]+)" % "|".join(BUNDLED_DIRS))
_PLACEHOLDER = re.compile(r"[<>{}*]")


def skills() -> list[Path]:
    """Every SKILL.md in the repo."""
    return sorted(p for g in SKILL_GLOBS for p in ROOT.glob(g))


def references(text: str):
    """Yield (line number, path from the skill root) for each file the text names."""
    for number, line in enumerate(text.splitlines(), 1):
        for match in _REFERENCE.finditer(line):
            target = match.group(1).rstrip(".,:;")
            if not _PLACEHOLDER.search(target):
                yield number, target
