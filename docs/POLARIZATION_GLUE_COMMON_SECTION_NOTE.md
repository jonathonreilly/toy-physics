# Polarization Glue Common Section on the Support/Curvature Interface

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** support-to-curvature glue attack only  
**Purpose:** test whether the exact support-side bright block and the universal exact `Pi_A1` core canonically identify the shared complement, or only reduce the combined gauge to a smaller residual orbit

## Verdict

The combined support/universal data do **not** yet define a fully rigid common
section.

What they do define is a sharper glued candidate:

`P_glue^cand := (Pi_A1, B_R, O_glue)`

with

`B_R := (K_R, I_TB, Xi_TB)`

and where `O_glue` is the orbit of frames compatible with both

- the exact support-side bright block `u_E, u_T`, and
- the exact universal invariant core `Pi_A1`.

The common compatibility conditions reduce the universal `SO(3)` residual
orbit and the support-side dark-complement freedom to the shared stabilizer of
the bright axis. The exact common connected residual gauge is therefore:

`SO(2)`.

The support-side disconnected `O(1)` sign on `E_perp` is already fixed once the
endpoint conventions in the support note are imposed, so it does not survive as
a common gauge freedom.

## What is exact on the support side

The support-side exact bright block is the ordered pair

`u_E = <E_x, q>`, `u_T = <T1x, q>`,

with exact support carrier

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

The exact support canonical-frame audit already established:

- the support-irrep split `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1` is exact;
- the bright pair `u_E, u_T` is exact and ordered;
- the remaining support freedom is the orthogonal freedom on the dark
  complement;
- after endpoint conventions are fixed, the residual support-side freedom is
  `O(1) × O(2)` on the dark complement.

That means the support side fixes a canonical block frame but not a fully rigid
polarization bundle.

## What is exact on the universal side

The universal exact core is the rank-2 invariant projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

That projector is exact and frame-invariant across sampled valid `3+1`
polarization frames, but the complement remains frame-dependent. The strongest
universal completion available from the current atlas is the associated
`SO(3)` orbit bundle on the complementary channels.

So the universal side also fixes a canonical core but not a distinguished
connection on the full complement.

## Glue test

The support bright block and the universal `Pi_A1` core are compatible, but
their overlap only selects a shared axis orbit.

The reason is structural:

1. the support bright block pins the aligned channels `u_E, u_T`;
2. the universal `Pi_A1` core pins the lapse/spatial-trace core;
3. the remaining universal complement still rotates by `SO(3)`;
4. the support dark complement still has `O(1) × O(2)` freedom;
5. the common symmetry preserving the shared bright axis is the stabilizer
   subgroup `SO(2)`.

So the two lanes do not collapse to a unique common section. They collapse to a
common axis-stabilized orbit.

## Strongest glued candidate

The strongest glued candidate currently forced by the atlas is:

`P_glue^cand := (Pi_A1, B_R, O_glue)`

with

- `Pi_A1` the exact invariant core;
- `B_R = (K_R, I_TB, Xi_TB)` the exact Route 2 bridge triple;
- `O_glue` the shared `SO(2)` orbit of compatible frames.

A corresponding block-connection prototype is:

`nabla_glue^cand := nabla_A1 ⊕ nabla_B ⊕ nabla_glue`

where `nabla_glue` is the natural axis-orbit connection on the shared `SO(2)`
bundle.

## Exact common residual gauge

The common residual gauge after enforcing compatibility across both lanes is:

`SO(2)`.

That is the exact stabilizer of the shared axis once the support endpoint
sign conventions have been fixed and the universal `Pi_A1` core has been
imposed.

The current atlas does **not** further reduce this to a canonical section.

## Bottom line

The support bright block plus the universal `Pi_A1` core do not canonically
identify the full complement. They do, however, reduce the combined freedom to
the exact common residual gauge `SO(2)`, and they promote the strongest glued
candidate to

`P_glue^cand := (Pi_A1, B_R, O_glue)`.

