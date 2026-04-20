# Koide Berry-Holonomy Theorem: Geometric Identification on the Actual Selected Route

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide phase `delta = 2/9` / AXIOM E audit
**Cycle:** 10B revised again
**Status:** **Geometric identification / support theorem**, not independent
axiom closure. On the exact charged-lepton selected line there is a canonical
Pancharatnam–Berry bundle/connection on the projective `C_3` doublet ray, and
the physical Brannen phase offset `delta` is exactly the Berry holonomy of
that actual-route bundle measured from the unique unphased selected-line
point. What this closes is the selected-line scalar/point law as a corollary
of `delta`: the exact selected-line scalar `kappa_sel` is an explicit function
of `delta`, so `delta = 2/9` (from Brannen–Zenczykowski, AXIOM E) fixes both
`kappa_sel,*` and the unique first-branch point `m_*`. What this does **not**
close is the value `delta = 2/9` itself: Berry geometry gives `delta` its
physical meaning as a holonomy but does not independently quantize the
specific value `2/9`. That value remains an input from Brannen–Zenczykowski;
the retirement-style caveat is recorded explicitly in §6 and cross-referenced
against the bundle-obstruction theorem.

The right scientific split after cross-referencing the bundle obstruction
theorem and the retirement observation is:

1. the ambient `S^2` / monopole / `n = 2` closure claim is false — the
   physical Koide locus is not `S^2`;
2. the physical phase observable **can** be identified canonically as a Berry
   holonomy on the actual charged-lepton selected route (this note);
3. that identification, combined with the exact selected-line scalar-phase
   bridge, removes the previous branch-local `m_* / kappa_sel,*` import;
4. it does **not** independently force `delta = 2/9` — a further axiom-native
   quantization principle would be needed for that; until then AXIOM E
   remains the retained input;
5. this still does **not** overwrite current-main authority by itself.

**Primary runner:** `scripts/frontier_koide_berry_phase_theorem.py`

---

## 0. Executive summary

The branch's original Berry note closed the `delta = 2/9` gate by:

1. replacing the physical scale-free Koide locus with an ambient `S^2`,
2. choosing a monopole line bundle of charge `n = 2`,
3. integrating its curvature over a nonphysical north-south `C_3` wedge, and
4. dividing the resulting holonomy by an extra factor of `d = 3` to recover
   Brannen units.

That arithmetic is internally coherent, but it does **not** discharge the
physical charged-lepton phase gap. The failures are structural:

- the actual scale-free Koide locus is a fixed-latitude circle, not an `S^2`;
- the `C_3` doublet bundle over that locus is globally trivial;
- on the retained charged-lepton circulant moduli the Berry connection is zero;
- restricting the same monopole connection to the actual Koide latitude does
  not reproduce `2/9`.

But the Berry story is not dead. Once the already-derived exact
charged-lepton reductions are used, the actual phase-carrying route is the
selected line

```text
H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3)
```

on its positive first branch. Along that branch the normalized Koide amplitude
has the exact Fourier form

```text
s(m) = (1/sqrt(2)) v_1 + (1/2) e^{ i theta(m)} v_omega
                     + (1/2) e^{-i theta(m)} v_omegabar,
```

with `theta(m)` continuous. The singlet weight is fixed, so the moving physical
datum is exactly the projective `C_3` doublet ray

```text
[e^{i theta(m)} : e^{-i theta(m)}] = [1 : e^{-2 i theta(m)}],
```

which lies on the equator of `CP^1`.

The tautological line bundle on that equator has the canonical
Pancharatnam-Berry connection

```text
A = d theta.
```

There is a unique unphased point `m_0` on the first branch where `u(m_0)=v(m_0)`
and `theta(m_0)=2 pi / 3`, i.e. `delta(m_0)=0`. Therefore

```text
Hol(m_0 -> m) = theta(m) - 2 pi / 3 = delta(m).
```

