# Common Residual Gauge of the Polarization-Bundle Candidate

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** sharpen the exact remaining gauge on the common polarization-bundle candidate

## Verdict

The exact remaining obstruction is smaller than a generic missing `3+1`
polarization bundle.

Starting from:

- the exact invariant core `Pi_A1`;
- the exact Route 2 bridge triple `B_R = (K_R, I_TB, Xi_TB)`;
- the exact support-side bright pair `u_E, u_T`;
- the exact support-side dark residual `O(1) x O(2)`;
- the exact universal-side complement orbit `SO(3)`;

the actual shared residual gauge of the common candidate is the bright-axis
stabilizer

`S(O(1) x O(2)) ~= O(2)`.

If one restricts to the connected component after fixing the bright-axis
orientation, the only surviving continuous gauge is

`SO(2)`.

So the remaining missing primitive is best understood as:

> a canonical axial phase / angle connection on the dark complement plane.

That is strictly sharper than “a missing full canonical `3+1` polarization
bundle.”

## Inputs

The support-side canonicalization note established:

- the exact scalar `A1` endpoint law is rigid;
- the exact bright pair `u_E, u_T` is rigid;
- the residual dark-complement freedom is exactly
  `O(1)_{E_perp} x O(2)_{T1_dark}`.

The universal-side canonicalization note established:

- the exact canonical invariant section is `Pi_A1`;
- the complement is an `SO(3)` orbit bundle over valid `3+1` frames;
- the Maurer-Cartan orbit connection is natural but not distinguished.

The common-bundle candidate note established:

- the exact shared candidate is `P_R^cand = (Pi_A1, B_R, O_R)`;
- the complement of `Pi_A1` is still noncanonical.

## Group-theoretic sharpening

On the common candidate, the support bright data already choose a preferred
axis inside the complementary channels.

That means the universal `SO(3)` freedom is no longer free to act on the full
three-dimensional complement. It must preserve the bright axis picked out by
the exact support-side bright pair.

The stabilizer of a chosen axis inside `SO(3)` is exactly the subgroup

`S(O(1) x O(2)) ~= O(2)`.

Equivalently, any allowed common residual transformation can be written in a
dark-complement basis as

`diag(det A, A)`, with `A in O(2)`.

This matches the support-side statement:

- the one-dimensional `E_perp` sign is tied to the determinant of the
  two-dimensional dark-plane transformation;
- the remaining continuous freedom is rotation in the dark `T1` plane.

So the support-side and universal-side residual gauges are compatible, and
their common exact residual is `O(2)`.

## Connected residual

If one further restricts to the connected component preserving the bright-axis
orientation, the determinant constraint forces the `E_perp` sign to be `+1`.

Then the common residual gauge collapses to:

`SO(2)`.

This is the single remaining continuous gauge angle on the dark complement.

## Consequence

The gravity obstruction is now sharper:

- we do **not** need to think of the missing object as a completely general
  polarization bundle anymore;
- the exact common candidate has already reduced the problem to a one-angle
  dark-plane gauge.

So the next exact theorem target should be:

> derive an axiom-native principle that fixes the residual `SO(2)` dark-plane
> angle, or prove that the current atlas cannot fix it.

Natural candidates for that last principle are:

- a canonical axial phase convention;
- a distinguished dark-plane connection;
- an extra compatibility law between the Route 2 bright carrier and the
  universal complement transport.

## Bottom line

The exact shared residual gauge on the common candidate is

`S(O(1) x O(2)) ~= O(2)`,

with connected component

`SO(2)`.

So the remaining polarization-bundle problem has collapsed to a single
continuous dark-plane gauge, not a fully arbitrary complement bundle.
