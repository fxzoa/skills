# TRIGGERS.md: Trigger & Smoke Test Guide (`multi-agent-team`)

## Positive Trigger Examples
1. **Parallel multi-agent refactoring**: "Split these 4 independent skill updates across parallel subagents and aggregate the validation results."
2. **Configure team delegation rules**: "Set up the 4-role multi-agent model delegation (`Coordinator`, `Advisor`, `Reviewer`, `Worker`) in this workspace using `configure_team.py`."
3. **Architecture + security review workflow**: "Have an Advisor (`pro`) design the API boundary, Workers (`flash_lite`) scan the codebase, and a Reviewer (`pro`) audit the final diff."

## Negative Trigger Examples
1. **Single-step file lookup**: "Read `package.json` and tell me the Express version." (Trivial single-step lookup; do not spawn redundant subagents.)
2. **Deploying a Docker stack to a VM**: "Deploy `docker-compose.yml` to my GCE VM." (Use `vm-docker-deploy` instead.)
3. **Creating a standalone HTML architecture diagram**: "Draw a light-themed HTML/SVG architecture diagram." (Use `architecture-diagram` instead.)

## Smoke Test
1. Verify the team configurator script responds cleanly to `--help`:
   ```bash
   python3 -B scripts/configure_team.py --help
   ```
2. Verify `prototype/team.json` is valid JSON and `SKILL.md` passes skill validation:
   ```bash
   python3 -B -c "import json; json.load(open('prototype/team.json'))"
   python3 -B /home/ppbb/.gemini/antigravity-cli/skills/create-new-skill/scripts/validate_skill.py .
   ```
