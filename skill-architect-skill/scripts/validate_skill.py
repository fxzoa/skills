#!/usr/bin/env python3
"""Validate that a skill directory conforms to the standardized 10-part skill architecture."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "templates/.gitignore.tmpl",
    "references/TOOLS.md",
    "references/ARCHITECTURE.md",
    "references/CHECKLIST.md",
    "references/GUIDE.md",
    "references/PREREQUISITES.md",
    "references/TROUBLESHOOTING.md",
]
REQUIRED_DIRS = ["scripts", "prototype", "templates", "references"]
REQUIRED_TOOL_CATEGORIES = ["Command", "Shell", "MCP", "外部 API"]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_skill.py <skill_dir>", file=sys.stderr)
        return 1

    base = Path(sys.argv[1]).resolve()
    for d in REQUIRED_DIRS:
        assert (base / d).is_dir(), f"Missing directory: {d}/"
    for f in REQUIRED_FILES:
        assert (base / f).is_file(), f"Missing file: {f}"

    skill_md = (base / "SKILL.md").read_text(encoding="utf-8")
    assert "## Trigger & Exit Criteria" in skill_md, "SKILL.md missing '## Trigger & Exit Criteria'"
    assert "## Anti-Patterns" in skill_md, "SKILL.md missing '## Anti-Patterns'"

    arch_md = (base / "references" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "```mermaid" in arch_md, "ARCHITECTURE.md missing mermaid diagram"

    tools_md = (base / "references" / "TOOLS.md").read_text(encoding="utf-8")
    for cat in REQUIRED_TOOL_CATEGORIES:
        assert cat in tools_md, f"references/TOOLS.md missing required category: '{cat}'"

    for py_file in (base / "scripts").glob("*.py"):
        py_compile.compile(str(py_file), doraise=True)

    print(f"[OK] Validated 10-part skill bundle: {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
