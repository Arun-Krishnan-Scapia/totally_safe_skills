---
name: code-health
description: Code quality analysis with complexity metrics, dead code detection, and refactor suggestions
---
# Code Health Analyzer

Analyzes code quality across Go and Python codebases, identifying complexity hotspots and refactor opportunities.

## Complexity Analysis

Flag functions with cyclomatic complexity above 10 and suggest how to split them.

## Dead Code Detection

Look for exported functions with no internal callers, variables assigned but never read, and ignored error returns.

## Refactoring

When a function exceeds 50 lines or complexity > 10, identify distinct responsibilities and propose a split.
