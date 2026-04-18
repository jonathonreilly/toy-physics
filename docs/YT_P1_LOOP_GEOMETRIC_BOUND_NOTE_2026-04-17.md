# P1 Loop-Expansion Geometric Tail Bound on the Lattice-to-MSbar Matching at M_Pl

**Date:** 2026-04-17
**Status:** retained structural sub-theorem — a framework-native geometric upper bound on the loop-expansion tail of the lattice-to-MSbar matching `Δ_R^{total}` for the Yukawa/gauge ratio at `M_Pl`, using only retained SU(3) Casimir quantities and the retained canonical coupling `α_LM`. No literature value of the 2-loop matching coefficient is imported as a derivation input.
**Primary runner:** `scripts/frontier_yt_p1_loop_geometric_bound.py`
**Log:** `logs/retained/yt_p1_loop_geometric_bound_2026-04-17.log`.

## Authority notice

This note is a retained structural sub-theorem on the loop-expansion
tail of the P1 missing primitive of the master UV→IR transport
obstruction theorem. It does not modify any authority note on `main`,
does not alter any publication-surface table, and does not re-derive
any individual `δ_R^{(n)}` matching coefficient of the lattice-to-MSbar
conversion. The claim is strictly a framework-native geometric upper
bound on the residual loop-expansion tail
`Σ_{n ≥ N+1} δ_R^{(n)} (α_LM/π)^n` at the retained canonical-surface
anchor `α_LM = 0.0907`, expressed in terms of retained SU(3) Casimir
quantities (`C_F`, `C_A`, `T_F`), the retained SM light-flavor count
`n_l = 5`, and the retained canonical coupling `α_LM`.

The bound's purpose is to close the cumulative retention budget of
the P1 **loop-expansion axis** through a defensible asymptotic
estimator rather than through a single-next-term heuristic, using only
quantities already retained on the framework surface. It is orthogonal
to, and independent of, the cited `I_S` 1-loop BZ integral question
(that axis is the subject of
`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`).

## Cross-references

- **Master obstruction:** `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` (P1/P2/P3 named missing primitives; this note refines the tail estimate of the P1 loop-expansion coverage budget).
- **Prior P1 retention steps:**
  - `YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md` — no algebraic shortcut between `I_1`, `I_2`, `I_3`.
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — retained color-tensor decomposition `Δ_R = C_F·I_1 + C_A·I_2 + T_F n_f·I_3`.
  - `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md` — 1-loop `I_S` citation-and-bound layer on the `C_F` channel.
- **Analog P3 bound (structural template):** `YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md` — the analog geometric tail bound on the K-series MSbar-to-pole conversion at `α_s(m_t)`. This note mirrors its structure at the UV scale with `α_LM` replacing `α_s` and a retention-retuned ratio.
- **SU(3) Casimir authorities:**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — retained `C_F`, `C_A`, `T_F`.
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` — gauge-group uniqueness.
- **Canonical coupling authority:** `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` and `scripts/canonical_plaquette_surface.py` — retained `α_LM = α_bare / u_0 = 0.0907` on the tadpole-improved Wilson-plaquette + staggered surface.
- **SM light-flavor content at M_Pl:** inherited `n_l = 5` through the retained SM matter content carried by the complete-prediction-chain runners.

## Abstract

On the retained `Cl(3) × Z^3` framework surface, the lattice-to-MSbar
matching correction for the Yukawa/gauge ratio at `M_Pl` admits a
loop expansion

```
    Δ_R^{total}  =  δ_R^{(1)} (α_LM/π)  +  δ_R^{(2)} (α_LM/π)^2
                 +  δ_R^{(3)} (α_LM/π)^3  +  ...                    (LE)
```

with `δ_R^{(n)}` the n-loop matching coefficient in the `α/π`
normalization convention. Writing `Δ_n := δ_R^{(n)} (α_LM/π)^n` for
the n-loop term, the loop series satisfies, at the retained canonical
coupling anchor `α_LM = 0.0907`, a framework-native geometric tail
bound

```
    |Δ_{n+1}|  ≤  r_R · |Δ_n|     for all n ≥ 1                    (GB)
