#!/usr/bin/env python3
"""
link_skills.py - Deterministic workspace and global skill linker for Antigravity.
Links all valid skills from /mnt/d/skills to:
1. /mnt/d/.agents/skills/ (Workspace scope)
2. ~/.gemini/config/skills/ (Global scope)
"""

import os
import sys
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Link Antigravity skills into workspace and global configurations.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without modifying system.")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.dry_run:
        print("[*] Dry run mode enabled.")
        return

    src_dir = Path("/mnt/d/skills")
    if not src_dir.exists():
        print(f"[!] Error: Source skills directory {src_dir} not found.", file=sys.stderr)
        sys.exit(1)

    home = Path.home()
    workspace_skills = Path("/mnt/d/.agents/skills")
    global_skills = home / ".gemini" / "config" / "skills"

    workspace_skills.mkdir(parents=True, exist_ok=True)
    global_skills.mkdir(parents=True, exist_ok=True)

    count = 0
    for child in src_dir.iterdir():
        if child.is_dir() and (child / "SKILL.md").exists():
            skill_name = child.name
            
            # Link to workspace
            ws_link = workspace_skills / skill_name
            if ws_link.exists() or ws_link.is_symlink():
                ws_link.unlink()
            ws_link.symlink_to(child)

            # Link to global
            gb_link = global_skills / skill_name
            if gb_link.exists() or gb_link.is_symlink():
                gb_link.unlink()
            gb_link.symlink_to(child)

            count += 1
            print(f"[*] Linked skill '{skill_name}' -> workspace & global")

    print(f"[OK] Successfully linked {count} skills.")

if __name__ == "__main__":
    main()
