# Neutrino Mass Reduction To The Dirac Lane

**Date:** 2026-04-15
**Status:** exact proposed_retained-stack reduction theorem, conditional on the admitted
Higgs / CW electroweak-scalar lane; not a full neutrino-mass closure
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_mass_reduction_to_dirac.py`

## Question

After the retained three-generation Majorana boundary

`M_R,current = 0_(3 x 3)`

is in place, do we still need a genuinely new charge-`2` primitive to close
**neutrino mass in general**?

Or is that only needed if we want a specifically Majorana / seesaw closure?

## Bottom line

A new charge-`2` primitive is needed only for a **Majorana / seesaw** closure.

On the retained stack, neutrino mass in general now reduces to the **Dirac
Yukawa lane**.

More precisely:

1. once the admitted Higgs / CW electroweak-scalar lane supplies the weak
   doublet scalar needed for lepton Yukawas, the one-generation Higgs-assisted
   `L_L <-> nu_R` Dirac channel is gauge-structurally unique
2. on the retained three-generation surface, that lifts to a general complex
   `3 x 3` Dirac Yukawa texture `Y_nu`
3. because the retained current-stack Majorana matrix is exactly zero, the
   current neutrino-mass closure problem reduces to deriving that Dirac Yukawa
   activation law

So the exact retained reduction is:

- Majorana / seesaw closure needs a new charge-`2` primitive
- neutrino mass closure in general does **not**
- the remaining retained-stack mass-closing object is `Y_nu`

## Atlas and axiom inputs

This theorem reuses the canonical atlas toolkit on `main`, specifically:

- `Framework axiom`
- `One-generation matter closure`
- `Three-generation matter structure`
- `Three-generation Majorana current-stack zero matrix`
- `Higgs / CW mass lane`

The first four are exact retained/current-stack inputs.
The Higgs row is explicitly marked in the atlas as an admitted but still
open/bounded electroweak-scalar lane, so this note is a reduction theorem
**conditional on that admitted Higgs lane** rather than a pure zero-input
closure theorem.

## Why the one-generation Dirac channel is unique

On the retained one-generation branch:

- `L_L : (2,1)_{-1}`
- `nu_R : (1,1)_0`

Once the electroweak scalar doublet `H : (2,1)_{+1}` is admitted, the neutrino
Yukawa channel is the unique weak-singlet contraction of two doublets:

`epsilon_ab L_L^a H^b nu_R`

The exact structural points are:

- `SU(3)` is trivial on this lane because `L_L`, `H`, and `nu_R` are color
  singlets
- `SU(2)` singlet contraction of two doublets is one-dimensional
- hypercharge cancels exactly: `-1 + 1 + 0 = 0`

So at one generation, the Higgs-assisted Dirac neutrino channel is unique up
to its coefficient.

## Three-generation lift

The retained three-generation matter structure gives one such channel for every
left/right generation pair.

Without additional `Z_3` information on the Higgs lane, the unresolved Dirac
texture is therefore a general complex `3 x 3` matrix.

That broad statement is now sharpened by the exact support companion
`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*):
if a single Higgs doublet with definite generation `Z_3` charge `q_H` is
admitted, the support of `Y_nu` collapses to one of three exact permutation
patterns, leaving only three coefficient slots on the selected support.

That is sharpened one step further by the exact obstruction companion
[NEUTRINO_DIRAC_MONOMIAL_NO_MIXING_NOTE.md](./NEUTRINO_DIRAC_MONOMIAL_NO_MIXING_NOTE.md):
on that fixed-`q_H` single-Higgs lane, `Y_nu` is monomial, so the neutrino
Dirac sector alone cannot generate nontrivial left mixing. Large PMNS mixing
therefore requires extra structure beyond the fixed-`q_H` monomial lane.

Two exact frontier companions now isolate that extra structure more sharply:

- [NEUTRINO_HIGGS_Z3_UNDERDETERMINATION_NOTE.md](./NEUTRINO_HIGGS_Z3_UNDERDETERMINATION_NOTE.md):
  the current retained stack constrains `q_H` to `{0,+1,-1}` but does not fix
  it
- [NEUTRINO_DIRAC_TWO_HIGGS_ESCAPE_NOTE.md](./NEUTRINO_DIRAC_TWO_HIGGS_ESCAPE_NOTE.md):
  the smallest exact neutrino-side escape from the single-Higgs no-mixing
  theorem is a two-Higgs `Z_3` sector with distinct Higgs charges
