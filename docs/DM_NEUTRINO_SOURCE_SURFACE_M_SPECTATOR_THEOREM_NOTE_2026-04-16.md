# DM Neutrino Source-Surface `m`-Spectator Theorem

**Date:** 2026-04-16
**Status:** exact blocker-reduction theorem on the live source-oriented sheet
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_source_surface_m_spectator_theorem.py`

## Question

Once the live source-oriented `H`-side inverse-image problem is reduced to the
explicit shift-quotient bundle over `(m, delta, r31)`, does every quotient
coordinate remain active for the current exact leptogenesis-facing mainline
data?

## Bottom line

No.

The quotient coordinate `m` is an exact spectator tangent on the live
source-oriented bundle:

```text
H(m + dm, delta, r31) = H(m, delta, r31) + dm T_m

T_m =
[ 1  0  0 ]
[ 0  0  1 ]
[ 0  1  0 ].
```

Along that tangent, all currently exact mainline outputs already stay fixed:

- the exact source-surface values `(gamma, B1, B2)`
- the intrinsic heavy-basis CP pair `(cp1, cp2)`
- the intrinsic `Z_3` singlet-doublet slot pair `(a_*, b_*)`

So the current exact leptogenesis-facing mainline object already factors
through the active bundle over `(delta, r31)`, not the full three-real bundle
over `(m, delta, r31)`.

On the positive carrier chart, define

```text
q_+(delta, r31) = sqrt(8/3) - delta + sqrt(r31^2 - 1/4).
```

Then the active response is already exact:

```text
gamma = 1/2
rho = sqrt(8/3) - delta
sigma sin(2v) = 8/9
sigma cos(2v) = sqrt(8)/9 - 3 q_+.
```

So the live mainline object is already an exact 2-real active bundle over
`(delta, r31)`, equivalently over `(delta, q_+)`, with the quotient coordinate
`m` only a spectator line.

## Inputs

This note sharpens:

- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md)

## Exact theorem

### 1. `m` is an exact spectator tangent on the quotient bundle

In the explicit quotient gauge

```text
d1 = m
d2 = delta
d3 = -delta
phi_+(r31) = asin(1 / (2 r31))
r12 = 2 sqrt(8/3) - 2 delta + r31 cos(phi_+)
r23 = m - delta + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi_+),
```

changing `m` by `dm` changes only:

- `d1 -> d1 + dm`
- `r23 -> r23 + dm`

with every other coordinate fixed.

So

```text
H(m + dm, delta, r31) - H(m, delta, r31) = dm T_m
```

for the fixed Hermitian tangent `T_m` above.

### 2. The current exact mainline outputs are already `m`-invariant

The source-surface values do not depend on `m`:

- `gamma = r31 sin(phi_+) = 1/2`
- `B1 = 2 sqrt(8/3)`
- `B2 = 2 sqrt(8)/3`

The intrinsic CP pair is already fixed by those same values, so it is
`m`-invariant too.

The intrinsic `Z_3` slot pair is already constant on the whole live
source-oriented quotient bundle, so it is `m`-invariant as well.

Therefore the current exact leptogenesis-facing mainline outputs already factor
through `(delta, r31)` alone.

### 3. Positive carrier chart: exact active two-real formulas

On the positive carrier chart already used by the live carrier normal form,

```text
q_+(delta, r31) = sqrt(8/3) - delta + sqrt(r31^2 - 1/4)
```

captures the active even-core response.

Then

- `rho = sqrt(8/3) - delta`
- `gamma = 1/2`
- `sigma sin(2v) = 8/9`
- `sigma cos(2v) = sqrt(8)/9 - 3 q_+`

and these active carrier data are unchanged when `m` moves along the spectator
line inside that chart.

So the live carrier-side response is already an exact 2-real active bundle over
`(delta, q_+)`, equivalently over `(delta, r31)`.

## The theorem-level statement

**Theorem (Exact `m`-spectator reduction on the live source-oriented sheet).**
Assume the exact source-surface, shift-quotient-bundle, intrinsic-slot, and
carrier-normal-form theorems. Then the quotient coordinate `m` is an exact
spectator tangent for the current leptogenesis-facing mainline outputs on the
live source-oriented bundle: changing `m` leaves the exact source-surface data,
the intrinsic CP pair, and the intrinsic `Z_3` slot pair unchanged. Therefore
the live mainline object already reduces from the three-real quotient bundle
over `(m, delta, r31)` to an exact 2-real active bundle over `(delta, r31)`,
equivalently over `(delta, q_+)` on the positive carrier chart.

## What this closes

This closes the live active-role ambiguity of the quotient coordinate `m`.

The branch no longer needs to treat the whole three-real quotient bundle as
equally active for the current leptogenesis-facing theorem stack.

It can say more sharply:

- `m` is spectator
- `(delta, r31)` are the live active quotient coordinates
- equivalently `(delta, q_+)` are the live active carrier coordinates on the
  positive chart

## What this does not close

This note still does **not** derive the post-canonical microscopic law that
selects the active two-real bundle itself from the current axiom bank.

So it is a blocker-reduction theorem, not yet the final constructive selection
law.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_m_spectator_theorem.py
```
