# Planck-Scale Time-Locked Factorized Cell Object Derivation

**Date:** 2026-04-23  
**Status:** branch-local object-derivation theorem candidate for the direct Planck lane  
**Audit runner:** `scripts/frontier_planck_timelocked_factor_cell_object_derivation.py`

## Question

Can the exact labeled factorized cell used by the direct Planck route be tied
to accepted package surfaces, rather than treated as a branch-local convenience?

The object to justify is:

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z ~= C^16`.

## Bottom line

Yes, in branch-local theorem-candidate form.

The direct Planck cell can be read as the exact synthesis of three already-open
surfaces:

1. **derived single time direction**
   from [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md);
2. **minimal exact `3+1` APBC block**
   from [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)
   and the minimal `2^4 = 16` block language already used in
   [HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md);
3. **exact spatial taste cube**
   `C^8 = (C^2)^{\otimes 3}`
   from [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
   and [S3_TASTE_CUBE_DECOMPOSITION_NOTE.md](./S3_TASTE_CUBE_DECOMPOSITION_NOTE.md).

Combining these:

- the exact spatial local carrier is the three-bit taste cube
  `C^8 = C^2_x ⊗ C^2_y ⊗ C^2_z`;
- the exact derived-time minimal APBC block contributes one temporal two-state
  factor `C^2_t`;
- therefore the exact time-locked local cell object is

  `H_cell = C^2_t ⊗ C^8 = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z ~= C^16`.

So the factorized cell object used by the direct Planck route is no longer just
an arbitrary rewrite. It is the natural local object assembled from already-used
time and cube surfaces.

## What this does and does not do

This note does:

- make the exact labeled factorized cell much more native to the branch-local
  direct route;
- reduce hostile-review force on the objection that `C^16` was an ad hoc
  convenience object;
- support the later object-well-definedness theorem as a statement about an
  earned cell object.

This note does **not** by itself finish the Planck close. It does not derive
the source-free tracial state. It only sharpens the object on which that state
law is being asked to live.

## Inputs

- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)
- [HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [S3_TASTE_CUBE_DECOMPOSITION_NOTE.md](./S3_TASTE_CUBE_DECOMPOSITION_NOTE.md)
- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)

## Theorem 1: exact spatial factorized cube object

The site-phase / cube-shift bridge gives the exact spatial cube object

`C^8 = (C^2)^{\otimes 3}`.

Its three tensor positions are exactly the three spatial axes.

So the spatial local cell object on this support surface is

`H_sp = C^2_x ⊗ C^2_y ⊗ C^2_z`.

## Theorem 2: exact derived-time two-state factor on the minimal `3+1` block

The anomaly/time theorem yields exactly one time direction, and the exact
minimal `3+1` APBC block uses one temporal coordinate together with three
spatial coordinates.

On the minimal `L_t = 2` APBC block, that temporal coordinate contributes a
two-state temporal factor:

`H_t = C^2_t`.

So the local minimal `3+1` block is a one-time-factor extension of the exact
spatial cube object.

## Corollary 1: exact time-locked factorized cell object

Combining Theorems 1 and 2 gives

`H_cell = H_t ⊗ H_sp = C^2_t ⊗ (C^2_x ⊗ C^2_y ⊗ C^2_z) ~= (C^2)^{\otimes 4} ~= C^16`.

This is exactly the labeled factorized cell used by the direct Planck route.

## Why this matters for the last blocker

The object-well-definedness route was vulnerable to the objection:

> maybe the exact labeled factorized cell is itself a branch-local convenience,
> so representation-independence on that object is not native enough.

This note weakens that objection sharply. The labeled factorized cell is now
the natural local object obtained by:

- exact spatial taste-cube factorization,
- exact derived single time direction,
- exact minimal `3+1` local block.

So the last state-law question can now be phrased more sharply:

> on this exact time-locked factorized cell object, does a source-free local
> state assignment have to be well-defined under factor-preserving
> presentation changes?

## Honest status

This is still branch-local science. It is not woven through `main`.

It does **not** by itself prove native Planck closure.

But it does move the branch materially forward: the direct Planck route’s local
cell object is now tied to already-earned time and cube surfaces rather than
floating as an unexplained convenience.
