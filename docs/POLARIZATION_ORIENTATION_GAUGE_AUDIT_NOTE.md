# Polarization Orientation / Chirality Gauge Audit

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Ownership:** orientation / chirality attack only

## Verdict

The atlas already contains exact orientation, chirality, handedness, and
anomaly-forced-time structure, but those inputs do **not** canonically reduce
the remaining polarization-bundle gauge beyond the residual groups already
identified in the support and universal blockers.

What they do canonically fix is:

1. the time orientation and single-clock `3+1` background;
2. the exact invariant `A1` core;
3. the ordered bright Route-2 carrier block;
4. the fact that the complement is an orbit bundle rather than a canonical
   section.

What they do **not** fix is:

1. a canonical support-side `Pi_3+1` on the dark complement;
2. a canonical universal-side `Pi_curv` / distinguished connection;
3. a reduction of the surviving residual gauge below the exact subgroups
   already measured in the existing atlas.

## Exact structures checked

### 1. Anomaly-forced time

[`ANOMALY_FORCES_TIME_THEOREM.md`](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)
forces a single clock:

`d_t = 1`.

That is a genuine orientation result: it fixes the temporal direction and
removes multi-time ambiguity. It does **not** supply a spatial polarization
frame for the remaining bundle complement.

### 2. Cap-map handedness

[`S3_EXISTING_WORK_FOR_CAP_MAP.md`](/private/tmp/physics-review-active/docs/S3_EXISTING_WORK_FOR_CAP_MAP.md)
records that both orientation choices on the cap map still give `S^3`, because
`S^3` admits an orientation-reversing self-homeomorphism.

So the cap-map handedness is a `Z_2` background choice, not a bundle gauge
fixing mechanism. It stabilizes the background topology, but it does not
canonically select the dark polarization complement.

### 3. Support-side canonical frame

[`FINITE_RANK_SUPPORT_CANONICAL_FRAME_NOTE.md`](/private/tmp/physics-review-active/docs/FINITE_RANK_SUPPORT_CANONICAL_FRAME_NOTE.md)
shows that the exact support data canonically fix:

- `A1(center)`;
- `A1(shell)`;
- the ordered bright pair `u_E, u_T`.

But the dark complement remains free. After endpoint sign conventions are
fixed, the exact leftover gauge is:

`O(1)_{E_perp} x O(2)_{T1_darken}`.

### 4. Universal canonical projector

[`UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md`](/private/tmp/physics-review-active/docs/UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md)
shows the exact invariant core

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`

is canonical, but the complement is still an `SO(3)` orbit bundle.

So the exact residual universal gauge is:

`SO(3)`.

## What orientation/chirality actually buys us

Orientation and chirality do buy a real reduction:

1. `d_t = 1` is fixed.
2. The `Pi_A1` core is fixed.
3. The bright support carrier block is ordered.
4. The background cap map is topologically pinned to `S^3`.

But none of those structures canonically chooses the dark polarization
complement or a distinguished curvature-localization connection.

## Residual subgroup theorem

On the current atlas, after all orientation/chirality/handedness/time
structure is applied, the exact surviving residual gauge is still:

- support side: `O(1)_{E_perp} x O(2)_{T1_darken}`
- universal side: `SO(3)`

There is no further canonical reduction visible from the current atlas.

## Bundle consequence

The strongest exact shared object remains the `Pi_A1`-anchored common bundle
candidate:

`P_R^cand = (Pi_A1, B_R, O_R)`,

with

`B_R = (K_R, I_TB, Xi_TB)`.

Orientation/chirality fixes the invariant core and time direction, but it does
not collapse the candidate into a full canonical bundle.

## Bottom line

The exact residual gauge that survives all orientation, chirality, handedness,
and anomaly-forced-time structure already in the atlas is unchanged from the
blockers:

- support: `O(1) x O(2)`
- universal: `SO(3)`

So the orientation/chirality attack does not reveal a hidden canonical bundle
reduction. It sharpens the same obstruction into its final surviving subgroup.
