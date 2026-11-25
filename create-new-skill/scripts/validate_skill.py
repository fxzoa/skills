#!/usr/bin/env python3
"""Validate that a skill directory conforms to Agent Skills standards and the 11-part Antigravity skill architecture."""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "templates/.gitignore.tmpl",
    "prototype/PROTOTYPE.md",
    "references/TOOLS.md",
    "references/ARCHITECTURE.md",
    "references/CHECKLIST.md",
    "references/GUIDE.md",
    "references/PREREQUISITES.md",
    "references/TRIGGERS.md",
    "references/TROUBLESHOOTING.md",
]
REQUIRED_DIRS = ["scripts", "prototype", "templates", "references"]
REQUIRED_TOOL_CATEGORIES = ["Command", "Shell", "MCP", "外部 API"]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
MAX_SKILL_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    """Parse simple YAML frontmatter delimited by '---' without external dependencies."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return None

    data: dict[str, str] = {}
    current_key: str | None = None
    for line in lines[1:end_idx]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace() and ":" in line:
            key, val = line.split(":", 1)
            current_key = key.strip()
            cleaned = val.strip().strip('"').strip("'")
            data[current_key] = cleaned
        elif current_key and line[0].isspace():
            extra = line.strip()
            data[current_key] = f"{data[current_key]} {extra}".strip()

    body = "\n".join(lines[end_idx + 1 :])
    return data, body


def validate_frontmatter(skill_md: str, base: Path, errors: list[str]) -> None:
    """Validate YAML frontmatter fields against Agent Skills standard."""
    parsed = parse_frontmatter(skill_md)
    if parsed is None:
        errors.append("SKILL.md missing valid YAML frontmatter ('---' block at top of file).")
        return

    meta, _ = parsed
    name = meta.get("name", "")
    desc = meta.get("description", "")

    if not name:
        errors.append("SKILL.md frontmatter missing required field: 'name'.")
    else:
        if not (1 <= len(name) <= 64) or not NAME_PATTERN.match(name):
            errors.append(
                f"SKILL.md frontmatter 'name' ({name!r}) must be 1-64 chars of lowercase alphanumeric and single hyphens."
            )
        if name != base.name:
            errors.append(
                f"SKILL.md frontmatter 'name' ({name!r}) must match parent directory name ({base.name!r})."
            )

    if not desc:
        errors.append("SKILL.md frontmatter missing required non-empty field: 'description'.")
    elif len(desc) > 1024:
        errors.append(f"SKILL.md frontmatter 'description' exceeds 1024 chars ({len(desc)} chars).")


def validate_markdown_links(md_path: Path, base: Path, errors: list[str]) -> None:
    """Ensure local Markdown links resolve cleanly inside the skill directory."""
    text = md_path.read_text(encoding="utf-8")
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().split()[0]
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        file_part = target.split("#", 1)[0]
        if not file_part:
            continue
        resolved = (md_path.parent / file_part).resolve()
        if not resolved.is_relative_to(base):
            errors.append(f"{md_path.relative_to(base)}: link '{target}' escapes skill directory.")
        elif not resolved.exists():
            errors.append(f"{md_path.relative_to(base)}: broken relative link '{target}'.")


def validate_scripts(scripts_dir: Path, errors: list[str]) -> None:
    """Syntax-check and smoke-test '--help' for every Python script in scripts/."""
    for py_file in sorted(scripts_dir.glob("*.py")):
        try:
            source = py_file.read_text(encoding="utf-8")
            ast.parse(source, filename=str(py_file))
        except SyntaxError as exc:
            errors.append(f"Syntax error in {py_file.name} (line {exc.lineno}): {exc.msg}")
            continue

        try:
            res = subprocess.run(
                [sys.executable, "-B", str(py_file), "--help"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if res.returncode != 0:
                errors.append(f"{py_file.name} --help exited with code {res.returncode}.")
        except Exception as exc:
            errors.append(f"Failed running {py_file.name} --help: {exc}")


def validate_skill_dir(base: Path) -> list[str]:
    """Run all validation checks and return a list of error messages."""
    errors: list[str] = []
    if not base.is_dir():
        return [f"Skill directory does not exist: {base}"]

    for d in REQUIRED_DIRS:
        if not (base / d).is_dir():
            errors.append(f"Missing directory: {d}/")
    for f in REQUIRED_FILES:
        if not (base / f).is_file():
            errors.append(f"Missing file: {f}")

    skill_md_path = base / "SKILL.md"
    if skill_md_path.is_file():
        skill_md = skill_md_path.read_text(encoding="utf-8")
        line_count = len(skill_md.splitlines())
        if line_count >= MAX_SKILL_LINES:
            errors.append(f"SKILL.md has {line_count} lines (must be < {MAX_SKILL_LINES} lines).")
        validate_frontmatter(skill_md, base, errors)
        if "## Trigger & Exit Criteria" not in skill_md:
            errors.append("SKILL.md missing '## Trigger & Exit Criteria'.")
        if "## Anti-Patterns" not in skill_md:
            errors.append("SKILL.md missing '## Anti-Patterns'.")
        validate_markdown_links(skill_md_path, base, errors)

    arch_path = base / "references" / "ARCHITECTURE.md"
    if arch_path.is_file():
        arch_md = arch_path.read_text(encoding="utf-8")
        if "```mermaid" not in arch_md:
            errors.append("references/ARCHITECTURE.md missing mermaid diagram.")

    tools_path = base / "references" / "TOOLS.md"
    if tools_path.is_file():
        tools_md = tools_path.read_text(encoding="utf-8")
        for cat in REQUIRED_TOOL_CATEGORIES:
            if cat not in tools_md:
                errors.append(f"references/TOOLS.md missing required category: '{cat}'.")

    scripts_dir = base / "scripts"
    if scripts_dir.is_dir():
        validate_scripts(scripts_dir, errors)

    return errors


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: validate_skill.py <skill_dir>")
        return 0 if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help") else 1

    base = Path(sys.argv[1]).resolve()
    errors = validate_skill_dir(base)
    if errors:
        print(f"[FAIL] Validation failed for {base} ({len(errors)} error(s)):", file=sys.stderr)
        for idx, err in enumerate(errors, 1):
            print(f"  {idx}. {err}", file=sys.stderr)
        return 1

    print(f"[OK] Validated standardized 11-part skill bundle: {base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
