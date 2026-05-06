# Lepton Single-Higgs PMNS Triviality Theorem

**Date:** 2026-04-15
**Status:** exact obstruction theorem on the shared single-Higgs lepton Yukawa
lane
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_lepton_single_higgs_pmns_triviality.py`

## Question

Suppose both lepton Yukawa sectors stay on the same exact class of
single-Higgs fixed-offset `Z_3` support surfaces.

Can charged-lepton misalignment still rescue a nontrivial PMNS matrix even
after the neutrino-side single-Higgs no-mixing theorem?

## Bottom line

No.

Any lepton Yukawa lane with one definite effective `Z_3` offset is monomial:

`Y = D P`

with `D` diagonal and `P` a permutation matrix.

So both the neutrino and charged-lepton single-Higgs lanes satisfy:

- `Y_nu Y_nu^dag` diagonal
- `Y_e Y_e^dag` diagonal

Hence their left diagonalizers are only phases and basis reorderings, and
`|U_PMNS|` is a permutation matrix.

That is incompatible with the observed large PMNS pattern.

So the full single-Higgs lepton-sector rescue route is closed negatively:
**charged-lepton misalignment does not save it.**

## Atlas and axiom inputs

This theorem reuses:

- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — supplies the underlying single-generation matter closure on which
  the three-generation extension and the `Z_3` generation-charge
  structure rest.
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  — supplies the three-generation `Z_3` charge structure used for the
  support analysis on both lepton Yukawa sectors.
- [`NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`](NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md)
  — supplies the upstream Dirac-lane reduction; the Neutrino Dirac
  monomial no-mixing content used in the bottom-line is established
  there together with `NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md`
  on the single-Higgs fixed-offset class.
- [`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md`](NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md)
  — companion theorem giving the three-pattern support reduction on
  the single-Higgs `Z_3` charge condition; the present triviality
  theorem is the PMNS-readout consequence on that same surface.

and keeps the bridge condition explicit:

- both lepton Yukawa sectors live on single-Higgs fixed-offset `Z_3` support
  surfaces

The key point is that the exact support analysis depends only on one effective
offset in `Z_3`. It does not matter whether that offset arose from the Higgs
charge directly or from the conjugated Higgs insertion on the charged-lepton
lane.

## Why the charged-lepton lane is also monomial

On the retained three-generation surface, the left/right generation charges are
the same exact conjugate pair used on the neutrino Dirac lane:

- left: `0,+1,-1`
- right: `0,-1,+1`

For any one fixed effective offset `s in Z_3`, the invariance condition takes
the same exact form

`q_L(i) + s + q_R(j) = 0 mod 3`.

Therefore each row has exactly one allowed target and each column has exactly
one allowed source.

So the charged-lepton Yukawa matrix also has the exact form

`Y_e = D_e P_e`.

Consequently

`Y_e Y_e^dag = D_e D_e^dag`

is diagonal.

So the charged-lepton sector does not supply a hidden single-Higgs left-basis
misalignment either.

## Full single-Higgs PMNS consequence

The neutrino companion theorem already proved that on the single-Higgs
fixed-offset lane,

`Y_nu = D_nu P_nu`

and therefore `Y_nu Y_nu^dag` is diagonal.

Putting the two sectors together:

- `U_nu` is only phases and/or basis reorderings
- `U_e` is only phases and/or basis reorderings

So

`U_PMNS = U_e^dag U_nu`

also has only phases and/or basis reorderings.

Its entrywise magnitude is therefore a permutation matrix.

That does not match the observed PMNS magnitudes, where every row carries
multiple large entries.

## The theorem-level statement

**Theorem (Single-Higgs lepton-sector PMNS triviality).**
Assume the retained one-generation matter closure, the retained
three-generation matter structure, the exact single-Higgs monomial neutrino
Dirac no-mixing theorem, and that the charged-lepton Yukawa lane also lives on
a single-Higgs fixed-offset `Z_3` support surface. Then:

1. the charged-lepton Yukawa matrix is monomial, `Y_e = D_e P_e`
2. `Y_e Y_e^dag` is diagonal
3. both lepton left diagonalizers are trivial up to phases and basis
   reorderings
4. the resulting PMNS matrix is trivial up to phases and basis reorderings

Therefore the observed PMNS structure cannot arise from the full
single-Higgs monomial lepton sector.

## What this closes

This closes the last exact single-Higgs PMNS rescue route.

It is now exact that:

- the single-Higgs neutrino lane alone cannot explain PMNS
- the single-Higgs charged-lepton lane does not rescue PMNS through left
  misalignment
- at least one lepton sector must leave the monomial single-Higgs class

So the remaining exact frontier is no longer "can the whole single-Higgs
lepton sector still work somehow?" The answer is no.

## What this does not close

This note does **not** determine:

- which lepton sector exits the single-Higgs monomial class in nature
- whether the realized extension is neutrino-side, charged-lepton-side, or both
- the actual PMNS angles

The neutrino-side two-Higgs companion shows one exact surviving extension class,
but this note does not claim that class is already derived.

## Safe wording

**Can claim**

- any single-Higgs fixed-offset lepton Yukawa lane is monomial
- the charged-lepton sector does not rescue PMNS on that exact lane
- the full single-Higgs lepton sector yields only trivial PMNS
- at least one lepton sector must exit the monomial single-Higgs class

**Cannot claim**

- the framework already derives which escape route nature uses
- PMNS is numerically closed
- the charged-lepton Yukawa texture is fully derived beyond this exact boundary

## Command

```bash
python3 scripts/frontier_lepton_single_higgs_pmns_triviality.py
```