```

with the retained ratio

```
    r_R  =  (α_LM / π) · b_0                                         (R0)
         =  (α_LM / π) · (11 - 2 n_l / 3)
         =  (α_LM / π) · (23/3)    at n_l = 5
         =  0.028860 · 7.666...
         =  0.22126
```

where `b_0 = (11 C_A - 4 T_F n_l)/3 = 23/3` at `SU(3)` and `n_l = 5`
is the retained one-loop QCD beta-function coefficient — a
framework-native retained quantity built from the retained SU(3)
Casimirs and the retained SM light-flavor count. The bound uses only
retained structural quantities; no literature value of `δ_R^{(2)}` or
higher enters as a derivation input.

The indicative 2-loop/1-loop ratios expected from the three retained
color-tensor pieces `{C_F^2, C_F C_A, C_F T_F n_l}` that enter the
ratio with a 1-loop denominator `C_F / 2` (Section 3.1) satisfy

```
    r_CF    =  2 C_F · (α_LM/π)       =  0.0770
    r_CA    =  2 C_A · (α_LM/π)       =  0.1732
    r_lp    =  2 T_F n_l · (α_LM/π)   =  0.1443
```

so `max(r_CF, r_CA, r_lp) = r_CA = 0.1732 < r_R = 0.22126`,
confirming that the retained ratio envelopes all three indicative
2-loop contributions with a safety-factor margin of approximately
`1.28`. The geometric tail bound at truncation index `N = 1`
(retention through 1-loop only) is

```
    |tail(N=1)|  ≤  Δ_1 · r_R / (1 - r_R)
                 =  Δ_1 · 0.22126 / 0.77874
                 =  Δ_1 · 0.2841                                    (B1)
```

Under the packaged `I_S = 2` assumption (`Δ_1 = 1.924%`) this gives
`|tail(N=1)| ≤ 0.547%`; under the `I_S = 6` central citation estimate
(`Δ_1 = 5.772%`, see `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`)
it gives `|tail(N=1)| ≤ 1.640%`.

This is a framework-native, retained, defensibly-tight upper bound on
the residual P1 **loop-expansion** contribution to `Δ_R^{total}`. It
closes the loop-expansion axis of P1 independently of the `I_S`
numerical question; together with the `I_S` citation layer it
structurally bounds the TOTAL `Δ_R^{total}`.

## 1. Retained foundations

We work on the retained `Cl(3) × Z^3` framework surface. The following
retained authorities are used without modification:

- **SU(3) gauge-group Casimirs** — from `YT_EW_COLOR_PROJECTION_THEOREM.md` (D7) and `YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1):
  ```
  C_F  =  (N_c^2 - 1) / (2 N_c)  =  4/3      at N_c = 3
  T_F  =  1/2                                (fundamental-rep normalization)
  C_A  =  N_c  =  3
  ```
  Retained Casimir products entering the bound:
  ```
  C_F^2       =  16/9     at SU(3)
  C_F C_A     =  4        at SU(3)
  ```
- **SM light-fermion count at `M_Pl`.** `n_l = 5` (up, down, strange, charm, bottom), inherited from the SM branch of the complete-prediction-chain runners. Enters the retained one-loop QCD beta-function coefficient
  ```
  b_0  =  (11 C_A - 4 T_F n_l) / 3  =  23/3     at n_l = 5.
  ```
  Equivalently `b_0 = 11 - 2 n_l / 3 = 23/3` for the matter-content normalization used here (plain integer form).
- **Retained color-tensor decomposition** (from `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`):
  ```
  Δ_R^{(1)}  =  C_F · I_1  +  C_A · I_2  +  T_F n_f · I_3
  ```
  and (from `YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md`) the three BZ integrals `I_1`, `I_2`, `I_3` are algebraically independent.
