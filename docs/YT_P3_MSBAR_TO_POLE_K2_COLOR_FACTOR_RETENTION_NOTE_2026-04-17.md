# P3 MSbar-to-Pole K_2 Color-Tensor Retention Theorem (2-loop structural skeleton)

**Date:** 2026-04-17
**Status:** retained structural sub-theorem — the two-loop color-tensor
skeleton of the MSbar-to-pole mass conversion coefficient `K_2` is
retained as exact SU(3) Casimir algebra; the four 2-loop integral
primitives (`J_FF`, `J_FA`, `J_Fl`, `J_Fh`) remain outside the
retention scope and are cited from the QCD on-shell mass-conversion
literature.
**Primary runner:** `scripts/frontier_yt_p3_msbar_to_pole_k2.py`.
**Log:** `logs/retained/yt_p3_msbar_to_pole_k2_2026-04-17.log`.

## Authority notice

This note extends the `K`-series structural retention program for the
P3 primitive of the master UV-to-IR transport obstruction theorem (the
MSbar-to-pole mass conversion series used for the top-quark pole mass).
It records the two-loop color-tensor decomposition of K_2 into four
gauge-group-irreducible channels and retains the four color-tensor
prefactors as exact rationals inherited from the retained SU(3) Casimir
authority. The four 2-loop integral primitives
(`J_FF`, `J_FA`, `J_Fl`, `J_Fh`) are named but deliberately left
outside the retention scope; they are cited from the QCD on-shell
mass-conversion literature (Gray-Broadhurst-Grafe-Schilcher 1990;
Marquard-Steinhauser 2016).

This note does NOT modify:

- the master obstruction theorem
  (`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`);
- any SU(3) Casimir authority;
- the K_1 framework-native retention
  (`docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`);
- any publication-surface file.

## Cross-references

- **Master obstruction:**
  `docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` —
  names the MSbar-to-pole series as a P3 sub-primitive; this note
  closes the structural color-tensor skeleton for K_2.
- **Prior K-series retention step:**
  `docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`
  — `K_1 = C_F = 4/3` retained framework-native.
- **Next K-series retention step:**
  `docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  — 10-tensor K_3 color-tensor retention.
- **K_2 2-loop integral citation:**
  `docs/YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md`
  — documents the cited values of `J_FF`, `J_FA`, `J_Fl`, `J_Fh`
  against the published K_2(n_l=5) = 10.9405 target.
- **SU(3) Casimir authorities:**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` (D7 — retained `C_F`,
    `C_A`, `T_F`).
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1 —
    gauge-group uniqueness).
- **SM matter content:**
  `docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` —
  carries `n_l = 5` at the top-mass scale.

## Abstract

On the retained `Cl(3)/Z^3` framework surface, the 2-loop coefficient
`K_2` of the MSbar-to-pole mass conversion decomposes into four
gauge-group-irreducible color channels whose prefactors are exact
rationals inherited from the retained SU(3) Casimir algebra
(`C_F = 4/3`, `C_A = 3`, `T_F = 1/2`). The retained light-flavor count
`n_l = 5` at the top-mass scale is carried from the Standard Model
matter content. The decomposition is:

```
K_2(n_l)  =  C_F² · J_FF  +  C_F · C_A · J_FA  +  C_F · T_F · n_l · J_Fl  +  C_F · T_F · J_Fh
```

with retained SU(3) color-tensor prefactors at `n_l = 5`:

```
C_F²             =  16/9                        (abelian-like ladder)
C_F · C_A        =  4                            (non-abelian)
C_F · T_F · n_l  =  (2/3) · 5  =  10/3           (light-fermion insertion)
C_F · T_F        =  2/3                          (heavy-fermion insertion)
```

The four 2-loop integrals `J_FF`, `J_FA`, `J_Fl`, `J_Fh` are cited from
Gray-Broadhurst-Grafe-Schilcher 1990 and Marquard-Steinhauser 2016
(see the K_2 integral citation note). Together with the retained
color-tensor skeleton, these reproduce the published numerical value
`K_2(n_l = 5) = 10.9405` at SU(3) to sub-permille.

## 1. Retained foundations

This note inherits without modification:

- **SU(3) Casimirs.** `C_F = (N_c² − 1)/(2 N_c) = 4/3`, `T_F = 1/2`,
  `C_A = N_c = 3` at N_c = 3, retained from
  `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` (D7) and
  `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1).
- **SM light-fermion count at the top-mass scale.** `n_l = 5` (up,
  down, strange, charm, bottom), with the top itself the single heavy
  decoupled flavor (`n_h = 1`). Retained from the SM matter content
  carried by the complete-prediction-chain runners.
- **K_1 framework-native.** `K_1 = C_F = 4/3` (single color tensor,
  exact). Inherited from
  `docs/YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`.

## 2. Theorem statement

**Theorem P3-K_2.** On the retained `Cl(3)/Z^3` framework surface, the
2-loop coefficient of the MSbar-to-pole mass conversion series
decomposes into four gauge-group-irreducible color channels:

```
K_2(n_l)  =  C_F² · J_FF  +  C_F · C_A · J_FA  +  C_F · T_F · n_l · J_Fl  +  C_F · T_F · J_Fh
                                                                                     (2.1)
