# Audit-Lane CI Templates

This directory contains workflow templates for the audit lane that need to
be installed manually because the bot/OAuth token used by automated commits
does not have the GitHub `workflow` scope required to create or update files
under `.github/workflows/`.

## Installing `audit_workflow.yml`

To enable the audit-lane GitHub Actions workflow on this repo, a user with
push permission and `workflow` token scope (a normal repo collaborator using
their personal access token works) must run:

```bash
mkdir -p .github/workflows
cp docs/audit/templates/audit_workflow.yml .github/workflows/audit.yml
git add .github/workflows/audit.yml
git commit -m "audit: install audit-lane CI workflow"
git push
```

Once installed, the workflow runs on:
- every pull request that touches audit-relevant docs, audit scripts,
  project scripts, or the workflow file,
- a nightly cron at 06:00 UTC,
- manual `workflow_dispatch`.

On scheduled and manual runs the workflow auto-commits regenerated audit-data
and publication-effective-status views back to the checked-out branch as
`audit-bot`. PR runs fail if the pipeline produces a diff (no auto-commit on
PRs to avoid write-permission issues with fork PRs).

See `docs/audit/CI_INTEGRATION.md` for the full integration spec.