So on the actual charged-lepton route the physical phase observable really is a
Berry holonomy. The old ambient `n = 2` story is replaced by a different exact
forcing step: the projective doublet coordinate is `[1 : e^{-2 i theta}]`, so
the load-bearing factor `2` comes from the conjugate-pair phase doubling of the
actual `C_3` doublet ray, not from a chosen monopole charge. Moreover, the
exact selected-line scalar-phase bridge

```text
kappa_sel(delta) = -sqrt(3) cos(delta + pi/6) / (sqrt(2) + sin(delta + pi/6))
```

shows that on the physical first branch the Berry offset and the surviving
selected-line scalar are the same coordinate in different gauges. Therefore
`delta = 2/9` fixes

```text
kappa_sel,* = -0.607918569997
```

and the unique first-branch point

```text
m_* = -1.160443440065.
```

The old imported `H_*` witness survives only as a branch-precision
compatibility check. What remains outside this note is not another free
selected-line scalar on the branch, but the question of whether the
current-main bounded charged-lepton package should adopt this branch-local
actual-route theorem stack.

---

## 1. The actual scale-free Koide locus is one-dimensional

Let

```text
s = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau)) in R^3_{>0},
u = (1,1,1) / sqrt(3),
K = (sum_i s_i^2) / ((sum_i s_i)^2).
```

The Koide condition is `K = 2/3`. On the unit sphere `|s| = 1`, this becomes

```text
|<u, s>|^2 = ((sum_i s_i)^2) / 3 = 1 / (3 K) = 1/2.
```

So the unit-scale Koide locus is

```text
K_unit = { s in S^2 : <u, s> = 1 / sqrt(2) }.
```

Equivalently,

```text
s(phi) = (1/sqrt(2)) u + (1/sqrt(2)) (cos(phi) e_1 + sin(phi) e_2),
```

for any orthonormal basis `{e_1, e_2}` of `u^perp`. Therefore:

- the scale-free real Koide locus is a one-real-dimensional circle `S^1`;
- the positive charged-lepton chamber is only an arc of that circle;
- the branch's ambient `S^2` is not the actual physical reduced space.

This already kills the original flux-through-`S^2` closure claim.

---

## 2. Why the ambient monopole package is not forced

The retained `C_3` action on `C^3` has the fixed Fourier decomposition

```text
C^3 = L_1 (+) L_omega (+) L_omegabar,
```

with global basis

```text
v_1        = (1, 1, 1) / sqrt(3),
v_omega    = (1, omega, omega^2) / sqrt(3),
v_omegabar = (1, omega^2, omega) / sqrt(3).
```

Over the actual Koide circle, the `C_3` doublet bundle is simply

```text
K_unit x span_C{v_omega, v_omegabar}.
```

So on the actual base:

- the bundle has an explicit global frame;
- its determinant line is trivial there;
- no nontrivial `c_1 = 2` is forced.

Even if one nevertheless chooses the branch's Dirac-monopole connection

```text
A_N = (n/2) (1 - cos(theta)) dphi
```

on the ambient sphere, restricting it to the actual Koide latitude
`theta_K = pi / 4` gives

```text
gamma_lat(step) = (n/2) (1 - 1/sqrt(2)) (2 pi / 3),
```

which at `n = 2` yields

```text
gamma_lat(step) / (2 pi * 3) ~= 0.03254,
```

not `2/9`.

So the ambient monopole construction remains only a geometric support model:
coherent once chosen, but not physically forced.

---

## 3. Why the retained circulant route still has zero Berry phase

Current main's charged-lepton route uses the circulant square-root family

```text
Y(delta) = a I + b(delta) C + b(delta)^* C^2,
```

with

```text
b(delta) = |b| exp(i (2 pi / 3 + delta)).
```

Every circulant is diagonalized by the same Fourier basis, independent of
`delta`. Therefore the Berry connection on the retained circulant moduli is
identically zero:

```text
A_k(delta) = i <v_k, partial_delta v_k> = 0.
```

This current-main boundary remains true. The actual physical Berry
identification must therefore live on a different actual route, not on the
retained circulant eigenvectors.

