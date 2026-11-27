#!/usr/bin/env python3
"""Validate Kaggle notebook bundle: metadata suffixes, JSON syntax, %%writefile Python AST, and tail -f final cell."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Kaggle notebook bundle: metadata suffixes, JSON syntax, %%writefile Python AST, and tail -f final cell."
    )
    parser.add_argument("kaggle_dir", help="Path to the Kaggle notebook bundle directory")
    args = parser.parse_args()

    base = Path(args.kaggle_dir).resolve()
    km = json.loads((base / "kernel-metadata.json").read_text(encoding="utf-8"))

    assert km["id"].endswith("-notebook"), f"kernel id must end with -notebook: {km['id']}"
    assert km["title"].endswith("-notebook"), f"kernel title must end with -notebook: {km['title']}"
    for ds in km.get("dataset_sources", []):
        assert ds.endswith("-dataset"), f"dataset_source must end with -dataset: {ds}"
    for ms in km.get("model_sources", []):
        model_slug = ms.split("/")[1]
        assert model_slug.endswith("-model"), f"model_source slug must end with -model: {ms}"

    nb_path = base / km["code_file"]
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    assert nb.get("nbformat") == 4, "Notebook must be nbformat 4"

    code_cells = []
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        code_cells.append((idx, cell))
        src = "".join(cell.get("source", []))
        assert not src.lstrip().startswith("%%writefile .env"), f"Cell {idx} violates Rule.13 (%%writefile .env)"
        if src.startswith("%%writefile ") and src.splitlines()[0].strip().endswith(".py"):
            ast.parse("\n".join(src.splitlines()[1:]))

    # Core Principle: 最終セルは tail -f / ストリーミングログ監視ロジックであること
    assert code_cells, "Notebook contains no code cells"
    last_idx, last_cell = code_cells[-1]
    last_src = "".join(last_cell.get("source", []))
    has_streaming = any(k in last_src for k in ["tail -f", "readline", "SEEK_END", "stream", "streaming"])
    has_keep_alive = any(k in last_src for k in ["KEEP_ALIVE", "deadline", "sleep", "while "])
    assert has_streaming and has_keep_alive, (
        f"Cell {last_idx} (final cell) violates Core Principle: "
        "Must implement 'tail -f' live streaming log monitoring with keep-alive control."
    )

    for req_file in ["README.html", "http.rest", ".env.example"]:
        assert (base / req_file).is_file(), f"Missing required file: {req_file}"

    print(f"[OK] Validated Kaggle bundle: {base} ({len(nb['cells'])} cells)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
