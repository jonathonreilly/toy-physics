#!/usr/bin/env bash
# Install per-developer audit-lane git hooks.
#
# Run once per local clone to install the audit-lane pre-commit hook.
# The hook runs the fast subset of the audit pipeline (build_citation_graph
# + seed_audit_ledger + audit_lint) before every commit, catching:
#   - new notes added without a ledger seed,
#   - hash drift on already-audited claims,
#   - hard-rule violations (author-declared retained, missing auditor, etc.).
#
# This is a per-clone setup (git hooks are not under version control).
# The audit-lane CI workflow (.github/workflows/audit.yml) enforces the full
# pipeline on every push and PR; this hook just gives developers fast local
# feedback before they push.
#
# Usage:
#   bash scripts/setup_audit_hooks.sh
#   bash scripts/setup_audit_hooks.sh --uninstall

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
HOOK_SOURCE="${REPO_ROOT}/docs/audit/scripts/pre_commit_audit_check.sh"

# Resolve the actual hooks directory — handles main worktree, secondary
# worktrees (.git is a file pointing at gitdir/.git/worktrees/<name>), and
# explicit core.hooksPath configuration.
HOOKS_DIR="$(git -C "${REPO_ROOT}" rev-parse --git-path hooks)"
HOOK_TARGET="${HOOKS_DIR}/pre-commit"

if [[ "${1:-}" == "--uninstall" ]]; then
  if [[ -L "${HOOK_TARGET}" ]] && [[ "$(readlink "${HOOK_TARGET}")" == *"pre_commit_audit_check.sh" ]]; then
    rm -f "${HOOK_TARGET}"
    echo "Removed ${HOOK_TARGET}"
  elif [[ -e "${HOOK_TARGET}" ]]; then
    echo "Existing pre-commit hook at ${HOOK_TARGET} is not ours. Refusing to remove." >&2
    exit 2
  else
    echo "No pre-commit hook installed; nothing to remove."
  fi
  exit 0
fi

if [[ ! -f "${HOOK_SOURCE}" ]]; then
  echo "FATAL: ${HOOK_SOURCE} not found. Are you in the repo root?" >&2
  exit 1
fi

if [[ ! -x "${HOOK_SOURCE}" ]]; then
  chmod +x "${HOOK_SOURCE}"
  echo "Made ${HOOK_SOURCE} executable."
fi

mkdir -p "${HOOKS_DIR}"

if [[ -e "${HOOK_TARGET}" || -L "${HOOK_TARGET}" ]]; then
  # Be conservative: don't overwrite an existing hook unless it's our own symlink.
  if [[ -L "${HOOK_TARGET}" ]] && [[ "$(readlink "${HOOK_TARGET}")" == *"pre_commit_audit_check.sh" ]]; then
    rm -f "${HOOK_TARGET}"
  else
    echo "Existing pre-commit hook at ${HOOK_TARGET} (not ours). Refusing to overwrite." >&2
    echo "If you want to install ours, back up the existing hook first, then re-run." >&2
    exit 2
  fi
fi

ln -s "${HOOK_SOURCE}" "${HOOK_TARGET}"

echo "Installed audit-lane pre-commit hook:"
echo "  ${HOOK_TARGET} -> ${HOOK_SOURCE}"
echo
echo "The hook runs on every git commit. It is fast (~2 seconds)."
echo "To uninstall: bash scripts/setup_audit_hooks.sh --uninstall"
