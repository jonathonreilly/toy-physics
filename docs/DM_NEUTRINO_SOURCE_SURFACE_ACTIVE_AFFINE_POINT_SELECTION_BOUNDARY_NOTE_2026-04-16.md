# DM Neutrino Source-Surface Active Affine Point-Selection Boundary

**Date:** 2026-04-16  
**Status:** exact blocker-identification theorem on the live source-oriented sheet  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py`

## Question

After reducing the live source-oriented sheet to the exact active half-plane in
`(delta, q_+)`, can the current exact bank reduce point selection any further?

## Bottom line

No.

On the live source-oriented sheet the active chart is already affine on `H`:

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q
```

with

```text
T_m =
[ 1  0  0 ]
[ 0  0  1 ]
[ 0  1  0 ]

T_delta =
[ 0 -1  1 ]
[-1  1  0 ]
[ 1  0 -1 ]

T_q =
[ 0  1  1 ]
[ 1  0  1 ]
[ 1  1  0 ]
```

and fixed base matrix

```text
H_base =
[ 0,       E1,          -E1 - i gamma ]
[ E1,      0,           -E2           ]
[ -E1+i gamma, -E2,      0            ]
```

where

```text
gamma = 1/2
E1 = sqrt(8/3)
E2 = sqrt(8)/3.
```

So the two active directions are already exact:

- `T_delta`: changes `delta` and `rho` oppositely while keeping
  `delta + rho = E1`
- `T_q`: changes `q_+`, equivalently the even carrier response
  `sigma cos(2v) = sqrt(8)/9 - 3 q_+`

The current exact source-facing bank is blind to both:

- exact source package
- intrinsic CP pair
- intrinsic slot pair
- slot torsion

all stay unchanged along both directions.

Therefore the minimal remaining mainline datum is exactly the 2-real affine
point-selection pair `(delta, q_+)`, equivalently the coefficients of
`(T_delta, T_q)` on the live source-oriented sheet. No smaller current-bank
object remains.

## Inputs

This note sharpens:

- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md)

## Exact theorem

### 1. The active chart is already affine on `H`

On the live source-oriented sheet,

```text
q_+ = sqrt(8/3) - delta + sqrt(r31^2 - 1/4)
```

so

```text
s := q_+ - sqrt(8/3) + delta = sqrt(r31^2 - 1/4) = r31 cos(phi_+).
```

Therefore in the quotient gauge:

```text
d1 = m
d2 = delta
d3 = -delta
r12 = E1 - delta + q_+
r23 = m + q_+ - E2
r31 e^{-i phi_+} = s - i gamma = q_+ - E1 + delta - i gamma.
```

So the Hermitian grammar becomes exactly affine in `(m, delta, q_+)`, with the
fixed matrices `T_m`, `T_delta`, and `T_q` above.

### 2. The two active generators are exact and independent

Changing `delta` at fixed `q_+` gives

```text
H -> H + ddelta T_delta
```

and changing `q_+` at fixed `delta` gives

```text
H -> H + dq T_q.
```

These are linearly independent real Hermitian directions.

Their meanings are exact:

- `T_delta` redistributes the fixed source channel `E1` between `delta` and
  `rho = E1 - delta`
- `T_q` changes the even carrier channel
  `sigma cos(2v) = sqrt(8)/9 - 3 q_+`

while the source package

```text
gamma = 1/2
delta + rho = E1
sigma sin(2v) = 8/9
```

stays fixed.

### 3. The current exact bank is blind to both active directions

The earlier exact theorems already show that on the live source-oriented
sheet:

- the intrinsic CP pair is fixed,
- the intrinsic slot pair is fixed,
- the slot torsion is fixed.

The new point is sharper:

- these exact outputs stay unchanged under `T_delta`,
- and they stay unchanged under `T_q`.

So the current bank sees the active chamber, but it does not see either of the
two active affine coordinates that would pick a point inside it.

## The theorem-level statement

**Theorem (Exact affine point-selection boundary on the live source-oriented
sheet).** Assume the exact active-half-plane, `m`-spectator, intrinsic-slot,
and slot-torsion boundary theorems. Then on the live source-oriented sheet the
active chart is exactly affine on `H`:
`H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`, with fixed
Hermitian generators `T_m`, `T_delta`, and `T_q` as above. The two active
generators are linearly independent and act by:
`T_delta`: redistribution of the fixed source channel `delta + rho = E1`,
`T_q`: change of the even carrier channel
`sigma cos(2v) = sqrt(8)/9 - 3 q_+`.
The current exact source-facing bank remains unchanged along both directions.
Therefore the minimal remaining mainline datum is exactly the 2-real affine
point-selection pair `(delta, q_+)`, equivalently the coefficients of
`(T_delta, T_q)` on the live sheet.

## What this closes

This closes the possibility that the remaining mainline object is hiding
inside some smaller current-bank quotient.

The branch can now say exactly:

- the remaining live datum is not a generic `H` law,
- not a generic 2-real chamber,
- but the exact affine point-selection pair `(delta, q_+)`

and the current bank is blind to both affine generators.

## What this does not close

This note still does **not** derive the post-canonical microscopic law that
selects the affine point `(delta, q_+)`.

It only proves that no smaller current-bank object remains to be reduced
first.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py
```
