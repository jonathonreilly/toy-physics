# DM Wilson Direct-Descendant Constructive Transport Plateau Observable-Affine No-Go

**Date:** 2026-04-19  
**Status:** exact no-go theorem for a named source-side plateau-breaker family.
On the current constructive transport plateau, exact affine laws in the
source-side observable pack

```text
(gamma, E1, E2, Delta_src)
```

do **not** canonically select a witness. The four known constructive plateau
witnesses `W0, W1, W2, W3` are affinely independent in this `4`-pack, and each
one is the unique maximizer of some exact affine combination. So the family is
too unconstrained: its coefficients are extra selector input, not a derived
plateau-breaking law.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_observable_affine_no_go_2026_04_19.py`

## Question

After the same-day plateau theorem and canonical column-fiber theorem, the next
natural source-side attempt was:

> keep transport fixed, and let an exact observable law in
> `(gamma, E1, E2, Delta_src)` break the plateau.

This note tests that family in the strongest simple form:

- exact single-channel laws;
- exact affine combinations of the observable `4`-pack.

## Bottom line

This family does not give a canonical selector.

The branch now proves three exact facts on the known constructive plateau:

1. the four witness images in `(gamma, E1, E2, Delta_src)` are pairwise
   distinct and affinely independent;
2. single-channel extremization already splits across all four witnesses:

   - `max gamma -> W0`,
   - `max Delta_src -> W1`,
   - `max E2 -> W2`,
   - `max E1 -> W3`;

3. for each `Wi`, the runner constructs an exact affine law

   ```text
   L_i = c_gamma gamma + c_1 E1 + c_2 E2 + c_Delta Delta_src
   ```

   that uniquely maximizes at `Wi`.

So the family does not fail because it is constant on the plateau. It fails
for the opposite reason:

> it can be tuned to pick any witness.

Hence an affine observable plateau-breaker is not yet retained selector
content. The missing object is the physics that would derive the coefficients.

## Why this matters

This closes the cleanest coefficient-level loophole on the source-side
observable pack.

The same-day local observable-coordinate theorem showed that

```text
(eta_1, gamma, E1, E2, Delta_src)
```

already gives local coordinates at the constructive closure root. One might
still hope that a particularly simple observable value law on the plateau would
pick the physically correct source.

The present no-go sharpens that hope negatively:

- the observable pack really does vary on the plateau;
- but the exact affine family is not canonical;
- because the family itself already contains enough freedom to expose any known
  plateau witness.

So the remaining selector gap is not “find some affine observable score.” It
is “derive the source-side law that fixes why one score, with one coefficient
choice, is physical.”

## Auxiliary evidence from the other candidate families

The same runner records two supporting splits:

- simple Schur-side spectral laws already disagree on the winner
  (`max Tr(H_e)` and `max lambda_min(H_e)` select different witnesses);
- simple local Hessian/curvature invariants of the transport objective also
  disagree (`max tr(Hess eta_1)` and `max ||Hess eta_1||_F` select different
  witnesses).

So the current branch does not show a natural consensus breaker from these
first low-order source-side families either.

## What this closes

- the idea that an exact affine observable law in `(gamma, E1, E2, Delta_src)`
  already canonically breaks the constructive transport plateau;
- the hope that one could promote that whole family without supplying new
  coefficient physics;
- the reading that the plateau ambiguity is merely a bad choice of linear
  observable score.

## What this does not close

- a non-affine source-side law on the same observable pack;
- a genuinely microscopic Schur-side value law derived from retained physics;
- the final DM source-fiber selector.

## Cross-references

- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_observable_affine_no_go_2026_04_19.py
```

Expected:

- the four single-channel winners split as `W0/W1/W2/W3`;
- each witness is uniquely exposed by some affine observable law;
- `PASS` with `FAIL=0`.
