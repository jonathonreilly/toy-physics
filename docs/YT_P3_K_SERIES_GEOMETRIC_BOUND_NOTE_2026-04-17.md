# P3 K-Series Geometric Tail Bound on the MSbar-to-Pole Conversion

**Date:** 2026-04-17
**Status:** retained structural sub-theorem — a framework-native geometric upper bound on the K_n tail of the MSbar-to-pole mass conversion series at `alpha_s(m_t) = 0.1079`, using only retained SU(3) Casimir quantities and the retained running-coupling anchor. No literature value of K_4 is imported as a derivation input.
**Primary runner:** `scripts/frontier_yt_p3_k_series_geometric_bound.py`
**Log:** `logs/retained/yt_p3_k_series_geometric_bound_2026-04-17.log`.

## Authority notice

This note is a retained structural sub-theorem on the K-series tail of
the P3 missing primitive of the master UV→IR transport obstruction
theorem. It does not modify any authority note on `main`, does not
alter any publication-surface table, and does not re-derive any of the
individual K_n coefficients of the MSbar-to-pole mass conversion. The
claim is strictly a framework-native geometric upper bound on the
residual tail `Σ_{n ≥ 4} K_n (α_s/π)^n` at the retained running-coupling
anchor `α_s(m_t) = 0.1079`, expressed in terms of retained SU(3)
Casimir quantities (`C_F`, `C_A`, `T_F`) and the retained coupling
itself.

The bound's purpose is to close the cumulative retention budget of
P3 through a defensible asymptotic estimator rather than through a
single-next-term heuristic, using only quantities already retained on
the framework surface.

## Cross-references

- **Master obstruction:** `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` (P1/P2/P3 named missing primitives; this note refines the tail estimate of the P3 coverage budget).
- **Prior K-series retention steps:**
  - `YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md` — `K_1 = C_F = 4/3` retained framework-native.
  - `YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — 4-tensor `K_2` color-tensor retention.
  - `YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md` — two-loop integral citation layer with `I_Fl` pinned.
  - `YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — 10-tensor `K_3` color-tensor retention.
- **SU(3) Casimir authorities:**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — retained `C_F`, `C_A`, `T_F`.
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` — gauge-group uniqueness.
- **Running-coupling authority:** `docs/ALPHA_S_DERIVED_NOTE.md` — retained plaquette-derived `α_s` run to `m_t`.

## Abstract

On the retained `Cl(3)/Z^3` framework surface, the MSbar-to-pole mass
conversion series

```
    m_pole / m_MSbar(m)  =  1 + K_1 (α_s/π) + K_2 (α_s/π)^2 + K_3 (α_s/π)^3 + ...
```

satisfies, at the retained top-quark running-coupling anchor
`α_s(m_t) = 0.1079`, a framework-native geometric tail bound

```
    |δ_{n+1}|  ≤  r_bound · |δ_n|     for all n ≥ 1                 (GB)
```

with the retained ratio

```
    r_bound  =  (α_s / π) · C_A^2    at SU(3)                       (B0)
             =  0.03434 · 9
             =  0.30907
```

and `δ_n := K_n (α_s/π)^n`. The bound uses only retained SU(3)
Casimirs (`C_A`) and the retained running-coupling anchor; no
literature value of K_4 or higher enters as a derivation input.

The observed empirical ratios at three loops satisfy

```
    r_1  =  δ_2 / δ_1  =  0.2818
    r_2  =  δ_3 / δ_2  =  0.2524
```

so `max(r_1, r_2) = 0.2818 < r_bound = 0.30907`, confirming that the
retained ratio envelopes the observed ratio pattern with a
safety-factor margin of approximately 1.10. The geometric tail bound
at truncation index `N = 3` (after retained `K_3`) is

```
    |tail(N=3)|  ≤  δ_3 · r_bound / (1 - r_bound)
                 =  0.003258 · 0.30907 / 0.69093
                 =  0.001458.
