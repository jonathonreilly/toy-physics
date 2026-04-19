# PMNS EWSB Alignment Nonforcing

**Date:** 2026-04-15  
**Status:** exact current-bank boundary theorem on EWSB alignment of the
active one-sided PMNS branch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_alignment_nonforcing.py`

## Question

After the new residual-`Z_2` Hermitian-core theorem, does the current retained
bank actually force the active PMNS-producing one-sided branch to align with
the exact weak-axis EWSB `1+2` split?

Or is that aligned core still a conditional refinement rather than an exact
current-bank output?

## Bottom line

It is still conditional. The current bank does not force EWSB alignment of the
active one-sided PMNS branch.

More precisely, on the same canonical active two-Higgs support class

`Y = A + B C`,

there exist:

- full-rank aligned points satisfying `P_23 H P_23 = H`
- full-rank generic points satisfying all the current canonical/support and
  inverse-problem conditions but with
  `P_23 H P_23 != H`

So the current bank already supports both:

- the aligned four-real Hermitian core
- and genuine non-aligned seven-coordinate active points

Therefore the current bank does not yet select the aligned submanifold. Any
future alignment theorem must introduce an additional exact bridge principle
beyond the present canonical-support and Hermitian-inverse-problem data.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Dirac two-Higgs canonical reduction`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`
- `PMNS right polar section`
- `PMNS EWSB residual-Z2 Hermitian core`

## Why this is exact

The current bank already proves:

1. the active one-sided PMNS branch reduces to the canonical support class
   `Y = A + B C`
2. the generic local Hermitian inverse problem on that branch is exact and
   seven-dimensional
3. the generic full-rank right orbit admits the canonical positive section
   `Y_+(H) = H^(1/2)`
4. under the **extra** EWSB-alignment bridge condition, the active Hermitian
   law collapses to the residual-`Z_2` core

So to test whether alignment is already forced, it is enough to ask:

- are there full-rank non-aligned points still lying on the same exact
  current-bank canonical branch?

If yes, alignment is not forced by the current bank.

## Exact nonforcing statement

Take the canonical active branch

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i phi}) C`.

Then:

- aligned points are the codimension-three locus
  `x_2^2 + y_2^2 = x_3^2 + y_3^2`,
  `x_2 y_1 = x_1 y_3`,
  `phi = 0`
- generic points on the same branch violate at least one of those conditions

Both types of points can be chosen full rank and on the same exact support
class.

So the current bank contains an exact **branch-with-submanifold** relation,
not a forcing theorem selecting the submanifold.

## Theorem-level statement

**Theorem (Current-bank nonforcing of EWSB alignment on the active one-sided
PMNS branch).** Assume the exact canonical active two-Higgs branch theorem,
the exact active-branch Hermitian inverse-problem theorem, the exact generic
right polar-section theorem, and the exact residual-`Z_2` Hermitian-core
theorem. Then:

1. the EWSB-aligned active Hermitian core is an exact admissible submanifold of
   the canonical active branch
2. there also exist full-rank non-aligned points on that same canonical active
   branch satisfying the current support and Hermitian inverse-problem
   conditions
3. therefore the current retained bank does not force the active one-sided
   PMNS branch to lie on the EWSB-aligned submanifold

So the aligned core is currently a conditional sharpening, not an exact
current-bank selection.

## What this closes

This closes the ambiguity about the status of the aligned Hermitian core.

It is now exact that:

- the aligned residual-`Z_2` Hermitian core is real
- it is useful
- but it is not yet forced by the current retained bank

So the next honest derivation target is not “use the aligned core as if it is
already selected,” but:

- derive an exact alignment bridge theorem
- or derive the breaking-slot law on the full non-aligned canonical branch

## What this does not close

This note does **not** derive:

- the alignment bridge theorem
- the four aligned-core parameters
- the three breaking-slot laws
- the residual selected-branch coefficient sheet

It is a boundary theorem only.

## Command

```bash
python3 scripts/frontier_pmns_ewsb_alignment_nonforcing.py
```