---

## 4. The actual Berry carrier is the selected-line projective doublet ray

The exact charged-lepton reductions already in the tree force the actual
positive route onto the selected line

```text
H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3),
```

with positivity threshold and branch continuity already fixed. On the small
branch, write the reachable Koide amplitudes as

```text
(u(m), v(m), w(m)).
```

Normalize to

```text
s(m) = (u, v, w) / ||(u, v, w)||.
```

Because `s(m)` remains on the Koide cone, its Fourier coefficients satisfy

```text
<v_1, s(m)>        = 1 / sqrt(2),
|<v_omega, s(m)>|  = 1/2,
|<v_omegabar, s(m)>| = 1/2,
<v_omegabar, s(m)> = overline(<v_omega, s(m)>).
```

So there is a unique continuous phase `theta(m)` on the first branch such that

```text
s(m) = (1/sqrt(2)) v_1 + (1/2) e^{ i theta(m)} v_omega
                     + (1/2) e^{-i theta(m)} v_omegabar.
```

The singlet coefficient is fixed. Therefore the actual moving phase datum is
exactly the projective doublet ray

```text
ell(m) = C ( e^{ i theta(m)} v_omega + e^{-i theta(m)} v_omegabar ).
```

In projective coordinates this is

```text
[e^{ i theta(m)} : e^{-i theta(m)}] = [1 : e^{-2 i theta(m)}].
```

So the image of the first branch is the equator of `CP^1`. This is the actual
phase-carrying reduced space on the exact selected charged-lepton route.

### The canonical bundle and connection

On `CP^1`, the canonical line bundle is the tautological line bundle. Over the
equator we can use the unit section

```text
chi(theta) = (1, e^{-2 i theta}) / sqrt(2).
```

Its Pancharatnam-Berry connection is

```text
A = i <chi, d chi> = d theta.
```

This is the actual canonical Berry connection on the actual selected-line
phase carrier. No ambient enlargement and no chosen monopole charge are needed.

### The unique unphased reference point

On the first branch there is a unique point `m_0` where

```text
u(m_0) = v(m_0).
```

At that point the Fourier phase is

```text
theta(m_0) = 2 pi / 3,
```

so the Brannen offset vanishes:

```text
delta(m_0) = theta(m_0) - 2 pi / 3 = 0.
```

This point gives the canonical phase origin on the actual charged-lepton route.

### The physical phase observable really is a Berry holonomy

Define the Brannen offset on the first branch by

```text
delta(m) = theta(m) - 2 pi / 3.
```

Then the tautological Berry holonomy from the unique unphased point `m_0` to
any selected-line point `m` is

```text
Hol(m_0 -> m) = integral_{m_0}^m A = theta(m) - theta(m_0) = delta(m).
```

This is the actual physical bundle/holonomy identification that the ambient
`S^2` note never achieved:

> on the exact charged-lepton selected line, the physical charged-lepton phase
> offset is exactly the Berry holonomy of the tautological line over the
> projective `C_3` doublet ray.

At the directly Berry-selected point, the runner finds

```text
delta = 2/9,
```

`delta = 2/9` exactly, with the legacy witness remaining only as a
near-coincident compatibility datum.

### Exact scalar-phase bridge on the selected line

Write the surviving selected-line scalar as

```text
kappa_sel(m) := (v(m) - w(m)) / (v(m) + w(m)).
```

Using the exact Fourier form above and transforming back to the axis basis,
the normalized Koide amplitudes on the first branch satisfy

```text
u(delta) = sqrt(6)/6 - (sqrt(3)/3) sin(delta + pi/6),
v(delta) = sqrt(6)/6 - (sqrt(3)/3) cos(delta + pi/3),
w(delta) = sqrt(6)/6 + (sqrt(3)/6) (2 cos(delta) + sqrt(2)),
```

with `delta = theta - 2 pi / 3`. Therefore

```text
kappa_sel(delta)
  = (v(delta) - w(delta)) / (v(delta) + w(delta))
  = -sqrt(3) cos(delta + pi/6) / (sqrt(2) + sin(delta + pi/6)).
```