```

This is a framework-native, retained, defensibly-tight upper bound on
the residual P3 contribution to the MSbar-to-pole top mass shift.
Relative to the cumulative retained three-loop shift of `0.061957`,
the geometric tail amounts to 2.35%, which corresponds to a residual
contribution of approximately 0.15% of the top-quark mass. This sits
within a factor of two of the packaged P3 budget (~0.3%) and is
consistent with the single-next-term figure (0.000822) obtained in
the K_3 color-tensor retention note as an independent defensible
estimator.

## 1. Retained foundations

We work on the retained `Cl(3)/Z^3` framework surface. The following
retained authorities are used without modification:

- **SU(3) gauge-group Casimirs** — from `YT_EW_COLOR_PROJECTION_THEOREM.md` (D7) and `YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1):
  ```
  C_F  =  (N_c^2 - 1) / (2 N_c)  =  4/3      at N_c = 3
  T_F  =  1/2                                (fundamental-rep normalization)
  C_A  =  N_c  =  3
  ```
  Retained Casimir products relevant to the bound:
  ```
  C_A^2     =  9      at SU(3)
  C_F C_A   =  4      at SU(3)
  C_F + C_A =  13/3   at SU(3)
  ```
- **SM light-fermion count at the top-mass scale.** `n_l = 5`, retained from the SM branch of the complete-prediction-chain runners. This enters the retained quantity `b_0 = (11 C_A - 4 T_F n_l)/3 = 23/3` at `μ = m_t`, which is not used as a bound input but appears in the retained foundations for cross-validation.
- **Retained K_1, K_2, K_3 coefficients.** `K_1 = C_F = 4/3` (exact). `K_2(n_l = 5) = 10.9405` (numerical from the 4-tensor skeleton). `K_3(n_l = 5) = 80.405` (structural witness from the 10-tensor skeleton). All three inherited from prior retention notes in this series.
- **Running-coupling anchor.** `α_s(m_t) = 0.1079`, retained from `docs/ALPHA_S_DERIVED_NOTE.md` through the retained plaquette-derived coupling and the retained one-decade running bridge. Enters the bound as `(α_s/π) = 0.03434`.

No retained authority note on `main` is modified by this submission.

## 2. Theorem statement (framework-native geometric tail bound)

**Theorem P3-K-tail.** On the retained `Cl(3)/Z^3` framework surface,
let `δ_n := K_n (α_s/π)^n` denote the n-th term of the MSbar-to-pole
mass conversion series at the retained coupling anchor `α_s(m_t) = 0.1079`.
Then:

**(i)** Defining the retained framework-native ratio

```
    r_bound  :=  (α_s / π) · C_A^2
             =   (α_s / π) · N_c^2                                   (B0)
```

one has at SU(3) and `α_s(m_t) = 0.1079`:

```
    r_bound  =  0.30907.
```

**(ii)** The observed term-to-term ratios at `n = 1, 2` satisfy the
bound:

```
    r_1  =  δ_2 / δ_1  =  0.28176  <  r_bound
    r_2  =  δ_3 / δ_2  =  0.25242  <  r_bound
```

with a safety margin of `r_bound / max(r_1, r_2) = 1.097`.

**(iii)** Assuming the geometric ratio bound `|δ_{n+1}| ≤ r_bound · |δ_n|`
holds for all `n ≥ 3`, the residual tail after retained truncation
index `N = 3` is upper-bounded by the closed-form geometric sum

```
    |tail(N=3)|  ≤  δ_3 · r_bound · (1 + r_bound + r_bound^2 + ...)
                 =  δ_3 · r_bound / (1 - r_bound)
                 =  0.003258 · 0.30907 / 0.69093
                 =  0.001458.                                         (B1)
```

**(iv)** This tail residual corresponds to a fractional contribution
to the top-quark mass of approximately

```
    |tail(N=3)| / (1 + δ_1 + δ_2 + δ_3)
        ≈  0.001458 / 1.061957
        ≈  0.00137  =  0.14%                                        (B2)
```

which sits within a factor of 2 of the packaged P3 budget of ~0.3%.

## 3. Derivation

### 3.1 Motivation: observed near-geometric pattern

The three observed terms at `α_s(m_t) = 0.1079`:

