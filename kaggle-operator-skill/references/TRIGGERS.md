# TRIGGERS.md: Trigger & Smoke Test Guide (`kaggle-operator`)

## Positive Trigger Examples
1. **Push and monitor a Kaggle notebook**: "Deploy the inference notebook in `./kaggle_llm` to Kaggle Cloud, ensure its dataset/model dependencies exist, and monitor the run until it finishes."
2. **Debug a failing Kaggle kernel**: "My Kaggle kernel failed with Exit Code 137 (OOM). Download the logs with `kaggle-operator`, diagnose the issue, and re-deploy."
3. **Verify Kaggle dependencies before push**: "Check that `dataset_sources` and `model_sources` in `kernel-metadata.json` are published on Kaggle before running `kaggle kernels push`."

## Negative Trigger Examples
1. **Local Jupyter/Colab notebook authoring**: "Create a Google Colab `.ipynb` notebook with an external `.env` file." (Use `colab-notebook` instead.)
2. **Cloud VM Docker deployment**: "Deploy this `docker-compose.yml` stack to a GCE Linux VM." (Use `vm-docker-deploy` instead.)
3. **Pure Python unit testing**: "Write pytest unit tests for a local FastAPI service." (No Kaggle CLI or kernel deployment involved.)

## Smoke Test
1. Verify all Python scripts parse and respond to `--help`:
   ```bash
   python3 -B scripts/deploy_kaggle.py --help
   python3 -B scripts/schedule_kaggle_monitor.py --help
   ```
2. Verify `prototype/kernel-metadata.json` is valid JSON and `SKILL.md` passes skill validation:
   ```bash
   python3 -B -c "import json; json.load(open('prototype/kernel-metadata.json'))"
   python3 -B /home/ppbb/.gemini/antigravity-cli/skills/create-new-skill/scripts/validate_skill.py .
   ```
