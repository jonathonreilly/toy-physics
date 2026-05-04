#!/usr/bin/env bash
# Fast pre-commit hook for the audit lane.
#
# Runs ONLY the mechanical seeding + lint stages (graph + seed + lint).
# Does NOT run runner classification, load-bearing recompute, or
# invalidation — those belong to the full pipeline run on CI / cron.
#
# Goal: catch obvious problems (new note added without seeding, hash
# drift on an audited claim, hard-rule violation) before commit, in a
# few seconds.
#
# Install:
#   ln -sf ../../docs/audit/scripts/pre_commit_audit_check.sh .git/hooks/pre-commit
#
# Bypass with --no-verify only when you understand the cost.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

STAGED="$(git diff --cached --name-only)"

# Runner cache staleness: if any staged file is a primary runner under
# scripts/, its cache MUST reflect the new SHA-256. Otherwise the
# auditor would read stale evidence — exactly what the cache exists to
# prevent.
if echo "$STAGED" | grep -qE '^scripts/.*\.py$'; then
    if ! python3 scripts/precompute_audit_runners.py --staged-only --check-only; then
        echo "[pre-commit] runner cache STALE for one or more staged runners."
        echo "  Refresh with:"
        echo "    python3 scripts/precompute_audit_runners.py --staged-only"
        echo "  then 'git add logs/runner-cache/' and commit again."
        echo "  (Pass --no-verify only if you understand the audit-evidence cost.)"
        exit 1
    fi
fi

# Quick path: skip ledger checks if no docs/ files are staged.
if ! echo "$STAGED" | grep -qE '^docs/.*\.md$'; then
    exit 0
fi

echo "[pre-commit] audit-lane check"

python3 docs/audit/scripts/build_citation_graph.py >/dev/null
python3 docs/audit/scripts/seed_audit_ledger.py >/dev/null

if ! python3 docs/audit/scripts/audit_lint.py; then
    echo "[pre-commit] audit_lint FAILED"
    echo "  Fix the errors above, or run the full pipeline with"
    echo "    bash docs/audit/scripts/run_pipeline.sh"
    echo "  to refresh the ledger."
    exit 1
fi

# If staging includes the ledger or graph, that's fine. If they were
# updated by this hook but not staged, ask the developer to stage them.
if ! git diff --quiet docs/audit/data/citation_graph.json docs/audit/data/audit_ledger.json 2>/dev/null; then
    echo "[pre-commit] audit ledger or graph updated by seeding."
    echo "  Stage docs/audit/data/citation_graph.json and"
    echo "  docs/audit/data/audit_ledger.json, then commit again."
    exit 1
fi

echo "[pre-commit] audit-lane check OK"
