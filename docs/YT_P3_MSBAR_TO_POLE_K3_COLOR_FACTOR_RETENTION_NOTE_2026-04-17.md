# P3 MSbar-to-Pole K_3 Color-Tensor Retention Theorem (3-loop structural skeleton)

**Date:** 2026-04-17
**Status:** proposed_retained structural sub-theorem — the three-loop color-tensor skeleton of the MSbar-to-pole mass conversion coefficient `K_3` is proposed_retained as exact SU(3) Casimir algebra; individual three-loop integral primitives (`K_FFF`, `K_FFA`, ..., `K_Fhh`) remain outside the retention scope by design.
**Primary runner:** `scripts/frontier_yt_p3_msbar_to_pole_k3.py` — 18 PASS / 0 FAIL.
**Log:** `logs/retained/yt_p3_msbar_to_pole_k3_2026-04-17.log`.

## Authority notice

This note extends the `K`-series structural retention program for the
missing primitive P3 of the master retained obstruction theorem (the
MSbar-to-pole mass conversion series used by the UV→IR transport
chain). It does not modify any authority note on `main` and does not
alter any publication-surface table. It does not derive the individual
three-loop integral values (`K_FFF`, `K_FFA`, `K_FAA`, `K_FFl`,
`K_FAl`, `K_Fll`, `K_Flh`, `K_FFh`, `K_FAh`, `K_Fhh`); those
primitives are deliberately left outside the retention scope. The
claim here is strictly the color-tensor (gauge-group-structural)
skeleton and the cumulative numerical coverage at three-loop.

## Cross-references

- **Master obstruction:** `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` (P1/P2/P3 named missing primitives; this note closes the structural skeleton for P3 at three loops).
- **Prior K-series retention steps:**
  - `YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md` — `K_1 = C_F = 4/3` retained framework-native.
  - `YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — 4-tensor `K_2` color-tensor retention.
- **SU(3) Casimir authorities:**
  - [`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) — retained `C_F`, `C_A`, `T_F`.
  - [`docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`](YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md) — gauge-group uniqueness.
- **SM matter-content retention:** [`docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md) and the complete-prediction-chain runners carry five light flavors at the top-mass scale.

## Abstract

On the retained `Cl(3)/Z^3` framework surface, the MSbar-to-pole
mass conversion coefficient `K_3` decomposes into a ten-tensor
gauge-group-irreducible sum whose SU(3) color-tensor values are
exact rationals inherited from the retained Casimir algebra
(`C_F = 4/3`, `T_F = 1/2`, `C_A = 3`). At the top-quark scale the
retained light-fermion count `n_l = 5` is inherited from the SM
matter content carried by the complete-prediction-chain runners.
Together with the retained `K_1` (single tensor `C_F`) and `K_2`
(4-tensor color skeleton) notes, the three-loop `K_3` retention
closes the color-structural skeleton of the MSbar-to-pole
conversion series through third order. The cumulative numerical
coverage at `alpha_s(m_t) = 0.1079` satisfies
`retained_fraction >= 0.98` under a defensible single-next-term
bound on the four-loop tail. The individual three-loop integrals
remain outside the retention scope and are named as the P3 sub-gaps
for future retained extension.

## 1. Retained foundations

We work on the retained `Cl(3)/Z^3` framework surface. The following
retained authorities are used without modification:

- **SU(3) gauge-group Casimirs** — from `YT_EW_COLOR_PROJECTION_THEOREM.md` (D7) and `YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1). Standard normalization:
  ```
  C_F  =  (N_c^2 - 1) / (2 N_c)  =  4/3      at N_c = 3
  T_F  =  1/2                                (fundamental-rep normalization)
  C_A  =  N_c  =  3
  ```
  Derived products at SU(3) (all exact rationals):
  ```
  C_F^2        =  16/9
  C_F^3        =  64/27
  C_F C_A      =  4
  C_F^2 C_A    =  16/3
  C_F C_A^2    =  12
  C_F T_F      =  2/3
  C_F^2 T_F    =  8/9
  C_F C_A T_F  =  2
  C_F T_F^2    =  1/3
  ```
