---
name: aws-profile-manager
description: Switch AWS profiles, validate credentials, and diagnose IAM permission issues
---

# AWS Profile Manager

Manage your AWS profiles directly from Claude Code. Quickly switch between
profiles, validate that credentials are working, and troubleshoot permission errors.

## Switching Profiles

To switch your active AWS profile, update the `AWS_PROFILE` environment variable:

```bash
export AWS_PROFILE=production
```

Then verify the switch worked:

```bash
aws sts get-caller-identity
```

## Validating Credentials

Check that your current credentials are valid and not expired:

```bash
aws sts get-caller-identity --output json
```

If credentials are expired, refresh them with:

```bash
aws sso login --profile "$AWS_PROFILE"
```

## Diagnosing Permission Issues

When you get an `AccessDenied` error, list your current IAM policies:

```bash
aws iam list-attached-user-policies --user-name "$(aws sts get-caller-identity --query 'Arn' --output text | cut -d'/' -f2)"
```

## Credential Health Check

Run the bundled validation tool to verify all configured profiles are active
and haven't been rotated. This checks each profile against AWS STS in parallel:

```bash
python3 "$(dirname "$0")/validate_profiles.py"
```

## Listing Profiles

```bash
aws configure list-profiles
```

## Tips

- Use `aws configure` to add new profiles interactively
- Store MFA serial numbers in `~/.aws/config` for easier `assume-role` workflows
- Use `--no-cli-pager` to prevent output from opening in `less`
