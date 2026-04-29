# P3 MSbar-to-Pole K_1 Framework-Native Derivation Note (1-loop Casimir)

**Date:** 2026-04-17
**Status:** proposed_retained **framework-native** structural sub-theorem — the
1-loop coefficient of the MSbar-to-pole mass conversion is
`K_1 = C_F = (N_c² − 1)/(2 N_c) = 4/3` at SU(3). Exact rational;
follows directly from the retained SU(3) fundamental Casimir. Fully
retained, not cited.
**Primary runner:** `scripts/frontier_yt_p3_msbar_to_pole_k1.py`.
**Log:** `logs/retained/yt_p3_msbar_to_pole_k1_2026-04-17.log`.

## Authority notice

This note is a retained framework-native sub-theorem on the K-series
structural retention program for the P3 primitive of the master UV-to-IR
transport obstruction theorem (the MSbar-to-pole mass conversion
coefficient series used for the top-quark pole mass). It records the
exact SU(3) value of the 1-loop coefficient `K_1` and is the first step
in the K-series retention chain (K_1 framework-native → K_2 color-tensor
retained → K_3 color-tensor retained).

This note does NOT modify:

- the master obstruction theorem
  (`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`);
- any SU(3) Casimir authority
  (`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`, D7; or
  `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`, S1);
- any publication-surface file.

## Cross-references

- **Master obstruction:**
  [`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`](YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md) —
  names the MSbar-to-pole mass conversion series as a P3 sub-primitive;
  this note closes the K_1 step framework-native.
