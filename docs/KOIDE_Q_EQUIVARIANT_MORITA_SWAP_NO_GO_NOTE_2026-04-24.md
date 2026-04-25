# Koide Q equivariant-Morita swap no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_equivariant_morita_swap_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use a stronger Morita argument:

```text
M_1 ⊕ M_2 Morita-equivalent to C ⊕ C
swap the two C components
  -> equal component weights
  -> K_TL = 0.
```

## Positive-looking part

The runner verifies that the non-equivariant skeleton swap would force:

```text
w_plus = 1/2
Q = 2/3
K_TL = 0.
```

This is the closest Morita route to a closure.

## Obstruction

The retained charged-lepton blocks are not merely matrix algebras.  They carry
C3 character-orbit data:

```text
P_plus orbit = {0}
P_perp orbit = {1,2}.
```

A retained equivariant Morita/naturality theorem must preserve trivial versus
nontrivial real character orbit.  The component swap exists only after
forgetting that retained C3 structure.

## Residual

```text
RESIDUAL_SCALAR = equivariant_component_weight_w_plus_minus_one_half_equiv_K_TL
RESIDUAL_EQUIVARIANCE = nontrivial_C3_orbit_type_blocks_Morita_skeleton_swap
```

## Why this is not closure

Non-equivariant Morita would close by erasing the C3 orbit type that defines
the retained Koide lane.  Equivariant Morita keeps that structure and leaves
the component-weight simplex.

## Falsifiers

- A proof that the retained physical source is Morita-invariant after
  forgetting C3 character-orbit type.
- A C3-equivariant Morita autoequivalence exchanging `{0}` and `{1,2}`.
- A physical theorem that the C3 orbit distinction is not source-visible.

## Boundaries

- Covers the strongest skeleton-swap version of the Morita route.
- Does not refute a new principle explicitly declaring C3 orbit type
  source-invisible, but that principle would need independent justification.

## Hostile reviewer objections answered

- **"Morita makes both blocks into points."**  Non-equivariantly, yes; the
  retained C3 orbit labels are then forgotten.
- **"The skeleton has a swap."**  The skeleton swap is not C3-equivariant.
- **"Uniform over Morita components closes Q."**  It closes only after adding
  source-invisibility of the retained orbit type.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_equivariant_morita_swap_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_EQUIVARIANT_MORITA_SWAP_NO_GO=TRUE
Q_EQUIVARIANT_MORITA_SWAP_CLOSES_Q=FALSE
RESIDUAL_SCALAR=equivariant_component_weight_w_plus_minus_one_half_equiv_K_TL
RESIDUAL_EQUIVARIANCE=nontrivial_C3_orbit_type_blocks_Morita_skeleton_swap
```
