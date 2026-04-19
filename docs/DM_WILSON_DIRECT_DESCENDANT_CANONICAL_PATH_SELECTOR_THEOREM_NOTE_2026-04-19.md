# DM Wilson Direct-Descendant Canonical Path Selector Theorem

**Date:** 2026-04-19  
**Status:** explicit path-selected law on the constructive positive exact-
closure route. On the exact affine path from the aligned native seed to the
explicit constructive witness, the favored column `eta_1` crosses exact
closure exactly once and transversely. So the current branch now carries an
explicit selector-law candidate:

```text
choose the unique eta_1 = 1 point on the aligned-seed -> constructive-witness path.
```

This is real science progress on the open DM gate, but it is still a
**path-chosen** law, not a reviewer-grade derivation of the selected object
from retained physics alone.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_canonical_path_selector_theorem_2026_04_19.py`
(`PASS=15 FAIL=0`).

## Question

The old constructive continuity theorem proved only existence:

- on the explicit interpolation family from the aligned native seed to the
  constructive witness, there exists `lambda_* in (0,1)` with `eta_1 = 1`.

But that did not yet make the interpolation family into a law. Two sharper
questions remained:

1. is the exact root on that path unique?
2. if so, does that unique path-selected root survive as a genuine positive
   direct-descendant selector candidate rather than just an existence witness?

## Bottom line

Yes, on the current branch.

Write the exact fixed-seed affine path

```text
(x, y, delta)(lambda)
  = (1 - lambda) (x_seed, y_seed, 0) + lambda (x_w, y_w, delta_w),
  lambda in [0, 1].
```

Then:

1. the path stays exactly on the fixed native `N_e` seed surface;
2. `eta_1(lambda) - 1` changes sign exactly once on a dense current-branch
   scan;
3. after a shallow initial dip, `eta_1(lambda)` is strictly increasing on the
   sampled tail, so the exact crossing is unique on the canonical path;
4. the crossing is transverse:

   ```text
   d eta_1 / d lambda |_* = 0.445808799932... > 0;
   ```

5. the selected point still satisfies

   ```text
   eta_1 = 1,
   gamma > 0,
   E1 > 0,
   E2 > 0,
   Delta_src > 0;
   ```

6. the projected-source scalar pack

   ```text
   (eta_1, gamma, E1, E2, Delta_src)
   ```

   again has full local rank there, so the path-selected point is already
   visible in a locally complete observable chart;
7. this selected point is distinct from the other already-certified exact
   constructive positive roots from the multiplicity packet.

So the branch now has an explicit selector-law candidate on the open DM gate:

> choose the unique exact closure point on the canonical aligned-seed ->
> constructive-witness affine path.

## The selected point

The unique canonical-path crossing is

```text
lambda_* = 0.795532193595...
```

with direct-descendant coordinates

```text
(x1, x2, y1, y2, delta)
= (1.04926685, 0.48315245, 0.66630668, 0.08410670, 1.49766553),
```

and projected-source observable pack

```text
(eta_1, gamma, E1, E2, Delta_src)
= (1.0, 0.177466004463..., 0.247922610478..., 1.552085732579..., 0.006583113927...).
```

These are strictly constructive and positive-branch values.

## Why this matters

This upgrades the old continuity witness in a real way.

Before this theorem, the explicit aligned-seed -> constructive-witness path
only supplied:

- one existence argument for an exact closure point.

After this theorem, the same path supplies:

- a unique exact crossing,
- a transverse selection event,
- an explicit selected point,
- and a point that remains locally visible in the full projected-source scalar
  coordinates.

So the path is no longer only an existence device. It is now an explicit
selector-law candidate on the current branch.

## Relation to the other exact positive roots

The multiplicity packet already certified three other exact constructive
positive roots on the fixed native seed surface:

- family `A`,
- family `B`,
- family `C`.

The present theorem proves the canonical-path-selected root is not secretly one
of those previously certified points:

- each of `A`, `B`, and `C` stays a definite distance off the canonical path
  segment;
- each is also a definite distance away in direct-descendant parameter space.

So this is genuinely new selector content, not a relabeling of the earlier
multiplicity witnesses.

## What this closes

- the loophole that the constructive interpolation family only proved
  existence but not uniqueness on its own path;
- the ambiguity over whether the canonical constructive path lands on a
  locally visible projected-source point;
- the idea that the continuity route had no actual selector interpretation.

## What this does not close

- a reviewer-grade derivation of the path itself from retained physics;
- a derivation of the explicit constructive witness from retained physics;
- the finer microscopic value law on `L_e = Schur_{E_e}(D_-)`;
- the final DM flagship gate.

So the honest status is:

- **path-selected law:** yes;
- **reviewer-grade object derivation:** still no.

## Cross-references

- `docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_canonical_path_selector_theorem_2026_04_19.py
```

Expected:

- `PASS=15 FAIL=0`