```

where:

- **`C_F²` channel (`J_FF`)** is the abelian-like (photon-like) ladder
  topology: two gluons exchanged on the heavy-quark line in an abelian
  configuration, with no three-gluon vertex and no closed fermion
  loop.
- **`C_F C_A` channel (`J_FA`)** is the non-abelian topology: two-gluon
  exchange containing the non-abelian three-gluon vertex or a one-loop
  gluon self-interaction subdiagram.
- **`C_F T_F n_l` channel (`J_Fl`)** is a closed massless-fermion loop
  inserted into the gluon propagator dressing the heavy-quark
  self-energy; `n_l` counts the light flavors.
- **`C_F T_F` channel (`J_Fh`)** is the same vacuum-polarization
  topology as `J_Fl` but with the heavy quark itself (mass `m`) in the
  inner loop; kinematically distinct from `J_Fl` because the inner-loop
  mass equals the external on-shell mass.

On the retained framework surface:

1. All four color-tensor prefactors evaluate to exact rationals at
   SU(3) (Section 3.1).
2. The light-fermion count `n_l = 5` at the top-mass scale is retained
   from the SM matter content (Section 3.2).
3. The four 2-loop integrals `J_FF`, `J_FA`, `J_Fl`, `J_Fh` are cited
   from the QCD literature (Gray-Broadhurst-Grafe-Schilcher 1990;
   Marquard-Steinhauser 2016); these are **not** derived here, and
   are the open 2-loop sub-gaps of P3 K_2 (Section 4).
4. With the cited integral values, the decomposition reproduces the
   published numerical value `K_2(n_l = 5) = 10.9405` at SU(3) (Section
   4).

## 3. Color-tensor structure (retained)

### 3.1 Four-tensor skeleton at SU(3)

The 2-loop on-shell heavy-quark self-energy topologies partition by
color-tensor structure into exactly four gauge-group-irreducible
classes. At N_c = 3:

| Topology class | Color tensor | Exact value at SU(3) |
|---|---|---|
| abelian-like ladder | `C_F²` | `16/9` |
| non-abelian | `C_F · C_A` | `4` |
| light-fermion insertion | `C_F · T_F · n_l` | `(2/3) · n_l` |
| heavy-fermion insertion | `C_F · T_F` | `2/3` |

At the retained SM light-flavor count `n_l = 5`:

```
C_F²              =  (4/3)²               =  16/9                    (3.1a)
C_F · C_A         =  (4/3) · 3            =  4                        (3.1b)
C_F · T_F · n_l   =  (4/3) · (1/2) · 5    =  10/3                    (3.1c)
C_F · T_F         =  (4/3) · (1/2)        =  2/3                      (3.1d)
```

All four are exact rationals inherited from the retained SU(3) Casimir
authority. None is a citation.

### 3.2 Retained `n_l = 5` at the top-mass scale

On the SM branch, five quark flavors (`u, d, s, c, b`) lie below the
top-quark mass. The MSbar-to-pole conversion of `m_t` therefore uses
`n_l = 5`. The top itself is the heavy decoupled flavor (`n_h = 1`)
whose pole mass is being converted. Retention from the SM matter
content carried by the complete-prediction-chain runners; no
modification.

### 3.3 Exactness of the four-channel decomposition

The four color tensors `{C_F², C_F · C_A, C_F · T_F · n_l, C_F · T_F}`
are linearly independent over `Q[C_F, C_A, T_F, n_l]` and form a basis
of the 2-loop on-shell heavy-quark color-tensor subspace. At 2-loop
there are no other independent color tensors: a hypothetical `C_A²`
piece or a double-fermion-loop `(T_F n_l)²` piece would correspond to
three-loop topologies (two gluon self-interaction insertions, or two
fermion loops, respectively). This establishes the four-channel
decomposition (2.1) as structurally complete at 2-loop.

## 4. Numerical verification at SU(3), `n_l = 5`

With the four retained color-tensor prefactors (3.1) and the cited
2-loop integral values from the QCD literature (see
`docs/YT_P3_MSBAR_TO_POLE_K2_INTEGRAL_CITATION_NOTE_2026-04-17.md`
§§2–4), the published target

```
K_2(n_l = 5)  =  10.9405                                             (4.1)
```

at SU(3) is reproduced as the linear combination

```
K_2(n_l = 5)  =  (16/9) J_FF  +  4 J_FA  +  (10/3) J_Fl  +  (2/3) J_Fh
              =  10.9405                    (literature target)
