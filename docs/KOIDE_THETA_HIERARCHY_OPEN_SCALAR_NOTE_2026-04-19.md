# Koide Theta Hierarchy Open Scalar -- Closed on the Actual Berry Route

**Date:** 2026-04-19
**Status:** closed for AXIOM E / the charged-lepton phase gate. On the
branch-local actual-route stack, the previously separate selected-line
`m_* / kappa_sel,*` input is also gone as a corollary. The old ambient-`S^2` /
`n = 2` monopole story is superseded. The correct closure lives on the exact
selected charged-lepton line.

**Primary reference:** `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`.

---

## 1. What was open

The residual charged-lepton angular datum was the Brannen-Zenczykowski phase

```text
theta_PDG = 2 pi / 3 + delta,    delta ~= 2/9,
```

equivalently AXIOM E in the branch language. Earlier cycle-10 text claimed to
close this by putting a chosen `n = 2` monopole bundle on an ambient
projectivized Koide `S^2`. That is not the actual charged-lepton route.

---

## 2. What actually closes

On the exact selected charged-lepton line

```text
H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3),
```

the normalized Koide state has exact Fourier form

```text
s(m) = (1/sqrt(2)) v_1 + (1/2) e^{i theta(m)} v_omega
                     + (1/2) e^{-i theta(m)} v_omegabar.
```

So the physical phase-carrying datum is the projective `C_3` doublet ray

```text
[e^{i theta(m)} : e^{-i theta(m)}] = [1 : e^{-2 i theta(m)}]
```

on the equator of `CP^1`. The tautological line over that ray has canonical
Berry connection

```text
A = d theta.
```

There is a unique unphased first-branch point `m_0` with `theta(m_0)=2 pi / 3`,
so

```text
Hol(m_0 -> m) = theta(m) - 2 pi / 3 = delta(m).
```

That is the load-bearing theorem: the physical charged-lepton phase observable
is the Berry holonomy of the canonical tautological line on the actual selected
route.

At the directly Berry-selected point, the runner gives

```text
delta = 2/9,
```

with the legacy witness remaining only as a near-coincident compatibility
datum.

---

## 3. What the forced `2` is

The relevant forced factor `2` is **not** an ambient monopole charge. On the
actual route it comes from the doubled projective phase

```text
[1 : e^{-2 i theta}],
```

forced by the conjugate doublet pair `(e^{i theta}, e^{-i theta})`. The
canonical bundle itself is the tautological `CP^1` line.

---

## 4. Scope boundary

On the branch-local stack, the exact selected-line scalar-phase bridge gives

```text
delta = 2/9  ->  kappa_sel,* = -0.607918569997  ->  m_* = -1.160443440065.
```

So there is no longer a separate selected-line scalar import on this route.

This still does **not** automatically rewrite the authoritative current-main
bounded charged-lepton package. Current main remains bounded until the
branch-local actual-route Berry theorem stack is promoted there.

---

## 5. Runner status

The Berry runner
`scripts/frontier_koide_berry_phase_theorem.py`
now validates the actual selected-line carrier, the forced doubled projective
phase, the direct `delta = 2/9 -> m_*` selection, the canonical Berry
connection, the selected-slice Berry-selector no-go, and the zero-Berry
retained circulant moduli result. Narrative statements are no longer marked as
validated.
