# Exact No-Go Against Finite `B/X` Low-Carrier Closure on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact no-go against any exact finite face-alphabet / finite `B/X` closure  
**Script:** `scripts/frontier_finite_bx_low_carrier_no_go.py`

## Question

Now that the full finite-periodic-lattice plaquette law is known exactly as an
absolutely convergent `SU(3)` character/intertwiner foam ratio, can that exact
law be compressed further to a **small finite** quotient foam with:

- a finite plaquette face alphabet, and
- only the low singular-link defect carriers `B` and `X`?

## Exact answer

No.

There is no exact finite low-carrier closure of that form.

The obstruction already appears before any `B` or `X` defect can occur:
the isolated one-plaquette / simply-sheeted disk sector itself has an
**infinite** family of strictly positive `SU(3)` character coefficients.

So the exact law does not compress to any finite face alphabet.
Consequently, it also does not compress to any exact small finite `B/X`
low-carrier closure.

What remains true is narrower:

- the full exact law is known,
- `B` and `X` are the first explicit singular-link carriers inside that law,
- and small low-carrier packages remain exact only as finite-order / finite-window
  corollaries, not as a globally exact finite closure.

## Theorem 1: exact multiplicity expansion of the one-plaquette coefficients

Write

`t = beta / 6`

and

`w_beta(U) = exp[t Tr U] exp[t Tr U^dag]`.

For any irreducible `SU(3)` representation `R`, the character coefficient in

`w_beta(U) = sum_R c_R(beta) chi_R(U)`

is

`c_R(beta) = int dU w_beta(U) conj(chi_R(U))`.

Expanding both exponentials gives

`c_R(beta) = sum_{m,n >= 0} t^(m+n) / (m! n!) * N_{m,n}^R`

where

`N_{m,n}^R = mult(R in 3^(⊗m) ⊗ 3bar^(⊗n))`

is the exact tensor-product multiplicity.

So every coefficient `c_R(beta)` is a sum of nonnegative terms.

## Theorem 2: infinite symmetric family

Take the symmetric representation `R = (m,0)`.

Inside `3^(⊗m)`, the symmetric power `Sym^m(3)` appears exactly once, so

`N_{m,0}^{(m,0)} = 1`.

Therefore the `m,n = m,0` term in the exact multiplicity sum contributes

`t^m / m!`

and all other terms are nonnegative. Hence for every `m >= 0`,

`c_(m,0)(beta) >= t^m / m! > 0`.

By conjugation symmetry the same is true for `c_(0,m)(beta)`.

So the one-plaquette Wilson weight has infinitely many nonzero character
coefficients even before any singular-link geometry is introduced.

At `beta = 6`, `t = 1`, so the exact lower bound is simply

`c_(m,0)(6) >= 1 / m!`.

The runner verifies this numerically for `0 <= m <= 12`.

## Corollary: no exact finite face alphabet

Consider the singularity-free sector:

- one plaquette,
- or more generally a simply-sheeted disk surface with only regular links.

In that sector there are no `B` or `X` defect slots at all.

So any exact compression of the full law to a finite local carrier would still
need to reproduce the isolated one-plaquette weight using only a finite set of
face labels.

But Theorem 2 shows that the exact one-plaquette weight needs infinitely many
nonzero `SU(3)` face characters.

Therefore:

> no exact finite face alphabet can reproduce the full Wilson plaquette law.

## Main no-go statement

Any exact compression of the finite-periodic-lattice plaquette law to a
low-carrier quotient foam with

- finitely many face carriers, and
- only finitely many local singular-link carrier types such as `regular`, `X`,
  and `B`,

is impossible.

The reason is already present in the singularity-free sector, where `B` and `X`
do not appear.

So the exact law **cannot** be a small finite `B/X` closure.

## What survives

This does **not** kill the exact plaquette derivation.

The exact law from

- `docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md`

remains fully valid as the canonical exact finite-periodic-lattice law.

What this note kills is only the last simplification hope that the exact law
might collapse to a genuinely small finite low-carrier package.

So the honest final picture is:

1. exact law: closed
2. exact finite small `B/X` compression: impossible
3. exact low-carrier sector theorems (`p`, `p_8`, `B`, `X`, first non-disk
   split, disk sector) remain valuable as explicit low-order corollaries

## Paper-safe conclusion

The strongest honest claim is now:

> the plaquette is analytically derived exactly as an absolutely convergent
> finite-periodic-lattice `SU(3)` character/intertwiner foam ratio, but the
> full exact law does not compress to a finite small `B/X` low-carrier closure.

That is a stronger and cleaner endpoint than “the law is still missing.”

## Commands run

```bash
python3 scripts/frontier_finite_bx_low_carrier_no_go.py
```

Output summary:

- exact one-plaquette symmetric-family lower bound `c_(m,0)(6) >= 1 / m!`
- explicit numeric verification for `0 <= m <= 12`
- exact no-go against finite face alphabets
- exact no-go against any exact small finite `B/X` low-carrier closure
