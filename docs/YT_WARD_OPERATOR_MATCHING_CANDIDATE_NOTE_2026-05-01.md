# Top-Yukawa Ward Operator-Matching Candidate Note

**Date:** 2026-05-01  
**Status:** conditional-support / open; no retention proposal  
**Runner:** `scripts/frontier_yt_ward_operator_matching_candidate.py`  
**Certificate:** `outputs/yt_ward_operator_matching_candidate_2026-05-01.json`

## Purpose

This is the positive follow-up to the Ward physical-readout repair audit.  It
does not close the theorem.  It isolates the tree-level operator-normalization
arithmetic that a repaired Ward route would need, while keeping every remaining
physical-readout bridge explicit.

## Computed Tree-Level Map

The candidate uses only structural counts and standard tree-level operator
normalizations:

| Factor | Value |
|---|---:|
| color count `N_c` | 3 |
| iso count `N_iso` | 2 |
| scalar-singlet normalization | `1/sqrt(N_c N_iso) = 1/sqrt(6)` |
| top trilinear component projection | `1/(sqrt(N_c) sqrt(N_iso)) = 1/sqrt(6)` |
| HS scalar-channel residue amplitude at `g_bare = 1` | `1/sqrt(2 N_c) = 1/sqrt(6)` |
| Dirac chirality decomposition coefficient | 1 |
| SM SSB vertex readout convention factor | 1 |

The runner checks that these independent tree-level factors numerically meet
at

```text
1/sqrt(6) = 0.408248290463863
```

but it also checks the firewall: matching arithmetic is not physical Yukawa
closure unless the open readout bridges are derived.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_ward_operator_matching_candidate.py
# SUMMARY: PASS=9 FAIL=0
```

The important pass is not the arithmetic.  The important pass is the status
firewall:

```text
open imports=[
  source_or_hs_normalization,
  chirality_projection_and_right_handed_selector,
  physical_scalar_uniqueness,
  scalar_lsz_external_leg,
  common_tadpole_dressing
]
```

## What This Candidate Shows

The old Ward theorem's `1/sqrt(6)` is not numerically mysterious.  Three
different tree-level readings land on the same normalization:

1. the color/iso scalar singlet;
2. the top component of the physical trilinear;
3. the HS scalar-channel residue at the canonical `g_bare = 1` surface.

That agreement is useful because it narrows the repair.  The missing theorem is
not another normalization calculation.  The missing theorem is the physical
readout map from the retained action to the SM Yukawa vertex.

## Required Repairs Before Closure

| Open import | Required theorem |
|---|---|
| source / HS normalization | derive the Legendre/HS source normalization and VEV division as functional derivatives of the retained action |
| chirality / right-handed selector | derive the `Q_L` to `q_R` chirality/species selector without matrix-element identification |
| physical scalar uniqueness | prove the scalar carrier selected by the source functional is the physical Higgs fluctuation |
| scalar LSZ leg | derive the `Z_phi` / LSZ bridge as a physical external-leg theorem |
| common dressing | prove gauge and scalar readouts share the needed dressing without alpha_LM or plaquette normalization as load-bearing proof inputs |

## Non-Claims

- This note does not define the top Yukawa via an `H_unit` matrix element.
- This note does not use observed `m_t` or observed `y_t` as proof input.
- This note does not promote the Ward theorem.
- This note does not update any manuscript claim surface.
