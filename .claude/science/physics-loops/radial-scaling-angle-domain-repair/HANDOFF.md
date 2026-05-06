# Handoff

## Block

`radial-scaling-angle-domain-repair`, block 01.

## What Changed

- T4 in `docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md`
  now has the required finite-tangent exclusions `rho != 1` and `mu*rho != 1`.
- The T4 proof now derives the exact difference
  `eta*(mu - 1)/((1 - mu*rho)*(1 - rho))`, so equality holds iff `mu = 1`
  on the defined subdomain.
- `scripts/frontier_radial_scaling_protected_angle_narrow.py` now verifies the
  T4 factorization and note domain wording.
- Refreshed runner output is stored in
  `outputs/frontier_radial_scaling_protected_angle_narrow_2026-05-06.txt`.
- Mechanical audit metadata was refreshed so the edited source note hash is
  current and the old `audited_failed` row is archived under
  `previous_audits`; the live row is reset to `unaudited` pending independent
  re-audit.

## Checks

```text
python3 scripts/frontier_radial_scaling_protected_angle_narrow.py
TOTAL: PASS=11, FAIL=0
```

```text
python3 -m py_compile scripts/frontier_radial_scaling_protected_angle_narrow.py
OK
```

```text
python3 docs/audit/scripts/audit_lint.py
OK: no errors
```

The lint command still reports pre-existing repo-wide warnings unrelated to
this row.

## Proposed Status

Branch-local author status: `proposed_retained`.

Do not update repo-wide publication authority surfaces until an independent
audit reruns this row. The known downstream authority surface that still
records the old audit state is
`docs/publication/ci3_z3/DERIVATION_ATLAS_EFFECTIVE_STATUS.md`.

## Next Exact Action

Open a PR against `main` and request independent audit of
`radial_scaling_protected_angle_narrow_theorem_note_2026-05-02`.
