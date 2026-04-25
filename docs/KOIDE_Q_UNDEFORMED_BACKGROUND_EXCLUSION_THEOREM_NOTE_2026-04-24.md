# Koide Q undeformed-background exclusion theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py`  
**Status:** defense theorem sharpening the Q `J0` falsifier

## Purpose

Attack the remaining Q reviewer escape hatch:

```text
retain a nonzero undeformed charged-lepton scalar background J0.
```

## Theorem

On the two-channel source-response carrier, decompose a general background as:

```text
J0 = (s + z, s - z).
```

Here:

```text
s = common scalar background
z = traceless source-label background.
```

The response coefficients around `D+J0` are:

```text
Y(J0) = (1/(1+s+z), 1/(1+s-z)).
```

The dimensionless Koide ratio depends only on the relative/traceless response.
At `z=0`:

```text
Y = (1/(1+s), 1/(1+s))
K_TL = 0
Q = 2/3
```

for any common scalar `s`.

So a nonzero `J0` alone is too broad to falsify the dimensionless lane.  Only a
retained traceless background:

```text
z != 0
```

can change `Q`.

## Boundary

The common scalar `s` is scale-like.  It belongs to the separate overall lepton
scale lane `v0`, not to the dimensionless Q closure.

## Sharpened Falsifier

The dimensionless Q theorem is falsified only by retaining:

```text
retained_traceless_undeformed_charged_lepton_background_z_ne_0.
```

That is an additional dimensionless source datum, not a consequence of the
retained probe-source coefficient at `J=0`.

## Verification

```bash
python3 scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py
python3 -m py_compile scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py
```

Expected closeout:

```text
KOIDE_Q_UNDEFORMED_BACKGROUND_EXCLUSION_THEOREM=TRUE
NONZERO_J0_ALONE_IS_TOO_BROAD_FOR_DIMENSIONLESS_Q=TRUE
COMMON_BACKGROUND_BELONGS_TO_SCALE_BOUNDARY=TRUE
DIMENSIONLESS_Q_FALSIFIER_IS_RETAINED_TRACELESS_BACKGROUND_Z_NE_0=TRUE
KOIDE_Q_CLOSED_ABSENT_RETAINED_TRACELESS_BACKGROUND=TRUE
NO_TARGET_IMPORT=TRUE
FALSIFIER=retained_traceless_undeformed_charged_lepton_background_z_ne_0
BOUNDARY=common_scalar_background_s_belongs_to_v0_scale_lane
```