So on the first branch the surviving selected-line scalar and the Berry offset
are exactly one-to-one coordinates on the same actual route. On the branch-local
theorem stack, there is therefore no independent selected-line scalar law left
once `delta` is fixed.

### What happened to the old `n = 2` story

On the actual route the canonical bundle is the tautological `CP^1` line with
`c_1 = 1`. The load-bearing factor `2` now comes from the forced projective
coordinate

```text
[e^{ i theta} : e^{-i theta}] = [1 : e^{-2 i theta}],
```

i.e. from the doubled relative phase of the conjugate doublet pair, not from a
chosen ambient monopole charge. So the old ambient-`S^2` `n = 2` closure claim
remains false, but the actual-route phase identification becomes canonical.

---

## 5. Why this now also fixes the selected-line point on the branch stack

The actual-route Berry identification closes the physical phase-observable
question, and on the branch-local stack it does more than that.

The surviving selected-line scalar is

```text
kappa_sel(m) := (v(m) - w(m)) / (v(m) + w(m)).
```

Section 4 already gave the exact bridge

```text
kappa_sel(delta)
  = -sqrt(3) cos(delta + pi/6) / (sqrt(2) + sin(delta + pi/6)).
```

On the physical first branch, the runner verifies that both `delta(m)` and
`kappa_sel(m)` are strictly monotone. Therefore:

```text
delta = 2/9  ->  kappa_sel,* = -0.607918569997  ->  m_* = -1.160443440065.
```

So the previously separate branch-local selected-point law does **not** survive
once AXIOM E (which supplies `delta = 2/9`) is combined with the actual-route
geometric identification.

The old `H_*` witness is now only a compatibility check:

```text
kappa_legacy = -0.607912649682,
m_legacy     = -1.160469470086,
```

which differs from the Berry-selected point only at branch precision.

This still does **not** rewrite current-main authority by itself. Current main
continues to record a bounded charged-lepton package because it has not
retained this branch-local actual-route Berry theorem stack.

---

## 6. No-go for natural selected-slice Berry selector laws

One might hope that the selected-line point `m` is itself selected by the Berry
geometry of the canonical `2 x 2` `Z_3` doublet block on the selected slice.
That hope fails for the natural classes checked in the runner.

Let `K_2(m)` be the selected-slice `2 x 2` Hermitian doublet block. It has two
canonical eigenline bundles. The obvious open-path geometric-phase candidates
are:

1. the lower-eigenline geometric phase from the unique unphased point `m_0`,
2. the lower-eigenline geometric phase from the positivity threshold `m_pos`,
3. the upper-eigenline geometric phase from `m_0`.

At the Berry-selected point these are approximately

```text
gamma_lower(m_0 -> m_*)   ~= 0.17815,
gamma_lower(m_pos -> m_*) ~= -0.01480,
gamma_upper(m_0 -> m_*)   ~= 0.27634,
```

none of which equals `2/9`.

Stronger still, solving the most natural equation

```text
gamma_lower(m_0 -> m) = delta(m)
```

selects

```text
m_sel ~= -0.87678,
```

not the Berry-selected point

```text
m_* ~= -1.16044.
```

So the canonical selected-slice eigenline Berry phases do **not** supply the
point-selection mechanism.

This is the relevant new no-go:

> **No-go for naive selected-slice Berry selector closure.**
> On the actual charged-lepton selected slice, the canonical eigenline geometric
> phases of the `Z_3` doublet block do not pick the physical selected point.

So these natural selected-slice Berry phases are **not** the mechanism that
fixes the point. The point is fixed instead by the exact actual-route
scalar-phase bridge above.

---

## 7. Closure audit against the five required questions

### 7.1 Why the relevant reduced phase space is physical

Not the ambient `S^2`: that claim fails.

But on the exact selected charged-lepton route the relevant phase-carrying
reduced space **is** the projective `C_3` doublet ray, because the singlet
weight is fixed and only the conjugate doublet phase moves.

