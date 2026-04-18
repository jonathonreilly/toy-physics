# Gauge-Vacuum Plaquette First Symmetric Three-Sample Current-Stack Constraint Boundary

**Date:** 2026-04-17  
**Status:** exact boundary theorem on the plaquette PF lane; after the exact
radical reconstruction-map theorem, the strongest honest further sharpening on
the first retained three-sample seam is that the current exact stack supplies
no additional symmetry or source-observable collapse below the three named
same-surface values  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_current_stack_constraint_boundary_2026_04_17.py`

## Question

After the exact radical reconstruction-map theorem fixes the first symmetric
three-sample matrix and its exact inverse, is there one stronger honest theorem
on the live `beta = 6` seam?

## Answer

Yes, but it is a boundary theorem rather than explicit `beta = 6` closure.

On the first symmetric retained witness sector, the current exact stack does
**not** reduce the live burden below the three explicit same-surface values

`Z_6^env(W_A)`,

`Z_6^env(W_B)`,

`Z_6^env(W_C)`.

More precisely:

- the three named holonomies are pairwise neither conjugate nor
  inverse-conjugate, so centrality and class-function reality do not identify
  any pair of sample values,
- the exact radical-form orbit-evaluation matrix remains full rank,
- the `W_A` decoupling of the `chi_(1,1)` orbit is real and structural, but it
  does not collapse the remaining sample burden below three because the two
  non-decoupled rows remain independent and separate the `chi_(1,1)` orbit with
  opposite sign,
- the connected-hierarchy, bridge-support, and observable-principle surfaces
  constrain scalar/source data, not holonomy-resolved boundary amplitudes.

So the strongest honest next theorem on the first retained three-sample seam is
not a new hidden linear relation among the three sample values. It is the exact
statement that the current stack still leaves those three explicit values to be
evaluated.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md):

- the first symmetric retained witness sector is

`v = a_(0,0) chi_(0,0)
   + a_(1,0) (chi_(1,0) + chi_(0,1))
   + a_(1,1) chi_(1,1)`,

- the three named marked holonomies are

`W_A = W(-13 pi / 16,  5 pi / 8)`,

`W_B = W( -5 pi / 16, -7 pi / 16)`,

`W_C = W(  7 pi / 16,-11 pi / 16)`,

- and the exact radical-form evaluation matrix is already explicit and
  invertible.

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md)
and
[GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md):

- `Z_beta^env(W)` is a central positive-type class function,
- after compression,
  `Z_beta^env(W) = <K(W), v_beta>`,
- so the only compressed unknown is the coefficient vector `v_beta`.

From
[GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md)
and
[GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md):

- on the first symmetric witness sector, three independent symmetric samples are
  exactly the right burden,
- and fewer generically leave one retained direction underdetermined.

From
[GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md),
[GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md),
and
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the live exact source-observable theorems constrain scalar plaquette-response
  data and connected cumulants,
- but they do not derive holonomy-resolved relations among the three named
  boundary samples.

## Theorem 1: the three named sample points are not collapsed by centrality or reality

Let

`W(theta1, theta2)
 = diag(exp(i theta1), exp(i theta2), exp(-i(theta1 + theta2)))`.

Then the three named holonomies `W_A, W_B, W_C` have pairwise distinct torus
eigenvalue multisets, and no pair is related by inversion followed by
conjugation.

Therefore:

- no pair of the three sample points is identified by centrality,
- no pair is identified by the reality relation of a real central class
  function,
- so the current exact class-function symmetries do not collapse the three
  sample values to two or one.

## Theorem 2: the exact radical three-sample map is already irreducible on the first witness sector

Let

`Phi_0 = chi_(0,0)`,

`Phi_1 = chi_(1,0) + chi_(0,1)`,

`Phi_2 = chi_(1,1)`.

Define the exact orbit-evaluation matrix

`F_(i,j) = <K(W_i), Phi_j>`

for `i in {A,B,C}` and `j in {0,1,2}`.

Then:

- `F_(A,2) = 0` exactly,
- `F_(B,2) > 0` and `F_(C,2) < 0` exactly,
- the lower `2 x 2` block on rows `B,C` and columns `Phi_1, Phi_2` is
  nonsingular,
- and `det(F) != 0`.

So the first named three-sample system is not merely invertible; it is already
irreducible in the sense that:

- one sample is designed to kill the `chi_(1,1)` orbit,
- but the remaining two non-decoupled rows still carry independent orbit data,
- hence there is no further symmetry collapse below the full three named sample
  values on this witness sector.

## Corollary 1: there is no current-stack universal linear relation among the three named samples

On the first symmetric retained witness sector,

`Z = F a`,

with

`Z = [Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C)]^T`.

Because `F` is invertible, there is no nonzero universal row vector `lambda`
such that

`lambda^T Z = 0`

for every retained coefficient triple `a`.

The current exact character-measure and compressed evaluation laws fix the
class-function structure of `Z`, but do not add a new universal sample relation
beyond the already-explicit evaluation map.

## Corollary 2: the current source-observable stack does not yet reduce this seam further

The connected-hierarchy theorem, bridge-support stack, and observable-principle
theorem constrain:

- scalar plaquette expectations,
- source derivatives,
- connected cumulants,
- and the exact operator-theoretic location of the remaining environment data.

They do **not** yet produce holonomy-resolved equations forcing a new linear
relation among

`Z_6^env(W_A)`,

`Z_6^env(W_B)`,

`Z_6^env(W_C)`.

So the first retained three-sample `beta = 6` seam remains exactly what the
exact radical theorem suggests: evaluate the three named same-surface values
themselves.

## What this closes

- exact clarification that the three named sample points are not collapsed by
  current class-function symmetries
- exact clarification that the `W_A` decoupling does not reduce the burden
  below three because the remaining two rows are still independent
- exact clarification that the current exact source-observable stack does not
  supply a new linear collapse on the first retained three-sample seam
- exact sharpening of the first retained `beta = 6` PF target to explicit
  same-surface evaluation of the three named samples themselves

## What this does not close

- explicit same-surface values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit closed-form class-sector matrix elements of `K_6^env`
- explicit closed-form class-sector matrix elements of `B_6(W)`
- explicit coefficients beyond the first symmetric retained witness sector
- the global sole-axiom PF selector theorem

## Why this matters

This is the strongest honest theorem the current repo supports beyond the exact
radical reconstruction-map theorem.

It prevents one more wrong shortcut.

The branch no longer has to say only:

- the first sample matrix is explicit and invertible.

It can now say the sharper thing:

- the first sample matrix is explicit and irreducible on the current exact
  stack,
- the named samples are not collapsed by centrality or reality,
- the live source-observable theorems do not yet add a holonomy-resolved
  relation,
- so the next real work is explicit evaluation of those three named same-surface
  values.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_current_stack_constraint_boundary_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=4 FAIL=0`
