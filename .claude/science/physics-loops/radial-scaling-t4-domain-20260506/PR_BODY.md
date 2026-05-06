# Summary

Closes the radial-scaling T4 missing-derivation gap by making the
finite-tangent subdomain explicit and runner-checked.

## Changes

- T4 now states that the finite tangent claim only applies when
  `rho != 1` and `mu*rho != 1`.
- The proof defines `D_T4` and reduces equality to
  `eta*(mu - 1) = 0` after the denominator guard.
- The runner now checks the denominator and numerator separately.
- The SHA-pinned runner cache is refreshed with `PASS=13, FAIL=0`.
- Audit-derived files were regenerated; the edited claim is correctly reset to
  `unaudited` pending independent audit.

## Verification

- `python3 -m py_compile scripts/frontier_radial_scaling_protected_angle_narrow.py`
- `python3 scripts/frontier_radial_scaling_protected_angle_narrow.py`
- `python3 scripts/cached_runner_output.py scripts/frontier_radial_scaling_protected_angle_narrow.py`
- `bash docs/audit/scripts/run_pipeline.sh`
- `python3 docs/audit/scripts/audit_lint.py --strict`
- `git diff --check`

## Audit Note

This PR does not apply an audit verdict. Independent audit is still required
before effective retained status is restored.
