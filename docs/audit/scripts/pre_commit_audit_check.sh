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

# Quick path: skip if no docs/ files are staged.
if ! git diff --cached --name-only | grep -qE '^docs/.*\.md$'; then
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
