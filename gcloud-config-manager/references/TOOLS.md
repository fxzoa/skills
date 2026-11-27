# Tools Specification: `manage_gcloud_configs.py`

## Tool Classifications (4 Categories)

### 1. Command
- **Command:** `manage_gcloud_configs.py`
- **Path:** `scripts/manage_gcloud_configs.py`
- **Purpose:** Deterministic Python 3 CLI managing multi-account configuration INI profiles without interactive prompts.
- **Operations:**
  - `sync-env --env-file <path>`
  - `set --name <name> --account <email> --project <id> [--zone <zone>] [--region <region>]`
  - `list`
  - `activate <name>`

### 2. Shell
- **Command:** `gcloud config configurations list`
  - Inspect all registered configuration names, active flags, and compute defaults.
- **Command:** `gcloud auth login <email>`
  - Interactive browser login for new profile authentication.

### 3. MCP
- *(Not directly required; local command execution handles all profile writes)*

### 4. 外部 API
- **Google OAuth 2.0 / Cloud Resource Manager API**:
  - Accessed upstream via authenticated `gcloud` commands once credentials are obtained.
