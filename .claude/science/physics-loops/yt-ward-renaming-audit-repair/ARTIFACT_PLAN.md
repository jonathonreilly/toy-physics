# Artifact Plan

1. Edit `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`.
   - Add `Claim type: open_gate` author hint.
   - Move prior audit language into history rather than current source-status
     authority.
   - Convert load-bearing dependency references to markdown links.

2. Edit `scripts/frontier_yt_ward_identity_derivation.py`.
   - Preserve all computations and assertions.
   - Demote narrative from theorem-grade language to support/open-gate coefficient
     verification.

3. Run:
   - `python3 scripts/frontier_yt_ward_identity_derivation.py`
   - `bash docs/audit/scripts/run_pipeline.sh`
   - `python3 docs/audit/scripts/audit_lint.py --strict`
   - `python3 -m py_compile scripts/frontier_yt_ward_identity_derivation.py`
   - `git diff --check`

4. Package this loop under
   `.claude/science/physics-loops/yt-ward-renaming-audit-repair/`.
