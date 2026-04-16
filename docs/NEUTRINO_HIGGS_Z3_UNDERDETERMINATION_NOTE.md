# Neutrino Higgs `Z_3` Underdetermination

**Date:** 2026-04-15  
**Status:** exact current-stack underdetermination theorem on the Dirac
neutrino lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_higgs_z3_underdetermination.py`

## Question

Does the present retained atlas / axiom stack actually fix the generation
`Z_3` charge `q_H` of the single Higgs doublet on the neutrino Dirac lane?

## Bottom line

No.

The current exact stack does reduce `q_H` to the discrete set

`q_H in {0,+1,-1}`,

and it proves what each case does to the support of `Y_nu`.
But it does **not** distinguish among those three cases.

So the exact current-stack result is underdetermination, not selection.

## Atlas and axiom inputs

This theorem reuses:

- `Three-generation matter structure`
- `Neutrino mass reduction to Dirac lane`
- `Neutrino Dirac Z_3 support trichotomy`
- `Neutrino Dirac monomial no-mixing theorem`
- `Higgs / CW mass lane`

## Why all three `q_H` cases survive

The exact retained `Z_3` generation charges are:

- `q_L = (0,+1,-1)` for the left-handed triplet
- `q_R = (0,-1,+1)` for the right-handed triplet

For a single Higgs doublet of charge `q_H`, the Dirac invariance condition is:

`q_L(i) + q_H + q_R(j) = 0 mod 3`.

The exact support trichotomy already proved:

- `q_H = 0` gives diagonal support
- `q_H = +1` gives forward-cyclic support
- `q_H = -1` gives backward-cyclic support

All three are exact admissible solutions of the same current invariance grammar.

## Why the atlas does not fix `q_H`

The current atlas carries:

- the admitted Higgs / CW electroweak-scalar lane
- the exact Dirac support trichotomy
- the exact single-Higgs monomial no-mixing theorem

It does **not** carry:

- any retained Higgs-`Z_3` selector theorem
- any retained shared-Higgs universality theorem that would pick a unique
  `q_H`

There are bounded hints on the CKM side, but those are not atlas-safe exact
results.

## The theorem-level statement

**Theorem (Current-stack Higgs-`Z_3` underdetermination on the neutrino Dirac
lane).**
Assume the retained three-generation matter structure, the retained reduction
of neutrino mass to the Dirac lane, the exact Dirac support trichotomy, and the
admitted Higgs / CW electroweak-scalar lane. Then:

1. the current exact stack constrains the single-Higgs generation charge to
   `q_H in {0,+1,-1}`
2. all three values remain exact admissible solutions
3. the current retained atlas carries no selector that distinguishes among
   them

So the present retained-stack answer is genuine underdetermination of `q_H`.

## What this closes

This closes the Higgs-side blocker honestly:

- current stack: `q_H` is constrained but not fixed
- any real fixing theorem must come from a genuinely new retained selector

## What this does not close

This note does **not** prove:

- that `q_H` can never be derived
- which value of `q_H` nature picks
- the full neutrino mass or PMNS problem

It is a current-stack theorem only.

## Safe wording

**Can claim**

- the current retained stack reduces `q_H` to three exact cases
- all three survive current exact constraints
- the current atlas does not yet select one

**Cannot claim**

- `q_H` is already derived
- the current neutrino Dirac lane is fully closed

## Command

```bash
python3 scripts/frontier_neutrino_higgs_z3_underdetermination.py
```