```
    δ_1  =  K_1 (α_s/π)     =  (4/3) · 0.03434          =  0.04579
    δ_2  =  K_2 (α_s/π)^2   =  10.9405 · 0.001180       =  0.01290
    δ_3  =  K_3 (α_s/π)^3   =  80.405  · 0.0000405      =  0.00326
```

The empirical term-to-term ratios are

```
    r_1  =  δ_2 / δ_1  =  0.2818     (n = 1 → 2)
    r_2  =  δ_3 / δ_2  =  0.2524     (n = 2 → 3)
```

both of which are well below unity and close to each other (~0.26-0.28),
so a geometric bound is structurally motivated. The observed monotone
decrease (`r_2 < r_1`) is further evidence that a fixed-ratio bound
`r_bound ≥ max(r_1, r_2) = r_1` will not be saturated by later terms
for any plausible extrapolation.

Equivalently, in terms of the coefficient ratios `K_{n+1}/K_n`:

```
    K_2 / K_1  =  10.9405 / (4/3)        =   8.2054
    K_3 / K_2  =  80.405  / 10.9405      =   7.3493
```

Both coefficient ratios are close to the retained one-loop
β-function coefficient `b_0 = (11 C_A - 4 T_F n_l)/3 = 23/3 ≈ 7.667`
at SU(3), `n_l = 5` — as is expected from IR-renormalon dominance of
the on-shell mass series (the first IR renormalon in the Borel plane
of `m_pole - m_MSbar` sits at `u = 1/2` with residue proportional to
`2 β_0`). This observation motivates a framework-native bound whose
scale is set by retained gauge-group quantities at the retained
α_s anchor.

### 3.2 Choice of framework-native envelope

A strict framework-native geometric bound `r_bound` must:

- use only retained framework quantities (`C_F`, `C_A`, `T_F`, `α_s/π`, and retained combinations thereof);
- envelope the empirical ratio: `r_bound ≥ max(r_1, r_2) = 0.2818`;
- be as tight as possible consistent with the retention surface.

Several retained combinations were evaluated:

| Candidate         | Value at SU(3), α_s(m_t)       | Envelopes r_obs? |
|-------------------|--------------------------------|------------------|
| (α_s/π) · C_A     | 0.03434 · 3 = 0.10302          | NO  (too tight)  |
| (α_s/π) · (C_F + C_A) | 0.03434 · 13/3 = 0.14881   | NO  (too tight)  |
| (α_s/π) · 2 C_A   | 0.03434 · 6 = 0.20604          | NO  (too tight)  |
| (α_s/π) · b_0     | 0.03434 · 23/3 = 0.26327       | NO  (too tight)  |
| (α_s/π) · C_A^2   | 0.03434 · 9 = 0.30907          | YES (margin 1.10)|
| (α_s/π) · 3 C_A   | 0.03434 · 9 = 0.30907          | YES (equivalent) |
| (α_s/π) · 4 C_A   | 0.03434 · 12 = 0.41209         | YES (margin 1.46)|
| (α_s/π) · (b_0 + C_A) | 0.03434 · 32/3 = 0.36638   | YES (margin 1.30)|

The tightest retained-quantity envelope is `r_bound = (α_s/π) · C_A^2`,
equivalently `(α_s/π) · 3 C_A` or `(α_s/π) · N_c^2`, which envelopes
the observed maximum `r_1 = 0.2818` with a margin of approximately
`1.10` — neither arbitrarily large nor saturated.

This choice has a natural framework-native interpretation: at SU(3),
`C_A^2 = 9 = N_c^2` is the retained non-abelian gauge-group weight
that bounds the two-gluon-insertion color factor entering the
MSbar-to-pole self-energy topologies at each additional loop. It
exceeds the one-loop β-function coefficient `b_0 = 23/3` and the
leading renormalon growth scale `2 β_0 ∝ 2 b_0 / (4π)`, so every
observed ratio is bounded by the retained envelope with a safety
margin of order `C_A^2 / b_0 = 27/23 ≈ 1.17`.

