#!/usr/bin/env python3
"""Validate standalone HTML deliverables (Rule.11: zero CDN scripts, zero Mermaid)."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate standalone HTML deliverables (zero external CDNs, zero Mermaid)."
    )
    parser.add_argument("html_file", help="Path to the standalone HTML file to validate.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    p = Path(args.html_file).resolve()
    text = p.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in text or "<html" in text, "Missing HTML root"
    assert "cdn.jsdelivr.net" not in text and "unpkg.com" not in text, "External CDN forbidden (Rule.11)"
    assert "mermaid" not in text.lower(), "Mermaid forbidden in HTML deliverables (Rule.11)"
    print(f"[OK] Validated standalone HTML: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
