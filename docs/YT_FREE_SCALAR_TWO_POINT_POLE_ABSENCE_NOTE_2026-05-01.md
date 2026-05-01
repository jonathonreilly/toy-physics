# Top-Yukawa Free Scalar Two-Point Pole Absence

**Date:** 2026-05-01  
**Status:** exact negative boundary / free source pole absence  
**Runner:** `scripts/frontier_yt_free_scalar_two_point_pole_absence.py`  
**Certificate:** `outputs/yt_free_scalar_two_point_pole_absence_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future interacting scalar kernel theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The free source curvature has no physical scalar pole or canonical kinetic normalization."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The remaining analytic route needs a momentum-dependent scalar two-point
function with a physical pole or canonical kinetic normalization.  This note
checks whether the free Wilson-staggered source curvature already supplies that
object.

## Free Source Bubble

The free logdet source curvature gives the bubble

```text
Pi(p) = sum_k 1 / [(m^2 + D(k)) (m^2 + D(k+p))].
```

On this surface, `Pi(p)` is a finite source curvature.  The inverse curvature
`1/Pi(p)` has no zero; there is no pole denominator.

## Runner Result

```text
python3 scripts/frontier_yt_free_scalar_two_point_pole_absence.py
# SUMMARY: PASS=6 FAIL=0
```

The runner scans two volumes, three masses, and four external momenta.  It
finds finite positive source curvature throughout:

```text
Pi_range = [0.297232, 2.14088]
zero_inverse_count = 0
```

It also verifies that source normalization only rescales the bubble:

```text
Pi[2O] / Pi[O] = 4.
```

## Consequence

The free source generator is exact support for the scalar-curvature formalism,
but it is not a physical scalar pole theorem.  A positive closure route still
needs:

```text
interacting scalar two-point denominator
-> finite-volume / IR limit
-> isolated pole or canonical kinetic term
-> residue and kappa_H
```

This points back to the scalar-channel Bethe-Salpeter/RPA route or to direct
production evidence.

## Non-Claims

- This note does not reject interacting scalar poles.
- This note does not derive `y_t`.
- This note does not use `H_unit` matrix-element authority.
- This note does not use observed top, Higgs, or Yukawa values.
