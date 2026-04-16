# PMNS EWSB Residual-Z2 Hermitian Core

**Date:** 2026-04-15  
**Status:** exact conditional theorem on the active lepton Hermitian data law  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_residual_z2_hermitian_core.py`

## Question

Once the exact one-sided PMNS branches are isolated, can the axiom bank say
anything sharper about the missing Hermitian data `H_nu` or `H_e` than “seven
real coordinates on a canonical two-Higgs branch”?

In particular, if the active PMNS-producing lepton sector is aligned with the
exact EWSB weak-axis selection that already gives the exact `1+2` generation
split, does that residual symmetry reduce the active Hermitian data law?

## Bottom line

Yes, conditionally.

If the active one-sided PMNS branch inherits the exact EWSB residual
`Z_2 = {1, P_23}` that swaps the two degenerate light generations, then the
active Hermitian matrix obeys

`P_23 H_act P_23 = H_act`.

On the canonical active two-Higgs branch, with Hermitian coordinates

`(d_1,d_2,d_3,r_12,r_23,r_31,phi)`,

this is exactly equivalent to

- `d_2 = d_3`
- `r_12 = r_31`
- `phi = 0`

so the active Hermitian data reduce from the generic seven-coordinate grammar
to the four-real-parameter core

```text
H_act =
[ a  b  b ]
[ b  c  d ]
[ b  d  c ]
```

with `a,b,c,d in R` and `b >= 0` in the canonical gauge.

At the same time, the passive monomial sector stays diagonal:

`H_pass = diag(m_1^2,m_2^2,m_3^2)`.

So the piecewise Hermitian law on the one-sided minimal PMNS surface becomes:

- neutrino-side active branch:
  `H_nu = H_act`, `H_e = H_pass`
- charged-lepton-side active branch:
  `H_nu = H_pass`, `H_e = H_act`

Equivalently, the generic seven-coordinate active Hermitian grammar now splits
into:

- a four-coordinate exact aligned core
- plus three explicit symmetry-breaking slots
  `(d_2-d_3, r_12-r_31, phi)`

## Atlas and axiom inputs

This theorem reuses:

- `Generation axiom boundary`
- `Neutrino Dirac monomial no-mixing`
- `Lepton single-Higgs PMNS triviality theorem`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`
- `PMNS right polar section`

The only extra bridge condition is explicit:

- the active PMNS-producing lepton sector is aligned with the exact EWSB
  weak-axis selection, so the residual `2 <-> 3` permutation survives on that
  sector’s Hermitian data.

This is a **conditional refinement**, not a current-bank theorem that the
alignment itself has already been derived.

## Why the active Hermitian core is four-dimensional

On the canonical active branch,

```text
H =
[ d_1              r_12               r_31 e^{-i phi} ]
[ r_12             d_2                r_23            ]
[ r_31 e^{i phi}   r_23               d_3             ]
```

with `r_12, r_23, r_31 >= 0` after the canonical diagonal rephasing gauge
choice.

Conjugation by

```text
P_23 =
[ 1 0 0 ]
[ 0 0 1 ]
[ 0 1 0 ]
```

swaps the second and third generations. The equality `P_23 H P_23 = H`
therefore forces:

- `d_2 = d_3`
- `r_12 = r_31`
- `r_12 = r_31 e^{-i phi}`

and on the canonical gauge patch with `r_12,r_31 > 0` this implies
`phi = 0 (mod 2pi)`.

So the active Hermitian matrix collapses exactly to

```text
[ a  b  b ]
[ b  c  d ]
[ b  d  c ]
```

This is a four-real-parameter Hermitian core.

## Exact 2+1 spectral split

The same residual `Z_2` gives the exact even/odd basis

- `e_1`
- `(e_2 + e_3)/sqrt(2)`
- `(e_2 - e_3)/sqrt(2)`

In that basis, the aligned Hermitian core block-diagonalizes as

```text
[ a      sqrt(2) b   0   ]
[ sqrt(2) b   c+d    0   ]
[ 0          0      c-d  ]
```

So the active spectral problem is not generic `3 x 3` diagonalization.
It is an exact `2 + 1` split:

- one odd state with eigenvalue `c-d`
- one even `2 x 2` block carrying the remaining pair

This is the Hermitian analogue of the exact EWSB `1+2` generation split.

## Piecewise `H_nu` / `H_e` law

On the one-sided minimal PMNS surface there are only two branch shapes:

1. active two-Higgs sector + passive monomial sector
2. the same with `nu <-> e`

So under the explicit EWSB-alignment bridge condition:

### Neutrino-side active branch

- `H_nu = [[a,b,b],[b,c,d],[b,d,c]]`
- `H_e = diag(m_e^2,m_mu^2,m_tau^2)` on the passive monomial lane

### Charged-lepton-side active branch

- `H_nu = diag(m_1^2,m_2^2,m_3^2)` on the passive monomial lane
- `H_e = [[a,b,b],[b,c,d],[b,d,c]]`

So the selected-branch Hermitian data law is now sharper than “some seven real
numbers” whenever the active PMNS branch is EWSB-aligned.

## What this closes

This closes a real chunk of the `H_nu` / `H_e` problem.

It is now exact that:

- the active Hermitian branch has a natural axiom-native aligned core
- that core is four-dimensional, not seven-dimensional
- the passive branch stays diagonal
- the active aligned spectral problem reduces to an exact `2 + 1` block
- the difference between the generic active branch and the exact aligned core
  is now isolated in three explicit breaking coordinates

## What this does not close

This note does **not** derive:

- that the PMNS-producing extension is aligned with the EWSB residual `Z_2`
- the four aligned core parameters `a,b,c,d`
- the three symmetry-breaking slots away from the aligned core
- the residual selected-branch `Z_2` coefficient sheet

So this note sharpens the Hermitian-data law; it does not by itself complete
positive neutrino closure.

## Safe wording

**Can claim**

- under the explicit EWSB-alignment bridge condition, the active one-sided
  PMNS Hermitian data reduce to the four-real-parameter core
  `[[a,b,b],[b,c,d],[b,d,c]]`
- the passive monomial sector remains diagonal
- the generic active seven-coordinate Hermitian grammar splits into a
  four-coordinate aligned core plus three explicit symmetry-breaking slots

**Cannot claim**

- the current retained bank has already derived the alignment condition
- `H_nu` and `H_e` are numerically closed
- the observed PMNS phase or nonzero `theta_13` are already derived from this
  exact aligned core alone

## Command

```bash
python3 scripts/frontier_pmns_ewsb_residual_z2_hermitian_core.py
```
