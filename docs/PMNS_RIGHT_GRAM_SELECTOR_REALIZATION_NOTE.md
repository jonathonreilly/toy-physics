# PMNS Right-Gram Selector Realization

**Date:** 2026-04-15  
**Status:** exact admitted-extension theorem on a right-sensitive PMNS selector
datum  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_right_gram_selector_realization.py`

## Question

The retained bank proved that the missing PMNS selector must be sector-odd,
supported only on the non-universal locus, and unique up to scale. It also
proved that the current left-Hermitian bank does not realize that selector.

If we admit one genuinely new right-sensitive branch datum, can the selector be
realized exactly?

## Bottom line

Yes.

On a sector-labeled lepton pair, define the right Gram matrices

- `K_nu = Y_nu^dag Y_nu`
- `K_e  = Y_e^dag Y_e`.

On the generic positive-modulus patch:

- any monomial lane `Y = D P` has diagonal `K`, hence zero off-diagonal
  right-support
- any canonical two-Higgs lane
  `Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`
  has full cyclic off-diagonal right-support in `K`

So if

`m_R(Y) = number of nonzero upper-triangular off-diagonal entries of Y^dag Y`,

then exactly:

- monomial lane: `m_R = 0`
- canonical two-Higgs lane: `m_R = 3`

and the mixed right-sensitive comparison

`a_sel^R = (m_R(Y_nu) - m_R(Y_e)) / 3`

has the reduced class values:

- `U1 -> 0`
- `U2 -> 0`
- `N_nu -> +1`
- `N_e -> -1`.

So this admitted right-sensitive datum realizes the unique reduced selector
class exactly.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS selector class-space uniqueness`
- `PMNS selector sign-to-branch reduction`
- `Neutrino Dirac monomial no mixing`
- `Neutrino Dirac two-Higgs canonical reduction`
- `Charged-lepton two-Higgs canonical reduction`
- `PMNS branch sheet nonforcing`

The last import is the key guidance: the current left-Hermitian bank is blind
to the residual branch sheet, so a right-sensitive completion is the honest
next place to look.

## Why this is not a contradiction of the current zero-law packet

The current zero-law and nonforcing theorems were about the **retained**
support-plus-scalar bank and the current left-Hermitian branch observables.

This note introduces a genuinely new datum:

- sector-labeled right Gram support

That datum was not in the retained packet. So this is an admitted extension
route, not a revision of the retained zero-law.

## Theorem-level statement

**Theorem (Right-Gram support comparison realizes the unique reduced PMNS
selector class).** Assume the exact monomial single-Higgs lepton lane, the
exact canonical two-Higgs lepton lane, and the exact reduced class labels
`U1, U2, N_nu, N_e`. On the generic positive-modulus patch define

`m_R(Y) = number of nonzero upper-triangular off-diagonal entries of Y^dag Y`

and

`a_sel^R = (m_R(Y_nu) - m_R(Y_e)) / 3`.

Then:

1. `m_R = 0` on every monomial lane
2. `m_R = 3` on every generic canonical two-Higgs lane
3. `a_sel^R` evaluates to `0,0,+1,-1` on `U1,U2,N_nu,N_e`

So `a_sel^R` is a right-sensitive realization of the unique reduced selector
class `chi_N_nu - chi_N_e`, with an exact discrete amplitude law on the
reduced class surface.

## What this closes

This closes the first positive extension route to the selector.

It is now exact that there exists an admitted right-sensitive datum which:

- vanishes on the universal classes
- flips sign across the non-universal orbit
- realizes the unique reduced selector class positively

## What this does not close

This note does **not** derive:

- the right-Gram datum from the retained axiom bank
- a canonical right-handed frame that makes that datum intrinsic on the
  retained bank
- the microscopic lattice object producing that datum
- the selected-branch Hermitian data

So it does not promote current retained closure. It identifies one exact
right-sensitive completion route. See
[PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md](./PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md)
for the exact orbit-level reason that this route is still basis-conditional.

## Command

```bash
python3 scripts/frontier_pmns_right_gram_selector_realization.py
```
