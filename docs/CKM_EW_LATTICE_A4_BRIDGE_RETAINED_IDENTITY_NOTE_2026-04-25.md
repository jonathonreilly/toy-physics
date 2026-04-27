# CKM-EW Lattice A4 Bridge Retained Identity

**Date:** 2026-04-25

**Status:** proposed_retained EW-CKM lattice-scale identity theorem; companion
corollary to the retained below-`W2` `A^2` source theorem.

**Primary runner:** `scripts/frontier_ckm_ew_lattice_a4_bridge.py`

## Purpose

This note packages the lattice-scale EW-CKM corollary

```text
sin^2(theta_W)|_lattice = A^4 = 4/9
```

on the retained surface.

The companion theorem
[`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
now separately grounds

```text
A^2 = N_pair/N_color = 2/3
```

below `W2` from the retained quark-doublet source theorem. This note keeps the
EW-CKM bridge itself isolated as the lattice-scale corollary.

The retained identity packaged here is:

```text
sin^2(theta_W)|_lattice = A^4 = 4/9.
```

The left side is retained by the EW lattice-normalization lane. The right
side is retained by the Wolfenstein `W2` lane. The equality is therefore a
retained cross-surface lattice-scale identity.

What is **not** claimed here is that the bridge note by itself re-derives
`A^2` below `W2` solely from the retained existence of `SU(2)_L` and
`SU(3)_c`.
The equality

```text
dim_fund(SU(2)) / dim_fund(SU(3)) = 2/3 = A^2
```

is a retained consistency equality at the accepted values. The actual
below-`W2` derivation now lives in the companion source theorem, not in this
corollary note alone.

## Retained Inputs

| Input | Authority | Status |
| --- | --- | --- |
| `g_2^2 = 1/(d+1)`, `g_Y^2 = 1/(d+2)`, `d=3` | [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) | retained EW normalization lane |
| `A^2 = N_pair/N_color = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | retained CKM structural identity |
| below-`W2` source theorem for `A^2 = N_pair/N_color = 2/3` | [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md) | retained companion theorem |
| `N_pair=2`, `N_color=3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained CKM structural-counts identity |
| `SU(2)_L`, `SU(3)_c` retained gauge structures | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) | retained framework/current-consequence surface |

Support-tier CL3 taste-generation readings are not used.

## Theorem 1: retained lattice-scale EW-CKM bridge

On the retained EW lattice-normalization lane,

```text
g_2^2 = 1/(d+1),
g_Y^2 = 1/(d+2),
d = 3.
```

Therefore

```text
sin^2(theta_W)|_lattice
  = g_Y^2 / (g_Y^2 + g_2^2)
  = (1/(d+2)) / (1/(d+2) + 1/(d+1))
  = (d+1)/(2d+3)
  = 4/9.
```

On the retained CKM Wolfenstein lane,

```text
A^2 = 2/3,
```

so

```text
A^4 = 4/9.
```

Thus

```text
sin^2(theta_W)|_lattice = A^4 = 4/9.
```

This is an exact retained identity at the lattice scale. It is not a claim
about the low-energy physical value of `sin^2(theta_W)` at `M_Z`.

## Theorem 2: gauge-dimension consistency equality

The retained gauge structures include `SU(2)_L` and `SU(3)_c`. Standard
representation theory gives

```text
dim_fund(SU(2)) = 2,
dim_fund(SU(3)) = 3.
```

Therefore

```text
dim_fund(SU(2)) / dim_fund(SU(3)) = 2/3.
```

Since retained `W2` gives

```text
A^2 = 2/3,
```

there is a retained equality

```text
A^2 = dim_fund(SU(2)) / dim_fund(SU(3)) = 2/3.
```

This is a consistency identity between retained structures. The actual
below-`W2` derivation of the Wolfenstein `A^2` law now comes from the
companion quark-doublet source theorem; the equality in this note remains the
gauge-dimension corollary.

## Claim Boundary

What is retained here:

- `sin^2(theta_W)|_lattice = A^4 = 4/9`;
- `A^2 = dim_fund(SU(2))/dim_fund(SU(3)) = 2/3` as a retained consistency
  equality;
- the companion theorem closes `A^2` below `W2` on current `main`;
- exact rational verification using retained EW and CKM authority files.

What is not retained here:

- an independent below-`W2` derivation inside this note alone;
- a promotion of `CL3_TASTE_GENERATION_THEOREM` or any support-tier theorem;
- a physical `M_Z` prediction for `sin^2(theta_W)`;
- a Koide closure or charged-lepton mass theorem.

## Reproduction

```bash
python3 scripts/frontier_ckm_ew_lattice_a4_bridge.py
```

Expected result:

```text
TOTAL: PASS=36, FAIL=0
PASSED: 36/36
```

## Closeout Flags

```text
CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY=TRUE
SIN2_THETA_W_LATTICE_EQUALS_A4=TRUE
GAUGE_DIMENSION_RATIO_EQUALS_A2_CONSISTENCY=TRUE
A2_BELOW_W2_DERIVATION_CLOSED=TRUE
SUPPORT_TIER_PROMOTION=FALSE
KOIDE_CLOSURE=FALSE
```
