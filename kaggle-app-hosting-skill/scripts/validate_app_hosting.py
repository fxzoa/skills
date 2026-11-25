#!/usr/bin/env python3
"""Validate Kaggle CPU App Hosting bundle: CPU-only metadata, suffixes, JSON, and %%writefile AST."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Kaggle CPU App Hosting bundle: CPU-only metadata, suffixes, JSON, and %%writefile AST."
    )
    parser.add_argument("kaggle_dir", help="Path to the Kaggle app hosting bundle directory")
    args = parser.parse_args()

    base = Path(args.kaggle_dir).resolve()
    km = json.loads((base / "kernel-metadata.json").read_text(encoding="utf-8"))

    assert km.get("enable_gpu") is False and km.get("enable_tpu") is False, "App hosting must be CPU-only"
    assert km["id"].endswith("-notebook"), f"kernel id must end with -notebook: {km['id']}"
    for ds in km.get("dataset_sources", []):
        assert ds.endswith("-dataset"), f"dataset_source must end with -dataset: {ds}"

    nb = json.loads((base / km["code_file"]).read_text(encoding="utf-8"))
    assert nb.get("nbformat") == 4, "Notebook must be nbformat 4"
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        assert not src.lstrip().startswith("%%writefile .env"), f"Cell {idx} violates Rule.13"
        if src.startswith("%%writefile ") and src.splitlines()[0].strip().endswith(".py"):
            ast.parse("\n".join(src.splitlines()[1:]))

    for req_file in ["README.html", "http.rest", ".env.example"]:
        assert (base / req_file).is_file(), f"Missing required file: {req_file}"

    print(f"[OK] Validated App Hosting bundle: {base} ({len(nb['cells'])} cells)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
