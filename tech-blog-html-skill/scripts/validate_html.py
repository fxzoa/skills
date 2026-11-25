#!/usr/bin/env python3
"""Validate standalone HTML deliverables (Rule.11: zero CDN scripts, zero Mermaid)."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_html.py <file.html>", file=sys.stderr)
        return 1
    p = Path(sys.argv[1]).resolve()
    text = p.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in text or "<html" in text, "Missing HTML root"
    assert "cdn.jsdelivr.net" not in text and "unpkg.com" not in text, "External CDN forbidden (Rule.11)"
    assert "mermaid" not in text.lower(), "Mermaid forbidden in HTML deliverables (Rule.11)"
    print(f"[OK] Validated standalone HTML: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
