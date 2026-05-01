# Top-Yukawa Scalar Pole Determinant Gate

**Date:** 2026-05-01
**Status:** exact-support / scalar pole determinant gate
**Runner:** `scripts/frontier_yt_scalar_pole_determinant_gate.py`
**Certificate:** `outputs/yt_scalar_pole_determinant_gate_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support / scalar pole determinant gate
conditional_surface_status: conditional-support if the interacting scalar-channel denominator and pole derivative are derived or measured
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The determinant gate is exact support, but K(x), K'(pole), and production pole data remain open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Gate

After the FH/LSZ invariant readout theorem, the same-source scalar pole problem
reduces to the interacting denominator:

```text
C_ss(x) = Pi(x) / D(x)
D(x) = 1 - K(x) Pi(x)
D(x_pole) = 0
```

The pole derivative entering the LSZ readout is

```text
dGamma_ss/dp^2 at pole = D'(x_pole) / Pi(x_pole)
D'(x_pole) = -K'(x_pole) Pi(x_pole) - K(x_pole) Pi'(x_pole)
```

Validation:

```text
python3 scripts/frontier_yt_scalar_pole_determinant_gate.py
# SUMMARY: PASS=7 FAIL=0
```

## Result

The free source bubble has no determinant zero.  A scalar-channel
RPA/Bethe-Salpeter denominator can create a pole, but the pole location alone
does not fix the LSZ residue.  Holding `D(x_pole)=0` fixed while varying
`K'(x_pole)` changes the residue and the FH/LSZ readout factor.

Therefore the remaining positive route is sharply specified:

- derive the interacting scalar-channel `K(x)` from the retained
  Wilson-staggered dynamics;
- fix gauge-zero-mode, finite-volume, and IR limiting order;
- prove `D(x_pole)=0` for a physical scalar pole;
- compute or production-measure `D'(x_pole)`;
- insert that derivative into the same-source FH/LSZ invariant readout formula.

## Claim Boundary

This is exact support, not retained closure.  It does not supply `K(x)`, does
not set `kappa_s = 1`, does not use `H_unit` or `yt_ward_identity`, and does
not use observed top/Yukawa values.