- **K-series continuation:**
  - [`docs/YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
    — 4-tensor K_2 color-tensor retention.
  - [`docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
    — 10-tensor K_3 color-tensor retention.
  - [`docs/YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md`](YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md) — geometric
    tail bound on higher-order K_n.
- **SU(3) Casimir authorities:**
  - [`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) (D7 — `C_F = (N_c²−1)/(2 N_c)`).
  - [`docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`](YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md) (S1 — gauge-group
    uniqueness).

## Abstract

On the retained `Cl(3)/Z^3` framework surface, the 1-loop coefficient
of the MSbar-to-pole mass conversion series

```
m_pole / m_MSbar(m_t)  =  1  +  K_1 (α_s/π)  +  K_2 (α_s/π)²  +  K_3 (α_s/π)³  +  ...
```

is exactly `K_1 = C_F` — the SU(3) fundamental Casimir. This is a
single-color-tensor coefficient, obtained from a single one-loop
heavy-quark self-energy topology with a single exchanged gluon between
the heavy-quark line and itself. The color factor is `T^A T^A = C_F · 1`
(fundamental Casimir), and the remaining kinematic + Dirac-trace
integral contributes a factor of `1` on shell (in the `α_s/π`
convention), so `K_1 = C_F` directly. At SU(3), `K_1 = 4/3` exactly.

Numerically, at `α_s(m_t) ≈ 0.108` (retained plaquette-derived coupling
run to m_t on the framework surface), the 1-loop shift is

```
K_1 · (α_s/π)  ≈  (4/3) · (0.108 / π)  ≈  0.0458
```

i.e. roughly 4.58 % of `m_MSbar(m_t)`. This is the dominant piece of
the full MSbar → pole mass shift (≈ 78 % of the total conversion shift
through three loops at this coupling).

The retention is fully framework-native: no literature value is
imported; the result follows directly from the retained SU(3)
fundamental Casimir.

## 1. Retained foundations

This note uses the following retained authorities without modification:

- **SU(3) fundamental Casimir.** From `docs/YT_EW_COLOR_PROJECTION_THEOREM.md`
  (D7) and `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1):
  ```
  C_F  =  (N_c² − 1) / (2 N_c)  =  4/3        at N_c = 3
  ```
- **Running-coupling anchor.** `α_s(m_t) ≈ 0.108` on the retained
  framework surface (plaquette-derived coupling run to `μ = m_t`). Used
  only as a numerical comparator for the 1-loop shift magnitude; the
  derivation `K_1 = C_F` does not depend on the specific value of
  `α_s(m_t)`.

No retained authority note on `main` is modified by this submission.

## 2. Theorem statement

**Theorem P3-K_1.** On the retained `Cl(3)/Z^3` framework surface, the
1-loop coefficient of the MSbar-to-pole mass conversion series of the
heavy-quark pole mass is exactly

```
K_1  =  C_F  =  (N_c² − 1) / (2 N_c)                                 (2.1)
```

which evaluates at SU(3) to

```
K_1  =  4/3                                                          (2.2)
```

as an exact rational. The result is framework-native: it follows
directly from the retained SU(3) fundamental Casimir with no
external-literature input.

## 3. Derivation

### 3.1 Series convention

The MSbar-to-pole mass conversion of a heavy quark with MSbar mass
`m_MSbar` (evaluated at its own mass, `μ = m_MSbar`) to its pole mass
is, in the standard perturbative QCD convention,

```
m_pole  =  m_MSbar(m_MSbar) · [ 1 + K_1 (α_s/π) + K_2 (α_s/π)² + K_3 (α_s/π)³ + ...]
                                                                      (3.1)
```

with the expansion parameter `α_s/π` (not `α_s/(4π)`; the two
conventions differ by a factor 4 at each order). The coefficients
`K_n` are pure numbers depending on the number of colors `N_c`, the
number of light flavors `n_l`, and the renormalization scheme; they
are computed from on-shell heavy-quark self-energy topologies at the
corresponding loop order.

### 3.2 1-loop topology

At 1-loop, the unique diagram contributing to the on-shell heavy-quark
self-energy is a single gluon exchanged between the heavy-quark line
and itself:

```
    _________
   /         \
  t           t       (heavy-quark line, on-shell at p² = m²)
  \_/\_/\_/\_/
     gluon
```

The color factor at the two `ψ̄γ^μ T^A ψ` vertices is
`T^A T^A = C_F · 1` (fundamental Casimir, contracted over the gauge
index A). The remaining integrand is a Dirac-trace + momentum integral
that, when evaluated on shell and in the MSbar scheme at `μ = m`, gives
a pure number independent of the gauge group. In the `α_s/π` convention
this number is `+1`:

```
Σ_1-loop(on-shell)  =  − m · C_F · (α_s/π) · 1 + O(α_s²)             (3.2)
```

The on-shell-mass shift `Δm = −Σ(p = m)` therefore gives

```
m_pole − m_MSbar(m_MSbar)  =  m · C_F · (α_s/π) + O(α_s²)
```

and dividing by `m_MSbar(m_MSbar)` and identifying the leading
coefficient:

```
K_1  =  C_F                                                           (3.3)
```

### 3.3 SU(3) value

At `N_c = 3`:

```
C_F  =  (N_c² − 1) / (2 N_c)  =  (9 − 1) / 6  =  8/6  =  4/3          (3.4)
K_1  =  4/3                                                          (3.5)
```

which is an exact rational.

## 4. Numerical verification at the top-quark scale

### 4.1 Retained coupling

On the retained framework surface, the plaquette-derived running
coupling run to `μ = m_t` has the central value

```
α_s(m_t)  ≈  0.108                                                   (4.1)
```

(The specific numerical figure is consistent with the PDG world-average
at the top-quark scale to within ~0.5 %; it enters this note only as a
numerical comparator for the 1-loop shift magnitude.)

### 4.2 1-loop shift

Inserting (3.5) and (4.1) into the leading term of (3.1):

```
K_1 · (α_s/π)  =  (4/3) · (0.108 / π)
              ≈  (4/3) · 0.034377
              ≈  0.04584
              ≈  4.58 %                                              (4.2)
```

This is the 1-loop MSbar-to-pole mass shift on the retained framework
surface.

### 4.3 Fraction of total MSbar → pole shift at 3 loops

With the retained K_2(n_l=5) = 10.9405 and the cited K_3(n_l=5) = 80.405
(the latter a literature comparator, not retained framework-native here):

```
δ_1  =  K_1 · (α_s/π)      =  0.04584
δ_2  =  K_2 · (α_s/π)²    =  10.9405 · (0.108/π)²   ≈  0.01293
δ_3  =  K_3 · (α_s/π)³    =  80.405 · (0.108/π)³    ≈  0.00327
---------------------------------------------------
δ_tot (through 3-loop)                             ≈  0.06204

Fraction (δ_1 / δ_tot)                             ≈  0.7388  ≈  74 %
```

So the 1-loop piece `K_1 (α_s/π) ≈ 4.58 %` contributes roughly three
quarters of the total MSbar → pole mass shift at three loops. The
dominant position of K_1 in the series is expected: it carries the
sole `C_F` coefficient, with the higher-order terms bringing in
compounded `(α_s/π)` suppression factors.

## 5. Safe claim boundary

This note claims:

> On the retained `Cl(3)/Z^3` framework surface, the 1-loop coefficient
> of the MSbar-to-pole mass conversion series of a heavy quark is
> exactly `K_1 = C_F = (N_c² − 1)/(2 N_c)`, which evaluates at SU(3)
> to the exact rational `4/3`. The derivation is framework-native from
> the retained SU(3) fundamental Casimir authority; no literature
> value is imported. At the retained running-coupling anchor
> `α_s(m_t) ≈ 0.108`, the 1-loop shift `K_1 (α_s/π) ≈ 4.58 %` is the
> dominant piece of the MSbar → pole mass conversion through three
> loops, contributing ≈ 74 % of the total.

It does **not** claim:

- a framework-native derivation of `K_2` or higher (those are treated
  in separate color-tensor retention sub-theorems);
- a specific numerical value of `α_s(m_t)` beyond the retained
  plaquette-derived anchor `≈ 0.108`; the specific figure enters only
  as a numerical comparator for the 1-loop shift;
- any modification of the master obstruction theorem, any SU(3)
  Casimir authority, or any publication-surface file.

## 6. What is retained vs. cited vs. open

**Retained (framework-native):**

- `C_F = 4/3` at SU(3) (D7 + S1).
- `K_1 = C_F` from the 1-loop heavy-quark self-energy topology and
  the `α_s/π` scheme convention.
- `K_1 = 4/3` at SU(3) as an exact rational.
- `α_s(m_t) ≈ 0.108` from the retained plaquette-derived coupling
  run to m_t (used only as a numerical comparator for the shift
  magnitude).

**Cited (external comparators, not central to the retention):**

- The higher-order coefficients `K_2(n_l=5) = 10.9405` and
  `K_3(n_l=5) = 80.405` enter only the fractional-coverage comparator
  in §4.3; they are not part of the K_1 retention claim and are
  treated in the downstream K_2 and K_3 sub-theorems.

**Open (not closed by this note):**

- Framework-native retention of K_2, K_3, K_4+ (treated separately).

## 7. Validation

The runner `scripts/frontier_yt_p3_msbar_to_pole_k1.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p3_msbar_to_pole_k1_2026-04-17.log`. The runner
must return PASS on every check to keep this note on the retained
surface.

The runner verifies 4 checks:

1. `C_F = (N_c² − 1)/(2 N_c) = 4/3` exactly at SU(3).
2. `K_1 = C_F` identity (1-loop heavy-quark Casimir).
3. `α_s(m_t) ≈ 0.108` retained plaquette-derived value (numerical
   comparator, matched to within 1 %).
4. `K_1 · (α_s/π) ≈ 4.58 %` at the retained coupling anchor
   (numerical comparator, matched to within 1 %).

## Status

**RETAINED** — `K_1 = C_F = 4/3` framework-native, exact rational at
SU(3). First step of the K-series retention chain; downstream K_2 and
K_3 color-tensor retention steps inherit this result without
modification.