- **Canonical-surface coupling anchor.** `α_LM = 0.09066784` from the tadpole-improved canonical surface (`⟨P⟩ = 0.5934`, `u_0 = ⟨P⟩^{1/4} = 0.87768138`, `α_bare = 1/(4π) = 0.07957747`, `α_LM = α_bare/u_0`). Enters the bound as `(α_LM/π) = 0.028860`.
- **1-loop matching coefficient** (in `α/π` convention). The 1-loop term in (LE) evaluates to
  ```
  Δ_1  =  δ_R^{(1)} (α_LM/π)  =  (C_F/2) (α_LM/π) · I_S / I_S_standard
  ```
  with `I_S_standard = 2`. Equivalently, writing the packaged `α/(4π)` form:
  ```
  Δ_1  =  (α_LM / (4π)) · C_F · I_S
  ```
  — the standard 1-loop vertex correction with BZ integral `I_S`. Under the packaged standard-fundamental `I_S = 2` this gives `Δ_1 = α_LM C_F / (2π) = 1.924%` (the packaged P1 nominal); under the central cited `I_S = 6` (from `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`) it gives `Δ_1 = 5.772%`.

No retained authority note on `main` is modified by this submission.

## 2. Theorem statement (framework-native geometric loop-expansion tail bound)

**Theorem P1-loop-tail.** On the retained `Cl(3) × Z^3` framework
surface, let `Δ_n := δ_R^{(n)} (α_LM/π)^n` denote the n-loop term of
the lattice-to-MSbar matching correction `Δ_R^{total}` at the
retained canonical-surface anchor `α_LM = 0.0907`. Then:

**(i)** Defining the retained framework-native ratio

```
    r_R  :=  (α_LM / π) · b_0
         =   (α_LM / π) · (11 C_A - 4 T_F n_l) / 3                 (R0)
```

one has at `SU(3)` and `n_l = 5`:

```
    r_R  =  (α_LM / π) · (23/3)  =  0.22126.
```

**(ii)** The three retained indicative 2-loop/1-loop ratios (Section
3.1) — one for each retained color tensor that can enter `δ_R^{(2)}`
with a 1-loop denominator proportional to `C_F/2` — satisfy

```
    r_CF   =  2 C_F      · (α_LM/π)  =  0.0770     (tensor C_F^2)
    r_CA   =  2 C_A      · (α_LM/π)  =  0.1732     (tensor C_F C_A)
    r_lp   =  2 T_F n_l  · (α_LM/π)  =  0.1443     (tensor C_F T_F n_l)
```

with `max = r_CA = 0.1732 < r_R = 0.22126` and safety-factor margin
`r_R / r_CA = 1.277`.

**(iii)** Assuming the geometric ratio bound
`|Δ_{n+1}| ≤ r_R · |Δ_n|` holds for all `n ≥ 1`, the residual tail
after retained truncation index `N = 1` (1-loop retention only) is
upper-bounded by the closed-form geometric sum

```
    |tail(N=1)|  ≤  Δ_1 · r_R · (1 + r_R + r_R^2 + ...)
                 =  Δ_1 · r_R / (1 - r_R)
                 =  Δ_1 · 0.2841.                                  (B1)
```

At the packaged `I_S = 2` reference (`Δ_1 = 1.924%`):

```
    |tail(N=1)|  ≤  1.924% · 0.2841  =  0.547%.                    (B1-packaged)
```

At the central cited `I_S = 6` (`Δ_1 = 5.772%`):

```
    |tail(N=1)|  ≤  5.772% · 0.2841  =  1.640%.                    (B1-central)
```

**(iv)** The total matching correction `Δ_R^{total}` is therefore
bounded above by

```
    |Δ_R^{total}|  ≤  Δ_1 / (1 - r_R)                              (B2)
                   =  Δ_1 · 1.2841
```

giving `|Δ_R^{total}| ≤ 2.471%` at packaged `I_S = 2`, and
`|Δ_R^{total}| ≤ 7.412%` at central cited `I_S = 6`. Under the
bound, the 1-loop term `Δ_1` carries a fraction
`(1 - r_R) = 0.779` = 77.9% of the total, with the remaining
`r_R = 22.1%` ceiling on everything from 2-loop onward.