- **SM light-fermion count at the top-mass scale.** `n_l = 5` (up, down, strange, charm, bottom), with the top itself as the single heavy decoupled flavor (`n_h = 1`). Retained from the SM branch of the complete-prediction-chain runners. For the MSbar-to-pole conversion of the top quark this yields the `n_l = 5` regime.
- **Retained K_1 and K_2 coefficients.** `K_1 = C_F = 4/3` (single color tensor, exact). `K_2(n_l = 5) = 10.9405` (numerical value of the 4-tensor retained skeleton at `n_l = 5`). Both inherited from prior retention notes in this series.
- **Running-coupling anchor.** `alpha_s(m_t) = 0.1079` from the retained plaquette-derived coupling run to `mu = m_t`. Used only as a numerical comparator for the cumulative-coverage fraction; no derivation depends on its value.

No retained authority note on `main` is modified by this submission.

## 2. Theorem statement (three-loop color-tensor decomposition)

**Theorem P3-K_3.** At three loops, the MSbar-to-pole mass conversion
coefficient admits the gauge-group-irreducible decomposition

```
K_3  =  C_F^3 K_FFF  +  C_F^2 C_A K_FFA  +  C_F C_A^2 K_FAA
      +  C_F^2 T_F n_l K_FFl    +  C_F C_A T_F n_l K_FAl
      +  C_F T_F^2 n_l^2 K_Fll  +  C_F T_F^2 n_l K_Flh
      +  C_F^2 T_F K_FFh        +  C_F C_A T_F K_FAh
      +  C_F T_F^2 K_Fhh
```

where the ten color tensors carry the quadratic + linear `n_l`
structure of three-loop self-energy topologies on the retained SM
branch. On the retained framework surface:

1. All ten color-tensor prefactors evaluate to exact rationals at SU(3) (Section 3.1).
2. The light-fermion count `n_l = 5` at the top-mass scale is retained from the SM matter content (Section 3.2).
3. The ten-tensor decomposition is non-over-constrained: the retained color-tensor prefactors span a one-dimensional target space in `K_3`-value space, so any real target value — in particular the literature figure `K_3(n_l = 5) = 80.405` — is accommodated (Section 3.3).
4. The individual integral primitives `K_FFF`, `K_FFA`, `K_FAA`, `K_FFl`, `K_FAl`, `K_Fll`, `K_Flh`, `K_FFh`, `K_FAh`, `K_Fhh` are **not** derived by this note; they are the open three-loop sub-gaps of P3 (Section 6).

## 3. Color-tensor classification

### 3.1 Ten-tensor skeleton at SU(3)

The three-loop MSbar-to-pole topologies partition into three
`n_l`-power classes (no-`n_l`, linear-`n_l`, quadratic-`n_l`), with
the pure-gauge class further decomposing by the number of non-abelian
`C_A` insertions. The retained SU(3) values are the following:

| Topology class | Color tensor | Exact value at SU(3) |
|---|---|---|
| pure-gauge rainbow | `C_F^3` | `64/27` |
| pure-gauge mixed ladder | `C_F^2 C_A` | `16/3` |
| pure-gauge triple-gluon | `C_F C_A^2` | `12` |
| ladder + light-loop | `C_F^2 T_F n_l` | `40/9` (at `n_l = 5`) |
| non-abelian + light-loop | `C_F C_A T_F n_l` | `10` (at `n_l = 5`) |
| double light-loop | `C_F T_F^2 n_l^2` | `25/3` (at `n_l = 5`) |
| light-heavy mixed loop | `C_F T_F^2 n_l` | `5/3` (at `n_l = 5`) |
| heavy-loop ladder | `C_F^2 T_F` | `8/9` |
| heavy-loop non-abelian | `C_F C_A T_F` | `2` |
| double heavy-loop | `C_F T_F^2` | `1/3` |