- `LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*):
  even allowing charged-lepton misalignment does not rescue the full
  single-Higgs monomial lepton sector; at least one lepton sector must leave
  that class to reproduce PMNS
- `NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md` (downstream
  companion artifact; backticked to avoid length-3 cycle through
  `LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md` — citation graph
  direction is *two_higgs_canonical_reduction → lepton_single_higgs →
  this_reduction*):
  on the minimal surviving neutrino-side class, all distinct two-Higgs charge
  pairs reduce to one canonical support class and the exact remaining gap is
  seven real quantities: six moduli and one phase
- [NEUTRINO_DIRAC_TWO_HIGGS_OBSERVABLE_INVERSE_PROBLEM_NOTE.md](./NEUTRINO_DIRAC_TWO_HIGGS_OBSERVABLE_INVERSE_PROBLEM_NOTE.md):
  on that canonical minimal lane, there is no hidden continuous redundancy;
  deriving those seven canonical quantities is generically equivalent to local
  full Dirac-neutrino closure

So the current retained Dirac unknown is more precisely:

- at coarse resolution: the unresolved `3 x 3` Dirac Yukawa matrix `Y_nu`
- at sharper `Z_3` resolution: the Higgs `Z_3` offset `q_H` plus three
  coefficients on the selected support pattern

And the exact PMNS boundary is now also sharper:

- the full single-Higgs monomial lepton sector is closed negatively
- a realistic PMNS matrix requires at least one lepton sector to exit that lane
- on the minimal surviving neutrino-side lane, the remaining closure gap is
  seven real axiom-side quantities rather than a generic texture family
- and the local inverse problem on that lane is generically well-posed, so no
  additional continuous redundancy remains to be quotiented out

That PMNS boundary is now sharpened one step further on the charged-lepton side
as well:

- [CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md](./CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md):
  if the charged-lepton sector is the first non-monomial lepton lane, its
  minimal surviving branch is also canonical and seven-dimensional
- [CHARGED_LEPTON_TWO_HIGGS_OBSERVABLE_INVERSE_PROBLEM_NOTE.md](./CHARGED_LEPTON_TWO_HIGGS_OBSERVABLE_INVERSE_PROBLEM_NOTE.md):
  on that canonical charged-lepton branch, the seven canonical quantities are
  also locally identifiable from `H_e = Y_e Y_e^dag`
- [NEUTRINO_FULL_CLOSURE_LAST_MILE_REDUCTION_NOTE.md](./NEUTRINO_FULL_CLOSURE_LAST_MILE_REDUCTION_NOTE.md):
  the remaining full-neutrino closure gap is now reduced piecewise on the
  minimal-branch assumption: `7` quantities on the neutrino-side branch, or
  `3 + 7` quantities on the charged-lepton-side branch, with the current atlas
  still not selecting the branch

## Why this answers the “do we need the last stuff?” question

The retained three-generation Majorana theorem already proved:

`M_R,current = 0_(3 x 3)`.

So the current neutral-fermion mass problem is not:

- “find a hidden retained-stack Majorana source just to give neutrinos mass”

Instead it is:

- “derive the retained Dirac Yukawa matrix”

If `Y_nu` closes with `M_R = 0`, the retained stack gives **Dirac neutrino
masses**.

If one wants **Majorana neutrinos** or a **type-I seesaw** specifically, then
yes, one still needs a genuinely new charge-`2` primitive beyond the retained
current stack.

## The theorem-level statement

**Theorem (Retained neutrino-mass reduction to the Dirac lane).**
Assume the framework axiom, retained one-generation matter closure, retained
three-generation matter structure, the retained three-generation Majorana
current-stack law `M_R,current = 0_(3 x 3)`, and the admitted Higgs / CW
electroweak-scalar lane. Then:

1. the one-generation Higgs-assisted neutrino Dirac channel is gauge
   structurally unique
2. the retained three-generation Dirac texture space is `Mat_3(C)`
3. the current retained neutrino-mass problem reduces to the Dirac Yukawa
   activation law `Y_nu`
4. a genuinely new charge-`2` primitive is required only for a Majorana /
   seesaw closure, not for neutrino mass in general

## What this closes

This closes an important planning ambiguity on the neutrino lane.

It is now exact that:

- the retained stack has already exhausted the current Majorana side
- the last Majorana-side primitive is **not** required just to get neutrino
  masses in principle
- the next honest retained-stack science step for neutrino mass closure is the
  neutrino Dirac Yukawa lane

## What this does not close

This note does **not** derive:

- the actual `3 x 3` Dirac Yukawa matrix `Y_nu`
- the absolute neutrino masses
- PMNS angles
- whether nature picks Dirac or Majorana neutrinos

It is a reduction theorem only.

## Safe wording

**Can claim**

- the retained current-stack Majorana problem is closed negatively as
  `M_R,current = 0_(3 x 3)`
- this does not force neutrinos to be massless in principle
- on the admitted Higgs lane, the remaining retained-stack mass-closing object
  is the Dirac Yukawa matrix `Y_nu`
- a new charge-`2` primitive is needed only for Majorana / seesaw closure

**Cannot claim**

- the neutrino masses are now fully derived
- the Dirac Yukawa texture is already closed
- the framework has already chosen Dirac neutrinos over Majorana neutrinos in
  nature

## Command

```bash
python3 scripts/frontier_neutrino_mass_reduction_to_dirac.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `publication/ci3_z3/DERIVATION_ATLAS.md` <!-- cycle-break 2026-05-15: forward ref backticked -->
- [publication.ci3_z3.publication_matrix](publication/ci3_z3/PUBLICATION_MATRIX.md)
