---
name: git-workflow
description: Smart git branch management, PR summaries, and merge conflict resolution
---
# Git Workflow Assistant

Helps with common git tasks: writing PR descriptions, naming branches, and resolving conflicts.

## PR Descriptions

Run `git log origin/main..HEAD --oneline` then write a structured description with Summary, Changes, and Testing sections.

## Branch Naming

Pattern: `<type>/<ticket-id>-<short-description>`
Types: `feat`, `fix`, `chore`, `refactor`, `docs`

## Conflict Resolution

Explain what each side changed, propose the correct merge, and flag any tests that need updating.
