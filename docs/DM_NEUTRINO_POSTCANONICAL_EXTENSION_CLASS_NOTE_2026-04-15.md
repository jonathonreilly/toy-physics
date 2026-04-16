# DM Neutrino Post-Canonical Extension Class

**Date:** 2026-04-15  
**Status:** exact extension-class theorem after the full canonical two-Higgs
source-phase route closes negatively  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_postcanonical_extension_class.py`

## Question

After all the current local denominator routes are exhausted, what is the
smallest honest positive object left?

More precisely:

- universal Dirac bridge: dead
- exact circulant bridge class: dead
- simplest symmetric canonical two-Higgs sublane: dead
- full admitted canonical two-Higgs lane on the exact source-phase branch:
  dead

So what extension class still survives?

## Bottom line

The minimal surviving positive class is now fully specified.

Any future positive exact DM denominator object must be:

- beyond the admitted canonical two-Higgs lane
- right-sensitive at the Hermitian-kernel level
- non-circulant in the `Z_3` basis
- supported on the physical singlet-doublet carrier
- and parameterized minimally by two real slot amplitudes:
  one residual-`Z_2`-even amplitude `u` and one residual-`Z_2`-odd amplitude
  `v`

So the smallest honest remaining object is:

> a non-canonical right-sensitive mixed bridge with two real slot amplitudes
> on the singlet-doublet carrier.

## Inputs

This note packages the exact consequences of:

- [DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md](./DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md)
- [DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_CIRCULANT_MASS_BASIS_NO_GO_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [DM_NEUTRINO_TWO_HIGGS_23_SYMMETRIC_SLOT_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_TWO_HIGGS_23_SYMMETRIC_SLOT_NO_GO_NOTE_2026-04-15.md)
- [DM_NEUTRINO_CANONICAL_TWO_HIGGS_SLOT_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_CANONICAL_TWO_HIGGS_SLOT_NO_GO_NOTE_2026-04-15.md)

## Exact theorem

### 1. Exhausted classes

The following classes are now exact no-go routes:

1. the universal Dirac bridge
2. the exact `Z_3`-covariant circulant bridge class
3. the simplest `2↔3`-symmetric canonical two-Higgs sublane
4. the full admitted canonical two-Higgs lane on the exact source-phase branch

So any future positive object must lie **outside** the admitted canonical local
bank currently in play.

### 2. The physical carrier is still fixed

Even though the old classes die, the physical carrier itself is now sharper
than before.

The exact singlet-doublet CP-slot theorem says the physical denominator tensor
still lives on the `Z_3`-basis singlet-doublet carrier with

- one even slot amplitude `u`
- one odd slot amplitude `v`

and the standard tensor is exactly proportional to `u v`.

So the surviving problem is not a generic new flavor algebra. The carrier and
its slot content are already fixed.

### 3. Minimal surviving positive class

Since the admitted canonical source-phase route is dead but the physical slot
carrier remains fixed, any future positive route must:

- be right-sensitive
- be non-circulant
- live beyond the admitted canonical local class
- and turn on both slot amplitudes `u` and `v`

That is exactly the extension-class statement above.

## The theorem-level statement

**Theorem (Minimal surviving positive denominator class after the full
canonical no-go).**
Assume the exact universal-Yukawa no-go, the exact circulant mass-basis no-go,
the exact singlet-doublet CP-slot theorem, the exact `2↔3`-symmetric canonical
two-Higgs slot no-go, and the exact full canonical two-Higgs slot no-go.
Then any future positive exact DM denominator realization must lie beyond the
admitted canonical two-Higgs lane, remain right-sensitive and non-circulant,
and carry the physical singlet-doublet slot amplitudes `u` and `v`.
Therefore the minimal surviving positive class is a non-canonical
right-sensitive mixed bridge with two real slot amplitudes on the
singlet-doublet carrier.

## What this closes

This closes the extension-class ambiguity again.

The branch no longer needs to say only:

- “some asymmetric two-Higgs realization”

It can now say more sharply:

- the admitted canonical two-Higgs lane is exhausted
- the physical carrier still survives
- so the remaining object is necessarily post-canonical

## What this does not close

This note does **not** derive:

- the microscopic support class of that post-canonical bridge
- the activation law for `u`
- the activation law for `v`
- the final heavy-neutrino-basis epsilon kernel on that future bridge

So it is an extension-class theorem only.

## Command

```bash
python3 scripts/frontier_dm_neutrino_postcanonical_extension_class.py
```
