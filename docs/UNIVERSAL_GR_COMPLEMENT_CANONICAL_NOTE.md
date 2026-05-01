# Universal GR Complement Canonicalization Audit

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** direct universal route / complement canonicalization only  
**Ownership:** universal complement canonicalization only

## Verdict

The direct universal `A1`-anchored route does not canonically split the
complement `E \oplus T1` using only the universal data currently in the
atlas.

The strongest axiom-native object the universal data support is still the
orbit bundle, not a canonical section:

`P_comp^cand := (Pi_A1, O_{E \oplus T1}, \omega_MC)`

where:

- `Pi_A1` is the exact rank-2 invariant projector onto lapse and spatial
  trace;
- `O_{E \oplus T1}` is the associated `SO(3)` orbit bundle of the
  complementary channels over valid `3+1` polarization frames;
- `\omega_MC` is the natural Maurer-Cartan / orbit connection on that frame
  orbit.

This is the strongest complement-frame candidate the universal stack can
produce, but it is not a canonical split of the complement.

## What the universal data do fix

The current direct universal route already gives the following exact
structures:

1. the scalar observable generator `W[J] = log|det(D+J)| - log|det D|`;
2. the exact `3+1` lift `PL S^3 x R`;
3. the exact tensor-valued variational candidate
   `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`;
4. the exact unique symmetric `3+1` quotient kernel on the finite prototype;
5. the exact invariant `A1` projector
   `Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

Those pieces are enough to isolate the invariant core and the complement
orbit, but not enough to choose a canonical complement section.

## What the audit tests

The runner checks four universal-only facts:

1. `Pi_A1` is rank-2 and commutes with valid `3+1` spatial rotations;
2. the induced rotation generators close as `so(3)` on the complement;
3. the `Pi_A1`-projected quotient-kernel data are invariant under valid frame
   changes, while the complement block is not;
4. the curvature-localization probe remains orbit-valued rather than
   section-valued on the `E \oplus T1` complement.

If those tests pass, then the exact residual gauge surviving all current
universal invariants is still the full spatial rotation group:

`SO(3)`.

## Complement canonicalization result

The universal `A1` core is canonical, but the complement is not canonically
split by any invariant presently available in the universal atlas.

What survives is:

- the exact `Pi_A1` core;
- the exact `SO(3)` orbit bundle on the complement;
- the natural orbit / Maurer-Cartan connection.

What does **not** survive is:

- a canonical `E \oplus T1` section;
- a distinguished curvature-localization connection;
- a universal axis choice inside the complement.

So the direct universal route bypasses the phase-lift `lambda`, but it still
does not canonically resolve the complement frame. The complement remains an
`SO(3)` orbit bundle.

## Strongest exact statement

The strongest statement supported by the current universal data is:

> `Pi_A1` is canonical, the direct universal complement is only orbit-canonical,
> and the exact residual gauge that survives every current universal invariant
> is `SO(3)`.

Equivalently:

> the current atlas does not canonically split `E \oplus T1`; it only fixes
> the invariant `A1` core and the complement orbit.

## Honest status

The direct universal route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- still blocked at the canonical complement-frame level.

The remaining obstruction is not `lambda` on this route. It is the absence of
a canonical complement section inside the `SO(3)` orbit bundle.
