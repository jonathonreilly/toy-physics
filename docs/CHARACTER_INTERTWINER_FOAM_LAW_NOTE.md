# Exact Finite-Lattice Character/Intertwiner Foam Law for the Plaquette

**Date:** 2026-04-16  
**Status:** exact finite-`beta` law on the same finite periodic evaluation surface  
**Script:** `scripts/frontier_character_intertwiner_foam_law.py`

## Question

Is there an exact analytic law for the plaquette on the retained pure-gauge
surface, rather than only a sequence of low-order carrier theorems?

## Exact answer

Yes.

On the same finite periodic `3 spatial + 1 time` lattice evaluation surface
already used elsewhere in the repo, the plaquette expectation is exactly a
ratio of absolutely convergent `SU(3)` character/intertwiner foam sums.

So the finite-`beta` law is now closed.

What remains open is only compression:

- a faster exact resummed evaluator,
- a closed-form number,
- or a low-state recursion that sums the exact law efficiently.

But the exact law itself is no longer missing.

## Theorem 1: absolutely convergent one-plaquette character expansion

For one plaquette,

`w_beta(U) = exp[(beta/6)(Tr U + Tr U^dag)]`

is a positive class function on compact `SU(3)`. By Peter-Weyl,

`w_beta(U) = sum_R c_R(beta) chi_R(U)`

with

`c_R(beta) = int dU w_beta(U) conj(chi_R(U))`.

Write

`t = beta / 6`

and expand

`w_beta(U) = exp[t Tr U] exp[t Tr U^dag]`.

Then

`c_R(beta) = sum_{m,n >= 0} t^(m+n) / (m! n!) * N_{m,n}^R`

where

`N_{m,n}^R = mult(R in 3^(⊗m) ⊗ 3bar^(⊗n))`

is the exact tensor-product multiplicity.

So every `c_R(beta)` is a sum of nonnegative terms.

Also

`|chi_R(U)| <= chi_R(I) = d_R`.

Evaluating at the identity gives

`sum_R c_R(beta) d_R = w_beta(I) = exp(beta)`.

Therefore the character expansion is absolutely and uniformly convergent:

`sum_R |c_R(beta) chi_R(U)| <= sum_R c_R(beta) d_R = exp(beta)`.

At `beta = 6`, the low coefficients are:

- `p_3(6) = c_3 / (3 c_0) = 0.422531739649983`
- `p_8(6) = c_8 / (8 c_0) = 0.162259799479938`
- `p_6(6) = c_6 / (6 c_0) = 0.135961727363391`

So the earlier `p`, `p_8`, `B`, and `X` data are low-carrier pieces of a
fully exact representation law, not standalone guesses.

## Theorem 2: exact finite-lattice foam law

Take a finite periodic `L^4` lattice on the retained same-surface gauge
evaluation surface.

Since there are finitely many plaquettes, the product

`prod_p w_beta(U_p)`

is a finite product of absolutely convergent expansions.

Hence Tonelli/Fubini applies and the character sums may be interchanged with
the finite product of Haar integrals.

So the partition function is exactly

`Z_L(beta) = sum_{R_p} [ prod_p c_{R_p}(beta) ] I_L({R_p})`

where `R_p` labels an `SU(3)` irrep on each plaquette and `I_L({R_p})` is the
finite product of local link Haar integrals.

Each link integral is a projector onto the invariant tensor space of the
incident representation legs. So after resolving those projectors/intertwiners,

`Z_L(beta) = sum_{foams F} W(F; beta)`

with a strictly local weight built from:

- plaquette character coefficients `c_R(beta)`
- local invariant projectors/intertwiners at links

This is the exact finite-`beta` representation-labeled foam law.

## Theorem 3: exact plaquette law with anchored boundary

Insert the normalized plaquette observable

`P_q = (1/3) Tr U_q`.

Then the numerator is the same exact foam law, but with one anchored
fundamental boundary loop at the tagged plaquette `q`:

`N_{L,q}(beta) = sum_{anchored foams F_q} W_q(F_q; beta)`.

Therefore

`<P_q>_L = N_{L,q}(beta) / Z_L(beta)`

is an exact ratio of absolutely convergent foam sums.

This is the exact analytic law for the finite periodic lattice plaquette.

## Corollary: the earlier carrier theorems are the first low-order pieces

The previously derived local data sit inside this exact general law.

At the first singular-link levels:

- regular link projector:
  - `int dU U_ij U^dag_kl = delta_il delta_jk / 3`
- crossing tensor `X`:
  - coefficients `+1/8` and `-1/24`
- baryon junction tensor `B`:
  - coefficient `1/6`

So:

- `docs/FUNDAMENTAL_DISK_ACTIVITY_THEOREM_NOTE.md`
- `docs/FIRST_NONDISK_Z3_LIFT_THEOREM_NOTE.md`
- `docs/FIRST_NONDISK_CHARACTER_FOAM_THEOREM_NOTE.md`
- `docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md`

are not parallel alternative closures anymore. They are the first explicit
low-carrier corollaries of the exact character/intertwiner foam law.

## Why this closes the derivation surface

The repo’s retained same-surface claim was already:

> the plaquette is a unique observable of the finite periodic Wilson partition
> function, and Monte Carlo evaluates that observable.

This note strengthens that claim:

> the same plaquette observable now has an exact absolutely convergent analytic
> character/intertwiner foam law on that same finite periodic surface.

So the law is derived. Numerical work is evaluation of that derived law.

## Honest scope

This note still does **not** give:

- a low-state closed recursion,
- a compact closed form for the final number,
- or a small exact finite low-carrier closure.

`docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md` now sharpens that last point:

> the full exact law does not compress to any exact finite face alphabet, and
> therefore not to any exact small finite `B/X` low-carrier closure either.

So the remaining compression question is no longer “find a small finite
carrier,” but “find a faster evaluator for the already exact compressed law.”

`docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md` now supplies the
useful exact resummed/state-compressed representation itself: the exact
infinite-carrier law reorganizes into iid plaquette occupation pairs with
explicit finite local alphabets `Omega_K` and explicit truncation tails.
`docs/POISSONIZED_LINK_CHANNEL_COMPRESSION_NOTE.md` then closes the exact local
link side of that compression: after truncation, the evaluator is a finite
tensor network with finite invariant-channel link alphabets `Lambda_K`.

But the exact finite-`beta` law itself is no longer open.

## Practical conclusion

The branch can now support the stronger paper-safe claim:

> on the retained finite periodic `3+1` Wilson-plaquette evaluation surface,
> the plaquette expectation is analytically derived as an exact absolutely
> convergent `SU(3)` character/intertwiner foam ratio; Monte Carlo is one
> evaluation method for that exact law, not the source of the law itself.

## Commands run

```bash
python3 scripts/frontier_character_intertwiner_foam_law.py
```

Output summary:

- exact `p_3(6)`, `p_8(6)`, `p_6(6)`
- explicit low-link intertwiners `regular`, `X`, `B`
- partial character-identity sum bounded by `exp(6)`
- exact finite-lattice character/intertwiner foam law statement
