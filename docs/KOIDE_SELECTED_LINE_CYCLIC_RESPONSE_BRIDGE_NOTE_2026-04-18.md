# Koide Selected-Line Cyclic-Response Bridge

**Date:** 2026-04-18  
**Status:** exact bridge theorem on the branch-local actual-route stack. Once
AXIOM E is closed on the actual Berry route, the previously separate
selected-line scalar/point law is no longer open: `delta = 2/9` fixes
`kappa_sel,*` and the unique first-branch point `m_*`. The old `H_*` witness is
demoted to a compatibility check.
**Runner:** `scripts/frontier_koide_selected_line_cyclic_response_bridge.py`
(PASS=20 FAIL=0)

## Question

After the branch-local Berry theorem identifies the physical charged-lepton
phase as the actual-route holonomy

```text
delta = theta - 2 pi / 3 = 2/9,
```

does the selected line still need one extra imported scalar `kappa_sel,*` to
choose the physical point?

## Bottom line

No.

On the exact selected line

```text
G_m = H(m, sqrt(6)/3, sqrt(6)/3),
```

the surviving cyclic scalar

```text
kappa_sel := sqrt(3) r2 / (2 r0 - r1) = (v-w) / (v+w)
```

is an exact function of the Berry offset:

```text
kappa_sel(delta)
  = -sqrt(3) cos(delta + pi/6) / (sqrt(2) + sin(delta + pi/6)).
```

On the physical first branch, both `delta(m)` and `kappa_sel(m)` are strictly
monotone. Therefore

```text
delta = 2/9  ->  kappa_sel,* = -0.607918569997  ->  m_* = -1.160443440065,
```

with

```text
w/v = 4.100981191542.
```

So the selected-line scalar/point law is not an independent remaining gap once
AXIOM E is genuinely closed on the actual route.

## 1. Exact cyclic/orbit inversion

The selected-line `Gamma`-orbit reduction gives

```text
r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w).
```

This inverts exactly to

```text
u = (r0 + r1) / 3,
v = r0/3 - r1/6 + sqrt(3) r2/6,
w = r0/3 - r1/6 - sqrt(3) r2/6.
```

So the cyclic responses and the physical orbit slots are exactly equivalent
coordinates.

## 2. The bridge is one scalar, and that scalar is the Berry offset

Define

```text
kappa_sel := sqrt(3) r2 / (2 r0 - r1).
```

Using the inversion formulas,

```text
2 r0 - r1 = 3 (v+w),
sqrt(3) r2 = 3 (v-w),
```

so

```text
kappa_sel = (v-w) / (v+w),
w/v = (1-kappa_sel) / (1+kappa_sel).
```

Along the exact first selected-line branch, the normalized Koide state has
Fourier form

```text
s(m) = (1/sqrt(2)) v_1 + (1/2) e^{i theta(m)} v_omega
                     + (1/2) e^{-i theta(m)} v_omegabar,
```

with `delta = theta - 2 pi / 3`. Transforming back to the axis basis yields the
exact scalar-phase bridge

```text
kappa_sel(delta)
  = -sqrt(3) cos(delta + pi/6) / (sqrt(2) + sin(delta + pi/6)).
```

That is the load-bearing step: the selected-line scalar is not independent of
the actual-route Berry phase.

## 3. The first branch is one-to-one

The runner verifies two exact branch anchors:

```text
m_pos = -1.295794904067,    kappa_pos = -1/sqrt(3),
m_0   = -0.265815998702,    delta(m_0) = 0.
```

On the open interval `(m_pos, m_0)`, both

```text
kappa_sel(m)
```

and

```text
delta(m)
```

are strictly monotone. Therefore either one is a complete coordinate on the
physical first branch, and solving `delta(m) = 2/9` gives one unique
selected-line point.

## 4. Corollary: AXIOM E fixes `kappa_sel,*` and `m_*`

Substituting the actual-route Berry target `delta = 2/9` into the exact bridge
gives

```text
kappa_sel,* = -0.607918569997.
```

Solving

```text
delta(m) = 2/9
```

on the first branch gives

```text
m_* = -1.160443440065.
```

At that point:

```text
kappa_sel(m_*) = -0.607918569997,
w/v = 4.100981191542,
Q = 2/3 exactly,
cos(dir(m_*), dir_PDG) > 0.99999999997.
```

So the selected-line direction is fixed directly by AXIOM E once the actual
Berry theorem is in place.

## 5. The old `H_*` witness is no longer load-bearing

The imported one-clock `H_*` witness still lands very near the Berry-selected
point:

```text
kappa_legacy = -0.607912649682,
m_legacy     = -1.160469470086.
```

The differences are only

```text
Delta kappa = -5.92e-06,
Delta m     = +2.60e-05.
```

So the old witness remains a branch-precision compatibility check, not the step
that fixes the selected-line point.

## 6. Scope boundary

This note closes the branch-local selected-line scalar/point law on the
combined Berry-plus-selected-line route:

```text
delta = 2/9  ->  kappa_sel,*  ->  unique first-branch m_*.
```

It does **not** by itself rewrite the authoritative current-main bounded
charged-lepton package. Current main still records a bounded result because the
actual-route Berry theorem is branch-local science, not current-main authority.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_selected_line_cyclic_response_bridge.py
```