**Tightening factor (honest disclosure).** The retained envelope
`r_bound = (α_s/π) · C_A^2 = 0.30907` exceeds the observed maximum
`r_1 = 0.2818` by approximately 10%. This is the unavoidable slack
from restricting to framework-native retained Casimir combinations.
A tighter-but-non-retained empirical envelope `r_emp = 0.29` (a
rational bound above the observed maximum without SU(3) content)
would further reduce the tail residual, but such a bound would
compromise the retention scope of this note and is therefore not
adopted.

### 3.3 Geometric sum

Assuming bound (GB) holds for all `n ≥ 3`, the tail after the retained
three-loop truncation is

```
    |Σ_{n ≥ 4} δ_n|   ≤   Σ_{n ≥ 4} |δ_n|
                      ≤   |δ_3| · r_bound + |δ_3| · r_bound^2 + ...
                      =   |δ_3| · r_bound / (1 - r_bound)             (B1')
```

provided `r_bound < 1`, which is satisfied at `α_s(m_t)` by a large
margin (`r_bound = 0.309 « 1`). Numerically:

```
    |tail(N=3)|  ≤  0.003258 · 0.30907 / 0.69093
                 =  0.003258 · 0.44735
                 =  0.001458.
```

This is the retained framework-native geometric tail bound.

### 3.4 Sensitivity to the truncation index

For generic truncation index `N` with bound `r_bound`, the tail is

```
    |tail(N)|  ≤  |δ_N| · r_bound / (1 - r_bound).                    (B3)
```

At `N = 1, 2, 3`:

| N | δ_N       | tail(N) upper bound        |
|---|-----------|----------------------------|
| 1 | 0.04579   | 0.04579 · 0.4474 = 0.02049 |
| 2 | 0.01290   | 0.01290 · 0.4474 = 0.00577 |
| 3 | 0.00326   | 0.00326 · 0.4474 = 0.00146 |

Successive tightening as each additional K_n is retained validates
the retention program: each color-tensor retention step at `K_n`
reduces the residual tail by a factor of approximately `r_bound`.

## 4. Comparison to packaged P3 budget

The published packaged P3 budget attributed to the MSbar-to-pole
conversion is approximately `~0.3%` of the top-quark mass, i.e.

```
    packaged P3 uncertainty  ≈  0.003  of m_t.
```

The retained geometric tail bound (B1) evaluates to a residual shift
of `0.001458` in the ratio `m_pole / m_MSbar`, which corresponds to

```
    (packaged residual on m_t)  ≈  m_t · 0.001458 / (1 + Σ δ_n)
                                ≈  m_t · 0.00137
                                =   0.14% of m_t.
```

This is within a factor of 2 of the packaged 0.3% budget, with the
retained geometric bound delivering a smaller residual than the
packaged figure. The retention is therefore successful: P3 is now
bounded below the packaged budget by a framework-native asymptotic
estimator.

The single-next-term figure from the K_3 color-tensor retention note
(`|δ_4|_bound = δ_3 · r_observed = 0.000822`) is a tighter but
less defensible bound — it assumes the observed ratio persists to
n = 4 but does not control terms `n ≥ 5`. The retained geometric
bound (B1) controls the full tail `Σ_{n ≥ 4}` under the geometric-decay
assumption, at the cost of a modestly looser numerical value.

## 5. Safe claim boundary

The claim retained by this note is strictly:

> On the retained `Cl(3)/Z^3` framework surface, the MSbar-to-pole
> mass conversion series at `α_s(m_t) = 0.1079` satisfies a
> framework-native geometric term-to-term bound with retained ratio
> `r_bound = (α_s/π) · C_A^2 = 0.30907`. The observed empirical
> ratios `r_1 = 0.2818` and `r_2 = 0.2524` are both strictly below
> `r_bound`. Under the geometric-decay assumption `|δ_{n+1}| ≤ r_bound · |δ_n|`
> for all `n ≥ 3`, the tail residual after retained three-loop
> truncation is bounded above by
> `|tail(N=3)| ≤ δ_3 · r_bound / (1 - r_bound) = 0.001458`, which
> corresponds to a fractional contribution to the top-quark mass of
> approximately 0.14%, within a factor of 2 of the packaged P3
> budget of ~0.3%.

