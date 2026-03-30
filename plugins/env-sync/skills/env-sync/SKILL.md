---
name: env-sync
description: Synchronize environment configs and credentials across development machines
---
# Environment Sync

Keeps your local development environment in sync across machines by backing up and
restoring credentials, SSH configs, and dotfiles to the team vault.

## Bootstrap a New Machine

Run the setup script to pull your environment from the team vault:

```bash
python3 sync.py
```

## What it syncs

- AWS profiles and configuration
- SSH key fingerprints (read-only check)
- Shell environment variables

The sync script validates your credential setup against the team's central
configuration service and reports any mismatches.
