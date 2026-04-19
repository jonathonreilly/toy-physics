# PMNS Right-Conjugacy-Invariant No-Go

**Date:** 2026-04-15  
**Status:** exact current-bank no-go theorem on intrinsic right-sensitive PMNS
completion  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_right_conjugacy_invariant_nogo.py`

## Question

The admitted PMNS right-Gram route already gives exact positive completion
data:

- the selector can be realized by right-Gram support
- the residual sheet can be fixed by one right-Gram scalar

Can those admitted data become intrinsic just by passing to a more clever
right-unitary conjugacy-invariant observable of

`K = Y^dag Y`?

## Bottom line

No.

If an observable of the right Gram matrix satisfies

`I(U K U^dag) = I(K)` for every `U in U(3)`,

then it is constant on the exact right orbit

`Y -> Y U^dag`.

But along that same right orbit:

- the admitted selector datum `m_R(Y)` can change
- the admitted sheet-fixing scalar `|(Y^dag Y)12|` can change

while:

- `H = Y Y^dag` stays fixed
- the singular values stay fixed
- every conjugacy-invariant function of `K` stays fixed

So no right-conjugacy-invariant observable can make the admitted right-Gram
completion route intrinsic.

Together with the scalar-bridge nonrealization theorem, this means the missing
object is now sharper than “some right-sensitive observable”:

> it must be genuinely non-conjugacy-invariant on the right Gram data and it
> must come with a canonical right-frame law (or equivalent right-sensitive
> observable principle) that makes it intrinsic.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS right-frame orbit obstruction`
- `PMNS right-Gram selector realization`
- `PMNS right-Gram sheet fixing`
- `PMNS scalar bridge nonrealization`
- `Observable principle`

## Theorem-level statement

**Theorem (Right-conjugacy-invariant observables cannot intrinsicize the
admitted PMNS right-Gram route).** Assume the exact PMNS right-frame orbit
obstruction theorem, the exact admitted PMNS right-Gram selector theorem, and
the exact admitted PMNS right-Gram sheet-fixing theorem. Let `I(Y)` be any
observable depending on the right Gram matrix only through a conjugacy-invariant
functional `F`:

`I(Y) = F(Y^dag Y)`, with `F(U K U^dag) = F(K)` for all `U in U(3)`.

Then `I(Y)` is constant on every exact right orbit `Y -> Y U^dag`.

But on explicit retained-branch samples, the admitted selector datum `m_R(Y)`
and the admitted sheet-fixing datum `|(Y^dag Y)12|` vary along the same right
orbit.

Therefore no right-conjugacy-invariant observable of `K` can make the admitted
right-Gram completion route intrinsic.

## What this closes

This closes the next large loophole after the agent sweep.

It is now exact that:

- the missing intrinsic object is not hidden among spectral or trace-type
  observables of `K`
- it is not enough to “upgrade” from matrix entries to clever conjugacy
  invariants
- the missing object must genuinely break right-orbit blindness

## What this does not close

This note does **not** derive:

- the canonical right-handed frame
- the non-conjugacy-invariant right-sensitive observable principle
- the selected branch Hermitian data law

So it does not complete positive PMNS closure. It sharpens the missing object.

## Command

```bash
python3 scripts/frontier_pmns_right_conjugacy_invariant_nogo.py
```
