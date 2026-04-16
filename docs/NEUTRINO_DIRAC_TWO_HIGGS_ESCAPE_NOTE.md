# Neutrino Dirac Two-Higgs Escape Theorem

**Date:** 2026-04-15  
**Status:** exact extension-class theorem on the neutrino Dirac lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_dirac_two_higgs_escape.py`

## Question

What is the smallest exact neutrino-side extension that can evade the current
single-Higgs monomial no-mixing theorem?

## Bottom line

A two-Higgs `Z_3` sector with **distinct Higgs charges**.

If the neutrino Dirac matrix is

`Y_nu = D_a P_a + D_b P_b`

with `P_a != P_b` coming from two distinct Higgs `Z_3` charges, then `Y_nu`
is no longer monomial. Generically:

- its support has six entries rather than three
- `Y_nu Y_nu^dag` is non-diagonal
- nontrivial left mixing becomes available

So the smallest exact neutrino-side extension class that survives the current
single-Higgs obstruction is a two-Higgs `Z_3` sector.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Dirac Z_3 support trichotomy`
- `Neutrino Dirac monomial no-mixing theorem`

and adds one exact extension-class input:

- two Higgs doublets with distinct generation `Z_3` charges

## Why one Higgs is still obstructed

The exact single-Higgs theorem says:

`Y_nu = D P_q`

for fixed `q_H`.

Therefore

`Y_nu Y_nu^dag = D D^dag`

is diagonal, so the left mixing is trivial up to phases and permutations.

That closes the one-Higgs lane negatively.

## Why two distinct Higgs charges escape

If two Higgs charges are both active, then

`Y_nu = D_a P_a + D_b P_b`

with `P_a != P_b`.

Because the two permutation supports are disjoint:

- the union support has six entries
- `Y_nu` is not monomial

And because the relative permutation `P_a P_b^dag` is off-diagonal, the cross
terms in

`Y_nu Y_nu^dag`

are generically off-diagonal as soon as both Higgs sectors are turned on with
generic nonzero coefficients.

So the exact one-Higgs no-mixing obstruction no longer applies.

## The theorem-level statement

**Theorem (Minimal two-Higgs escape from the single-Higgs monomial no-mixing
theorem).**
Assume the exact Dirac-`Z_3` support trichotomy and the exact single-Higgs
monomial no-mixing theorem. Then:

1. every fixed-charge single-Higgs neutrino Dirac texture is monomial and has
   trivial left mixing
2. admitting two Higgs doublets with distinct `Z_3` charges produces a Dirac
   texture of the form `Y_nu = D_a P_a + D_b P_b` with `P_a != P_b`
3. such textures are generically non-monomial and generically yield
   non-diagonal `Y_nu Y_nu^dag`

Therefore the smallest exact neutrino-side extension class that can evade the
current no-mixing chain is a two-Higgs `Z_3` sector.

## What this closes

This closes the higher-order / extension-class path to first exact order:

- the minimal neutrino-side PMNS-producing extension class is now isolated

It also says the next neutrino-side structural question is no longer “can one
Higgs do it somehow?” The answer is no. The next question is whether a
two-Higgs `Z_3` sector is actually derived or selected.

## What this does not close

This note does **not** derive:

- the actual Higgs charges
- the Higgs coefficients
- the observed PMNS angles

It is an extension-class theorem only.

## Safe wording

**Can claim**

- one fixed-charge Higgs gives exact no-mixing
- two distinct Higgs charges are the minimal neutrino-side escape
- a two-Higgs sector can generically generate nontrivial left mixing

**Cannot claim**

- the framework already derives the two-Higgs sector
- PMNS is now numerically closed

## Command

```bash
python3 scripts/frontier_neutrino_dirac_two_higgs_escape.py
```
