# the cubic variational selection obstruction: Z_3 Cubic Right-Sensitive Selector — Obstruction Theorem

**Date:** 2026-04-17
**Status:** **obstruction theorem** — narrowed gap, no theorem-grade closure
**Script:** `scripts/frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

This note establishes a precise **obstruction theorem** for the cubic variational selection obstruction of the selector gate
gate closure attempt: the cubic right-sensitive direction of the
Z_3-circulant norm form.

It is explicitly **not** a theorem-grade closure. The selector principle
remains open, and this note records the sharpened reason why the cubic
right-sensitive route alone cannot supply it. Claim class: **obstruction /
narrower gap**.

This note is paired with the upstream Schur-baseline partial closure:

- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)

which closed sub-objection (i) (baseline choice forced by Schur) and left open
the selector principle. The present note closes off one of the three candidate
routes (the cubic variational route; item (b) in the upstream "narrowed gap"
list) by showing it cannot terminate the problem on its own.

## Setup

Retained upstream (all theorem-grade, no new axioms):

- exact active chart on the live source-oriented sheet:
 `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`
- exact chamber: `q_+ >= sqrt(8/3) - delta`
- Schur-baseline theorem: `D = m I_3` forced on `H_hw=1`
- axiom-native scalar generator:
 `W[J_act] = log|det(m I + J_act)| - log|det(m I)|`
- exact Z_3-circulant norm form:
 `det(m I + delta T_delta + q_+ T_q) = m^3 - 3 m |w|^2 + 2 Re(w^3)`,
 with `w = q_+ + i delta`
- zero-source isotropic curvature (Schur-Q):
 `Q(delta, q_+) = 6 (delta^2 + q_+^2) / m^2`
- Schur-Q chamber-boundary minimum at `(delta_*, q_+*) = (sqrt(6)/3, sqrt(6)/3)`

The the cubic variational selection obstruction question: does the cubic piece `2 Re(w^3)`, which breaks the
quadratic isotropy `delta <-> q_+`, pick a unique axiom-native chamber point?

## Obstruction theorem

**Theorem (the cubic variational selection obstruction obstruction).** Let `W[J_act]` be the Schur-baseline scalar
generator above, and let `f_c(delta, q_+) = 2 Re(w^3) = 2 q_+ (q_+^2 - 3
delta^2)` be the cubic piece, with `w = q_+ + i delta`. Every axiom-native
right-sensitive functional built from `W` or from the retained cubic
invariants `{tr(J_act^3), det(J_act), Re(w^3)}` fails to have a unique,
`m`-invariant, finite chamber extremum. Explicitly:

1. **(A) Fixed-m boundary extremum is m-dependent.** On the chamber boundary
  `q_+ = sqrt(8/3) - delta`, critical points of `W(m; delta, q_+)` in
  `delta` at fixed `m` are exactly

  ```
  t_+-(m) = m/2 +- sqrt(9 m^2 - 12 sqrt(6) m + 48) / 6,
  ```

  with `t := delta`. The reduced discriminant of the quadratic in `m` under
  the outer radical is `144 * 6 - 4 * 9 * 48 = -864 < 0`, so the radical is
  positive for every real `m` and the critical points are real.

  The bounded branch has

  ```
  t_-(m) = m/2 - sqrt(9 m^2 - 12 sqrt(6) m + 48)/6
     = sqrt(6)/3 - 2/(3 m) + O(1/m^2)  as m -> infinity.
  ```

  So `t_-(m) -> sqrt(6)/3` (the Schur-Q minimum) **only** in the limit
  `m -> infinity`, which is exactly the limit in which the cubic
  contribution `2 Re(w^3) / m^3` vanishes relative to the quadratic
  `-3 |w|^2 / m^2`. This is a vacuous recovery: the cubic route recovers
  the Schur-Q point only when the cubic is turned off.

2. **(B) Joint (m, t) stationary points are singular.** Adding the
  `m`-stationarity condition `m * df/dm - 3 f = 0` to the boundary-critical
  equation yields three real joint critical points

  ```
  CP1: (m, t) = (2 sqrt(6)/3, 0),           arg(w) = 0
  CP2: (m, t) = (2 sqrt(6)/3 - 2 sqrt(2), sqrt(6) - sqrt(2)), arg(w) = 60
  CP3: (m, t) = (2 sqrt(6)/3 + 2 sqrt(2), sqrt(6) + sqrt(2)), arg(w) = 120
  ```

  Every one of them satisfies `det(m I + J_act) = 0`. They are the three
  components of the Z_3 orbit of the boundary singular locus of
  `W = log|det|`, where `W -> -infinity`. They are boundary singularities,
  not proper extrema, and their Hessians on `f/m^3` have non-positive
  determinant (saddle or degenerate), as the runner verifies.

3. **(C) Cubic-only functionals collapse.** Among the retained cubic
  invariants,

  ```
  tr(J_act^3) = 6 Re(w^3),    det(J_act) = 2 Re(w^3).
  ```

  All three functionals are proportional to `Re(w^3)`, so there is a single
  axiom-native cubic form on the active pair. Its chamber-boundary extrema
  are

  ```
  t = +- 2 / sqrt(3),
  ```

  and neither matches `t = sqrt(6)/3` (Schur-Q) nor `t = 0`
  (Z_3-axis `w = sqrt(8/3)` at the boundary).

4. **(D) Z_3 cubic-max orbit is not unique in chamber.**
  `Re(w^3) = |w|^3 cos(3 arg(w))` has maximum `+|w|^3` on three rays
  `arg(w) in {0, 2 pi/3, -2 pi/3}`. The chamber
  `q_+ + delta >= sqrt(8/3)` requires `r (cos theta + sin theta) >= sqrt(8/3)`,
  which is:
  - `theta = 0`: accessible, boundary at `r = sqrt(8/3)`,
  - `theta = 2 pi/3`: accessible, boundary at
   `r = sqrt(8/3) / ((sqrt(3) - 1)/2)`,
  - `theta = -2 pi/3`: inaccessible (linear form is negative).

  Two chamber-accessible representatives, distinguished only by overall
  `|w|`, not by the cubic-max value (`cos(3 theta) = 1` on both). No
  axiom-native chamber-intrinsic object selects one.

5. **(E) Sign of cubic is invisible to W.** `W = log|det|` is even in
  `sign(det)`; hence max vs min of the cubic is a post-axiom sign
  convention not expressible in `W`.

Each of (A)-(E) is independent; each blocks a different naive closure of
the cubic variational selection obstruction.

**Corollary.** Any the cubic variational selection obstruction closure of selector requires at least one post-axiom
input: a canonical choice of `m`, a canonical sign/extremum-type convention,
or a canonical Z_3 representative within the chamber-accessible orbit. None
of these is currently retained.

## Why this is a genuine advance (narrower gap)

Before this note, the selector narrowed-gap statement read (from the upstream
Schur-baseline note):

> "Any future closure of selector must supply one of:
> (a) a sole-axiom derivation of a minimum-coupling variational principle ...
> (b) a right-sensitive axiom-native functional on the chamber that breaks
>   the delta <-> q_+ isotropy and has a unique chamber-interior extremum
>   (the cubic Z_3-circulant structure is the natural target);
> (c) a direct microscopic Z_3 doublet-block law ..."

This note closes (b) as a stand-alone route: no axiom-native cubic-based
functional has a unique, `m`-invariant, finite chamber extremum. The open
object reduces to:

```
(a) OR (c),
or (b) + explicit post-axiom supplement.
```

This is a strictly narrower surviving gap. The cubic attack vector is not
eliminated entirely, but it is demonstrably insufficient on its own.

## Proof (runner-verifiable)

The runner `scripts/frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py` verifies each
of the five sub-claims:

1. **Upstream consistency (Part 1).** Verifies the Z_3-circulant closed
  form for `det(m I + J_act)` and the Schur-Q isotropic Hessian
  `-6/m^2` at several values of `m`, and the chamber minimizer
  `sqrt(6)/3`.

2. **(A) m-dependent boundary extremum (Part 2).** Computes `t_+-(m)` at
  multiple values of `m`, verifies each is a boundary critical point via
  finite-difference derivative, verifies monotone approach of `t_-(m)` to
  `sqrt(6)/3` as `m -> infinity`, verifies the `-2/(3m)` first-order
  correction, and confirms the discriminant under the outer radical is
  positive for all `m`.

3. **(B) singular joint critical points (Part 3).** Confirms each of the
  three joint CPs satisfies the boundary stationarity condition, the
  `m`-stationarity condition, lies on `det = 0`, has `arg(w) in {0, 60,
  120} deg`, and has Hessian with non-positive determinant.

4. **(C) cubic functional collapse (Part 4).** Numerically verifies
  `tr(J^3) = 6 Re(w^3)` and `det(J) = 2 Re(w^3)` on random samples,
  confirms boundary extrema of `Re(w^3)` at `t = +- 2/sqrt(3)`, and
  checks neither extremum is at `sqrt(6)/3` or `t = 0`.

5. **(D) Z_3 orbit multiplicity (Part 5).** Verifies exactly two of three
  orbit representatives have `cos(theta) + sin(theta) > 0`, constructs
  boundary-hit points explicitly, and confirms all three orbit rays have
  `cos(3 theta) = 1`.

6. **(E) sign invisibility (Part 6).** Verifies the cubic values at
  `t = +- 2/sqrt(3)` have opposite signs, and records the symmetry of
  `log|x|` under `x -> -x`.

Running: `PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py`.

Expected: `PASS = 26, FAIL = 0`.

## Atlas inputs used

All retained / theorem-grade:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SCALAR_BASELINE_ACTIVE_QUADRATIC_DIAGNOSTIC_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCALAR_BASELINE_ACTIVE_QUADRATIC_DIAGNOSTIC_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)

No new axioms are introduced.

## Claim boundary

This note is **not**:

- a closure of the selector gate
- a promotion of the selector principle to theorem-grade
- a statement that the cubic route is useless; it only establishes the
 route is insufficient on its own

This note **is**:

- a theorem-grade **obstruction**: the cubic the cubic variational selection obstruction route cannot produce an
 m-invariant, finite, unique chamber selector from axiom-native objects
 alone
- a narrowing of the the selector gate open-surface: route (b) in the upstream narrowed-gap
 list is now closed off as a stand-alone

## Position on publication surface

Appropriate placement:

- atlas support row in
 [DERIVATION_ATLAS.md](./publication/ci3_z3/DERIVATION_ATLAS.md)
 under the DM neutrino source-surface family, labeled as **narrowed gap
 / obstruction**
- no change to the DM flagship gate status (still open)
- paired with the upstream Schur-baseline partial closure; the two notes
 together pin the remaining open object at "selector principle only, via
 (a) or (c), not via (b) stand-alone"

This note should not be used to promote anything in the flagship paper
quantitative section.

## What this file must never say

- that selector is closed
- that the DM flagship gate is closed
- that the cubic route is theorem-grade selector-compatible
- that the Z_3 axis `w = sqrt(8/3)` or the Schur-Q point `sqrt(6)/3` is
 axiom-native-forced by the cubic variational selection obstruction

If any future revision tightens those boundaries, it must cite a new source
on the live retained/promoted surface. Until then, the safe read is:
**cubic the cubic variational selection obstruction obstructed; selector selector principle still open; route (b)
closed as stand-alone**.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py
```

Current expected: `PASS = 26, FAIL = 0`.
