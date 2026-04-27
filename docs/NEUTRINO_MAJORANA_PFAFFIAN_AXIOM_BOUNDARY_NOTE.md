# Current Pfaffian Axiom Boundary

**Date:** 2026-04-15
**Status:** exact boundary result on the current proposed_retained stack; not a no-go
against future closure
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py`

## Question

After the operator-classification theorem, the native-Gaussian no-go, and the
minimal Pfaffian extension, does the current retained `Cl(3)` on `Z^3` stack
already **force** a Pfaffian/Nambu sector?

## Bottom line

No.

On the current retained stack:

- the unique allowed `Delta L = 2` **channel** is fixed
- but the existence of an antisymmetric pairing block is **not** fixed
- and its amplitude `mu` is **not** fixed

So the Pfaffian/Nambu sector is currently an **admitted extension**, not a
forced consequence of the retained derivation stack.

## Why this is exact

The current retained stack fixes a determinant-based microscopic grammar:

- framework axiom: `Cl(3)` on `Z^3`
- interpretive commitment: Hamiltonian formulation is the physical theory
- observable principle on the current Gaussian surface:
  `W[J] = log|det(D+J)| - log|det D|`

That grammar determines the current normal bilinear surface.

Separately, the exact operator-classification theorem fixes the unique
same-chirality Majorana channel:

`nu_R^T C P_R nu_R`

But those two facts together still do not force a Pfaffian sector.

## The exact boundary argument

There is a one-parameter family of candidate antisymmetric pairing sectors

`Delta(mu) = mu S_unique`

on the unique allowed channel `S_unique`.

For all `mu`:

- the channel support is the same
- the normal determinant observables on the current retained surface are the
  same
- but the Pfaffian response is different

So the retained stack cannot distinguish:

- `mu = 0`  (no Pfaffian sector effectively present)
- `mu != 0` (Pfaffian sector present)

That is enough to prove the current boundary statement:

the Pfaffian/Nambu sector is not yet forced by the retained stack.

## Relationship to the earlier companions

The three earlier surfaces now fit together cleanly:

1. [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
   fixes the unique allowed operator
2. [NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md](./NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md)
   shows the current determinant/native surface gives coefficient zero
3. [NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md)
   constructs the minimal exact beyond-determinant extension once admitted

This new note answers the next boundary question:

4. is that Pfaffian extension already forced?

Current answer: no.

That boundary statement can now be strengthened to the exact current-stack
no-forcing theorem:

- [NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md)
- `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py`

The stronger result there is not just that the Pfaffian sector is "not yet
forced," but that no exact principle whose inputs are restricted to the
current retained normal grammar can force it.

## Safe wording

**Can claim**

- the retained stack forces the unique `Delta L = 2` channel
- the retained stack does not yet force the existence of a Pfaffian/Nambu
  sector
- the retained stack does not yet fix the Pfaffian amplitude

**Cannot claim**

- the framework will never derive a Pfaffian sector
- the neutrino Majorana problem is closed

## Next honest task

The next high-bar step is now sharply localized:

- derive an additional exact axiom-side principle that forces a pairing sector,
  or
- prove that no such principle exists on `Cl(3)` on `Z^3`

Until one of those is done, the Pfaffian sector remains constructed but not
derived.

## Command

```bash
python3 scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py
```