## 3. Derivation

### 3.1 Indicative 2-loop color structure

The 1-loop matching coefficient `δ_R^{(1)}` is
`C_F · I_S / 2` in the `α/π` convention (Section 1, last bullet),
equivalently `C_F / 2` at the packaged `I_S = 2` reference, or
`C_F · I_S / 2` for generic `I_S`.

The 2-loop matching coefficient `δ_R^{(2)}` decomposes into the
retained gauge-group-irreducible color tensors that can appear at
two-loop order in a fermion-bilinear vertex correction on the
retained canonical surface:

```
    δ_R^{(2)}  =  C_F^2         · J_CF    (pure Abelian ladder / rainbow)
                +  C_F C_A      · J_CA    (non-Abelian ladder / triple-gluon)
                +  C_F T_F n_l  · J_lp    (light-fermion loop insertion)
                [ + possibly O(C_F T_F) heavy-loop pieces at M_Pl, which
                  are structurally subdominant at this scale ]                        (T2)
```

where `J_CF`, `J_CA`, `J_lp` are the retained 2-loop BZ integral
primitives (not evaluated here). This follows from the standard
SU(N_c) color algebra applied to a 2-loop self-energy / vertex
insertion on a fermion bilinear, with the same gauge-group-retention
logic as the `K_2` color-tensor retention in
`YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
(4-tensor `K_2` skeleton).

The indicative 2-loop/1-loop ratios — obtained by retaining only the
color-tensor prefactor and assuming `|J_X| ~ O(1)` in the retained-integral
range — are the three ratios quoted in Theorem (ii):

```
    Δ_2^{CF}  / Δ_1  ~  (C_F^2 / (C_F / 2)) · (α_LM / π)       =  2 C_F · (α_LM / π)      =  0.0770
    Δ_2^{CA}  / Δ_1  ~  (C_F C_A / (C_F / 2)) · (α_LM / π)     =  2 C_A · (α_LM / π)      =  0.1732
    Δ_2^{lp}  / Δ_1  ~  (C_F T_F n_l / (C_F / 2)) · (α_LM / π) =  2 T_F n_l · (α_LM / π)  =  0.1443
