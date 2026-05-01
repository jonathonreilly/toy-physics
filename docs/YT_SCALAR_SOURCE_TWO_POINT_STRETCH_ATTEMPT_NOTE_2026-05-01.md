# Top-Yukawa Scalar Source Two-Point Stretch Attempt

**Date:** 2026-05-01  
**Status:** exact support / open bridge; no retention proposal  
**Runner:** `scripts/frontier_yt_scalar_source_two_point_stretch.py`  
**Certificate:** `outputs/yt_scalar_source_two_point_stretch_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support / open bridge
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The source-curvature formula is exact support, but the physical scalar pole residue and common dressing remain open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

This is the first 12-hour campaign stretch attempt on the PR #230 key blocker.
It asks how far the scalar source two-point route gets from the minimal allowed
surface:

```text
A_min = retained Cl(3)/Z^3 Wilson-staggered action + structural counts
        + functional derivative definitions.
```

Forbidden inputs remain forbidden: no `H_unit` matrix-element definition of
`y_t_bare`, no observed top mass or Yukawa, no fitted selector, and no
`alpha_LM`/plaquette bridge as a proof input.

## Exact Source-Curvature Formula

Introduce a scalar-bilinear source `J O` into the staggered Dirac determinant:

```text
W[J] = log det(D + m + J O).
```

At `J = 0`, the connected scalar source two-point curvature is

```text
C_OO(p) = - d^2 W / dJ_p dJ_-p
        = - Tr[ G(k) O_p G(k+p) O_-p ],
```

with `G = (D + m)^-1`.  This is a dynamical fermion-bubble object.  It is not
fixed by the group counts `N_c = 3`, `N_iso = 2`, or by SSB bookkeeping.

## Free Wilson-Staggered Stress Test

The runner evaluates the free staggered finite-volume bubble with antiperiodic
time fermion momenta and fits the first three bosonic temporal momenta to

```text
C(p)^-1 = A + B p_hat^2,
Z_proxy = 1 / B.
```

The structural source count fixes

```text
c_source = 1 / sqrt(N_c N_iso) = 1 / sqrt(6).
```

But the residue proxy is not selected to one and is not universal:

| L^3 x T | mass | residue proxy |
|---|---:|---:|
| `6^3 x 12` | `0.10` | `0.415073902876` |
| `6^3 x 12` | `0.25` | `0.337421383982` |
| `6^3 x 12` | `0.50` | `0.192724650348` |
| `6^3 x 12` | `1.00` | `0.009635373019` |
| `8^3 x 16` | `0.10` | `0.406810214752` |
| `8^3 x 16` | `0.25` | `0.359254099430` |
| `8^3 x 16` | `0.50` | `0.234186652284` |
| `8^3 x 16` | `1.00` | `0.022448382770` |
| `10^3 x 20` | `0.10` | `0.386810689300` |
| `10^3 x 20` | `0.25` | `0.352947627218` |
| `10^3 x 20` | `0.50` | `0.244163334349` |
| `10^3 x 20` | `1.00` | `0.028352641956` |

The scan gives a residue spread of `43.078135331639`.  No scanned point is
within `5%` of `1`.

The runner also verifies the source-normalization sanity check:

```text
Z_proxy(2 c_source) / Z_proxy(c_source) = 4.
```

So the source two-point normalization is a real field-normalization datum.  It
cannot be erased by group-count arithmetic.

## Runner Result

```text
python3 scripts/frontier_yt_scalar_source_two_point_stretch.py
# SUMMARY: PASS=12 FAIL=0
```

## Claim Movement

This block moves the PR #230 blocker from:

```text
missing scalar pole residue theorem
```

to the sharper statement:

```text
the retained source calculus gives an exact fermion-bubble curvature, and the
free Wilson-staggered surface does not select kappa_H = 1 or common dressing.
```

The remaining positive theorem is now specifically interacting and dynamical:

1. prove that the interacting `C_OO(p)` has an isolated physical
   Higgs-carrier pole;
2. compute the pole residue `Z_phi` and the source-to-canonical factor
   `kappa_H`;
3. derive or independently measure the relative scalar/gauge dressing.

## Non-Claims

- This note does not rule out a future interacting scalar bound-state theorem.
- This note does not promote the Ward theorem.
- This note does not define `y_t_bare` by an `H_unit` matrix element.
- This note does not use observed `m_t` or `y_t` as a proof input.
- This note does not certify direct production measurement.
