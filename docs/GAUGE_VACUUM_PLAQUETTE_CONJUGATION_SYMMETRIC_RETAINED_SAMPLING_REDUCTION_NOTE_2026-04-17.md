# Gauge-Vacuum Plaquette Conjugation-Symmetric Retained Sampling Reduction

**Date:** 2026-04-17
**Status:** exact retained-sector symmetry reduction theorem on the plaquette PF
lane; because the physical retained coefficient vectors already satisfy
conjugation symmetry, the finite sampling dimension reduces from retained-basis
size to conjugation-orbit count
**Type:** positive_theorem
**Runner:** none; restored as a dependency note for current gauge-vacuum runner closure.

## Question

After the retained class-sampling inversion theorem, is the finite sampling
burden still the full retained-basis dimension, or does the already-known
conjugation symmetry reduce it?

## Answer

It reduces it.

The retained plaquette environment coefficients already satisfy

`c_(p,q) = c_(q,p)`.

So on any retained finite sector, one should not invert on the full character
basis but on the conjugation-symmetric orbit basis.

For a retained set `Lambda`, let `Lambda / ~` be the set of conjugation orbits
under `(p,q) ~ (q,p)`. Then the number of independent retained coefficients is
`|Lambda / ~|`, not `|Lambda|`.

Therefore the exact finite-sampling problem reduces accordingly:

- one generic sample is still not enough,
- `|Lambda / ~|` generic samples are generically enough on the symmetric
  retained subspace.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md):

- the retained coefficients obey
  `rho_(p,q)(beta) = rho_(q,p)(beta)`.

From
[GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md):

- on a retained finite class sector, exact coefficient recovery is a finite
  holonomy-sampling inversion problem.

So the next honest sharpening is to quotient that finite inversion problem by
the already-exact conjugation symmetry.

## Theorem 1: exact orbit-basis reduction of the retained sampling problem

Let `Lambda` be a finite retained marked class sector that is closed under
conjugation.

For each orbit `O in Lambda / ~`, define the retained symmetric basis element

- `Phi_O = chi_(p,p)` if `O = {(p,p)}`,
- `Phi_O = chi_(p,q) + chi_(q,p)` if `O = {(p,q),(q,p)}` with `p != q`.

Then every conjugation-symmetric retained coefficient vector has the unique form

`v_sym^Lambda = sum_(O in Lambda/~) a_O Phi_O`.

So the number of independent retained coefficients is exactly the orbit count
`|Lambda / ~|`.

## Corollary 1: exact reduced sampling matrix

For marked holonomies `W_i`, define the reduced orbit-evaluation matrix

`F_(i,O) = <K_Lambda(W_i), Phi_O>`.

Then the sampled boundary values satisfy

`Z_i = sum_(O in Lambda/~) F_(i,O) a_O`.

If `m = |Lambda / ~|` and `F` is invertible, the conjugation-symmetric retained
coefficient vector is recovered exactly from `m` samples.

## Corollary 2: first nontrivial retained witness drops from four samples to three

For the retained four-weight set

`Lambda = {(0,0),(1,0),(0,1),(1,1)}`,

the conjugation orbits are

- `{(0,0)}`,
- `{(1,0),(0,1)}`,
- `{(1,1)}`.

So the full retained-basis dimension `4` drops to orbit count `3`.

Therefore three generic marked-holonomy samples recover the symmetric retained
data exactly on that witness sector.

## Explicit witness

Take

`v = c_(0,0) chi_(0,0) + c_(1,0) (chi_(1,0)+chi_(0,1)) + c_(1,1) chi_(1,1)`.

For the generic witness used in the runner, the `3 x 3` orbit-evaluation matrix
is invertible and recovers `(c_(0,0), c_(1,0), c_(1,1))` exactly.

But with only two samples, one symmetric retained direction remains
underdetermined.

## What this closes

- exact reduction of the retained finite inversion problem by the already-known
  conjugation symmetry
- exact clarification that the physical retained sampling dimension is orbit
  count, not full retained-basis size
- exact recovery of the first symmetric four-weight witness from three generic
  marked-holonomy samples

## What this does not close

- explicit same-surface values of the required marked-holonomy samples
- explicit closed-form class-sector matrix elements of `K_6^env`
- explicit closed-form class-sector matrix elements of `B_6(W)`
- explicit full infinite-sector coefficient data
- the global sole-axiom PF selector theorem

## Why this matters

This is the first symmetry-reduced constructive step on the live retained PF
seam.

The branch no longer has to say only:

- finite truncations are recoverable from finitely many samples.

It can now say the sharper physical thing:

- because conjugation symmetry is already exact, the retained sample burden
  drops to orbit count.

## Command

No standalone runner is present on current `main` for this restored dependency
note.

Expected summary:

- `THEOREM PASS=6 SUPPORT=3 FAIL=0`
