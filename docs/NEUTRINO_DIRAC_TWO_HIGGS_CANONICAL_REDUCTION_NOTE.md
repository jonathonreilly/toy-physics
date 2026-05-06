# Neutrino Dirac Two-Higgs Canonical Reduction Theorem

**Date:** 2026-04-15
**Status:** exact reduction/counting theorem on the minimal surviving
neutrino-side extension class
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_dirac_two_higgs_canonical_reduction.py`

## Question

After the exact retained boundary work:

- the Majorana current-stack law is `M_R,current = 0_(3 x 3)`
- the full single-Higgs lepton sector is closed negatively for PMNS
- the smallest exact surviving neutrino-side escape class is a two-Higgs
  `Z_3` sector with distinct Higgs charges

what exactly is still left between the current boundary and **full Dirac
neutrino closure** on that minimal surviving class?

## Bottom line

Much less than a generic texture fit.

Up to generation relabeling and lepton field rephasings, every distinct-charge
two-Higgs neutrino texture reduces to one canonical support class:

`Y_nu = A + B C`

with:

- `C` the forward `3`-cycle permutation
- `A` diagonal
- `B` diagonal

And for a generic point on that class, exact phase reduction gives the normal
form

`Y_nu,can = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C`

with all `x_i > 0`, all `y_i > 0`, and **one** surviving physical phase
`delta`.

So the exact remaining gap on the minimal surviving neutrino-side class is:

- six positive moduli
- one phase

i.e. **seven real axiom-side numbers**.

## Atlas and axiom inputs

This theorem reuses:

- [`DM_NEUTRINO_TWO_HIGGS_MINIMALITY_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_TWO_HIGGS_MINIMALITY_THEOREM_NOTE_2026-04-15.md)
  — the Neutrino Dirac two-Higgs escape / minimality theorem, supplying
  the *minimal surviving neutrino-side extension class* assumption used
  in the question.
- [`LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md`](LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md)
  — the Lepton single-Higgs PMNS triviality theorem, which is what
  closes the full single-Higgs lepton sector negatively for PMNS and
  forces the bridge condition that the charged-lepton lane stay on the
  monomial single-Higgs class while only the neutrino lane goes
  two-Higgs.

and keeps the exact bridge condition explicit:

- the charged-lepton lane stays on the monomial single-Higgs class
- the neutrino lane is on the minimal surviving two-Higgs class with distinct
  Higgs charges

## Why the charge-pair label is not a remaining physical ambiguity

There are only three unordered distinct Higgs-charge pairs:

- `(0,1)`
- `(0,2)`
- `(1,2)`

Any texture on that lane has the form

`Y_nu = D_a P_a + D_b P_b`

with `P_a != P_b`.

Right-multiplying by `P_a^dag` makes the first term diagonal and turns the
second into a relative permutation `R = P_b P_a^dag`.

For every distinct pair, `R` is a nontrivial `3`-cycle, and all such cycles are
conjugate by generation relabeling.

Therefore all distinct-charge pairs reduce to the same canonical support class
`A + B C`.

So the choice of pair is **not** a remaining exact physical ambiguity on this
minimal lane.

## Exact phase reduction

Write the canonical support class as

`Y_nu = diag(a_1,a_2,a_3) + diag(b_1,b_2,b_3) C`.

This starts with `6` complex numbers, i.e. `12` real parameters.

Diagonal rephasings of the left-handed lepton doublets and the right-handed
neutrinos act by

`Y_nu -> L^dag Y_nu R`.

Exactly:

1. the three diagonal entries `a_i` can all be made positive and real
2. two of the three `b_i` phases can also be removed
3. one common phase direction is redundant because it leaves `Y_nu` unchanged

So one exact invariant phase remains. A convenient generic canonical form is:

`Y_nu,can = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C`

with `x_i > 0`, `y_i > 0`.

The surviving phase can be taken as the invariant combination

`delta = arg[(b_1 b_2 b_3)/(a_1 a_2 a_3)]`.

## Exact parameter count

The generic two-Higgs lane therefore carries:

- `12` starting real parameters
- minus `5` exact removable phase directions

leaving

`12 - 5 = 7`

physical real parameters.

Equivalently:

- `3` positive `x_i`
- `3` positive `y_i`
- `1` phase `delta`

## Why this matters for full neutrino closure

On the charged-lepton-monomial lane, Dirac-neutrino observables consist of:

- `3` neutrino masses
- `3` PMNS angles
- `1` Dirac CP phase

again `7` real quantities.

So the minimal surviving neutrino-side extension class is now reduced to a
parameter-count-complete canonical lane.

This does **not** prove the map to observables is automatically surjective.
It does **not** derive the seven numbers.

But it does prove that the exact remaining gap between the current boundary and
full Dirac-neutrino closure on this minimal class is no longer “some unknown
texture family.” It is exactly:

- six moduli
- one phase

to be derived from the axiom-side dynamics.

## The theorem-level statement

**Theorem (Canonical reduction of the minimal two-Higgs neutrino Dirac lane).**
Assume the exact two-Higgs neutrino-side escape theorem and the exact
single-Higgs monomial charged-lepton boundary. Then:

1. every distinct-charge two-Higgs neutrino texture is equivalent up to
   generation relabeling to the canonical support class `Y_nu = A + B C`
   with `A,B` diagonal and `C` the forward `3`-cycle
2. after exact diagonal lepton-field rephasings, the generic canonical point
   has the normal form
   `diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`
   with `x_i > 0`, `y_i > 0`
3. the minimal surviving neutrino-side extension class therefore carries
   exactly `7` real physical parameters

Therefore the exact remaining gap to full Dirac-neutrino closure on that
minimal surviving class is seven axiom-side quantities: six moduli and one
phase.

## What this closes

This closes the next real planning ambiguity on the neutrino lane.

It is now exact that:

- the charge-pair label is not itself the main unresolved object
- the minimal surviving class is canonical up to relabeling
- the remaining unknown is not a generic complex `3 x 3` matrix
- the remaining unknown is exactly seven real quantities

So the next honest science target is to derive those seven quantities, not to
keep searching for more exact freedom on this minimal lane.

## What this does not close

This note does **not** derive:

- the seven quantities
- the observed neutrino masses
- the observed PMNS angles
- the Dirac CP phase

It is an exact reduction theorem only.

## Safe wording

**Can claim**

- all distinct minimal two-Higgs neutrino lanes are support-equivalent
- the generic canonical normal form has six moduli plus one phase
- the exact remaining minimal-lane gap is seven real quantities

**Cannot claim**

- those seven quantities are already derived
- PMNS is numerically closed
- the framework has already selected the minimal two-Higgs lane in nature

## Command

```bash
python3 scripts/frontier_neutrino_dirac_two_higgs_canonical_reduction.py
```