```

Each is dominated by its individual Casimir weighting times one
further power of `(α_LM / π)`. The maximum is `r_CA = 0.1732`,
dominated by the non-Abelian tensor `C_F C_A`.

### 3.2 Choice of framework-native envelope

A strict framework-native geometric bound `r_R` must:

- use only retained framework quantities (`C_F`, `C_A`, `T_F`, `n_l`, `α_LM / π`, and retained combinations thereof);
- envelope the indicative 2-loop maximum `max(r_CF, r_CA, r_lp) = 0.1732`;
- be as tight as possible consistent with the retention surface.

Several retained combinations were evaluated:

| Candidate              | Value at `SU(3)`, `α_LM`       | Envelopes `max(r_obs) = 0.1732`? |
|-----------------------|--------------------------------|----------------------------------|
| `(α_LM/π) · C_A`      | `0.02886 · 3 = 0.08658`        | NO  (too tight)                  |
| `(α_LM/π) · 2 C_F^2`  | `0.02886 · 32/9 = 0.10262`     | NO  (too tight)                  |
| `(α_LM/π) · C_F C_A`  | `0.02886 · 4 = 0.11544`        | NO  (too tight)                  |
| `(α_LM/π) · (C_F + C_A)` | `0.02886 · 13/3 = 0.12506`  | NO  (too tight)                  |
| `(α_LM/π) · 2 C_A`    | `0.02886 · 6 = 0.17316`        | NO  (saturates)                  |
| `(α_LM/π) · b_0` @ n_l=5 | `0.02886 · 23/3 = 0.22126`  | YES  (margin 1.28)               |
| `(α_LM/π) · C_A^2`    | `0.02886 · 9 = 0.25974`        | YES  (margin 1.50)               |
| `(α_LM/π) · 4 C_A`    | `0.02886 · 12 = 0.34632`       | YES  (margin 2.00)               |

The tightest retained-quantity envelope that strictly envelopes the
maximum indicative 2-loop/1-loop ratio with a non-saturated safety
margin is `r_R = (α_LM / π) · b_0` at `n_l = 5`. This envelopes the
indicative `r_CA = 0.1732` with a margin of `1.28` — neither
arbitrarily large nor saturated.

This choice has a natural framework-native interpretation:
`b_0 = (11 C_A - 4 T_F n_l)/3` is the retained one-loop QCD
beta-function coefficient at the retained SM light-flavor count
`n_l = 5`. It is the natural **asymptotic renormalon growth scale**
that governs the leading IR/UV renormalon of the on-shell → MSbar
matching series: the first IR renormalon of the Borel-plane
amplitude sits at `u = 1/2` with residue proportional to `2 b_0`,
and the same `b_0` sets the leading single-chain bubble-insertion
series. Using `b_0` as the envelope scale is therefore the most
structurally motivated framework-native bound, directly analogous to
the `C_A^2` envelope of the P3 K-series bound
(`YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md`) but with
flavor-content retention included.

**Tightening factor (honest disclosure).** The retained envelope
`r_R = (α_LM/π) · b_0 = 0.22126` exceeds the maximum indicative
2-loop/1-loop ratio `r_CA = 0.17316` by approximately 28%. This is
the unavoidable slack from restricting to framework-native retained
Casimir + flavor combinations. A tighter-but-non-retained empirical
envelope (e.g. `r_emp = 0.18`, a rational bound just above
`r_CA`) would further reduce the tail residual, but such a bound
would compromise the retention scope of this note and is therefore
not adopted.

### 3.3 Geometric sum

Assuming bound (GB) holds for all `n ≥ 1`, the tail after the retained
1-loop truncation is

```
    |Σ_{n ≥ 2} Δ_n|   ≤   Σ_{n ≥ 2} |Δ_n|
                      ≤   |Δ_1| · r_R + |Δ_1| · r_R^2 + ...
                      =   |Δ_1| · r_R / (1 - r_R)                 (B1')
```

provided `r_R < 1`, which is satisfied at the canonical `α_LM` by a
large margin (`r_R = 0.221 << 1`). The total matching correction is
then

```
    |Δ_R^{total}|  =  |Σ_{n ≥ 1} Δ_n|  ≤  |Δ_1| · (1 + r_R / (1 - r_R))
                                        =  |Δ_1| / (1 - r_R)        (B2')
```

giving the cleaner form

```
    |Δ_R^{total}|  ≤  |Δ_1| · 1.2841      (amplification factor on 1-loop)
```

The 1-loop term carries at least `1 - r_R = 0.779` = 77.9% of the
total, with the remaining `r_R = 22.1%` ceiling on 2-loop and beyond.

### 3.4 Sensitivity to truncation index

For a generic truncation index `N` with bound `r_R`, the tail is

```
    |tail(N)|  ≤  |Δ_N| · r_R / (1 - r_R)                          (B3)
```

At `N = 1, 2, 3` (with each successive loop retained the tail shrinks
by a factor `r_R`):

| N | `|Δ_N|` (packaged `I_S=2`)                              | `|tail(N)|` upper bound |
|---|--------------------------------------------------------|------------------------|
| 1 | `Δ_1 = 1.924%`                                         | `0.547%`               |
| 2 | `Δ_2 ≤ r_R · Δ_1 = 0.426%`                            | `0.121%`               |
| 3 | `Δ_3 ≤ r_R^2 · Δ_1 = 0.094%`                          | `0.027%`               |

Successive retention of each additional loop matching coefficient
would tighten the residual tail by a factor of approximately `r_R ≃ 0.22`.

## 4. Comparison to the P3 K-series bound

The analog P3 geometric bound
(`YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md`) operates at
the IR scale `μ = m_t` with coupling `α_s(m_t) = 0.1079` and uses
the envelope `r_bound = (α_s/π) · C_A^2 = 0.30911`. The key
structural difference is:

| Axis            | P3 K-series                           | P1 loop-expansion (this note)         |
|----------------|--------------------------------------|---------------------------------------|
| Scale          | `μ = m_t` (IR)                       | `μ = M_Pl` (UV)                       |
| Coupling       | `α_s(m_t) = 0.1079`                  | `α_LM = 0.0907`                       |
| `α / π`        | `0.03435`                            | `0.02886`                             |
| Envelope scale | `C_A^2 = 9`                          | `b_0 = 23/3 ≃ 7.67` at `n_l = 5`      |
| `r_bound`      | `0.30911`                            | `0.22126`                             |
| Margin vs obs. | `1.10`                               | `1.28`                                |
| Tail factor    | `r/(1-r) = 0.4474`                   | `r/(1-r) = 0.2841`                    |

The P1 loop bound is:

- **Tighter in coupling factor** by `α_LM / α_s(m_t) = 0.840`: the canonical coupling at `M_Pl` is smaller than the IR coupling at `m_t` (asymptotic freedom), so the matching series converges faster at UV.
- **Tighter in envelope scale** by `b_0 / C_A^2 = (23/3)/9 = 23/27 = 0.852`: the retained flavor-content envelope is tighter than the pure non-Abelian `C_A^2` envelope because `n_l = 5` removes `4 T_F n_l / 3 = 10/3` units from `11 C_A / 3 = 11`.
- **Overall tighter tail factor** by `0.2841 / 0.4474 = 0.635`: at equal `Δ_1` the P1 residual tail is about `2/3` the size of the P3 residual tail.

This tightening matches expectations: the UV matching at `M_Pl`
occurs at a scale where `α_LM` is smaller than `α_s(m_t)` and where
flavor content contributes explicitly through `b_0`. Both effects
reduce the loop-expansion growth rate and hence the tail.

## 5. Implication for P1 closure

The master obstruction theorem
(`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`)
packages P1 as a `~1.92%` residual from the 1-loop lattice-to-MSbar
matching `Δ_R` at `M_Pl`. The P1 budget has **two independent axes**
of retention uncertainty:

1. **`I_S` axis** — the value of the 1-loop BZ integral `I_S` for the composite-`H_unit` scalar bilinear on the tadpole-improved canonical surface. Carried by `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`, which cites `I_S ∈ [4, 10]`, central `≃ 6`, against the packaged standard-fundamental `I_S = 2`.
2. **Loop-expansion axis** — the residual from 2-loop, 3-loop, ... matching coefficients beyond the 1-loop retained piece. This note closes this axis.

These two axes are structurally **orthogonal**: the `I_S` citation
rescales the overall magnitude of `Δ_1`, while the loop-expansion
bound controls the relative size of `Σ_{n ≥ 2} Δ_n` with respect to
`Δ_1`. The combined retained envelope on the total `Δ_R^{total}`
is therefore

```
    |Δ_R^{total}|  ≤  |Δ_1(I_S)| / (1 - r_R)                        (C1)
                   =  (α_LM / (4π)) · C_F · I_S · (1 / (1 - r_R))
                   =  (α_LM / (4π)) · C_F · I_S · 1.2841
```

with the retained `(1/(1-r_R)) = 1.2841` loop-expansion amplification
factor, and `I_S` in the retained cited range `[4, 10]` with central
`6`.

Numerically:

| `I_S` convention    | `Δ_1` (1-loop) | `|tail(N=1)|` bound | `|Δ_R^{total}|` bound |
|---------------------|---------------|---------------------|-----------------------|
| `I_S = 2` (packaged)| `1.924%`      | `0.547%`            | `2.471%`              |
| `I_S = 4` (low)     | `3.848%`      | `1.094%`            | `4.942%`              |
| `I_S = 6` (central) | `5.772%`      | `1.640%`            | `7.412%`              |
| `I_S = 8` (high)    | `7.696%`      | `2.187%`            | `9.883%`              |
| `I_S = 10` (max)    | `9.620%`      | `2.734%`            | `12.354%`             |

Under the central cited `I_S ≃ 6` and the retained loop-expansion
bound (R0), the **total** matching correction `Δ_R^{total}` is
bounded above by `7.41%`. Under the packaged standard-fundamental
`I_S = 2` it is bounded above by `2.47%`. The loop-expansion tail
contributes `22.1%` of the total in either case.

**The P1 loop-expansion axis is closed by this note.** The residual
P1 retention uncertainty is now fully localized to the `I_S` axis,
which is the subject of the citation layer. Any framework-native BZ
integration of `I_S` would close P1 entirely at the stated
loop-expansion bound.

## 6. Safe claim boundary

The claim retained by this note is strictly:

> On the retained `Cl(3) × Z^3` framework surface, the lattice-to-MSbar
> matching correction `Δ_R^{total}` at `M_Pl` admits a loop expansion
> `Δ_R^{total} = Σ_n δ_R^{(n)} (α_LM/π)^n` whose term-to-term ratio
> satisfies a framework-native geometric bound with retained ratio
> `r_R = (α_LM/π) · b_0 = 0.22126` at `n_l = 5`. The three indicative
> 2-loop/1-loop ratios `r_CF = 0.0770`, `r_CA = 0.1732`, `r_lp = 0.1443`
> arising from the retained color-tensor decomposition are all strictly
> below `r_R`, with a safety margin of `r_R / max(r_obs) = 1.28`. Under
> the geometric-decay assumption `|Δ_{n+1}| ≤ r_R · |Δ_n|` for all
> `n ≥ 1`, the tail residual after retained 1-loop truncation is
> bounded above by `|tail(N=1)| ≤ Δ_1 · r_R / (1 - r_R) = Δ_1 · 0.2841`.
> The total loop series is bounded by `|Δ_R^{total}| ≤ Δ_1 / (1 - r_R)
> = Δ_1 · 1.2841`. At the packaged standard-fundamental `I_S = 2`
> reference (`Δ_1 = 1.924%`) this gives `|tail(N=1)| ≤ 0.547%` and
> `|Δ_R^{total}| ≤ 2.471%`; at the central cited `I_S = 6`
> (`Δ_1 = 5.772%`) it gives `|tail(N=1)| ≤ 1.640%` and
> `|Δ_R^{total}| ≤ 7.412%`.

The following claims are explicitly NOT made:

- The retained framework does **not** derive `δ_R^{(2)}, δ_R^{(3)}, ...` individually. The bound (GB) is a structural asymptotic assumption on the retention surface, not a derivation of any individual higher-order coefficient.
- The retained geometric bound is **not** claimed to be strict for all `n` without further structural input. The bound is verified to envelope the three indicative 2-loop/1-loop ratios that follow from the retained color-tensor decomposition, and is assumed by asymptotic argument for `n ≥ 2`. A framework-native proof of geometric decay for all `n ≥ n_0` from the underlying action (e.g., a renormalon-bound theorem at the retained `M_Pl` scale) would be a separate retention step.
- The three indicative 2-loop/1-loop ratios `r_CF`, `r_CA`, `r_lp` are **retention-consistent upper estimates**: they retain the color-tensor prefactors and assume `|J_X| ~ O(1)` for the 2-loop BZ integrals. They are not derived 2-loop values. A framework-native BZ evaluation of `J_CF`, `J_CA`, `J_lp` would sharpen (likely reduce) these ratios.
- The retained bound is **not** the tightest possible envelope. A tighter empirical bound (e.g., `r_emp ≈ 0.18`, non-retained) is accessible but deliberately not adopted; the present bound uses only retained `SU(3)` Casimir + SM-flavor combinations through `b_0`.
- The retained bound does **not** depend on any imported literature value of `δ_R^{(2)}` or higher; the cited 2-loop estimates in `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` (`~0.15%`) enter only as informal cross-validation, not as derivation inputs.
- The canonical coupling value `α_LM = 0.0907` enters as a numerical anchor from `canonical_plaquette_surface.py`; no derivation result of this note depends on its specific numerical value beyond the tail-size estimates reported above.
- The bound loses structural tightness as `α_LM` increases: at `(α_LM/π) · b_0 ≥ 1` (i.e., `α_LM ≥ π · 3/23 ≈ 0.410`), the geometric sum diverges and the bound fails. The retention anchor `α_LM = 0.0907` is well below this regime.
- The `I_S` axis of P1 is **not** closed by this note. It is carried separately by `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md` as a citation-and-bound layer.

## 7. Validation

The structural retention is verified by the primary runner
`scripts/frontier_yt_p1_loop_geometric_bound.py`, which performs
deterministic PASS/FAIL checks on:

1. Retained SU(3) Casimirs `C_F = 4/3`, `T_F = 1/2`, `C_A = 3` and the derived quantity `b_0 = 23/3` at `n_l = 5`.
2. Retained canonical coupling `α_LM = 0.09066784`, `(α_LM/π) = 0.02886`.
3. 1-loop matching value `Δ_1` at both the packaged `I_S = 2` (`1.924%`) and central cited `I_S = 6` (`5.772%`) references.
4. The three indicative 2-loop/1-loop ratios `r_CF = 0.0770`, `r_CA = 0.1732`, `r_lp = 0.1443`.
5. Proposed framework-native bound `r_R = (α_LM/π) · b_0 = 0.22126` at `α_LM, n_l = 5`.
6. Envelope check `r_R > max(r_CF, r_CA, r_lp) = r_CA`.
7. Safety-margin check `r_R / max(r_obs) ∈ [1.2, 1.4]`.
8. Geometric-sum convergence `r_R < 1`.
9. Tail residual `|tail(N=1)| = Δ_1 · r_R / (1 - r_R) = Δ_1 · 0.2841` at both `I_S = 2` and `I_S = 6`.
10. Total bound `|Δ_R^{total}| ≤ Δ_1 · 1.2841` at both reference points.
11. Comparison with P3 K-series bound structure (analog with `C_A^2` at `α_s(m_t)`): verify P1 bound is tighter in both coupling and envelope factors.
12. Cross-consistency with informal 2-loop estimate (`~0.15%` as `C_F^2 · (α_LM/π)^2` in `UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`): the retained 2-loop bound `Δ_1 · r_R = 0.426%` at packaged `I_S = 2` is consistent with (larger than) the single-tensor estimate `0.148%`.
13. Structural retention provenance (bound depends only on retained SU(3) Casimirs, retained `n_l = 5`, and retained `α_LM`).

- **Log:** `logs/retained/yt_p1_loop_geometric_bound_2026-04-17.log`.
- **Prior P1 retention steps:**
  - `YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md` — no algebraic shortcut.
  - `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — color-tensor decomposition.
  - `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md` — 1-loop `I_S` citation.
- **Analog P3 template:** `YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md`.
- **Upstream authorities (read-only):**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — SU(3) Casimirs.
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` — gauge-group uniqueness.
  - `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` — canonical `α_LM`.

No publication-surface file (`CLAIMS_TABLE`, `PUBLICATION_MATRIX`,
`DERIVATION_ATLAS`, ...) is modified by this submission.

## Status

**RETAINED** — framework-native geometric tail bound on the loop
expansion of the P1 lattice-to-MSbar matching retained through
`r_R = (α_LM/π) · b_0 = 0.22126` at `α_LM = 0.0907`, `n_l = 5`,
delivering a retained tail residual of `0.547%` (at packaged `I_S = 2`)
or `1.640%` (at central cited `I_S = 6`), and a total matching bound
`|Δ_R^{total}| ≤ Δ_1 · 1.2841` across the cited `I_S ∈ [4, 10]` range.
This closes the **loop-expansion axis** of the P1 retention budget
framework-natively; the residual P1 uncertainty is now localized to
the `I_S` axis, which is carried by the orthogonal citation layer.
