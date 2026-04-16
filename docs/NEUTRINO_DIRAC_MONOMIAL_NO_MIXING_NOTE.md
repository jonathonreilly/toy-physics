# Neutrino Dirac Monomial No-Mixing Theorem

**Date:** 2026-04-15  
**Status:** exact obstruction theorem on the retained single-Higgs Dirac
neutrino lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_dirac_monomial_no_mixing.py`

## Question

Suppose the retained neutrino Dirac lane is restricted to:

- the exact `Z_3` support trichotomy, and
- one single Higgs doublet with fixed `Z_3` charge `q_H`.

Can that neutrino Dirac sector by itself generate nontrivial left mixing and
hence a realistic PMNS matrix?

## Bottom line

No.

For fixed `q_H`, the exact support theorem already says:

`Y_nu = D P_q`

with `D` diagonal and `P_q` a permutation matrix.

Therefore

`Y_nu Y_nu^dag = D D^dag`

is exactly diagonal.

So the left singular vectors of the neutrino Dirac matrix are only coordinate
phases and/or permutations. The single-Higgs fixed-`q_H` neutrino Dirac sector
has no structurally forced nontrivial left mixing.

## Why this matters

This explains an important observation-facing fact:

- the old fitted neutrino lane needed extra symmetry breaking and extra
  asymmetry terms to produce realistic PMNS angles

That was not an accident.

On the exact retained single-Higgs monomial lane, large PMNS mixing cannot come
from the neutrino Dirac sector alone.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino mass reduction to Dirac lane`
- `Neutrino Dirac Z_3 support trichotomy`

and keeps the same bridge condition:

- a single Higgs doublet with fixed `Z_3` charge `q_H`

## Exact monomial form

For each fixed `q_H in Z_3`, the support trichotomy gives one of three
permutation patterns:

- diagonal
- forward cyclic
- backward cyclic

So the full Dirac matrix can be written exactly as:

`Y_nu = D P_q`

with `D = diag(y_1, y_2, y_3)`.

That is a monomial matrix: one nonzero entry in each row and each column.

## Exact left-mixing consequence

Because permutation matrices are unitary,

`Y_nu Y_nu^dag = D P_q P_q^dag D^dag = D D^dag`

which is diagonal.

Hence the left-handed diagonalization of `Y_nu` is trivial up to coordinate
phases and permutations.

So on this exact lane:

- masses can be nonzero
- but left mixing is trivial

## The theorem-level statement

**Theorem (Single-Higgs monomial neutrino Dirac no-mixing).**
Assume the retained neutrino mass reduction to the Dirac lane, the exact
Dirac-`Z_3` support trichotomy, and a single Higgs doublet with fixed `Z_3`
charge `q_H`. Then the neutrino Dirac Yukawa matrix has the exact monomial form
`Y_nu = D P_q`. Consequently `Y_nu Y_nu^dag` is diagonal, and the neutrino
Dirac sector alone has only trivial left mixing up to phases and permutations.

## What this closes

This closes the next structural question on the retained Dirac lane:

- once `q_H` is fixed, the neutrino Dirac sector does **not** have enough
  structure by itself to explain large PMNS mixing

So any realistic PMNS closure must come from extra structure such as:

- charged-lepton misalignment
- multiple Higgs `Z_3` charges
- higher-order symmetry breaking beyond the fixed-`q_H` monomial lane

## What this does not close

This note does **not** prove which of those extra structures is realized.

It does **not** derive:

- the charged-lepton Yukawa matrix
- the Higgs `Z_3` charge
- the final PMNS matrix

It is an exact obstruction theorem only.

## Safe wording

**Can claim**

- fixed-`q_H` single-Higgs neutrino Dirac textures are monomial
- they can generate masses but not nontrivial left mixing by themselves
- observed PMNS mixing requires extra structure beyond this exact lane

**Cannot claim**

- PMNS mixing is impossible in the framework
- the charged-lepton sector is already derived
- the full neutrino mixing problem is solved

## Command

```bash
python3 scripts/frontier_neutrino_dirac_monomial_no_mixing.py
```
