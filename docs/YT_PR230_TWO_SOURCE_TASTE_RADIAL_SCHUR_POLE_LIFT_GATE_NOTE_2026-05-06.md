# PR230 Two-Source Taste-Radial Schur Pole-Lift Gate

**Status:** exact negative boundary / finite Schur A/B/C rows do not lift to
strict pole-row authority without model-class, pole, and FV/IR authority
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_schur_pole_lift_gate.py`
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json`

The finite Schur A/B/C row certificate computes inverse-block rows at the
zero mode and first nonzero momentum shell.  This gate asks whether those
endpoint rows can be promoted to strict neutral-kernel A/B/C pole rows or
`K'(pole)` authority.

They cannot on the current surface.  Even under the favorable assumption that
the zero-mode point is the pole, two endpoint values do not determine the pole
derivative.  For any measured row value pair `(f(0), f(dp))`, the family

```text
f_lambda(x) = f(0) + ((f(dp)-f(0))/dp) x + lambda x (x-dp)
```

matches both endpoint values for every `lambda`, while
`f_lambda'(0) = (f(dp)-f(0))/dp - lambda dp` changes with `lambda`.

The runner applies this endpoint-preserving witness to the measured finite
`A_f`, `B_f`, and `C_f` rows from chunks001-030.  It therefore keeps the
finite-row support, but blocks treating finite endpoint secants or finite
inverse rows as strict pole derivatives.

The current blockers are:

- `ready=30/63`, no combined 63/63 row packet;
- Schur kernel row contract still open;
- strict neutral-kernel A/B/C pole rows absent;
- isolated-pole derivative rows absent;
- FV/IR zero-mode authority absent;
- canonical `O_H` identity absent;
- endpoint values do not determine derivatives.

This is a stricter Schur-route firewall, not closure.  It does not claim
retained/proposed_retained status, does not set `kappa_s=1`, and does not use
`H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or
`u0`.

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_pole_lift_gate.py
# SUMMARY: PASS=13 FAIL=0
```
