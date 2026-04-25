# Koide Q moment-map / D-term source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_moment_map_dterm_source_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use a physical neutrality law to set the remaining source scalar:

```text
D-term / moment-map neutrality
  -> center-source moment map is zero
  -> K_TL = 0.
```

## Executable theorem

With normalized center weights:

```text
p_plus + p_perp = 1
```

a moment-map source equation has the form:

```text
mu = p_plus - p_perp = zeta.
```

Thus:

```text
p_plus = (1+zeta)/2
p_perp = (1-zeta)/2.
```

The runner verifies:

```text
K_TL = 0 <=> zeta = 0.
```

The strengthened runner also records the exact residual identity:

```text
K_TL(zeta) = -zeta/(1-zeta^2).
```

## Obstruction

D-flatness minimizes:

```text
V = (mu-zeta)^2 / 2
```

at:

```text
mu = zeta.
```

The auxiliary-field completed-square form gives the same result.  With

```text
V_D = (D - g^2(mu-zeta))^2/(2g^2) + g^2(mu-zeta)^2/2,
```

integrating out `D` gives:

```text
D* = g^2(mu-zeta)
V_eff = g^2(mu-zeta)^2/2.
```

So the formal D-term mechanism does not by itself select the zero level; it
enforces whichever level is supplied.

The level `zeta` is an FI/source parameter unless a retained physical theorem
sets it.  Nonzero levels are admissible and give non-closing sources:

```text
zeta = -1/3 -> u = 1/3, Q = 1,   K_TL = 3/8
zeta =  0   -> u = 1/2, Q = 2/3, K_TL = 0
zeta =  1/3 -> u = 2/3, Q = 1/2, K_TL = -3/8.
```

## Exchange and charge neutrality

An exact center-label exchange would force `zeta=0`, but the retained real
C3 carrier has:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

For general center charges, the neutrality equation:

```text
q_plus p_plus + q_perp p_perp = 0
```

sets:

```text
zeta = -(q_perp + q_plus)/(q_plus - q_perp),
```

so the zero level is again an extra charge/source condition, not a consequence
of the retained data alone.

The strengthened runner also checks that retained anomaly/source-inflow data
have zero derivative in the center-source direction, so the existing anomaly
package supplies no hidden equation for `zeta`.

## Residual

```text
RESIDUAL_SCALAR = moment_map_level_zeta_equiv_center_label_source_u_minus_one_half
RESIDUAL_FI_LEVEL = center_source_D_term_zero_level_not_retained
```

## Why this is not closure

The moment-map mechanism is a serious physical route, but it converts the Q
primitive into the statement that the relevant FI/source level is zero.  A
Nature-grade proof still has to derive that zero level from retained structure.

## Falsifiers

- A retained center-gauge symmetry whose moment-map level is forced to zero by
  gauge invariance or anomaly cancellation.
- A physical charge assignment on the C3 center source that fixes `zeta=0`
  without introducing the target value.
- A retained exchange/charge-conjugation symmetry that survives the rank
  obstruction.

## Boundaries

- Covers normalized two-label D-term/moment-map constraints and general linear
  center-charge neutrality.
- Does not refute a stronger theorem deriving a zero FI/source level.

## Hostile reviewer objections answered

- **"D-terms set moment maps to zero."**  They set them to the chosen level;
  zero level is an additional physical input.
- **"Neutrality should mean zero."**  The runner shows general charges shift
  the neutral level unless the charge/source law is retained.
- **"Use charge conjugation."**  That is the missing exchange symmetry and is
  obstructed on the retained rank-1/rank-2 carrier.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_moment_map_dterm_source_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_MOMENT_MAP_DTERM_SOURCE_NO_GO=TRUE
Q_MOMENT_MAP_DTERM_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=moment_map_level_zeta_equiv_center_label_source_u_minus_one_half
RESIDUAL_FI_LEVEL=center_source_D_term_zero_level_not_retained
```