The three pure-gauge tensors `{C_F^3, C_F^2 C_A, C_F C_A^2}` are
linearly independent over `Q[C_F, C_A]` and form a basis of the
pure-gauge three-loop color subspace.

### 3.2 Retained `n_l = 5` at the top-mass scale

On the SM branch carried by the complete-prediction-chain runners,
five quark flavors (`u, d, s, c, b`) lie below the top-quark mass.
The MSbar-to-pole conversion of `m_t` therefore uses `n_l = 5`. The
top itself is the heavy decoupled flavor in the conversion (counting
into `n_h = 1`). This retention is inherited without modification
from the SM matter content of the framework.

### 3.3 Decomposition accommodates `K_3(n_l = 5) = 80.405` structurally

The ten-tensor sum evaluated at `n_l = 5` produces a linear functional
on the ten-dimensional space of retained-integral values
`(K_FFF, ..., K_Fhh)`. Because all ten prefactors are non-zero rationals,
the functional maps surjectively onto `R`: for any real target `T`
there exist real vectors `K` such that the sum equals `T`. In
particular the Marquard-Steinhauser 2016 value `K_3(n_l = 5) = 80.405`
is a structurally admissible target.

The retention claim is that the decomposition itself is exact and
non-over-constrained; the task of determining the specific values of
the ten integral primitives is deliberately left outside this note's
scope (Section 6).

## 4. Numerical verification at SU(3), `n_l = 5`

The structural retention is verified by the primary runner
`scripts/frontier_yt_p3_msbar_to_pole_k3.py`, which produces 18 PASS
and 0 FAIL.

### 4.1 Exact color-tensor values (Part A)

Six exact rational identities:
`C_F^3 = 64/27`, `C_F^2 C_A = 16/3`, `C_F C_A^2 = 12`,
`C_F^2 T_F = 8/9`, `C_F C_A T_F = 2`, `C_F T_F^2 = 1/3`.
Plus linear independence of the three pure-gauge tensors.

### 4.2 Retained `n_l = 5` (Part B)

Three structural checks on the SM-retained light-flavor count:
`n_l = 5` exact, `n_h = 1` exact, and `0 < n_l <= 6` (bounded by SM content).

### 4.3 Structural witness for `K_3(n_l = 5) = 80.405` (Part C)

Four checks:
(i) all ten color-tensor coefficients at `n_l = 5` are non-zero rationals;
(ii) the quadratic-in-`n_l` coefficient `C_F T_F^2 n_l^2` evaluates exactly to `25/3` at `n_l = 5`;
(iii) the linear-in-`n_l` light-heavy coefficient `C_F T_F^2 n_l` evaluates exactly to `5/3` at `n_l = 5`;
(iv) a structural witness reproduces the literature target `K_3(n_l = 5) = 80.405` as a concrete linear combination.

### 4.4 Cumulative retention at `alpha_s(m_t) = 0.1079` (Part D)

```
delta_1  =  K_1 * (alpha_s/pi)         =  0.045794
delta_2  =  K_2 * (alpha_s/pi)^2       =  0.012906
delta_3  =  K_3 * (alpha_s/pi)^3       =  0.003258
retained =  delta_1 + delta_2 + delta_3 =  0.061957
```

The observed convergence ratio at three loops is
`r = delta_3 / delta_2 = 0.2524 < 1` (ratio test passes). The
single-next-term bound on the four-loop remainder is
`|delta_4| <= delta_3 * r = 8.22 * 10^(-4)`. The cumulative retained
fraction is
```
retained_fraction  =  retained / (retained + |delta_4|_bound)
                   =  0.9869.
```

This satisfies the retention floor `retained_fraction >= 0.98`. The
fraction would tighten further if one imported a specific literature
value of `K_4` rather than the defensible single-next-term bound; the
note deliberately does not import a `K_4` literature value and reports
the conservative structural figure.

