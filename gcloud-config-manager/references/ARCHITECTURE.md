# Architecture: gcloud Multi-Account Management

## 1. Logical Architecture (Data Flow & Responsibility)

```mermaid
flowchart TD
    ENV[Environment File<br/>/mnt/d/conf/.env] -->|GCP_CONFIG_*| SCRIPT[manage_gcloud_configs.py]
    CLI_ARGS[CLI Arguments<br/>--name / --account / --project] --> SCRIPT
    SCRIPT -->|Direct INI Write<br/>No Interactive Prompt| CONFIGS[gcloud Storage<br/>~/.config/gcloud/configurations/]
    CONFIGS --> CFG_BTC[config_btczoa]
    CONFIGS --> CFG_NAN[config_nanbjbank]
    CONFIGS --> CFG_OTH[config_*]
    GCLOUD[gcloud CLI tool] -->|Read Active Profile| CONFIGS
```

## 2. Infrastructure Architecture (File & Permission Boundaries)

- **Config Root:** `/home/<user>/.config/gcloud/configurations/`
- **Active Profile Pointer:** `/home/<user>/.config/gcloud/active_config`
- **Permissions:** User private (`0600` or `0644`), owned by workstation non-root user.
- **Network Boundaries:** Local filesystem operation; no external network egress required to write profiles.
