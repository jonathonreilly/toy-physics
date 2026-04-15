# Polarization Common Bundle Candidate and Distinguished Connection

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** common polarization-bundle primitive family / strongest axiom-native candidate
**Purpose:** promote the exact invariant `A1` selector, the exact Route 2 bridge triple, and the exact localized-frame orbit into a single common bundle candidate with an explicit distinguished-connection prototype

## Verdict

The strongest axiom-native common bundle candidate is now:

`P_R^cand := (Pi_A1, B_R, O_R)`

with

`B_R := (K_R, I_TB, Xi_TB)`.

This is stronger than the earlier orbit-only candidate because it contains the
exact invariant core already latent in the universal stack:

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

So the candidate now has three exact layers:

1. the canonical invariant `A1` core `Pi_A1`
2. the exact Route 2 bridge triple `B_R`
3. the exact orbit of localized `3+1` channel coefficients `O_R`

The candidate is exact as a construction, but it is not yet a finished
canonical bundle because `O_R` is an orbit, not a canonical section.

## Exact invariant core

The universal `A1` projector is the strongest exact canonical selector
currently visible in the atlas.

It is the rank-2 projector onto:

- lapse `h_00`
- spatial trace `tr(h_ij)`

In the canonical symmetric `3+1` basis, it is

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

The exact invariant properties already verified by the universal runner are:

- `Pi_A1` is rank 2;
- `Pi_A1` is invariant to machine precision across sampled valid `3+1`
  frames;
- the complementary `E \oplus T1` channels remain frame-dependent.

So `Pi_A1` is the canonical core of the candidate bundle.

## Exact bridge triple

The Route 2 bridge triple is

`B_R = (K_R, I_TB, Xi_TB)`.

Its exact components are:

- `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`
- `I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - K_R(q)||^2`
- `Xi_TB(t ; q) = vec(K_R(q)) \otimes exp(-t Lambda_R) u_*`

This triple is exact on the current Route 2 stack and provides the support /
curvature interface for the common bundle candidate.

## Distinguished-connection prototype

The strongest concrete connection candidate available from the current atlas
is the block connection prototype

`nabla_R^cand := nabla_A1 \oplus nabla_B \oplus nabla_O`

where:

- `nabla_A1` is flat on the invariant `A1` core;
- `nabla_B` is the exact Route 2 transport induced by `exp(-t Lambda_R)` on
  `Xi_TB`;
- `nabla_O` is the frame-orbit transport on the localized `3+1` coefficient
  orbit.

This is exact on the `A1` core and exact on the Route 2 carrier, but only
candidate-level on the complement because the complement still depends on the
choice of valid `3+1` polarization frame.

## Exact invariance properties

The current atlas already proves the following exact properties for the common
bundle candidate:

- the `A1` core is exactly invariant;
- the Route 2 carrier is exact on the bright channels `u_E` and `u_T`;
- the Route 2 semigroup factor `exp(-t Lambda_R)` is exact;
- the support-side enlargement `A1(center) \oplus A1(shell) \oplus E \oplus
  T1` is exact but noncanonical;
- the support-side support-generator family has rank 3 at the source-family
  level;
- the localized frame orbit remains frame-dependent away from the `A1` core.

## Sharp obstruction

The candidate does **not** yet close into a canonical full polarization bundle.

The obstruction is still the same, but it is now sharpened against the exact
`A1` core:

> the complementary `E \oplus T1` channels are not canonically sourced from
> the current exact support stack, so there is no canonical distinguished
> connection on the full bundle from the current atlas alone.

Equivalently:

> `Pi_A1` is canonical; the complement is only orbit-canonical.

That means the current atlas supports a reducible bundle candidate, not a full
canonical bundle with a uniquely determined `\nabla_R`.

## Candidate status

The common bundle candidate now has the strongest possible exact core the
current atlas can supply:

- exact canonical section: `Pi_A1`
- exact bridge data: `B_R`
- exact localized orbit: `O_R`

What remains missing for full canonical closure is a distinguished connection
that canonically extends `Pi_A1` over the complementary `E \oplus T1`
channels.

## Compatibility requirements

Any support-side `Pi_3+1` specialization must satisfy:

1. it preserves the exact scalar support datum `delta_A1`;
2. it preserves the aligned bright channels `u_E` and `u_T`;
3. it commutes with the Route 2 tensorized action `I_TB`;
4. it factors through the exact Route 2 carrier `K_R`;
5. it agrees with the exact invariant `A1` core `Pi_A1`.

Any curvature-side `Pi_curv` specialization must satisfy:

1. it preserves the unique symmetric quotient kernel;
2. it preserves the exact orbit `O_R` of localized `3+1` channel
   coefficients;
3. it is realized by a covariant `3+1` polarization-frame / projector bundle;
4. it uses a distinguished connection `nabla_R` rather than a frame-dependent
   ad hoc section;
5. it agrees with the canonical `A1` core `Pi_A1`.

## Bottom line

The strongest axiom-native candidate is:

`P_R^cand := (Pi_A1, B_R, O_R)`

with the block-connection prototype

`nabla_R^cand := nabla_A1 \oplus nabla_B \oplus nabla_O`.

This is the sharpest common-bundle object the current atlas supports, but it
is still a candidate because the complement of `Pi_A1` remains frame-dependent.
