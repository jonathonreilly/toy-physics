# DM Neutrino Canonical Two-Higgs Slot No-Go

**Date:** 2026-04-15  
**Status:** exact no-go theorem on the full admitted canonical two-Higgs
right-Gram lane at exact source phase  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_canonical_two_higgs_slot_nogo.py`

## Question

The branch already knows:

- the exact `Z_3`-covariant circulant class is physically dead
- the minimal surviving physical carrier is a `Z_3`-basis singlet-doublet slot
  family with one even amplitude `u` and one odd amplitude `v`
- the simplest `2↔3`-symmetric two-Higgs realization is dead too

But maybe that was still too restrictive. Could the **full admitted canonical
two-Higgs lane**

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`

still realize the exact source-phase singlet-doublet carrier?

## Bottom line

No.

On the full canonical right-Gram lane with the exact source phase

`delta = 2 pi / 3`,

exact singlet-doublet slot alignment gives two polynomial conditions whose sum
forces

`x_3 y_3 = 0`.

But the physical heavy-neutrino-basis CP tensor on the same lane is
proportional to `x_3 y_3`.

So the exact source-phase aligned branch on the admitted canonical two-Higgs
lane is structurally CP-empty.

This is the current harshest denominator result on the local neutrino lane:

> full zero-import DM closure cannot come from the admitted canonical
> two-Higgs lane alone.

## Inputs

This note combines:

- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md](./DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md)
- [DM_NEUTRINO_TWO_HIGGS_23_SYMMETRIC_SLOT_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_TWO_HIGGS_23_SYMMETRIC_SLOT_NO_GO_NOTE_2026-04-15.md)

The earlier positive bridge theorem showed that the canonical two-Higgs lane is
the right kind of right-sensitive arena. The singlet-doublet slot theorem then
identified the true physical carrier after the circulant no-go. The symmetric
restricted no-go killed the first obvious realization class. This note tests
the whole canonical lane itself.

## Exact theorem

### 1. Source-phase alignment on the full canonical lane

On the canonical right-Gram lane with `delta = 2 pi / 3`, the exact Hermitian
kernel is

```text
K =
[ x_1^2 + y_3^2       x_1 y_1             x_3 y_3 e^{-2pi i/3} ]
[ x_1 y_1             x_2^2 + y_1^2       x_2 y_2              ]
[ x_3 y_3 e^{+2pi i/3} x_2 y_2            x_3^2 + y_2^2        ].
```

Transforming to the `Z_3` basis and demanding exact alignment to the physical
singlet-doublet carrier gives

- `Im(K_01 e^{+2pi i/3}) = 0`
- `Im(K_02 e^{-2pi i/3}) = 0`

and these reduce exactly to

- `x_1^2 - x_2^2 - x_2 y_2 - 2 x_3 y_3 - y_1^2 + y_3^2 = 0`
- `-x_1^2 + x_2^2 + x_2 y_2 - x_3 y_3 + y_1^2 - y_3^2 = 0`

Adding them gives

`-3 x_3 y_3 = 0`,

so exact source-phase alignment forces

`x_3 y_3 = 0`.

### 2. But the physical CP tensor is proportional to `x_3 y_3`

Move from the `Z_3` basis to the heavy-neutrino mass basis by the exact real
doublet rotation already fixed by the current Majorana stack.

Then the physical CP tensor on the same canonical lane obeys

- `Im[(K_mass)_{01}^2] ∝ x_3 y_3`
- `Im[(K_mass)_{02}^2] ∝ x_3 y_3`

So once exact source-phase alignment forces `x_3 y_3 = 0`, the physical CP
tensor collapses to zero.

Therefore the full admitted canonical two-Higgs lane is exhausted as an exact
source-phase denominator route.

## The theorem-level statement

**Theorem (No-go on the full canonical two-Higgs right-Gram lane at exact
source phase).**
On the admitted canonical two-Higgs Dirac lane with exact source phase
`delta = 2 pi / 3`, exact alignment to the physical singlet-doublet slot
carrier implies `x_3 y_3 = 0`. But the heavy-neutrino-basis CP tensor on that
same lane is proportional to `x_3 y_3`. Therefore the exact aligned branch on
the canonical two-Higgs lane is structurally CP-empty.

## What this closes

This closes the entire admitted canonical two-Higgs rescue class for exact
axiom-native DM closure.

The branch no longer needs to wonder whether:

- a less symmetric point on the same canonical lane might still save the exact
  source-phase route

It does not.

## What this does not close

This note does **not** say the local neutrino lane is useless.

It says something more precise:

- the local neutrino lane was useful enough to isolate the correct physical
  carrier
- but the admitted canonical two-Higgs realization itself cannot supply that
  carrier on the exact source-phase branch

So the remaining positive object must lie beyond the admitted canonical
two-Higgs branch.

## Command

```bash
python3 scripts/frontier_dm_neutrino_canonical_two_higgs_slot_nogo.py
```
