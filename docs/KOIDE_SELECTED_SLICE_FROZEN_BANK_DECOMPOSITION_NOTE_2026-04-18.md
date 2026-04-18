# Koide Selected-Slice Frozen-Bank Decomposition

**Date:** 2026-04-18  
**Status:** exact reduction of the charged-lepton selected slice to the frozen
slot/CP bank plus one real microscopic coordinate  
**Runner:** `scripts/frontier_koide_selected_slice_frozen_bank_decomposition.py`

## Question

After the charged-lepton Koide lane was reduced to the selected line
```text
H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3),
```
how much of the intrinsic `K_Z3` kernel is already fixed by the exact
slot/CP bank, and what actually remains live?

## Bottom line

Everything except one real coordinate is already frozen.

On the exact selected slice `delta = q_+ = sqrt(6)/3`, the `Z_3` kernel is
exactly
```text
K_Z3^sel(m) = K_frozen + m T_m^(K),
```
with
```text
T_m^(K) =
[ 1  0  0 ]
[ 0  0  1 ]
[ 0  1  0 ]
```
and
```text
K_frozen =
[ -2 cp2 - 3 cp1                    a_*                              b_* ]
[ conj(a_*)   3 cp1/2 + cp2 - 1/(2 sqrt(3))   -2 cp2 - i 3 cp2/2 ]
[ conj(b_*)   -2 cp2 + i 3 cp2/2              3 cp1/2 + cp2 + 1/(2 sqrt(3)) ]
```
where `(a_*, b_*)` is the exact intrinsic slot pair and `(cp1, cp2)` is the
exact intrinsic CP pair.

So the charged-lepton microscopic finish line is not a free `2`-real doublet
block anymore. It is the coefficient of one fixed real direction `T_m^(K)`.

## Input stack

This note sharpens:

1. [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
2. [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
3. [DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md)
4. [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
5. [DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md)

## Theorem 1: the selected slice is already anchored to the frozen bank

The intrinsic slot theorem gives
```text
a_* = 2 sqrt(2)/9 - sqrt(3)/12 + i (1/4 + 2 sqrt(2)/3),
b_* = 2 sqrt(2)/9 + sqrt(3)/12 + i (1/4 - 2 sqrt(2)/3),
```
while the intrinsic CP theorem gives
```text
cp1 = -2 sqrt(6)/9,
cp2 =  2 sqrt(2)/9.
```

From these exact constants,
```text
Re(a_* + b_*) = 2 cp2 = 4 sqrt(2)/9,
q_+* = -3 cp1 / 2 = sqrt(6)/3.
```

So the observable-selector slice `q_+* = sqrt(6)/3` is already encoded in the
frozen intrinsic CP constant `cp1`, while the fixed real slot offset on the
doublet block is already encoded in `cp2`.

## Theorem 2: the whole selected kernel is `K_frozen + m T_m^(K)`

The exact `Z_3` doublet-block theorem gives on the live affine chart
```text
K11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3)),
K22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3)),
K12 = m - 4 sqrt(2)/9 + i (sqrt(3) delta - 4 sqrt(2)/3),
K00 = m + 2 q_+ - 4 sqrt(2)/9.
```

Imposing the exact selector slice `delta = q_+ = sqrt(6)/3` and substituting
the bank identities above gives
```text
K11 + K22 = 2 cp2 + 3 cp1,
K11 = 3 cp1/2 + cp2 - 1/(2 sqrt(3)),
K22 = 3 cp1/2 + cp2 + 1/(2 sqrt(3)),
Im K12 = -3 cp2 / 2,
K00 = m - 2 cp2 - 3 cp1,
Re K12 = m - 2 cp2.
```

Therefore the entire selected slice can be written as
```text
K_Z3^sel(m) = K_frozen + m T_m^(K).
```

So the selected slice is not merely "a line in some coordinates". It is an
exact affine line over the frozen slot/CP bank itself.

## Corollary 1: only one real microscopic coefficient survives

Once `(a_*, b_*, cp1, cp2)` are fixed, every selected-slice entry of `K_Z3`
is frozen except the coefficient of `T_m^(K)`.

Equivalently, the remaining charged-lepton datum can be read in any of the
following exactly equivalent ways:

- `m`,
- `Re K12 + 2 cp2`,
- `K00 + 2 cp2 + 3 cp1`,
- the coefficient of `T_m^(K)` in `K_Z3^sel(m)`.

So the live charged-lepton selector is one real coefficient over an otherwise
fully frozen intrinsic bank.

## Why this matters

This is one step tighter than the earlier scalar-selector target note.

That note proved the remaining object was one real scalar on the selected
slice. This note proves more: the entire selected `K_Z3` kernel is already
decomposed exactly into

```text
frozen bank part + one fixed real direction.
```

That is the smallest honest positive target now visible on the charged-lepton
Koide route.

## Consequence

Charged leptons are still not retained-closed today.

But the remaining promotion gap is now fully localized:

```text
derive the coefficient of T_m^(K) on the selected slice.
```

Everything else in the selected kernel is already fixed by exact slot/CP data
that the repo already controls.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_selected_slice_frozen_bank_decomposition.py
```
