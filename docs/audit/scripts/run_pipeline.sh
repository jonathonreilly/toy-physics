#!/usr/bin/env bash
# Run the full audit-lane pipeline end to end.
#
# This script is mechanical and deterministic. It does NOT perform any
# audits — those are done by Codex GPT-5.5 (or any independent auditor)
# using AUDIT_AGENT_PROMPT_TEMPLATE.md, with results applied via
# scripts/apply_audit.py.
#
# Run order:
#   1. build_citation_graph.py    -> data/citation_graph.json
#   2. seed_audit_ledger.py       -> data/audit_ledger.json (preserves
#                                    prior audits if note hash unchanged)
#   3. classify_runner_passes.py  -> data/runner_classification.json
#                                    (heuristic; optional, slow on cold cache)
#   4. compute_effective_status.py-> updates data/audit_ledger.json + summary
#   5. audit_lint.py              -> validates the ledger against hard rules
#   6. render_audit_ledger.py     -> writes AUDIT_LEDGER.md
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
cd "${REPO_ROOT}"

echo "==> 1/9 build_citation_graph.py"
python3 docs/audit/scripts/build_citation_graph.py

echo "==> 2/9 seed_audit_ledger.py"
python3 docs/audit/scripts/seed_audit_ledger.py

echo "==> 3/9 classify_runner_passes.py"
python3 docs/audit/scripts/classify_runner_passes.py

echo "==> 4/9 compute_load_bearing.py"
python3 docs/audit/scripts/compute_load_bearing.py

echo "==> 5/9 compute_effective_status.py"
python3 docs/audit/scripts/compute_effective_status.py

echo "==> 6/9 invalidate_stale_audits.py"
python3 docs/audit/scripts/invalidate_stale_audits.py

# Effective status may need to be recomputed after invalidation.
echo "==> 5/9 (re-run) compute_effective_status.py post-invalidation"
python3 docs/audit/scripts/compute_effective_status.py

echo "==> 7/9 compute_audit_queue.py"
python3 docs/audit/scripts/compute_audit_queue.py

echo "==> 8/9 audit_lint.py"
python3 docs/audit/scripts/audit_lint.py

echo "==> 9/9 render_audit_ledger.py"
python3 docs/audit/scripts/render_audit_ledger.py

echo
echo "Pipeline complete."
echo "  Read docs/audit/AUDIT_LEDGER.md for the rendered ledger."
echo "  Read docs/audit/AUDIT_QUEUE.md   for the next-up audit queue."
