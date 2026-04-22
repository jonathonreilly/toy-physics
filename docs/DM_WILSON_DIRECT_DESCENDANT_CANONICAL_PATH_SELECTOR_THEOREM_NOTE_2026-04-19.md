# DM Wilson Direct-Descendant Canonical Path Selector Status Note

**Date:** 2026-04-19  
**Status:** support-level candidate only — the path is still chosen, not
derived from retained physics  
**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_canonical_path_selector_theorem_2026_04_19.py`

## Verdict

The aligned-seed -> constructive-witness affine segment remains useful
support-level science, but it does **not** close the DM canonical-path lane.

What survives:

- on that explicit affine segment, the favored column `eta_1` still crosses
  exact closure uniquely and transversely;
- the selected point is still constructive, positive-branch, and locally
  visible in the full projected-source observable chart.

What fails:

- the path itself is still not forced by retained physics;
- other equally seed-fixed constructive affine laws already produce distinct
  exact positive roots;
- geodesic language does not rescue uniqueness;
- even the natural `Y`- and `H`-carrier pullback geometries do not recover the
  current constructive point;
- the neighboring source-surface selector theorems do not yet descend to this
  direct-descendant lane.

So the honest branch verdict is:

> the current path law is still chosen, not derived.

## The current support-level candidate still works on its own segment

On the explicit affine path

```text
v_P(lambda) = (1 - lambda) v_seed + lambda v_w,
```

from the aligned native seed to the explicit constructive witness, the runner
still certifies:

- one exact `eta_1 = 1` crossing;
- transverse slope

  ```text
  d eta_1 / d lambda |_P = 0.445808799932... > 0;
  ```

- constructive positive selected point

  ```text
  P
  = (1.04926685, 0.48315245, 0.66630668, 0.08410670, 1.49766553),
  ```

  with observable pack

  ```text
  (eta_1, gamma, E1, E2, Delta_src)
  = (1.0, 0.177466004463..., 0.247922610478..., 1.552085732579..., 0.006583113927...).
  ```

So the old candidate is still real science. It is just not yet a reviewer-grade
canonical path law.

## Why the path is still not derived

The new load-bearing negative result is recorded in
[DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_DERIVATION_NO_GO_NOTE_2026-04-19.md](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_DERIVATION_NO_GO_NOTE_2026-04-19.md).

Its content is:

1. **Affine ambiguity remains.**  
   Three other retained constructive overshooting witnesses `A+`, `B+`, `C+`
   already live on the same fixed native seed surface. The seed-fixed affine
   segments to those witnesses also have exact transverse `eta_1 = 1` roots,
   and those roots are distinct from the current candidate point.

2. **Geodesic language remains ambiguous.**  
   In the present affine chart, the current segment and the competing `A+`,
   `B+`, `C+` segments are all straight lines. So under the natural
   constant-metric class they are all geodesics. No retained theorem yet fixes
   a metric that would single out only the current one.

3. **Gradient-flow language is not closed either.**  
   If one tries the obvious seed-based law "follow the `eta_1` gradient until
   `eta_1 = 1`", the answer depends on the chosen metric. Euclidean and
   `x1`-weighted constant metrics land on different exact roots, and neither
   root is the current constructive positive point.

4. **The most natural retained carrier metrics still fail.**  
   The runner now also tests the pullback of the Frobenius metric from the
   exact canonical carriers `Y` and `H = Y Y^dagger`. Both pullback metrics are
   positive definite at the aligned seed, so they are honest theorem-native
   metric candidates. But their `eta_1` gradient flows land on

   ```text
   v_grad^H = (0.65110101, 0.43193331, 0.30713402, 0.18639426, 0.0)
   v_grad^Y = (0.63953158, 0.42183722, 0.32104885, 0.18257746, 0.0),
   ```

   both with exact `eta_1 = 1` and both nonconstructive:

   ```text
   v_grad^H: (1.0, 0.0, -0.23699551..., 0.22450038..., 0.03806907...)
   v_grad^Y: (1.0, 0.0, -0.24405841..., 0.20824367..., 0.03763495...)
   ```

   So even the obvious carrier-native geometries do not derive the current
   constructive exact point.

5. **The source-surface selector packet does not yet descend here.**  
   The nearby source-surface theorems live on a different exact H-side sheet
   whose shift-invariant intrinsic slot pair and CP pair are fixed constants.
   The direct-descendant exact roots `P`, `A_path`, `B_path`, `C_path` and the
   constructive transport-plateau witnesses `W0`, `W1`, `W2`, `W3` all stay
   uniformly away from those source-surface constants. So the current lane does
   not yet carry a theorem-grade bridge that would let one import the
   source-surface local selector law as the missing endpoint-direction law.

That is enough to miss the closure bar.

## Exact competing affine-selected roots

The no-go packet certifies the following three additional seed-fixed affine
roots from equally constructive overshooting witnesses:

```text
A_path = (1.01497656, 0.49220909, 0.65328256, 0.11912803, 1.41237208)
B_path = (0.86063287, 0.32735058, 0.71332829, 0.10458238, 1.59013800)
C_path = (1.00712956, 0.30188412, 0.79571626, 0.02997295, 2.19344946)
```

with packs

```text
A_path: (1.0, 0.14792387..., 0.24958820..., 1.45193690..., 0.00880419...)
B_path: (1.0, 0.08784500..., 0.04543037..., 1.12265931..., 0.02001948...)
C_path: (1.0, 0.07715807..., 0.11679743..., 1.60542658..., 0.01311861...)
```

Each is constructive, positive-branch, and locally complete in the same
observable chart. So the statement

```text
choose the unique eta_1 = 1 point on a fixed-seed affine path to a
constructive overshooting witness
```

is still ambiguous.

## What extra ingredient is needed

To upgrade the path from chosen to derived, the branch still needs one more
retained theorem-grade ingredient of one of these types:

- a metric on the fixed seed surface that is itself forced by retained physics
  and gives a unique relevant geodesic;
- a scalar potential or vector field on that surface whose flow is
  theorem-fixed and lands on the physical constructive root;
- a theorem-fixed endpoint or tangent-direction law that selects one witness
  direction without importing it by hand;
- a direct-descendant bridge theorem proving that the source-surface selector
  packet is the correct descended law on this lane;
- or, more directly, the microscopic value law on the descended local block
  `L_e` itself;
- or an equivalent path law of the same selector strength.

Without one of those, the current affine segment cannot honestly be called the
canonical path.

## Bottom line

The branch now knows something sharper than before:

- the old affine segment is a real selector candidate;
- but the path-derivation problem is still open;
- and the exact reason is now pinned to affine/geodesic ambiguity, failure of
  the natural carrier pullback flows, and absence of a bridge from the
  source-surface selector packet.

So the DM canonical-path lane is **not closed**.

## Cross-references

- `docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_DERIVATION_NO_GO_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_MICROSCOPIC_VALUE_FRONTIER_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_canonical_path_selector_theorem_2026_04_19.py
```

Expected:

- `VERDICT: PATH STILL CHOSEN`
