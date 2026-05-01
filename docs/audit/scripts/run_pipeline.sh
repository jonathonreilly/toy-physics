#!/usr/bin/env bash
# Run the full audit-lane pipeline end to end.
#
# This script is mechanical and deterministic. It does NOT perform any
# audits — those are done by Codex GPT-5.5 (or any independent auditor)
# using AUDIT_AGENT_PROMPT_TEMPLATE.md, with results applied via
# scripts/apply_audit.py.
#
# Run order:
#   1. build_citation_graph.py       -> data/citation_graph.json
#   2. seed_audit_ledger.py          -> data/audit_ledger.json (preserves
#                                       prior audits if note hash unchanged)
#   3. classify_runner_passes.py     -> data/runner_classification.json
#                                       (heuristic; optional, slow on cold cache)
#   4. compute_load_bearing.py       -> updates graph criticality metrics
#   5. compute_effective_status.py   -> updates data/audit_ledger.json + summary
#   6. invalidate_stale_audits.py    -> resets stale audit verdicts
#   7. compute_audit_queue.py        -> data/audit_queue.json
#   8. compute_reaudit_candidates.py -> data/reaudit_candidates.json
#   9. audit_lint.py                 -> validates the ledger against hard rules
#  10. render_audit_ledger.py        -> writes AUDIT_LEDGER.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
cd "${REPO_ROOT}"

echo "==> 1/10 build_citation_graph.py"
python3 docs/audit/scripts/build_citation_graph.py

echo "==> 2/10 seed_audit_ledger.py"
python3 docs/audit/scripts/seed_audit_ledger.py

echo "==> 3/10 classify_runner_passes.py"
python3 docs/audit/scripts/classify_runner_passes.py

echo "==> 4/10 compute_load_bearing.py"
python3 docs/audit/scripts/compute_load_bearing.py

echo "==> 5/10 compute_effective_status.py"
python3 docs/audit/scripts/compute_effective_status.py

echo "==> 6/10 invalidate_stale_audits.py"
python3 docs/audit/scripts/invalidate_stale_audits.py

# Effective status may need to be recomputed after invalidation.
echo "==> 6b/10 compute_effective_status.py post-invalidation"
python3 docs/audit/scripts/compute_effective_status.py

echo "==> 7/10 compute_audit_queue.py"
python3 docs/audit/scripts/compute_audit_queue.py

echo "==> 8/10 compute_reaudit_candidates.py"
python3 docs/audit/scripts/compute_reaudit_candidates.py

echo "==> 9/10 audit_lint.py"
python3 docs/audit/scripts/audit_lint.py

echo "==> 10/10 render_audit_ledger.py"
python3 docs/audit/scripts/render_audit_ledger.py

echo
echo "Pipeline complete."
echo "  Read docs/audit/AUDIT_LEDGER.md for the rendered ledger."
echo "  Read docs/audit/AUDIT_QUEUE.md   for the next-up audit queue."
echo "  Read docs/audit/data/reaudit_candidates.json for unblocked re-audit candidates."
