# PMNS Unified Bridge Carrier

**Date:** 2026-04-15  
**Status:** minimal-unification theorem for the branch Hermitian bridge,
the breaking-source space, and the selector primitive  
**Script:** `scripts/frontier_pmns_unified_bridge_carrier.py`

## Question

The current retained bank has now reduced the remaining PMNS work to three
exact missing objects:

- the selected-branch Hermitian-data law itself
- the exact three-real breaking-source law for `(delta, rho, gamma)`
- the restricted Higgs-offset selector on the canonical `(0,1)` pair

Is there a single new bridge/carrier object that simultaneously accounts for all
three, or do they remain genuinely separate add-ons?

## Bottom line

There is no positive retained-bank closure law here.

The strongest exact result is a **minimal unified extension theorem**:
the smallest exact object that simultaneously accounts for the Hermitian
bridge package `B_H,min`, the breaking-source space `S_break`, and the
selector primitive `B_red` is the single bundle

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`,

where:

- `(A, B, u, v, delta, rho, gamma)` is the exact minimal Hermitian bridge
  package
- `(delta, rho, gamma)` is the exact 3-real breaking-source coordinate
  triple
- `a_sel` is the unique reduced selector amplitude slot
- `e in {0,1}` is the optional seed-edge selector bit needed only if
  coefficient-level closure on the compatible weak-axis seed patch is also
  required

This is a single exact unified bridge object, but it is not a positive
derivation from the current bank. It is the smallest exact carrier the
current bank forces us to admit if we want all three missing objects at once.

## Exact structure

The unified object has three exact projections:

`pi_H(U_min) = (A, B, u, v, delta, rho, gamma)`

`pi_break(U_min) = (delta, rho, gamma)`

`pi_sel(U_min) = (a_sel, e)`

The corresponding exact reconstruction maps are:

`H = H_core(A, B, u, v) + B(delta, rho, gamma)`

`B(delta, rho, gamma) = delta T_delta + rho T_rho + gamma T_gamma`

`B_red = a_sel (chi_N_nu - chi_N_e)`

and on the compatible weak-axis seed patch the optional binary edge bit selects
the two exact monomial edges:

`e = 0 -> sqrt(A) I`

`e = 1 -> sqrt(A) C`

So the unified object is exactly the joint carrier of:

- the Hermitian bridge package
- the breaking-source space
- the selector primitive

## Why this is minimal

The current exact reductions show that these three pieces live in distinct
quotient types:

- the Hermitian bridge is a `2 + 2 + 3` package
- the breaking sector is the exact 3-real source complement inside that
  Hermitian package
- the selector primitive is one reduced class with one amplitude slot, plus
  one binary edge bit if coefficient closure is required

The current bank does not collapse any of these pieces into a smaller exact
retained object:

- it does not derive the branch Hermitian values from the retained bank
- it does not derive the breaking-triplet values from the retained bank
- it does not fix the restricted Higgs-offset bit

Therefore no smaller unified retained-bank object is available.

## Theorem-level statement

**Theorem (Minimal unified PMNS bridge carrier).** Assume the exact global
Hermitian mode package, the exact branch-Hermitian-data obstruction, the
exact breaking-source construction, the exact selector primitive
construction, and the exact restricted-Higgs-offset selector reduction. Then
the smallest exact unified object that simultaneously accounts for:

1. the branch Hermitian bridge package `B_H,min`
2. the breaking-source space `S_break`
3. the selector primitive `B_red`

is the single bundle

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`.

Moreover:

1. `U_min` reconstructs the branch Hermitian law exactly
2. `U_min` reconstructs the breaking source exactly as a 3-real source space
3. `U_min` reconstructs the selector primitive exactly on the reduced class
4. the retained bank does not derive the values of these coordinates as
   retained-bank outputs
5. if coefficient closure on the seed patch is also required, the binary edge
   bit `e` is genuinely necessary and cannot be absorbed into the Hermitian
   coordinates

So the exact outcome is a minimal unified-extension theorem, not a positive
retained-bank closure theorem.

## What this closes

This closes the ambiguity about whether the three missing objects should be
treated as three unrelated add-ons.

They should not.

The exact smallest unified carrier is one bundle, with one Hermitian leg, one
breaking-source leg, and one selector leg.

## What this does not close

This note does **not** derive:

- the values of `(A, B, u, v, delta, rho, gamma)` from the retained bank
- the value of `a_sel` from the retained bank
- the binary edge bit `e`

So this is a minimal-unification theorem, not a positive closure theorem.

## Command

```bash
python3 scripts/frontier_pmns_unified_bridge_carrier.py
```