```

to sub-permille (`|Δ| ≤ 0.001` abs, `≤ 10⁻⁴` rel).

The 2-loop shift at the retained coupling anchor `α_s(m_t) ≈ 0.108` is

```
K_2 · (α_s/π)²  =  10.9405 · (0.108 / π)²  ≈  0.0129  ≈  1.29 %     (4.2)
```

which is about 22 % of the 1-loop shift `K_1 (α_s/π) ≈ 4.58 %` — a
ratio consistent with asymptotic-series convergence at this coupling.

## 5. Safe claim boundary

This note claims:

> On the retained `Cl(3)/Z^3` framework surface, the 2-loop MSbar-to-pole
> mass conversion coefficient `K_2` decomposes into exactly four
> gauge-group-irreducible color channels, whose SU(3) Casimir
> prefactors are exact rationals
> `{C_F² = 16/9, C_F C_A = 4, C_F T_F n_l = 10/3 at n_l = 5,
> C_F T_F = 2/3}`. The light-fermion count `n_l = 5` at the
> top-mass scale is retained from the SM matter content. Together with
> the cited 2-loop integral values `J_FF`, `J_FA`, `J_Fl`, `J_Fh` from
> the QCD on-shell mass-conversion literature, the decomposition
> reproduces the published `K_2(n_l = 5) = 10.9405` at SU(3) to
> sub-permille. The four 2-loop integrals themselves are **not**
> derived on the retained action; they are the open 2-loop sub-gaps
> of P3 K_2.

It does **not** claim:

- framework-native values for `J_FF`, `J_FA`, `J_Fl`, `J_Fh` on the
  retained action (these remain cited; a framework-native 2-loop
  derivation is an open next-level retention step);
- a framework-native derivation of the 3-loop coefficient `K_3` or
  higher (treated in separate sub-theorems);
- any modification of the master obstruction theorem, the K_1
  framework-native retention, any SU(3) Casimir authority, or any
  publication-surface file.

## 6. What is retained vs. cited vs. open

**Retained (framework-native):**

- `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` at SU(3) (D7 + S1).
- Retained light-flavor count `n_l = 5` at `μ = m_t` (SM matter).
- `K_1 = C_F = 4/3` (prior K-series step).
- Four-channel color-tensor decomposition
  `K_2 = C_F² J_FF + C_F C_A J_FA + C_F T_F n_l J_Fl + C_F T_F J_Fh`.
- Exact SU(3) prefactor values at n_l = 5:
  `{16/9, 4, 10/3, 2/3}`.

**Cited (external QCD literature):**

- The numerical value `K_2(n_l = 5) = 10.9405` at SU(3)
  (Chetyrkin-Steinhauser 2000; Marquard-Steinhauser 2016).
- The rational + ζ-value closed-form structure of each 2-loop integral
  `J_FF`, `J_FA`, `J_Fl`, `J_Fh` (Gray-Broadhurst-Grafe-Schilcher 1990;
  Broadhurst 1991–92; re-verified by Chetyrkin-Steinhauser 2000,
  Melnikov-van Ritbergen 2000, Marquard et al. 2016).

**Open (not closed by this note):**

- Framework-native 2-loop derivation of any of the four integrals
  `J_FF`, `J_FA`, `J_Fl`, `J_Fh` on the retained `Cl(3)/Z^3` action.

## 7. Validation

The runner `scripts/frontier_yt_p3_msbar_to_pole_k2.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p3_msbar_to_pole_k2_2026-04-17.log`. The runner
must return PASS on every check to keep this note on the retained
surface.

The runner verifies 5 checks:

1. `C_F² = 16/9` exactly at SU(3).
2. `C_F · C_A = 4` exactly at SU(3).
3. `C_F · T_F · n_l = 10/3` exactly at SU(3), n_l = 5.
4. Four-tensor decomposition identity
   `K_2 = C_F² J_FF + C_F C_A J_FA + C_F T_F n_l J_Fl + C_F T_F J_Fh`
   is structurally exact (symbolic assembly of the 2-loop heavy-quark
   topologies; `C_F T_F` for the heavy-loop piece equals `2/3`).
5. Numerical reconstruction: `K_2(n_l = 5) = 10.9405` reproduced from
   the retained color-tensor prefactors and the cited integral values
   to sub-permille.

## Status

**RETAINED** — four-channel color-tensor skeleton of K_2 retained
framework-native at 2-loop. The four 2-loop integral primitives
`J_FF`, `J_FA`, `J_Fl`, `J_Fh` remain cited; a framework-native
2-loop derivation is the next open retention level for P3 K_2.
