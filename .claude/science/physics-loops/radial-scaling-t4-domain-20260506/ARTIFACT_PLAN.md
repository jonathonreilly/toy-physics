# Artifact Plan

## Source

- Tighten T4 in `docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md`.
- Tighten T4 checks in `scripts/frontier_radial_scaling_protected_angle_narrow.py`.

## Runner

- Refresh `logs/runner-cache/frontier_radial_scaling_protected_angle_narrow.txt`.

## Audit Compatibility

- Run `bash docs/audit/scripts/run_pipeline.sh`.
- Run `python3 docs/audit/scripts/audit_lint.py --strict`.
- Run `git diff --check`.

## Delivery

- Commit and push the science-fix branch.
- Open or backlog a review PR.
