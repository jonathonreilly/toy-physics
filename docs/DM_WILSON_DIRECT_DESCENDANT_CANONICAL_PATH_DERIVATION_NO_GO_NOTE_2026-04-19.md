# DM Wilson Direct-Descendant Canonical Path Derivation No-Go Note

**Date:** 2026-04-19  
**Status:** exact negative result on the DM canonical-path lane  
**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_canonical_path_selector_theorem_2026_04_19.py`

## Question

Can the aligned-seed -> constructive-witness affine segment now be upgraded
from:

```text
a chosen support path with a unique exact crossing
```

to:

```text
a path that is itself forced by retained physics?
```

That would require one of:

- a unique geodesic,
- a unique flow line,
- a unique affine law on the fixed seed surface,
- or an equivalent theorem-grade path law selecting the same root without
  importing the witness by hand.

## Verdict

No. The path is still chosen.

The reason is now sharp:

1. the fixed-seed affine class already contains multiple distinct constructive
   exact selector candidates;
2. the natural constant-metric geodesic class inherits that same ambiguity;
3. the obvious seed-based `eta_1` gradient flow depends on the chosen metric
   and does not recover the current constructive root;
4. even the natural pullback metrics from the exact canonical carriers `Y` and
   `H = Y Y^dagger` fail in the same way;
5. the neighboring source-surface selector packet does not descend to the
   direct-descendant exact roots or plateau witnesses.

So the branch does not yet have a theorem-grade canonical path.

## Setup

Work on the fixed native `N_e` seed surface in local affine coordinates

```text
v = (a, b, c, d, e).
```

The aligned seed is

```text
v_seed = (0.56333333, 0.56333333, 0.30666667, 0.30666667, 0.0).
```

The current constructive witness is

```text
v_w = (1.17416156, 0.46254435, 0.75874142, 0.02690430, 1.88259576).
```

The current reviewed candidate path is the straight segment

```text
v_P(lambda) = (1 - lambda) v_seed + lambda v_w.
```

Its selected exact root is

```text
P = (1.04926685, 0.48315245, 0.66630668, 0.08410670, 1.49766553),
```

with observable pack

```text
(eta_1, gamma, E1, E2, Delta_src)
= (1.0, 0.17746600..., 0.24792261..., 1.55208573..., 0.00658311...).
```

## Theorem 1: fixed-seed affine laws remain ambiguous

The multiplicity packet already contains three other constructive overshooting
witness endpoints on the same fixed seed surface:

```text
A+ = (1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.89233895)
B+ = (0.86088785, 0.32714819, 0.71367707, 0.10440906, 1.59150180)
C+ = (1.00731313, 0.30177597, 0.79591855, 0.02985850, 2.19435677)
```

Each of these endpoints already satisfies

```text
eta_1 > 1,   gamma > 0,   E1 > 0,   E2 > 0,   Delta_src > 0.
```

Now define the three competing seed-fixed affine laws

```text
v_A(lambda) = (1 - lambda) v_seed + lambda A+
v_B(lambda) = (1 - lambda) v_seed + lambda B+
v_C(lambda) = (1 - lambda) v_seed + lambda C+.
```

The runner certifies exact transverse `eta_1 = 1` roots on each:

```text
lambda_A = 0.746363160385...,   d eta_1 / d lambda |_A = 0.545503299143...
lambda_B = 0.999143075148...,   d eta_1 / d lambda |_B = 0.414779858182...
lambda_C = 0.999586526822...,   d eta_1 / d lambda |_C = 0.510977622215...
```

with selected points

```text
A_path = (1.01497656, 0.49220909, 0.65328256, 0.11912803, 1.41237208)
B_path = (0.86063287, 0.32735058, 0.71332829, 0.10458238, 1.59013800)
C_path = (1.00712956, 0.30188412, 0.79571626, 0.02997295, 2.19344946)
```

and packs

```text
A_path: (1.0, 0.14792387..., 0.24958820..., 1.45193690..., 0.00880419...)
B_path: (1.0, 0.08784500..., 0.04543037..., 1.12265931..., 0.02001948...)
C_path: (1.0, 0.07715807..., 0.11679743..., 1.60542658..., 0.01311861...)
```

Each of these roots is constructive, positive-branch, and locally complete in
the same observable chart.

Therefore the class

```text
seed-fixed affine segment to a constructive overshooting witness
```

still contains multiple distinct exact selector candidates.

### Corollary

The statement

```text
choose the unique eta_1 = 1 point on the seed-fixed affine path
```

does not define a unique law until the affine direction itself is derived.

## Theorem 2: geodesic language does not fix the segment

In the current affine chart, all of

```text
v_P(lambda), v_A(lambda), v_B(lambda), v_C(lambda)
```

have vanishing second finite difference and exact midpoint linearity. So for
the natural constant-metric class on this affine chart they are all geodesics.

That means geodesic language by itself does not promote the current segment to
uniqueness. To get a unique geodesic one would first need a metric on the seed
surface that is itself theorem-fixed by retained physics. No such metric is
currently carried by this lane.

## Theorem 3: the obvious seed-based gradient flow is metric-dependent

The most obvious retained-looking flow law is:

```text
follow the eta_1 gradient from the aligned seed until eta_1 = 1.
```

But a gradient needs a metric. Different constant metrics on the same affine
chart already give different exact roots.

The runner certifies:

- Euclidean metric flow lands on

  ```text
  v_grad^E = (0.586277, 0.418078, 0.265861, 0.209304, 0.0)
  ```

  with `eta_1 = 1` but `gamma = 0` and `E1 < 0`;

- `x1`-weighted metric flow lands on

  ```text
  v_grad^(x1) = (0.569279, 0.422267, 0.195765, 0.238317, 0.0)
  ```

  with `eta_1 = 1` but `gamma = 0`, `E1 < 0`, and `E2 < 0`.

These two exact flow roots are distinct from each other and distinct from the
current constructive path-selected root `P`.

### Corollary

The gradient-flow class is not closed either:

- it depends on the chosen metric;
- and even the obvious `eta_1` flow does not recover the constructive
  positive target.

## Theorem 4: the natural `Y`- and `H`-carrier pullback metrics still miss the constructive root

One natural attempt to repair Theorem 3 is to stop using arbitrary constant
metrics and instead use the exact canonical carriers already present on this
lane:

```text
Y(x,y,delta),   H(x,y,delta) = Y Y^dagger.
```

Pull back the Frobenius metric from these carrier spaces to the fixed native
seed surface. The runner verifies that both pullback metrics are positive
definite at the aligned seed:

```text
lambda_min(G_H(seed)) = 5.968896e-02,
lambda_min(G_Y(seed)) = 9.404444e-02.
```

So they are honest theorem-native metric candidates. But their `eta_1`
gradient flows still land on nonconstructive exact roots:

```text
v_grad^H = (0.65110101, 0.43193331, 0.30713402, 0.18639426, 0.0)
v_grad^Y = (0.63953158, 0.42183722, 0.32104885, 0.18257746, 0.0)
```

with packs

```text
v_grad^H: (1.0, 0.0, -0.23699551..., 0.22450038..., 0.03806907...)
v_grad^Y: (1.0, 0.0, -0.24405841..., 0.20824367..., 0.03763495...)
```

These exact roots are:

- distinct from each other;
- distinct from the current constructive point `P`;
- and not constructive positive.

### Corollary

The missing object is not merely:

```text
pick a more natural metric.
```

The two most obvious exact carrier-native metric choices already fail.

## Theorem 5: the current source-surface selector packet does not descend to the direct-descendant lane

The nearby source-surface theorems live on an exact H-side source-oriented
sheet whose shift-invariant intrinsic slot pair and CP pair are fixed
constants:

```text
(a_*, b_*),   (cp1_*, cp2_*).
```

If the direct-descendant exact roots or constructive plateau witnesses already
lived on that same sheet, they would reproduce those constants exactly.

They do not.

The runner certifies uniform lower bounds for the direct-descendant exact roots
`P`, `A_path`, `B_path`, `C_path`:

```text
max-slot error  >= 1.005552...
max-CP   error  >= 0.514999...
```

and for the constructive transport-plateau witnesses `W0`, `W1`, `W2`, `W3`:

```text
max-slot error  >= 0.969966...
max-CP   error  >= 0.514645...
```

So neither the current exact roots nor the currently known constructive
endpoints lie on the source-surface selector sheet.

As auxiliary evidence, even the simple "nearest source-surface witness"
heuristics split:

- nearest in intrinsic-slot error: `W3`,
- nearest in CP-pair error: `W0`.

So the source-surface packet does not yet furnish a unique endpoint-direction
law on this lane.

### Corollary

The direct-descendant canonical-path lane cannot currently be closed by merely
quoting the source-surface local selector theorems. To use that packet here,
one would first need a new theorem-grade bridge from the direct-descendant
`L_e / dW_e^H` data to the source-oriented H-side sheet.

## What extra ingredient is needed

To derive the path rather than choose it, the branch still needs one more
theorem-grade object of one of the following types:

1. a retained metric on the fixed seed surface that singles out one geodesic
   and actually lands on the constructive exact root;
2. a retained scalar potential or vector field whose flow is fixed without
   metric ambiguity and lands on the constructive exact root;
3. a retained endpoint or tangent-direction law selecting one witness
   direction on the direct-descendant lane itself;
4. a theorem-grade bridge showing that the source-surface selector packet is
   the correct descended law on this lane;
5. or, more directly, the microscopic value law on the descended local block
   `L_e`;
6. or an equivalent path law of the same selector strength.

Without one of those ingredients, the current path remains support-level only.

## Bottom line

The branch now knows exactly why the path is not yet canonical:

- uniqueness on one chosen segment is real but insufficient;
- multiple competing affine/geodesic selector laws already exist;
- the obvious gradient route is metric-dependent and misses the current
  constructive root;
- the natural exact carrier pullback geometries also miss the constructive
  root;
- and the neighboring source-surface selector packet does not yet descend to
  this lane.

So the DM canonical-path lane is still open.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md`](DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_MICROSCOPIC_VALUE_FRONTIER_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_MICROSCOPIC_VALUE_FRONTIER_THEOREM_NOTE_2026-04-18.md)
- [`docs/DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md`](DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md)
- [`docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`](DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
