#!/usr/bin/env python3
"""
Configure multi-model AI team rosters with strict role-based model delegation.
Generates deterministic team configurations matching Rule.15:
- Coordinator / Main: Gemini 3.8 Flash (inherit)
- Advisor: Gemini 4 Carbon (pro)
- Reviewer: Gemini 4 Carbon (pro)
- Worker: Gemini 4 Hydrogen (flash_lite)
"""

from __future__ import annotations

import argparse
import json
import sys

ROSTER_PRESETS = {
    "code-review": {
        "description": "Strict code review, security audits, and verification",
        "roles": [
            {"role": "Coordinator", "model": "inherit", "duty": "Orchestration & user communication"},
            {"role": "Reviewer", "model": "pro", "duty": "Strict code quality and security verification"},
            {"role": "Worker", "model": "flash_lite", "duty": "Linting, grep search, and file inspection"}
        ]
    },
    "architecture": {
        "description": "System architecture design and deep technical advisory",
        "roles": [
            {"role": "Coordinator", "model": "inherit", "duty": "Task definition and delivery"},
            {"role": "Advisor", "model": "pro", "duty": "Architecture trade-off analysis & advisory"},
            {"role": "Worker", "model": "flash_lite", "duty": "Documentation lookups and dependency analysis"}
        ]
    },
    "fullstack": {
        "description": "End-to-end fullstack development pipeline",
        "roles": [
            {"role": "Coordinator", "model": "inherit", "duty": "Feature planning & integration"},
            {"role": "Advisor", "model": "pro", "duty": "API contract & database schema review"},
            {"role": "Reviewer", "model": "pro", "duty": "Verification and regression testing"},
            {"role": "Worker", "model": "flash_lite", "duty": "Component scaffolding & unit tests"}
        ]
    },
    "research": {
        "description": "Broad codebase exploration and targeted search",
        "roles": [
            {"role": "Coordinator", "model": "inherit", "duty": "Synthesis & final reporting"},
            {"role": "Worker-1", "model": "flash_lite", "duty": "Repository search and file parsing"},
            {"role": "Worker-2", "model": "flash_lite", "duty": "Documentation cross-referencing"}
        ]
    }
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure Multi-Agent Team Roster.")
    parser.add_argument("--preset", choices=list(ROSTER_PRESETS.keys()), default="code-review", help="Team preset")
    parser.add_argument("--task", default="", help="Specific task description")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    preset_data = ROSTER_PRESETS[args.preset]
    output = {
        "preset": args.preset,
        "description": preset_data["description"],
        "task": args.task or "General delegation",
        "delegation_rule": "Rule.15 (pro for advisory/review, flash_lite for workers)",
        "roster": preset_data["roles"]
    }

    if args.json:
        print(json.dumps(output, indent=2))
        return 0

    print("==================================================")
    print("Multi-Agent Team Roster: " + args.preset.upper())
    print("Task: " + str(output["task"]))
    print("==================================================")
    for r in preset_data["roles"]:
        role_str = r["role"]
        model_str = r["model"]
        duty_str = r["duty"]
        print(f"  [{role_str}] Model: {model_str} -> {duty_str}")
    print("\n[OK] Team configuration materialized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
