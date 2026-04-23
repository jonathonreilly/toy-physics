# DM Neutrino Two-Higgs `2↔3`-Symmetric Slot No-Go

**Date:** 2026-04-15
**Status:** exact no-go theorem on the simplest `2↔3`-symmetric canonical
two-Higgs sublane
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_two_higgs_23_symmetric_slot_nogo.py`

## Question

The branch now has a sharper physical CP carrier:

- not the exact circulant class
- but a `Z_3`-basis singlet-doublet slot family with one even amplitude `u`
  and one odd amplitude `v`

Can the **simplest** admitted local two-Higgs extension already realize that
carrier?

More concretely, on the restricted canonical sublane

`x = (a,b,b)`,
`y = (c,d,d)`,
`delta = 2 pi / 3`,

does exact source-phase alignment to the physical singlet-doublet slot family
produce a nonzero leptogenesis tensor?

## Bottom line

No.

On that restricted `2↔3`-symmetric two-Higgs sublane, the exact source-phase
alignment conditions imply

`b d = 0`.

But the physical heavy-neutrino-basis CP tensor on the same sublane is
proportional to `b d`.

So the exact aligned branch collapses back to zero CP.

This is a real route-pruning theorem:

> the simplest `2↔3`-symmetric canonical two-Higgs sublane is exhausted.

Full DM closure now needs a more asymmetric / right-sensitive realization on
the admitted two-Higgs lane.

## Inputs

This note combines:

- [DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md](./DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)

The first note says the local two-Higgs lane is the right kind of carrier
space. The second says what the physical CP carrier looks like after the exact
circulant no-go. This note tests the simplest symmetric sublane against that
new physical target.

## Exact theorem

### 1. Restricted canonical two-Higgs sublane

Take the canonical two-Higgs Dirac lane

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`

and restrict to the simplest `2↔3`-symmetric slice

- `x = (a,b,b)`
- `y = (c,d,d)`
- `delta = 2 pi / 3`

This is the obvious first local attempt after the circulant family fails: keep
the singlet distinguished, keep the doublet paired, and use the exact source
phase.

### 2. Exact source-phase alignment conditions

Transform the Hermitian kernel `K = Y^dag Y` to the `Z_3` basis.

Demanding exact singlet-doublet slot alignment at source phase `phi = 2 pi/3`
is equivalent to requiring

- `Im(K_01 e^{+i phi}) = 0`
- `Im(K_02 e^{-i phi}) = 0`

On the restricted sublane these become the exact polynomial conditions

- `a^2 - b^2 - 3 b d - c^2 + d^2 = 0`
- `-a^2 + b^2 + c^2 - d^2 = 0`

Adding them gives

`-3 b d = 0`,

so exact source-phase alignment forces

`b d = 0`.

### 3. But the physical CP tensor is proportional to `b d`

Moving to the heavy-neutrino mass basis by the exact real doublet rotation,
the physical CP tensor on this restricted sublane obeys

- `Im[(K_mass)_{01}^2] ∝ b d`
- `Im[(K_mass)_{02}^2] ∝ b d`

Therefore the exact aligned branch forced by the previous step is CP-empty.

So the restricted symmetric sublane does not merely “fail to close yet.”
Its exact source-phase aligned realization is structurally zero.

## The theorem-level statement

**Theorem (No-go on the simplest `2↔3`-symmetric canonical two-Higgs sublane).**
On the restricted canonical two-Higgs sublane
`x=(a,b,b)`, `y=(c,d,d)`, `delta = 2 pi / 3`, exact alignment to the physical
singlet-doublet slot carrier implies `b d = 0`. But the heavy-neutrino-basis
CP tensor on that same sublane is proportional to `b d`. Therefore the exact
aligned branch is CP-empty, and this simplest symmetric two-Higgs sublane
cannot close the DM denominator.

## What this closes

This closes another easy rescue class.

The branch no longer needs to wonder whether the simplest “singlet plus
paired doublet” two-Higgs sublane is enough.

It is not.

## What this does not close

This note does **not** say the full two-Higgs lane is dead.

It says something narrower and more useful:

- the admitted two-Higgs lane remains the right arena
- but the final physical activation cannot stay on its simplest
  `2↔3`-symmetric restricted slice

So the remaining theorem target is more asymmetric / right-sensitive than that.

## Command

```bash
python3 scripts/frontier_dm_neutrino_two_higgs_23_symmetric_slot_nogo.py
```
