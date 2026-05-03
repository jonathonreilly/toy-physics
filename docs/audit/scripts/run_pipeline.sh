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
#   3. sanitize_legacy_audit_artifacts.py
#                                      -> removes deprecated author-status keys
#   4. classify_runner_passes.py     -> data/runner_classification.json
#                                       (heuristic; optional, slow on cold cache)
#   5. compute_load_bearing.py       -> updates graph criticality metrics
#   6. compute_effective_status.py   -> applies claim_type-based status + summary
#   7. invalidate_stale_audits.py    -> resets stale audit verdicts
#   8. build_cycle_inventory.py      -> data/cycle_inventory.json
#   9. compute_audit_queue.py        -> data/audit_queue.json
#  10. compute_reaudit_candidates.py -> data/reaudit_candidates.json
#  11. audit_lint.py                 -> validates the ledger against hard rules
#  12. render_audit_ledger.py        -> writes AUDIT_LEDGER.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
cd "${REPO_ROOT}"

echo "==> 1/12 build_citation_graph.py"
python3 docs/audit/scripts/build_citation_graph.py

echo "==> 2/12 seed_audit_ledger.py"
python3 docs/audit/scripts/seed_audit_ledger.py

echo "==> 3/12 sanitize_legacy_audit_artifacts.py"
python3 docs/audit/scripts/sanitize_legacy_audit_artifacts.py

echo "==> 4/12 classify_runner_passes.py"
python3 docs/audit/scripts/classify_runner_passes.py

echo "==> 5/12 compute_load_bearing.py"
python3 docs/audit/scripts/compute_load_bearing.py

echo "==> 6/12 compute_effective_status.py"
python3 docs/audit/scripts/compute_effective_status.py

echo "==> 7/12 invalidate_stale_audits.py"
python3 docs/audit/scripts/invalidate_stale_audits.py

# Effective status may need to be recomputed after invalidation.
echo "==> 7b/12 compute_effective_status.py post-invalidation"
python3 docs/audit/scripts/compute_effective_status.py

echo "==> 8/12 build_cycle_inventory.py"
python3 docs/audit/scripts/build_cycle_inventory.py

echo "==> 9/12 compute_audit_queue.py"
python3 docs/audit/scripts/compute_audit_queue.py

echo "==> 10/12 compute_reaudit_candidates.py"
python3 docs/audit/scripts/compute_reaudit_candidates.py

echo "==> 11/12 audit_lint.py"
python3 docs/audit/scripts/audit_lint.py

echo "==> 12/13 render_audit_ledger.py"
python3 docs/audit/scripts/render_audit_ledger.py

echo "==> 13/13 render_publication_effective_status.py"
python3 docs/audit/scripts/render_publication_effective_status.py

echo
echo "Pipeline complete."
echo "  Read docs/audit/AUDIT_LEDGER.md for the rendered ledger."
echo "  Read docs/audit/AUDIT_QUEUE.md   for the next-up audit queue."
echo "  Read docs/audit/data/reaudit_candidates.json for unblocked re-audit candidates."
echo "  Read docs/publication/ci3_z3/PUBLICATION_AUDIT_DIVERGENCE.md for the"
echo "    audit-vs-publication-tables gap report."
echo "  Read docs/publication/ci3_z3/<NAME>_EFFECTIVE_STATUS.md for the audit-"
echo "    derived view of each publication table."
