# PMNS Branch-Conditioned Quadratic-Sheet Closure

**Date:** 2026-04-15  
**Status:** exact branch-conditioned coefficient-reconstruction theorem on the
minimal PMNS branches  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_branch_conditioned_quadratic_sheet_closure.py`

## Question

Once a future microscopic selector realizes `a_sel != 0` and picks the active
minimal PMNS branch, is the remaining coefficient problem still an open-ended
seven-parameter search?

Or can the selected-branch coefficients already be reconstructed explicitly
from the branch Hermitian data?

## Bottom line

They can be reconstructed explicitly, up to one residual `Z_2` sheet on the
selected two-Higgs branch.

On the canonical neutrino-side branch

`Y_nu = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`

with

`H_nu = Y_nu Y_nu^dag`,

write the exact invariant coordinates

- `d_1 = (H_nu)11`
- `d_2 = (H_nu)22`
- `d_3 = (H_nu)33`
- `r_12 = |(H_nu)12|`
- `r_23 = |(H_nu)23|`
- `r_31 = |(H_nu)31|`
- `phi = arg((H_nu)12 (H_nu)23 (H_nu)31)`

and set

- `alpha = r_12^2`
- `beta = r_23^2`
- `gamma = r_31^2`.

Then `t_1 = x_1^2` satisfies the exact quadratic

`(d_2 d_3 - beta) t^2 - (d_1 d_2 d_3 + gamma d_2 - alpha d_3 - beta d_1) t + gamma (d_1 d_2 - alpha) = 0`.

Once one root `t_1` is chosen, the remaining squared moduli reconstruct
rationally:

- `x_2^2 = alpha / (d_1 - t_1)`
- `x_3^2 = beta / (d_2 - x_2^2)`
- `y_i^2 = d_i - x_i^2`
- `delta = phi`

and therefore the full canonical branch coefficients are explicit.

Generically there are exactly two positive roots on the physical branch. They
give two distinct canonical coefficient sheets with the same `H_nu`.

On the charged-lepton-side minimal branch, the same cyclic formulas hold with
`H_e = Y_e Y_e^dag`. The additional monomial neutrino-side data on that branch
are just the three positive Dirac mass moduli, read directly from the monomial
neutrino singular values.

So once `sign(a_sel)` picks the branch, the remaining coefficient problem is
not an unconstrained seven-parameter search. It is an explicit algebraic
reconstruction problem with one residual sheet bit on the selected two-Higgs
branch.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS selector sign-to-branch reduction`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`
- `Neutrino full closure last-mile reduction`

It does **not** import a new selector. It sharpens what happens **after** a
selector is realized.

## Neutrino-side exact quadratic reconstruction

On the canonical neutrino-side branch,

`H_nu` has the exact cyclic form

```text
[ d_1              r_12               r_31 e^{-i phi} ]
[ r_12             d_2                r_23            ]
[ r_31 e^{i phi}   r_23               d_3             ]
```

with

- `d_1 = x_1^2 + y_1^2`
- `d_2 = x_2^2 + y_2^2`
- `d_3 = x_3^2 + y_3^2`
- `alpha = r_12^2 = x_2^2 y_1^2`
- `beta  = r_23^2 = x_3^2 y_2^2`
- `gamma = r_31^2 = x_1^2 y_3^2`.

Eliminating `x_2^2`, `x_3^2`, `y_1^2`, `y_2^2`, `y_3^2` in favor of the
observables leaves one scalar unknown `t_1 = x_1^2`, and that unknown obeys
the quadratic above.

So the neutrino-side selected-branch coefficient problem is already explicit:

1. solve one quadratic for `x_1^2`
2. back-substitute rationally for `x_2^2`, `x_3^2`
3. recover `y_i^2 = d_i - x_i^2`
4. set `delta = phi`.

## The residual `Z_2` sheet

The local inverse-problem theorem already showed that no hidden continuous
redundancy remains. The present theorem sharpens the global side:

- generic physical data on the canonical branch give exactly two positive
  quadratic roots
- each root reconstructs a full positive canonical coefficient sheet
- both sheets produce the same Hermitian matrix `H_nu`

So the residual global ambiguity on the selected neutrino-side branch is not a
continuous family. It is one exact `Z_2` sheet bit.

## Charged-lepton-side branch

If `sign(a_sel)` instead picks the charged-lepton-side minimal branch, the same
cyclic quadratic reconstruction holds for the canonical charged-lepton matrix

`Y_e = diag(x^e_1,x^e_2,x^e_3) + diag(y^e_1,y^e_2,y^e_3 e^{i delta_e}) C`

from the Hermitian data `H_e = Y_e Y_e^dag`.

The extra neutrino-side information on that branch is simpler: the neutrino
lane remains monomial, so its three positive Dirac masses are just the three
monomial singular values.

So the charged-lepton-side branch-conditioned coefficient problem is also
algebraic and explicit:

- one `Z_2` sheet on the two-Higgs charged-lepton branch
- plus three direct monomial neutrino mass moduli.

## The theorem-level statement

**Theorem (Branch-conditioned quadratic-sheet coefficient closure on the
minimal PMNS branches).** Assume the exact PMNS selector sign-to-branch
reduction theorem, together with the exact canonical two-Higgs observable
inverse-problem theorems on the neutrino-side and charged-lepton-side minimal
branches. Then:

1. if `a_sel > 0`, the canonical neutrino-side two-Higgs coefficients are
   reconstructed from `H_nu` by one explicit quadratic equation in `x_1^2`
   followed by rational back-substitution and `delta = phi`
2. if `a_sel < 0`, the same statement holds on the charged-lepton-side branch
   with `H_e`, while the monomial neutrino lane contributes three direct Dirac
   mass moduli
3. on either selected two-Higgs branch, the residual global ambiguity is
   generically a single `Z_2` sheet rather than a continuous coefficient family

Therefore once a future microscopic selector picks the active branch, the
remaining branch-conditioned coefficient problem is algebraically explicit up
to one residual sheet bit on the selected two-Higgs branch.

## What this closes

This closes the coefficient-side ambiguity after selector realization.

It is now exact that the post-selector problem is not:

- a generic complex `3 x 3` fit
- a hidden higher-dimensional continuous coefficient family
- another texture-search problem

The remaining coefficient ambiguity is finite and explicit.

## What this does not close

This note does **not** derive:

- the selector amplitude `a_sel`
- the sign of `a_sel`
- the branch Hermitian data `H_nu` or `H_e`
- the residual `Z_2` sheet bit from the retained bank alone

So it does not by itself promote full positive neutrino closure. It closes the
post-selector coefficient algebra as far as the current bank honestly allows.

## Command

```bash
python3 scripts/frontier_pmns_branch_conditioned_quadratic_sheet_closure.py
```