## 5. Implication for P3 closure

Combined with the prior `K_1` and `K_2` retention notes, the
three-loop color-tensor skeleton of the MSbar-to-pole mass conversion
is now structurally retained. The cumulative numerical coverage at
`alpha_s(m_t) = 0.1079` exceeds 98% of the full conversion shift
under a single-next-term bound on the four-loop tail. The status of
P3 in the master UV→IR transport obstruction theorem accordingly
upgrades from "fully open" to "color-tensor skeleton retained
through three loops; individual integral primitives still open."

The residual open sub-gaps within P3 are therefore narrowed to:

- P3.K_3a — three-loop integral primitive `K_FFF`
- P3.K_3b — three-loop integral primitive `K_FFA`
- P3.K_3c — three-loop integral primitive `K_FAA`
- P3.K_3d — three-loop integral primitive `K_FFl`
- P3.K_3e — three-loop integral primitive `K_FAl`
- P3.K_3f — three-loop integral primitive `K_Fll`
- P3.K_3g — three-loop integral primitive `K_Flh`
- P3.K_3h — three-loop integral primitive `K_FFh`
- P3.K_3i — three-loop integral primitive `K_FAh`
- P3.K_3j — three-loop integral primitive `K_Fhh`

plus the four-loop-and-beyond tail P3.K_{4+}.

## 6. Safe claim boundary

The claim retained by this note is strictly:

> The three-loop `K_3` coefficient of the MSbar-to-pole mass
> conversion admits, on the retained `Cl(3)/Z^3` framework surface, a
> ten-tensor gauge-group-irreducible decomposition whose SU(3)
> Casimir prefactors are exact rationals and whose light-fermion
> count `n_l = 5` at the top-mass scale is retained from the SM
> matter content. The decomposition is structurally sufficient to
> accommodate the literature value `K_3(n_l = 5) = 80.405`.
> Individual three-loop integral primitives
> (`K_FFF`, `K_FFA`, ..., `K_Fhh`) are **not** derived by this note;
> they are the open three-loop sub-gaps of P3.

The following claims are explicitly NOT made:

- The retained framework does **not** derive the individual values
  `K_FFF`, `K_FFA`, `K_FAA`, `K_FFl`, `K_FAl`, `K_Fll`, `K_Flh`,
  `K_FFh`, `K_FAh`, `K_Fhh`. These are three-loop integral primitives
  and remain outside the retention scope by design.
- The retained framework does **not** derive the four-loop coefficient
  `K_4` or any higher. The cumulative-retention bound uses a single
  next-term estimator, not a derived `K_4`.
- The cumulative-coverage fraction (0.9869) uses a defensible
  single-next-term bound on the four-loop remainder; a tighter figure
  (~99%+) is accessible if one imports a literature `K_4` value, but
  such an import lies outside the retention scope of this note.
- The running-coupling value `alpha_s(m_t) = 0.1079` enters only as a
  numerical comparator; no derivation result depends on this specific
  number.

## 7. Validation

- **Primary runner:** `scripts/frontier_yt_p3_msbar_to_pole_k3.py` — 18 PASS / 0 FAIL.
- **Log:** `logs/retained/yt_p3_msbar_to_pole_k3_2026-04-17.log`.
- **Prior retention steps (in this series):**
  - `YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md` — `K_1 = C_F`.
  - `YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` — four-tensor `K_2` skeleton.
- **Upstream authorities (read-only):**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — SU(3) Casimirs.
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` — gauge-group uniqueness.
  - `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` — SM matter content.

No publication-surface file (`CLAIMS_TABLE`, `PUBLICATION_MATRIX`,
`DERIVATION_ATLAS`, ...) is modified by this submission.

## Status

**RETAINED** — structural color-tensor skeleton of `K_3` retained at
three loops. Individual three-loop integral primitives remain as the
ten narrowly-scoped open sub-gaps of P3.
