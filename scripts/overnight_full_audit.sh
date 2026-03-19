#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$REPO_ROOT/logs"
mkdir -p "$LOG_DIR"

RUN_ID="$(date +%Y%m%d_%H%M%S)"
MASTER_LOG="$LOG_DIR/overnight_full_audit_${RUN_ID}.log"

log_line() {
  local message="$1"
  printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S')" "$message" | tee -a "$MASTER_LOG"
}

run_step() {
  local step_name="$1"
  shift
  local step_log="$LOG_DIR/${step_name}_${RUN_ID}.log"
  log_line "[start] ${step_name} -> ${step_log}"
  if "$@" 2>&1 | tee "$step_log"; then
    log_line "[done] ${step_name}"
  else
    local status=$?
    log_line "[fail] ${step_name} status=${status}"
    exit "$status"
  fi
}

cd "$REPO_ROOT"

log_line "overnight full audit started"
run_step py_compile python3 -m py_compile \
  toy_event_physics.py \
  scripts/benchmark_regression_audit.py \
  scripts/post_fix_predictor_audit.py \
  scripts/extended_route_classification_examples.py \
  scripts/threshold_scaling_explanation.py \
  scripts/long_extended_proxy_route_analysis.py \
  scripts/long_degree_profile_fallback_analysis.py \
  scripts/long_mechanism_family_split_analysis.py \
  scripts/long_compact_nonhub_bridge_analysis.py
run_step benchmark_regression_audit python3 scripts/benchmark_regression_audit.py
run_step post_fix_predictor_audit python3 scripts/post_fix_predictor_audit.py
run_step extended_route_examples python3 scripts/extended_route_classification_examples.py
run_step threshold_scaling_explanation python3 scripts/threshold_scaling_explanation.py
run_step long_extended_proxy_route_analysis python3 scripts/long_extended_proxy_route_analysis.py
run_step long_degree_profile_fallback_analysis python3 scripts/long_degree_profile_fallback_analysis.py
run_step long_mechanism_family_split_analysis python3 scripts/long_mechanism_family_split_analysis.py
run_step long_compact_nonhub_bridge_analysis python3 scripts/long_compact_nonhub_bridge_analysis.py
log_line "overnight full audit completed"
