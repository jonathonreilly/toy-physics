# PR230 Schur C_x|s One-Pole Finite-Residue Scout

**Status:** bounded-support / `C_x|s` one-pole finite-residue scout; no scalar-LSZ pole authority

**Runner:** `scripts/frontier_yt_pr230_schur_x_given_source_one_pole_scout.py`
**Certificate:** `outputs/yt_pr230_schur_x_given_source_one_pole_scout_2026-05-07.json`

## Result

The current chunks001-036 Schur residual

```text
C_x|s(q) = det([[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]) / C_ss(q)
```

is positive and decreases from the zero mode to the first shell.  The two
endpoint means determine the unique one-pole interpolation
`C(x)=R/(x+m^2)`:

- `C(0) = 0.28084214641236205`;
- `C(0.267949192431123) = 0.26954854925501315`;
- implied `m^2 = 6.395244587492961`;
- implied `R = 1.796054216783564`.

This is useful finite-row targeting information for future higher-shell or
multivolume Schur diagnostics.  It is not pole-residue authority.

## Model-Class Boundary

The runner also constructs positive two-pole Stieltjes families matching the
same two endpoint values.  The low-pole residue fraction can change from about
`0.0124` to `0.1734` of the one-pole residue in the displayed witnesses while
the two measured endpoints remain fixed.  Therefore the one-pole residue is a
model-class assumption, not a consequence of the current packet.

Closure still requires higher momentum shells or an analytic complete
monotonicity theorem, threshold/contact authority, isolated-pole/FV/IR control,
and either canonical `O_H/C_spH/C_HH` source-overlap authority or a genuine
W/Z physical-response bridge.

## Verification

```bash
python3 scripts/frontier_yt_pr230_schur_x_given_source_one_pole_scout.py
# SUMMARY: PASS=13 FAIL=0
```

## Non-Claim

This block does not claim retained or `proposed_retained` closure.  It does
not treat the one-pole interpolation as a physical scalar pole, does not
treat `C_x|s` as canonical `O_H`, does not supply `C_spH/C_HH` rows or W/Z
response rows, and does not set `kappa_s`, `c2`, or `Z_match` to one.
