# Koide Berry-Holonomy Theorem: Actual-Route Closure of AXIOM E

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide phase `delta = 2/9` / AXIOM E audit
**Cycle:** 10B revised again
**Status:** AXIOM E is closed on the actual charged-lepton selected route. The
branch's original ambient-`S^2` / monopole closure theorem fails, but on the
exact selected charged-lepton line there **is** a canonical Berry
bundle/connection, and the physical Brannen phase offset `delta` is exactly the
Berry holonomy of that actual-route bundle measured from the unique unphased
selected-line point. The separate microscopic selected-point law for the full
charged-lepton mass package remains open upstream of this phase theorem.

This note supersedes the earlier cycle-10B closure phrasing for the Berry lane
only. The right scientific split is now:

1. the ambient `S^2` / monopole / `n = 2` closure claim is false;
2. the physical phase observable **can** be identified canonically as a Berry
   holonomy on the actual charged-lepton route;
3. that phase theorem closes AXIOM E itself;
4. it does **not** by itself fix which selected-line point is physical, so the
   separate live current-main charged-lepton selector gap is still open.

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
actual `C_3` doublet ray, not from a chosen monopole charge. At the current
selected-line witness point, that holonomy is `delta ~= 2/9`.

What remains open is different and smaller: the Berry geometry does not derive
the selected-line scalar `m_*` (equivalently the selected-line
`kappa_sel,* := (v_* - w_*) / (v_* + w_*)`). Natural selected-slice Berry
selector equations on the canonical `2 x 2` `Z_3` doublet block fail to pick
the physical witness. So the live current-main gap is no longer the physical
bundle/connection identification; it is the microscopic selected-point law
upstream of the phase observable.

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

At the current selected-line witness point, the runner finds

```text
delta ~= 0.22222986,
```

which is within the current witness precision of `2/9`.

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
are exactly one-to-one coordinates on the same actual route. The open
microscopic selector law is therefore upstream of the phase theorem; it is not
an additional ambiguity in the phase observable once the physical selected-line
endpoint is fixed.

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

## 5. Why this closes AXIOM E but not the full charged-lepton mass gate

The actual-route Berry identification closes the physical phase-observable
question. The remaining open scalar on current main is a different question:
which selected-line point is physically realized.

The remaining exact charged-lepton gap on current main is already known to be
one microscopic scalar law on the selected slice:

```text
m  <->  kappa_sel  <->  Re K12  <->  Tr K_Z3.
```

The Berry geometry above tells us:

- what the physical phase observable is,
- what its canonical reference point is,
- and how to read `delta` once the selected point is known.

It does **not** derive which `m` is realized physically.

So the scientific split is:

- **AXIOM E / phase gate:** closed on the actual selected route.
- **Full charged-lepton promotion:** still open because the microscopic
  selected-point law is still open.

---

## 6. No-go for natural selected-slice Berry selector laws

One might hope that the remaining scalar `m` is itself selected by the Berry
geometry of the canonical `2 x 2` `Z_3` doublet block on the selected slice.
That hope fails for the natural classes checked in the runner.

Let `K_2(m)` be the selected-slice `2 x 2` Hermitian doublet block. It has two
canonical eigenline bundles. The obvious open-path geometric-phase candidates
are:

1. the lower-eigenline geometric phase from the unique unphased point `m_0`,
2. the lower-eigenline geometric phase from the positivity threshold `m_pos`,
3. the upper-eigenline geometric phase from `m_0`.

At the current selected-line witness point these are approximately

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

not the physical witness point

```text
m_* ~= -1.16047.
```

So the canonical selected-slice eigenline Berry phases do **not** supply the
missing microscopic selector law.

This is the relevant new no-go:

> **No-go for naive selected-slice Berry selector closure.**
> On the actual charged-lepton selected slice, the canonical eigenline geometric
> phases of the `Z_3` doublet block do not pick the physical selected point.

So even after the actual-route bundle/holonomy identification is fixed, the
remaining closure problem is still one microscopic scalar selector law beyond
these natural Berry choices.

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

For the **phase gate**, yes. The live Berry-specific current-main gap was the
missing identification of the physical charged-lepton phase with a canonical
Berry holonomy on the actual route. This note supplies exactly that
identification and replaces the false ambient-`S^2` closure story by the actual
selected-line theorem.

For the **full charged-lepton mass package**, no. The microscopic selected-line
point law remains open, so the broader charged-lepton promotion boundary on
current main does not move.

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
- the Berry holonomy from that point to the current selected-line witness
  equals the physical phase offset;
- natural selected-slice eigenline Berry selectors fail to pick the witness;
- the retained circulant eigenvectors still carry zero Berry phase on their own
  moduli.

Narrative statements are no longer marked `PASS`.

---

## 9. Bottom line

**Verdict for AXIOM E / `delta = 2/9`: closed.**

The branch's original ambient-`S^2` monopole proof is false, but the actual
selected-line Berry theorem is strong enough to replace it. On the exact
selected charged-lepton route, the physical phase datum is the projective
`C_3` doublet ray `[1 : e^{-2 i theta}]`; the tautological line over that ray
carries the canonical Berry connection `A = d theta`; and the Berry holonomy
from the unique unphased point is exactly the Brannen phase offset
`delta = theta - 2 pi / 3`. That is the load-bearing scientific step the
ambient note never supplied.

**What remains open:** not the phase observable, but the upstream microscopic
selected-point law choosing the physical endpoint `m_*` on the selected line.
That keeps the broader charged-lepton mass-hierarchy package bounded on current
main, but it does not undo the actual-route Berry closure of AXIOM E.