### 7.2 Why the bundle / connection are canonical

Yes on the actual selected route. The bundle is the tautological line on the
projective doublet ray, and the connection is the canonical Pancharatnam-Berry
connection.

### 7.3 Why the relevant `2` is forced

Not as an ambient `c_1 = 2` monopole charge: that earlier claim remains
unproved and in fact unnecessary.

On the actual route the forced `2` comes from the doubled projective phase
`e^{-2 i theta}` of the conjugate pair, while the canonical bundle itself has
`c_1 = 1`.

### 7.4 Why the physical charged-lepton phase is that Berry holonomy

Yes on the actual selected line. The unique unphased point `m_0` gives the
phase origin, and the Berry holonomy from `m_0` to `m` is exactly

```text
delta(m) = theta(m) - 2 pi / 3.
```

### 7.5 Why this closes the live current-main gap

For the **branch-local actual-route theorem stack**, yes. The live Berry-specific
gap was the missing identification of the physical charged-lepton phase with a
canonical Berry holonomy on the actual route. This note supplies exactly that
identification, and together with the exact selected-line scalar-phase bridge it
also removes the previous branch-local `m_* / kappa_sel,*` import.

For **current-main authority**, not yet. The authoritative bounded
charged-lepton package on main is not overwritten merely by recording this
branch-local theorem.

---

## 8. Runner verification

The companion runner now validates only claims that are actually checked:

- the Koide locus is a fixed-latitude circle and the positive chamber is an
  arc;
- the ambient `S^2` wedge arithmetic is support-only;
- on the actual selected line, the normalized Fourier coefficients have the
  fixed-modulus conjugate form above;
- the unique unphased selected-line point exists and sets `delta = 0`;
- the canonical tautological connection on the projective doublet ray is
  `A = d theta`;
- solving `delta(m) = 2/9` gives the unique first-branch selected point;
- the Berry holonomy from the unphased point to that point is exactly `2/9`;
- the old `H_*` witness is only a near-coincident compatibility check;
- natural selected-slice eigenline Berry selectors fail to pick that
  Berry-selected point;
- the retained circulant eigenvectors still carry zero Berry phase on their own
  moduli.

Narrative statements are no longer marked `PASS`.

---

## 9. Bottom line

**Verdict for AXIOM E / `delta = 2/9`: geometrically identified on the
physical selected route, not independently forced by Berry geometry.**

The branch's original ambient-`S^2` monopole proof is false (the actual Koide
locus is not `S^2`), and the actual selected-line Berry theorem correctly
identifies what the physical phase observable *is*: on the exact selected
charged-lepton route, the physical phase datum is the projective `C_3`
doublet ray `[1 : e^{-2 i theta}]`; the tautological line over that ray
carries the canonical Pancharatnam–Berry connection `A = d theta`; and the
Berry holonomy from the unique unphased point is exactly the Brannen phase
offset `delta = theta - 2 pi / 3`. That gives `delta` its canonical geometric
meaning. What it does **not** do is *quantize* `delta = 2/9` from Berry data
alone: any scalar shift of the reference section gives the same holonomy, and
the retirement-style argument in `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_…`
correctly records that the specific value `2/9` is not forced on natural
enlargements of the base. AXIOM E therefore remains the retained input that
supplies the specific number `2/9`.

What the theorem **does** close on the branch-local stack is the internal
consistency of the selected-line package: the exact selected-line
scalar-phase bridge

```text
delta = 2/9  ->  kappa_sel,*  ->  unique first-branch m_*,
```

shows that once `delta` is supplied by AXIOM E, the previously separate
branch-local imports `m_*` and `kappa_sel,*` are no longer free — they are
one-to-one coordinates on the same actual route. The legacy `H_*` witness
then reduces to compatibility data. What remains bounded is the authoritative
current-main charged-lepton package, because current main has not yet adopted
this branch-local actual-route theorem stack, and independently because the
axiom-native forcing of `2/9` itself is still open.