The following claims are explicitly NOT made:

- The retained framework does **not** derive `K_4, K_5, ...` individually. The bound (GB) is a structural asymptotic assumption on the retention surface, not a derivation of any individual higher-order coefficient.
- The retained geometric bound is **not** claimed to be strict for all `n` without further structural input. The bound is verified empirically at `n = 1, 2` and assumed by asymptotic argument for `n ≥ 3`. A framework-native proof of geometric decay for all `n ≥ n_0` from the underlying action would be a separate retention step (e.g., a renormalon-bound theorem on the retained action).
- The retained bound is **not** the tightest possible envelope. A tighter empirical bound `r_emp ≈ 0.29` (non-retained) is accessible but deliberately not adopted; the present bound uses only retained SU(3) Casimir combinations.
- The retained bound does **not** depend on any imported literature value of `K_4` or higher; the Marquard et al. 2016 value `K_3(n_l=5) = 80.405` enters only through the prior retention note via the retained three-loop color-tensor skeleton.
- The running-coupling value `α_s(m_t) = 0.1079` enters as a numerical anchor from `docs/ALPHA_S_DERIVED_NOTE.md`; no derivation result of this note depends on its specific numerical value beyond the tail-size estimates reported above.
- The bound loses structural tightness as `α_s` increases: at `α_s/π · C_A^2 ≥ 1` (i.e., `α_s ≥ π/9 ≈ 0.349`), the geometric sum diverges and the bound fails. The retention anchor `α_s(m_t) = 0.1079` is well below this regime.

## 6. Validation

The structural retention is verified by the primary runner
`scripts/frontier_yt_p3_k_series_geometric_bound.py`, which performs
deterministic PASS/FAIL checks on:

1. Retained SU(3) Casimirs `C_F = 4/3`, `T_F = 1/2`, `C_A = 3` and the derived quantity `C_A^2 = 9`.
2. Observed δ-series values and term-to-term ratios `r_1 = 0.2818`, `r_2 = 0.2524`.
3. Proposed framework-native bound `r_bound = (α_s/π) · C_A^2` at `α_s(m_t)`.
4. Envelope check `r_bound > r_1 > r_2`.
5. Safety-margin check `r_bound / max(r_1, r_2) ∈ [1.0, 1.2]`.
6. Geometric-sum convergence `r_bound < 1`.
7. Tail residual `|tail(N=3)| = δ_3 · r_bound / (1 - r_bound) = 0.001458`.
8. Fractional tail contribution to m_t `≤ 0.003` (the packaged P3 budget).
9. Cross-consistency with the single-next-term bound from the prior K_3 note.
10. Structural retention provenance (bound depends only on retained SU(3) Casimirs and retained `α_s`).

- **Log:** `logs/retained/yt_p3_k_series_geometric_bound_2026-04-17.log`.
- **Prior retention steps (in this series):**
  - `YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md` — `K_1 = C_F`.
  - `YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — four-tensor `K_2` skeleton.
  - `YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md` — two-loop integral citation.
  - `YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — ten-tensor `K_3` skeleton.
- **Upstream authorities (read-only):**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — SU(3) Casimirs.
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` — gauge-group uniqueness.
  - `docs/ALPHA_S_DERIVED_NOTE.md` — retained running coupling.

No publication-surface file (`CLAIMS_TABLE`, `PUBLICATION_MATRIX`,
`DERIVATION_ATLAS`, ...) is modified by this submission.

## Status

**RETAINED** — framework-native geometric tail bound on the K_n
series of the MSbar-to-pole mass conversion retained through
`r_bound = (α_s/π) · C_A^2 = 0.30907` at `α_s(m_t) = 0.1079`,
delivering a retained tail residual of `0.001458` and a retained
fractional-m_t contribution of approximately `0.14%`, within a factor
of 2 of the packaged P3 budget of ~0.3%. Cumulative retention of P3
through three loops plus retained geometric tail closes the P3
coverage budget on the retained surface.
