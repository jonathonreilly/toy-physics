# PR230 Schur-Complement Complete-Monotonicity Gate

**Status:** bounded support plus exact boundary / `C_x|s` first-shell support is
not strict scalar-LSZ authority

**Runner:** `scripts/frontier_yt_pr230_schur_complement_complete_monotonicity_gate.py`
**Certificate:** `outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json`

## Purpose

The Schur-complement repair gate found one useful finite diagnostic:

```text
C_x|s(q) = det([[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]) / C_ss(q)
```

On chunks001-030 this object decreases from zero mode to first shell, while
raw `C_ss` and `C_s|x` fail that necessary Stieltjes direction.  This block
tests whether that first-shell success is enough to promote `C_x|s` into
strict scalar-LSZ moment/threshold/FV authority.

## Result

It is not enough on the current surface.

The runner records real bounded support:

- `C_x|s` first-shell difference mean
  `-0.01129314476652999`;
- chunk-scatter z score `-459.08170655875074`;
- ready chunks `30/63`.

But the current packet still has only two ordered `q_hat^2` levels:

```text
0.0
0.267949192431123
```

That permits a first-difference check only.  Complete monotonicity would need
higher ordered momentum shells or an analytic moment theorem.  The current
surface also lacks a spectral threshold/measure certificate, isolated
pole/residue/model-class rows, multivolume FV/IR limiting order, and a
canonical `O_H` or W/Z physical-response bridge.

## Non-Claim

This block does not claim retained or `proposed_retained` closure.  It does
not treat `C_x|s` as canonical `O_H`, does not treat a first-shell decrease as
scalar-LSZ authority, does not supply `C_spH/C_HH` pole rows, and does not set
`kappa_s`, `c2`, or `Z_match` to one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_schur_complement_complete_monotonicity_gate.py
# SUMMARY: PASS=15 FAIL=0
```

## Exact Next Action

Use `C_x|s` as a targeted diagnostic while the 63-chunk row packet finishes,
but for closure add higher-shell/multivolume Schur rows plus a pole/threshold
theorem, or supply canonical `O_H/C_spH/C_HH` rows or a genuine W/Z response
bridge.
