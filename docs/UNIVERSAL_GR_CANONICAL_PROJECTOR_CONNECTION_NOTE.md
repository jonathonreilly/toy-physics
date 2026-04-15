# Universal GR Canonical Projector / Connection Candidate on `PL S^3 x R`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / canonicalization note  
**Purpose:** derive the strongest axiom-native candidate for a covariant
complementary projector / connection after the exact invariant `A1`
projector and the unique symmetric `3+1` quotient kernel are already in hand

## Verdict

The exact invariant `A1` projector is real, but it is not enough to fix a
canonical curvature-localization bundle on the complementary `E \oplus T1`
channels.

The strongest axiom-native candidate currently supported by the universal
stack is therefore not a finished `Pi_curv`. It is the associated
`3+1` polarization bundle over the valid frame orbit, with the exact `A1`
section fixed and the complementary channels carried by an `SO(3)` orbit
bundle:

`P_curv^cand := (Pi_A1, O_{E \oplus T1}, \omega_MC)`.

Here:

- `Pi_A1` is the exact rank-2 invariant projector onto lapse and spatial
  trace;
- `O_{E \oplus T1}` is the exact orbit of localized complementary channel
  coefficients over valid `3+1` polarization frames;
- `\omega_MC` is the natural Maurer-Cartan / orbit connection on that frame
  orbit.

This is the strongest axiom-native candidate because it is the smallest
structure compatible with:

1. exact `Pi_A1` invariance;
2. unique symmetric `3+1` quotient-kernel uniqueness;
3. `Xi_TB` compatibility on the Route 2 spacetime carrier;
4. the observed frame dependence of the complementary channels.

## What is exact already

### Exact invariant section

The universal stack already fixes the exact `A1` projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

This selects the lapse channel `h_00` and the spatial trace `tr(h_ij)`.
The projector is frame-independent across valid `3+1` rotations.

### Unique symmetric quotient kernel

The scalar observable generator

`W[J] = log|det(D+J)| - log|det D|`

has a unique symmetric `3+1` Hessian kernel on the finite prototype used by
the current audit. That kernel is nondegenerate on the prototype quotient.

So the tensor candidate is not ambiguous at quadratic order. The missing
piece is not kernel uniqueness; it is the covariant localization of the
complementary channels.

### Route 2 compatibility

The shared Route 2 bridge triple is

`B_R = (K_R, I_TB, Xi_TB)`.

The exact spacetime carrier is

`Xi_TB(t ; q) = vec K_R(q) \otimes exp(-t Lambda_R) u_*`.

The `exp(-t Lambda_R)` factor is independent of the valid `3+1` frame
choice. So `Xi_TB` compatibility constrains the projector bundle to be
equivariant over the frame orbit, but it does not by itself fix a canonical
section.

## Candidate bundle structure

The strongest candidate complementary structure is:

1. fix the exact invariant `A1` section;
2. take the complementary `E \oplus T1` channels as an associated orbit
   bundle over valid `3+1` frames;
3. equip that orbit bundle with the natural orbit / Maurer-Cartan connection;
4. require that the transport commute with the Route 2 carrier `Xi_TB`.

This is the smallest covariant completion that is still consistent with the
current universal data.

In particular, the candidate does **not** supply a distinguished connection
in the strong canonical sense. It supplies only the natural equivariant orbit
connection on the frame bundle.

## Covariance test

The current universal audit shows:

- `Pi_A1` is invariant to machine precision;
- the complement remains frame-dependent;
- valid `3+1` frame changes act nontrivially on the complementary channels.

That means covariance forces the complementary data to live in an
`SO(3)`-equivariant bundle, but does not collapse the orbit to a canonical
section.

So the best axiom-native completion is an associated `SO(3)` bundle, not a
unique curvature-localization projector.

## Exact residual gauge freedom

The remaining gauge freedom is exactly the spatial rotation orbit preserving
`Pi_A1`.

On the current atlas, that residual freedom is:

`SO(3)`

acting on the valid `3+1` polarization frames and hence on the complementary
`E \oplus T1` channels.

If one also allowed parity flips, the stabilizer would enlarge to `O(3)`, but
the current valid-frame orbit is the connected `SO(3)` component.

What this means operationally:

1. covariance does not force a unique `Pi_curv`;
2. quotient uniqueness does not force a unique `Pi_curv`;
3. `Xi_TB` compatibility does not force a unique `Pi_curv`;
4. the exact residual freedom is the spatial-rotation gauge orbit.

So the universal route is blocked not by missing scalar data, and not by
missing quotient uniqueness, but by the absence of a canonical gauge-fixing
primitive for that `SO(3)` bundle.

## Strongest exact candidate statement

The strongest exact candidate derivable from the current atlas is:

> The canonical universal projector data are the exact invariant `Pi_A1`
> section together with the associated `SO(3)` orbit bundle on the
> `E \oplus T1` complement, equipped with the natural orbit connection.
> This is the strongest covariant completion currently forced by the axioms,
> but it does not yet supply a distinguished connection or a canonical
> `Pi_curv`.

## Honest status

The current direct universal route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- blocked at the canonical curvature-localization level.

The exact residual bundle gauge on the current atlas is `SO(3)`.
