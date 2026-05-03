# Summary

This physics-loop block repairs the current top audit queue row,
`yt_ward_identity_derivation_theorem`.

The row was critical and ready for claim-type-backfill re-audit, but its ledger
had `deps=[]` even though the note imports several load-bearing authorities.
This PR exposes those dependencies and reframes the row as an open
identification gate rather than a theorem-grade surface.

# Changes

- Add `Claim type: open_gate` author hint to `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`.
- Move prior audit language into history rather than current status authority.
- Convert load-bearing source references to markdown links so the citation
  graph and audit prompt see the actual dependencies.
- Update the runner narrative to support/open-gate wording while preserving
  the 45 algebraic coefficient checks.
- Rerun the audit pipeline and include the generated ledger/queue updates.
- Add a branch-local physics-loop handoff packet.

# Verification

```bash
python3 scripts/frontier_yt_ward_identity_derivation.py
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
python3 -m py_compile scripts/frontier_yt_ward_identity_derivation.py
git diff --check
```

# Audit Result After Pipeline

`yt_ward_identity_derivation_theorem`:

```yaml
claim_type: open_gate
claim_type_provenance: author_hint
audit_status: unaudited
effective_status: unaudited
deps:
  - native_gauge_closure_note
  - left_handed_charge_matching_note
  - yukawa_color_projection_theorem
  - yt_ew_color_projection_theorem
  - yt_vertex_power_derivation
  - minimal_axioms_2026-04-11
```

Independent audit remains required. This PR does not apply an audit verdict.
