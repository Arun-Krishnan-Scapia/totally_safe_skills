# GitHub Actions Security Hardening — Developer Guide

We've enabled zizmor, a static analysis scanner, as a CI check on all GitHub Actions workflows. PRs that contain insecure workflow patterns will now be blocked from merging until the issues are resolved.

This document covers each finding type, why it matters, and how to fix it.

---

## 1. Unpinned Actions (`unpinned-uses`)

Action tags like `@v4` are mutable — an attacker who compromises the upstream repo can silently replace the tag with malicious code. This has happened in the wild (tj-actions/changed-files supply chain attack).

**Vulnerable:**
```yaml
- uses: actions/checkout@v4
- uses: docker://ubuntu
```

**Safe:**
```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
- uses: docker://ubuntu:24.04
```

Find the SHA on the action's GitHub releases page. Add the version as a comment for readability.

---

## 2. Secrets Without Environment (`secrets-outside-env`)

Without a GitHub Environment, there are no protection rules (required reviewers, branch restrictions) gating who or what can access your secrets.

**Vulnerable:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

**Safe:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

`secrets.GITHUB_TOKEN` is exempt. Reach out to the platform team if your environment doesn't exist yet.

---

## 3. Template Injection (`template-injection`)

`${{ }}` expressions in `run:` blocks are interpolated as raw strings before the shell runs — an attacker can inject arbitrary commands via a crafted PR title, issue body, or branch name.

**Vulnerable:**
```yaml
- name: Check title
  run: |
    title="${{ github.event.pull_request.title }}"
    echo "Checking: $title"
```

**Safe:**
```yaml
- name: Check title
  run: |
    title="${PR_TITLE}"
    echo "Checking: $title"
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
```

This applies to all user-controllable contexts: issue titles/bodies, PR titles/bodies, comment bodies, `github.head_ref`, etc. For PowerShell steps, use `${env:PR_TITLE}`.

---

## 4. Leaked Credentials in Artifacts (`artipacked`)

`actions/checkout` stores the `GITHUB_TOKEN` in `.git/config` by default. If a later step uploads the workspace as an artifact, the token leaks publicly.

**Vulnerable:**
```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
```

**Safe:**
```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
  with:
    persist-credentials: false
```

If your workflow needs `git push` after checkout, configure authentication manually and clean up credentials after use.

---

## 5. Excessive Permissions (`excessive-permissions`)

Without an explicit `permissions` block, `GITHUB_TOKEN` gets the repo default (often `write-all`). Workflow-level permissions are inherited by all jobs, even those that don't need them.

**Vulnerable:**
```yaml
name: CI
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: make build
```

**Safe:**
```yaml
name: CI
on: push
permissions: {}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - run: make build
```

Common permissions: `contents: read` (checkout/build), `contents: write` (push/tag), `pull-requests: write` (PR comments), `packages: write` (GHCR), `id-token: write` (OIDC). If you see `Resource not accessible by integration` in logs, add the missing permission.

---

## 6. Dangerous Triggers (`dangerous-triggers`)

`pull_request_target` and `workflow_run` execute in the base repo's context with write access to secrets — but can be triggered by untrusted forks. Checking out fork code here gives an attacker full repository compromise.

**Vulnerable:**
```yaml
on: pull_request_target

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@...
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: make build
```

**Safe:**
```yaml
on: pull_request

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@...
      - run: make build
```

If you genuinely need `pull_request_target` (labeling, commenting), never checkout fork code — only operate on metadata. Replace `workflow_run` with `workflow_call` where possible.

---

## 7. Dependabot Cooldown (`dependabot-cooldown`)

Without a cooldown, Dependabot updates dependencies immediately after release. Compromised packages are often taken down quickly, so immediate updates maximize your exposure window.

**Vulnerable:**
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
```

**Safe:**
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    cooldown:
      default-days: 7
```

---

## 8. Superfluous Actions (`superfluous-actions`)

Third-party actions that duplicate pre-installed CLI tools add unnecessary supply-chain risk.

**Vulnerable:**
```yaml
- uses: softprops/action-gh-release@v1
  with:
    files: dist/*.tar.gz
```

**Safe:**
```yaml
- run: gh release create "${{ github.ref_name }}" dist/*.tar.gz
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Other replacements: `peter-evans/create-pull-request` → `gh pr create`, `peter-evans/create-or-update-comment` → `gh issue comment`, `addnab/docker-run-action` → `docker run`, `dtolnay/rust-toolchain` → `rustup toolchain install`.

---

## 9. Unsafe Environment Writes (`github-env`)

Writing untrusted input to `$GITHUB_ENV` or `$GITHUB_PATH` lets attackers inject environment variables (`LD_PRELOAD`, `NODE_OPTIONS`) or shadow system binaries for all subsequent steps.

**Vulnerable:**
```yaml
- run: echo "BRANCH=${{ github.head_ref }}" >> $GITHUB_ENV
- run: echo "Building $BRANCH"
```

**Safe:**
```yaml
- id: get-branch
  run: echo "branch=${{ github.head_ref }}" >> $GITHUB_OUTPUT
- run: echo "Building $BRANCH"
  env:
    BRANCH: ${{ steps.get-branch.outputs.branch }}
```

Use `$GITHUB_OUTPUT` instead of `$GITHUB_ENV` — outputs are scoped per-step, not global.

---

## 10. Bot Identity Checks (`bot-conditions`)

`github.actor` reflects the last modifier, not the original author — an attacker can spoof it to bypass bot-gated privileged operations like auto-merge.

**Vulnerable:**
```yaml
if: github.actor == 'dependabot[bot]'
```

**Safe:**
```yaml
if: >-
  github.event.pull_request.user.login == 'dependabot[bot]' &&
  github.repository == github.event.pull_request.head.repo.full_name
```

---

## Need Help?

If your workflow has a legitimate reason to use a flagged pattern, reach out to the security team for an exception review.
