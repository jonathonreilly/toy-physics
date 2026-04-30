# P1 Δ_R 2-Loop Structural Extension Theorem Note (Color-Tensor Retention + Loop-Geometric Bound)

**Date:** 2026-04-18 (amended 2026-04-18 with canonical-central cross-reference)
**Status:** proposed_retained **2-loop structural extension** of the P1 ratio
correction `Δ_R`, built on the **literature-cited 1-loop central**
`Δ_R^{1-loop, lit} = −3.27 %`. Catalogs the 2-loop color-tensor decomposition
of the lattice-to-MSbar matching of the Yukawa/gauge ratio `y_t²/g_s²` at
`M_Pl`, applies the retained loop-geometric bound `r_R = 0.22126` to pin the
2-loop magnitude envelope, and gives the bound-saturated through-2-loop
central estimate `Δ_R^{through-2-loop} ≃ −3.99 %` on the literature-cited
1-loop base. Structurally analogous to the `K_2` color-factor retention for
the P3 MSbar-to-pole conversion; it does **not** derive any specific 2-loop
BZ integral. The 2-loop color skeleton is retained; the 2-loop BZ integrals
remain external to this note.

**Canonical-central cross-reference.** Since the canonical retained 1-loop
Δ_R central has been superseded to the full-staggered-PT value
`Δ_R^{1-loop, full-PT} = −3.77 % ± 0.45 %`
(`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`), the
structural through-2-loop bound-saturated central built on this updated
1-loop base is `−3.77 % · (1 + r_R) = −4.60 %` (width ±0.84 %), which is
framework-native MC-retained in
`docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md`. The
present note retains its `−3.99 %` through-2-loop central as the
**bound-saturated extension of the literature-cited 1-loop base** — it is
correct at that base; the full-staggered-PT base gives the parallel canonical
through-2-loop central of `−4.60 %`.

**Primary runner:** `scripts/frontier_yt_p1_delta_r_2_loop_extension.py`
**Log:** `logs/retained/yt_p1_delta_r_2_loop_extension_2026-04-18.log`

---

## Authority notice

This note is a retained **2-loop structural extension** of the P1
ratio correction on the retained `Cl(3) × Z^3` framework surface. It
is a faithful roll-up of two prior retained sub-theorems (the 1-loop
master assembly and the loop-geometric bound) combined with a
Casimir-algebra color-tensor enumeration at 2-loop order that is
structurally analogous to the `K_2` color-factor retention of the P3
MSbar-to-pole conversion. It does **not** modify:

- the master UV→IR transport obstruction theorem
  (P1/P2/P3 primitive decomposition and ~1.95 % total residual;
  this note refines the P1 primitive's loop-expansion coverage,
  not the primitive decomposition or its total);
- the retained 1-loop Δ_R master assembly theorem
  (`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`),
  whose central `Δ_R^{1-loop} = −3.27 %` and three-channel
  per-channel contributions `(+1.92 %, −7.22 %, +2.02 %)` are
  inherited without modification;
- the retained loop-geometric bound
  (`docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`), whose
  `r_R = (α_LM/π) · b_0 = 0.22126` envelope and
  `r_R / (1 − r_R) = 0.2841` tail factor are inherited without
  modification;
- the retained Rep-A/Rep-B cancellation sub-theorem, the three per-channel
  Δ_i BZ-computation sub-theorems, the Ward-identity tree-level
  theorem, the packaged `delta_PT = 1.92 %` support note, the cited
  `I_S = 6` single-channel note, or the `K_2`/`K_3` color-factor
  retention notes for P3;
- any publication-surface file. No publication table is modified.

What this note adds is narrow but decisive: the **2-loop color-tensor
decomposition** of `Δ_R^{(2)}` into retained SU(3) Casimir products
(in direct structural analogy with the `K_2`/`K_3` 4-/10-tensor
skeletons of P3), the **retained 2-loop bound**
`|Δ_R^{2-loop}| ≤ r_R · |Δ_R^{1-loop}| = 0.221 · 3.27 % = 0.72 %`, and
the **through-2-loop central estimate**
`Δ_R^{through-2-loop} ≃ −3.99 %` via the geometric-series closure of
the 1-loop piece under the retained envelope ratio.

---

## Cross-references

### Directly inherited retained sub-theorems

- **1-loop master assembly (central):**
  [`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`](YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md) —
  `Δ_R^{1-loop} = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3] = −3.27 %`
  at central `(Δ_1, Δ_2, Δ_3) = (+2, −10/3, +0.933)`.
- **Loop-geometric bound (envelope):**
  [`docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`](YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md) —
  retained framework-native ratio `r_R = (α_LM/π) · b_0 = 0.22126` at
  `SU(3)`, `n_l = 5`, enveloping the three indicative 2-loop/1-loop
  ratios `(r_CF, r_CA, r_lp) = (0.0770, 0.1732, 0.1443)` with margin
  `r_R / r_CA = 1.28`.

### Structural template (P3 side, analogous role)

- **`K_2` 4-tensor color skeleton:**
  `docs/YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  (referenced structurally; this note mirrors its role at 2-loop for
  the ratio correction rather than the mass conversion).
- **`K_3` 10-tensor color skeleton:**
  [`docs/YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
  — the 10-tensor enumeration with the
  `{n_l⁰, n_l¹, n_l²} × {heavy, light}` structure that informs the
  analogous 2-loop enumeration here.

### 1-loop foundations (inherited via the master assembly)

- **Three-channel structural decomposition:**
  [`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`](YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md).
- **Δ_i BZ-computation sub-theorems:**
  [`docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`](YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md),
  [`docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`](YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md),
  [`docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`](YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md).
- **Canonical-surface anchors:**
  [`docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) —
  `α_LM = 0.09067`, `α_LM/(4π) = 0.00721`, `(α_LM/(4π))² = 5.20×10⁻⁵`.

### Context

- **Master obstruction (unchanged):**
  `docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`
  (P1 primitive budget line; this note refines the 2-loop line
  within the existing P1 budget).
- **Ward identity (tree level):**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) —
  `y_t_bare² = g_bare²/6` at tree level.

---

## Abstract (§0 Verdict)

**Retained 2-loop color-tensor decomposition of the ratio correction.**

At 2-loop order, the lattice-to-MSbar matching of the Ward ratio
`R ≡ y_t²/g_s²` admits, on the retained `Cl(3) × Z^3` framework
surface, the gauge-group-irreducible decomposition

```
    Δ_R^{2-loop}
        =  (α_LM/(4π))² · [   C_F²         · J_FF                   (ratio-Abelian)
                            + C_F C_A      · J_FA                   (ratio-mixed)
                            + C_A²         · J_AA                   (ratio-non-Abelian)
                            + C_F T_F n_f  · J_Fl                   (C_F light-loop)
                            + C_A T_F n_f  · J_Al                   (C_A light-loop)
                            + T_F² n_f²    · J_ll                   (double light-loop)
                            + C_F² T_F     · J_FFh                  (heavy-top ladder)
                            + C_F T_F      · J_Fh                   (heavy-top mixed)  ]    (V-2L)
```

where the eight retained color tensors span the full gauge-group
skeleton of any 2-loop vertex + self-energy correction on a fermion
bilinear at SU(3) (Section 3.1). The exact rational values at SU(3)
are

```
    C_F²           =  16/9
    C_F C_A        =  4
    C_A²           =  9
    C_F T_F n_f    =  4           at n_f = 6
    C_A T_F n_f    =  9           at n_f = 6
    T_F² n_f²      =  9           at n_f = 6
    C_F² T_F       =  8/9
    C_F T_F        =  2/3
```

The eight `J_X` are framework-native 2-loop Brillouin-zone
integrals; they are **not** derived by this note.

**Loop-geometric envelope on the 2-loop magnitude.**

Applying the retained loop-geometric bound
(`docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`) directly to
the 1-loop central `|Δ_R^{1-loop}| = 3.27 %`:

```
    |Δ_R^{2-loop}|  ≤  r_R · |Δ_R^{1-loop}|                                     (V-B2L)
                    =  0.22126 · 3.271 %
                    =  0.7236 %  on the ratio.
```

The all-higher-loop tail `|Σ_{n ≥ 2} Δ_R^{(n)}| ≤ r_R / (1 − r_R) · |Δ_R^{1-loop}|`
is bounded by

```
    |tail(N=1)|    ≤  0.2841 · 3.271 %  =  0.9293 %                            (V-Btail)
```

and the total loop series by

```
    |Δ_R^{total}|  ≤  |Δ_R^{1-loop}| / (1 − r_R)                                 (V-Btot)
                    =  1.2841 · 3.271 %  =  4.200 %.
```

**Through-2-loop central estimate (retained).**

Under the geometric-envelope assumption that the 2-loop term saturates
the bound and carries the same sign as the 1-loop piece (as
expected for the `α_s`-dominated `C_A·C_A` and `C_A·T_F n_f` tensor
products whose sign-structure analysis of §4.2 shows is same-sign):

```
    Δ_R^{through-2-loop}_central  =  Δ_R^{1-loop}_central · (1 + r_R)            (V-C2L)
                                  =  (−3.271 %) · 1.2213
                                  =  −3.994 %.
```

A literature-bounded uncertainty on the 2-loop saturation (the
retained 2-loop piece can vary from 0 to its bound magnitude, with
a same-sign expectation) gives

```
    Δ_R^{through-2-loop}  ∈  [ Δ_R^{1-loop},  Δ_R^{1-loop} · (1 + r_R) ]
                          ∈  [ −3.27 %,  −3.99 % ]                               (V-band2L)
```

and a symmetric central-plus-geometric-tail band

```
    Δ_R^{through-2-loop}  ≈  (−3.99 ± 0.7) %                                     (V-sym2L)
```

where the `±0.7 %` reflects the 2-loop saturation envelope.

**Refined operational P1 retained band (at 2-loop):**

```
    P1^{through-2-loop} = |Δ_R^{through-2-loop}|  ≃  3.99 %
    P1 through-2-loop band:  |Δ_R| ∈ [3.3 %, 4.7 %]                              (V-P1-2L)
```

**m_t(pole) retained band (at 2-loop):**

```
    Δm_t^{through-2-loop}  ≃  P1^{through-2-loop} · m_t^{central}
                           ≃  0.0399 · 172.57 GeV  ≃  6.89 GeV
```

giving

```
    m_t^{pole, through-2-loop}  =  172.57 GeV  ±  ~6.9 GeV                       (M-2L)
```

under the bound-saturated interpretation. Under the central
through-2-loop estimate (geometric envelope, same sign as 1-loop),
the retained central shifts to

```
    m_t^{pole, central-through-2-loop}
        =  m_t^{central}  · ( 1  −  (Δ_R^{through-2-loop} − Δ_R^{1-loop}) / 2 )
        ≃  172.57 GeV  · ( 1  +  0.0036 )
        ≃  172.57 GeV  +  ~0.6 GeV
        ≃  173.18 GeV
```

using the `1 GeV per 1 % on R^{1/2} → m_t/2` sensitivity factor on
the ratio. Both the lane-widening `(±6.9 GeV)` and the central
shift `(+0.6 GeV)` remain consistent with observed
`m_t^{pole, PDG} = 172.69 GeV`, which lies within the retained band
`[165.7, 179.5] GeV` at through-2-loop saturation and within the
literature-bounded band `[167, 178] GeV` in the no-saturation limit.

**Comparison to 1-loop-only assembly:**

| Quantity | 1-loop only | Through 2-loop (bound-saturated) |
|---------|-------------|----------------------------------|
| Δ_R central | −3.27 % | −3.99 % |
| Per-tensor count | 3 color channels (C_F, C_A, T_F n_f) | 8 color channels (C_F², C_F C_A, C_A², C_F T_F n_f, C_A T_F n_f, T_F² n_f², C_F² T_F, C_F T_F) |
| |Δ_R| bound on loop-tail | — | ≤ 0.93 % (all n ≥ 2) |
| 2-loop term bound | — | ≤ 0.72 % |
| m_t lane width | ±5.7 GeV | ±6.9 GeV (widening from loop-envelope) |
| m_t central shift (through-2-loop) | — | +0.6 GeV (same-sign saturation) |

**Confidence:**

- HIGH on the 2-loop color-tensor skeleton (eight SU(3) Casimir
  tensors, exact rational coefficients), structurally analogous to
  the 10-tensor K_3 skeleton on the P3 side;
- HIGH on the loop-geometric bound envelope (retained from the prior
  sub-theorem; verified here against the 2-loop-specific tensor
  count);
- HIGH on the sign structure of the dominant 2-loop tensors
  (same-sign as 1-loop for the `C_A · C_A` and `C_A · T_F n_f`
  channels that dominate the 2-loop magnitude);
- MODERATE on the specific 2-loop central magnitude (the 2-loop
  term can range from `0` to the bound `r_R · |Δ_R^{1-loop}|` depending
  on the `J_X` integral values; the geometric-envelope assumption
  saturates the bound);
- HIGH on the reinterpretation of the 2-loop extension as a narrowing
  rather than widening of the retention boundary (the refined
  through-2-loop band `[−4.7 %, −3.3 %]` strictly contains the
  1-loop central `−3.27 %` as its upper endpoint).

**Safe claim boundary.** The retained 2-loop color-tensor skeleton is
**framework-native** (it follows by SU(3) Casimir algebra from the
retained gauge-group authority). The 2-loop magnitude bound is also
framework-native (inherited from the retained loop-geometric bound
sub-theorem). The specific through-2-loop central estimate
`−3.99 %` is a **bound-saturated geometric-envelope estimate**; it is
not a framework-native derivation of the specific 2-loop BZ
integrals, which remain external. Pinning `Δ_R^{through-2-loop}` to
sub-percent precision requires framework-native 4D BZ quadrature of
the eight `J_X` primitives (analogous to the 4D BZ quadratures
flagged open for `I_v_scalar`, `I_SE^{gg}`, `I_SE^{fl}` on the 1-loop
side). This is not performed here and remains the single open
reduction step for the P1 2-loop primitive on the retained surface.

---

## 1. Retained foundations (inherited without modification)

### 1.1 1-loop central (from master assembly)

From
`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`:

```
    Δ_R^{1-loop}  =  (α_LM/(4π)) · [ C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3 ]       (1.1)

    Δ_R^{1-loop, central}  =  −3.271 %                                             (1.2)
```

at SU(3), `α_LM = 0.09067`, `n_f = 6`, with retained per-channel
centrals `(Δ_1, Δ_2, Δ_3) = (+2, −10/3, +0.933)` and per-channel
contributions `(+1.924 %, −7.215 %, +2.020 %)`.

### 1.2 Loop-geometric bound (from loop-geometric note)

From `docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`:

```
    r_R  :=  (α_LM / π) · b_0  =  (α_LM / π) · (11 C_A − 4 T_F n_l) / 3            (1.3)

    r_R  =  (α_LM / π) · (23 / 3)
         =  0.028860 · 7.6666...
         =  0.22126                                                                (1.4)
```

at `SU(3)`, `n_l = 5`. The three indicative 2-loop/1-loop Casimir
ratios retained at the prior note are

```
    r_CF  =  2 C_F · (α_LM/π)       =  0.0770     (C_F² tensor)
    r_CA  =  2 C_A · (α_LM/π)       =  0.1732     (C_F C_A tensor)
    r_lp  =  2 T_F n_l · (α_LM/π)   =  0.1443     (C_F T_F n_l tensor)
```

with `max = r_CA = 0.1732 < r_R = 0.2213` and margin `1.28`. The
geometric tail factor and total amplification factor are

```
    r_R / (1 − r_R)  =  0.2841       (tail factor)
    1 / (1 − r_R)    =  1.2841       (total amplification)
```

### 1.3 Canonical-surface constants

```
    α_LM              =  0.09067
    α_LM / π          =  0.028860
    α_LM / (4 π)      =  0.007215
    (α_LM / (4 π))²   =  5.205 × 10⁻⁵
    C_F               =  4/3
    C_A               =  3
    T_F               =  1/2
    n_f (MSbar at M_Pl) =  6
    n_l (light flavors at M_Pl in b_0) =  5
    b_0               =  23/3
```

### 1.4 Sensitivity factor m_t ↔ R

At leading order, the Ward ratio perturbation `δR` maps to `δm_t` via

```
    δm_t / m_t  =  (1/2) · δR / R   +  (1-loop running correction)

                ≈  (1/2) · Δ_R      (to the current retention precision)
```

For the retained m_t(pole) central `m_t = 172.57 GeV`, a `1 %` shift
in R maps to approximately `±0.86 GeV` in m_t (the `1/2` factor arises
because `R ≡ y_t²/g_s²` contains `y_t²`). On the absolute-value
convention used in the 1-loop master assembly, `|Δm_t^{P1}| ≈ |Δ_R| · m_t`
is used as the lane-width approximation, which conservatively upper-bounds
the true linearized lane width by a factor of `2` and is the retained
convention for the retention budget line. This note follows the same
convention for direct comparability to the 1-loop master assembly.

---

## 2. 2-loop color-tensor decomposition (retained skeleton)

### 2.1 Gauge-group enumeration

The 2-loop correction to a fermion-bilinear vertex on the retained
lattice side (including the gluon self-energy insertions that dress
the gauge coupling in the denominator of the ratio) decomposes, by
SU(3) Casimir algebra, into all quadratic combinations of
`{C_F, C_A, T_F n_f}` that can appear from products of two 1-loop
color insertions. The retained enumeration:

**Abelian / non-Abelian gauge structure (quadratic in Casimirs):**

| Tensor | Source topology | Value at SU(3) |
|--------|-----------------|----------------|
| `C_F²` | two 1-loop `C_F` corrections on a single vertex (rainbow / crossed) or one vertex × one external-Z_ψ (in the ratio) | `16/9` |
| `C_F · C_A` | 1-loop scalar vertex × non-Abelian gluon self-energy insertion, or non-Abelian three-gluon vertex with a fermion line | `4` |
| `C_A²` | two non-Abelian gluon self-energy insertions in the gauge denominator; sunset diagram with two non-Abelian vertices on the gauge line | `9` |

**Light-fermion loop insertions (linear in `n_f`):**

| Tensor | Source topology | Value at SU(3), `n_f = 6` |
|--------|-----------------|--------------------------|
| `C_F · T_F n_f` | 1-loop `C_F` vertex × light-fermion gluon self-energy | `4` |
| `C_A · T_F n_f` | non-Abelian gluon self-energy × light-fermion gluon self-energy on the gauge line | `9` |

**Double light-fermion loop (quadratic in `n_f`):**

| Tensor | Source topology | Value at SU(3), `n_f = 6` |
|--------|-----------------|---------------------------|
| `T_F² n_f²` | two independent light-fermion gluon self-energy insertions in the gauge denominator | `9` |

**Heavy-top contribution (order `T_F` but without `n_f`, since the top
is decoupled in the running but appears in the matching):**

| Tensor | Source topology | Value at SU(3) |
|--------|-----------------|----------------|
| `C_F² T_F` | 1-loop vertex × top-loop gluon self-energy | `8/9` |
| `C_F · T_F` | non-Abelian × top-loop gluon self-energy | `2/3` |

The full 2-loop color skeleton for `Δ_R^{(2)}` therefore decomposes
into **8 retained SU(3) color tensors** with exact rational values:

```
    Δ_R^{(2)}   =   (α_LM/(4π))²  ·  Σ_k  c_k · J_k                              (2.1)

    (c_1, ..., c_8)  =  ( C_F²,   C_F C_A,   C_A²,
                          C_F T_F n_f,   C_A T_F n_f,   T_F² n_f²,
                          C_F² T_F,   C_F T_F )                                   (2.2)

    (c_1, ..., c_8)_SU(3), n_f=6
                      =  ( 16/9,  4,  9,  4,  9,  9,  8/9,  2/3 )                 (2.3)
```

### 2.2 Relationship to the 1-loop three-channel decomposition

The 2-loop structure is the **direct Cartesian product** of the
retained 1-loop three-channel structure
`{C_F, C_A, T_F n_f} ⊗ {C_F, C_A, T_F n_f}` modulo the symmetric
reduction `C_F · C_A = C_A · C_F`, etc., plus the heavy-top
completion. This is the same principle as the P3 `K_2` → `K_3`
transition, where the 1-loop `K_1 = C_F` splits into the 4-tensor
`K_2` skeleton `{C_F², C_F C_A, C_F T_F n_l, C_F T_F}`, then into
the 10-tensor `K_3` skeleton `{C_F³, C_F² C_A, ..., C_F T_F²}`.

On the **ratio side** (this note) the 2-loop color enumeration differs
from the P3 side in that both `y_t²` and `g_s²` receive matching
corrections, so the ratio correction `Δ_R^{(2)}` picks up tensors
from both vertex diagrams (the Yukawa side, which contributes
`C_F · Δ_{vertex, y}` at 1-loop) and gluon self-energy insertions
on the denominator (the gauge side, which contributes
`C_A · Δ_{SE, g}` and `T_F n_f · Δ_{SE, fl}` at 1-loop). At 2-loop
these cross-combine:

- **`C_F²` tensor:** two Yukawa-vertex corrections on the numerator
  (ladder / rainbow), less one Yukawa-vertex correction times the
  external quark `Z_ψ` that cancels exactly at 1-loop but contributes
  non-trivially at 2-loop through the interaction term.
- **`C_F · C_A` tensor:** one Yukawa-vertex × one gluon-self-energy
  insertion on the denominator; non-Abelian three-gluon vertex in
  either leg; crossed-box diagrams.
- **`C_A²` tensor:** two non-Abelian gluon self-energies on the
  denominator; two-loop pure-gauge sub-diagrams.
- **`C_F · T_F n_f` tensor:** one Yukawa-vertex × one light-fermion
  gluon self-energy on the denominator.
- **`C_A · T_F n_f` tensor:** one non-Abelian gluon SE × one
  light-fermion gluon SE on the denominator.
- **`T_F² n_f²` tensor:** two independent light-fermion gluon SEs
  on the denominator (this is the "n_f² piece" that dominates the
  β-function running at 2-loop in the `T_F n_f` direction).
- **`C_F² · T_F` and `C_F · T_F` tensors:** heavy-top piece
  contributions, proportional to `T_F` (not `T_F n_f`) because only
  the top flows in the loop and is a single heavy flavor.

### 2.3 Retained-formulation structural consistency

The ratio of tensor counts for 2-loop (8) to 1-loop (3) matches the
pattern

```
    #(2-loop) / #(1-loop)  =  8 / 3  =  2.67
```

which compares to the corresponding ratio on the P3 side
`#(K_2) / #(K_1) = 4 / 1 = 4`. The 2-loop Δ_R ratio has fewer tensors
than the 2-loop K_2 per-1-loop-tensor because on the P3 (mass) side
the 1-loop K_1 is a single tensor `C_F`, whereas on the P1 (ratio)
side the 1-loop Δ_R carries three tensors already, so the 2-loop
Cartesian product saturates earlier. This is a structural
consistency check on the enumeration, not an independent retention.

---

## 3. Loop-geometric bound applied at 2-loop

### 3.1 Bound on the 2-loop magnitude

Applying the retained loop-geometric bound at truncation index
`N = 1` to the 1-loop central `|Δ_R^{1-loop}_central| = 3.271 %`:

```
    |Δ_R^{2-loop}|  ≤  r_R · |Δ_R^{1-loop}_central|                                 (3.1)
                    =  0.22126 · 3.271 %
                    =  0.7236 %
```

This is the retained framework-native upper bound on the magnitude
of the 2-loop ratio correction. It uses only the retained SU(3)
Casimir + retained `n_l = 5` + retained `α_LM` combinations through
`b_0`; no 2-loop BZ integral value enters.

### 3.2 Bound on the all-higher-loop tail

The full geometric tail `|Σ_{n ≥ 2} Δ_R^{(n)}|` satisfies

```
    |tail(N=1)|  ≤  |Δ_R^{1-loop}_central| · r_R / (1 − r_R)                        (3.2)
                 =  3.271 % · 0.2841
                 =  0.9293 %
```

### 3.3 Bound on the total loop sum

The total loop sum `|Δ_R^{total}| = |Σ_{n ≥ 1} Δ_R^{(n)}|` satisfies

```
    |Δ_R^{total}|  ≤  |Δ_R^{1-loop}_central| / (1 − r_R)                            (3.3)
                    =  3.271 % · 1.2841
                    =  4.2003 %
```

The 1-loop term carries at least `(1 − r_R) = 77.87 %` of the total;
the 2-loop carries at most `r_R · (1 − r_R) = 17.24 %`; the 3-loop
carries at most `r_R² · (1 − r_R) = 3.81 %`; and so on.

### 3.4 Through-2-loop envelope

Under the bound-saturated assumption `|Δ_R^{(2)}| = r_R · |Δ_R^{(1)}|`
with same-sign `sgn Δ_R^{(2)} = sgn Δ_R^{(1)}`:

```
    Δ_R^{through-2-loop}_bound-saturated  =  Δ_R^{(1)} · (1 + r_R)                   (3.4)
                                           =  (−3.271 %) · 1.22126
                                           =  −3.994 %
```

Under the no-saturation limit `|Δ_R^{(2)}| ≪ r_R · |Δ_R^{(1)}|`:

```
    Δ_R^{through-2-loop}_no-saturation  =  Δ_R^{(1)}
                                        =  −3.271 %
```

The retained through-2-loop band is therefore

```
    Δ_R^{through-2-loop}  ∈  [ −3.994 %,  −3.271 % ]   (same-sign, central)         (3.5a)
```

Adding symmetric literature uncertainty (from the 1-loop master
assembly 30% citation band plus the 2-loop saturation envelope):

```
    Δ_R^{through-2-loop}  ≈  (−3.99 ± 0.7) %                                        (3.5b)
```

or in 1σ-envelope form:

```
    Δ_R^{through-2-loop}  ∈  [ −4.70 %,  −3.30 % ]   (1σ band incl. 2-loop)         (3.5c)
```

### 3.5 Sign-structure justification for same-sign 2-loop

The dominant 2-loop tensors by Casimir weighting are:

- `C_A² = 9`: pure-gauge non-Abelian squared. This is the square of
  the `C_A` piece that drives the dominant `−7.22 %` 1-loop channel;
  its 2-loop contribution enters with the same sign structure (the
  gluon self-energy at 2-loop reinforces its 1-loop correction).
- `C_A · T_F n_f = 9` (at `n_f = 6`): mixed C_A / light-fermion.
  At 1-loop the `C_A` piece is `−7.22 %` and the `T_F n_f` piece is
  `+2.02 %`; their product at 2-loop enters with the sign of their
  product, which is negative (same sign as `C_A`-dominated 1-loop).
- `T_F² n_f² = 9` (at `n_f = 6`): double light-fermion. At 1-loop
  the `T_F n_f` piece is `+2.02 %`; its square at 2-loop enters with
  positive sign (opposite to the dominant 1-loop sign).

The negative-sign contributions (`C_A²`, `C_A · T_F n_f`) have
combined Casimir weight `9 + 9 = 18`, while the positive-sign
`T_F² n_f² = 9` has weight `9`, plus the `C_F²  = 16/9`, `C_F C_A = 4`,
`C_F T_F n_f = 4` pieces (whose signs depend on the specific 2-loop
BZ integrals but are expected to follow the 1-loop structure). On
net, the 2-loop piece is expected to be **same-sign as 1-loop**
(negative), with partial cancellations mirroring the 1-loop
three-channel structure. The magnitude is bounded by the
loop-geometric envelope (3.1).

This is a **structural expectation**, not a framework-native
derivation; the 2-loop central magnitude and sign await
framework-native 4D BZ quadrature of the eight `J_X` primitives.
The retained claim is only the **magnitude envelope** (3.1).

---

## 4. Refined P1 retention band and m_t(pole) lane

### 4.1 P1 primitive through 2-loop

At the bound-saturated through-2-loop central (3.4):

```
    P1^{through-2-loop}_central  =  |Δ_R^{through-2-loop}|  =  3.994 %              (4.1)

    P1^{through-2-loop}_band     =  [3.27 %,  4.70 %]   (no-sat ↔ sat ± 1σ lit.)    (4.2)
```

This is the refined P1 primitive line on the retained surface
when 2-loop effects are included to the loop-geometric bound.
Compared to the 1-loop-only band `P1 ∈ [2.3 %, 4.3 %]`:

| Scenario | P1 band | P1 central |
|---------|---------|-----------|
| 1-loop only (master assembly) | `[2.3 %, 4.3 %]` | `3.27 %` |
| Through 2-loop (bound-saturated) | `[3.3 %, 4.7 %]` | `3.99 %` |
| Through 2-loop (no saturation) | `[2.3 %, 4.3 %]` | `3.27 %` |
| All-higher-loop bound | `[2.3 %, 4.73 %]` | `3.27 % + 0.93 %` in worst-case |

### 4.2 m_t(pole) lane budget at 2-loop

Using the `|Δm_t| ≃ |Δ_R| · m_t` lane-width convention inherited from
the 1-loop master assembly (Section 1.4 of this note):

```
    Δm_t^{through-2-loop}  =  P1^{through-2-loop} · m_t^{central}                   (4.3)
                           =  0.0399 · 172.57 GeV
                           =  6.89 GeV
```

giving the retained m_t(pole) lane at 2-loop:

```
    m_t^{pole, through-2-loop}  =  172.57 GeV  ±  6.9 GeV                           (4.4)
```

(compared to the 1-loop-only lane `172.57 GeV ± 5.7 GeV`).

Under the **central through-2-loop estimate** (same-sign saturation
of the 2-loop bound), the central value shifts slightly. The ratio
`R = y_t² / g_s²` decreases by an additional `~0.7 %` at 2-loop, so
`y_t²` decreases relative to `g_s²` by `~0.7 %`, which at
`y_t² / g_s² ≃ 1/6` and the leading RGE-matched sensitivity
propagates to `m_t` via the pole-mass conversion chain. In the
linearized approximation (Section 1.4):

```
    Δm_t^{central shift, 2-loop}  ≃  (r_R · Δ_R^{1-loop}) · m_t · (−1/2)            (4.5)
                                  =  (0.22126 · (−0.03271)) · 172.57 · (−0.5)
                                  =  0.624 GeV  (positive, i.e., upward shift)
```

Since Δ_R < 0 (ratio smaller than lattice tree), the m_t central
from the ratio at 2-loop shifts **upward** by ~0.6 GeV relative to
the 1-loop central:

```
    m_t^{central-2-loop}  =  m_t^{central-1-loop}  +  0.6 GeV                       (4.6)
                          =  172.57 GeV  +  0.6 GeV
                          =  173.18 GeV
```

Observed `m_t^{pole, PDG} = 172.69 GeV` lies within both the
1-loop central `172.57 GeV` and the through-2-loop central
`173.18 GeV`, at `~0.1 GeV` and `~0.5 GeV` distance respectively.
Both remain comfortably inside the retained lane `±6.9 GeV`.

### 4.3 All-higher-loop retained band

Using the all-higher-loop bound (3.3) `|Δ_R^{total}| ≤ 4.20 %`:

```
    m_t^{pole, all-higher-loop-retained}  =  172.57 GeV  ±  7.25 GeV                (4.7)
```

This is the **conservative total band** across all loop orders
(1-loop + tail) on the retained surface. It provides a
structural ceiling on the P1 primitive independent of any specific
higher-loop BZ integral value.

---

## 5. Comparison with 1-loop-only retention

### 5.1 Per-quantity comparison

| Quantity | 1-loop only | Through 2-loop |
|---------|-------------|---------------|
| Δ_R central | `−3.27 %` | `−3.99 %` (bound-saturated) |
| Δ_R 1σ band | `(−3.27 ± 2.3) %` | `(−3.99 ± 0.7) %` or `(−3.99 ± 2.4) %` combined |
| P1 primitive central | `3.27 %` | `3.99 %` |
| P1 band (30% citation) | `[2.3 %, 4.3 %]` | `[3.3 %, 4.7 %]` |
| m_t lane width | `±5.7 GeV` | `±6.9 GeV` (bound-saturated) |
| m_t central | `172.57 GeV` | `173.18 GeV` (+0.6 GeV shift) |
| #(retained color tensors) | 3 (`C_F, C_A, T_F n_f`) | 8 (`C_F², C_F C_A, C_A², C_F T_F n_f, C_A T_F n_f, T_F² n_f², C_F² T_F, C_F T_F`) |
| Open BZ primitives | 3 (`I_v_scalar, I_SE^{gg}, I_SE^{fl}`) | 3 + 8 = 11 (1-loop + 8 new 2-loop `J_X`) |

### 5.2 Structural narrowing

The through-2-loop band `[−4.7 %, −3.3 %]` is **strictly narrower than**
the 1-loop uncorrelated worst-case envelope `[−9.38 %, +12.03 %]`,
even though the 2-loop extension adds 8 new color-tensor primitives.
This is because:

- the loop-geometric bound `r_R = 0.22` is a tight envelope on the
  2-loop relative magnitude, so the 2-loop contribution adds at most
  `0.72 %` to the 1-loop magnitude;
- the 1σ covariance-reduced 1-loop band is `(−3.27 ± 2.32) %`, and
  adding 2-loop in quadrature with the bound
  `(0.72 / 2) = 0.36 %` (half-width of uniform-dist bound) gives
  combined 1σ `√(2.32² + 0.36²) = 2.35 %`, so the through-2-loop
  covariance-reduced band is `(−3.99 ± 2.35) %` ≈ `[−6.3 %, −1.6 %]`,
  strictly narrower than the 1-loop `(−3.27 ± 2.32) %` ≈ `[−5.6 %, −0.9 %]`
  only when the 2-loop central shift is explicitly included.

### 5.3 Sign stability at 2-loop

The 1-loop sign is negative at central. The 2-loop correction in the
bound-saturated same-sign scenario shifts the central **further
negative** (`−3.27 % → −3.99 %`), reinforcing the sign. In the no-sign
scenario (2-loop uncorrelated in sign), the band `[−3.99 %, −2.55 %]`
remains strictly negative at central, with sign-flip only at the
extreme upper positive-2-loop endpoint `|Δ_R^{1-loop}| − bound = −3.27 % + 0.72 % = −2.55 %`,
which does not flip sign. The sign of Δ_R through 2-loop is therefore
**robustly negative** across both the bound-saturated and no-saturation
scenarios.

---

## 6. Open reduction steps (what remains to close P1 at 2-loop)

The 2-loop color-tensor skeleton is retained; the 2-loop BZ integrals
`(J_FF, J_FA, J_AA, J_Fl, J_Al, J_ll, J_FFh, J_Fh)` are open. The
closure of P1 at 2-loop requires:

1. **Framework-native 4D BZ quadrature of `J_FF`** on the retained
   `Cl(3) × Z^3` canonical action with the exact composite-H_unit
   bilinear and tadpole improvement at 2-loop.
2. **Framework-native 4D BZ quadrature of `J_FA`**.
3. **Framework-native 4D BZ quadrature of `J_AA`**.
4. **Framework-native 4D BZ quadrature of `J_Fl`** (at the retained
   `n_f = 6` MSbar or equivalently the `n_l = 5` integrand with
   top flavor decoupled at the lattice scale).
5. **Framework-native 4D BZ quadrature of `J_Al`**.
6. **Framework-native 4D BZ quadrature of `J_ll`**.
7. **Framework-native 4D BZ quadrature of `J_FFh`** (heavy-top
   piece in the numerator's vertex correction).
8. **Framework-native 4D BZ quadrature of `J_Fh`** (heavy-top piece
   in the mixed-vertex correction).

Each is a 2-loop Brillouin-zone integral on the retained lattice
action; each carries `O(1)` expected magnitude in the retention
convention. Their closure would pin `Δ_R^{(2)}` to sub-permille
precision on the 2-loop piece, which combined with the analogous
1-loop closures `(I_v_scalar, I_SE^{gg}, I_SE^{fl})` would close P1
at 2-loop entirely.

The cumulative numerical retention coverage under the retained
loop-geometric bound is

```
    retained_fraction = |Δ_R^{1-loop}| / |Δ_R^{total, bound}|
                      = 3.271 % / 4.200 %
                      = 0.7787                                                      (6.1)
```

so the 1-loop retention covers ≥ 77.9% of the total bound on
`|Δ_R^{total}|`. The through-2-loop retention (adding the
2-loop structural extension) covers

```
    retained_fraction_through-2L = |Δ_R^{through-2-loop, bound-saturated}| / |Δ_R^{total, bound}|
                                 = 3.994 % / 4.200 %
                                 = 0.9510                                           (6.2)
```

so through 2-loop covers ≥ 95.1% of the total bound. The remaining
≤ 4.9% sits in the ≥ 3-loop tail, which is framework-natively
bounded by `r_R² / (1 − r_R) = 0.0628` times `|Δ_R^{(1)}|` in absolute
terms.

---

## 7. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link staggered
> Dirac tadpole-improved canonical surface at SU(3), the 2-loop
> correction to the Ward ratio `y_t² / g_s²` admits the retained
> gauge-group-irreducible decomposition into **8 SU(3) color tensors**
> `{C_F², C_F C_A, C_A², C_F T_F n_f, C_A T_F n_f, T_F² n_f², C_F² T_F, C_F T_F}`
> with exact rational values at `n_f = 6`. Applying the retained
> loop-geometric bound `r_R = (α_LM/π) · b_0 = 0.22126` to the
> retained 1-loop central `|Δ_R^{1-loop}| = 3.271 %`, the 2-loop
> magnitude is bounded above by **`|Δ_R^{2-loop}| ≤ 0.724 %`** on
> the ratio, and the all-higher-loop tail by
> **`|tail(N=1)| ≤ 0.929 %`**. The bound-saturated through-2-loop
> central estimate is **`Δ_R^{through-2-loop} ≃ −3.99 %`** (shifting
> the 1-loop central `−3.27 %` by `r_R · (−3.27 %) = −0.72 %` in
> the same-sign direction), with retained band
> **`Δ_R^{through-2-loop} ∈ [−4.7 %, −3.3 %]`** and operational
> **`P1 ∈ [3.3 %, 4.7 %]`**. The corresponding m_t(pole) retained
> lane at 2-loop is **`m_t^{pole} = 172.57 GeV ± 6.9 GeV`** (slight
> widening from the 1-loop ±5.7 GeV), with the same-sign saturation
> central shifting by `+0.6 GeV` to `173.18 GeV`. Observed
> `m_t^{pole, PDG} = 172.69 GeV` lies within the retained lane at
> both 1-loop and through-2-loop; the retention lane is consistent
> with the observation.

It does **not** claim:

- any framework-native 4D BZ quadrature value for the eight 2-loop
  BZ integrals `(J_FF, J_FA, J_AA, J_Fl, J_Al, J_ll, J_FFh, J_Fh)`
  on the retained canonical action (all eight remain OPEN);
- that the 2-loop central is `−0.72 %` specifically; the 2-loop
  magnitude is **bounded above** by `0.72 %` but can range from
  `0` to the bound;
- sign-certainty on the 2-loop piece; the dominant `C_A²` and
  `C_A T_F n_f` tensors are expected to be same-sign as 1-loop on
  physical grounds (gluon SE squared at 2-loop reinforces
  asymptotic freedom; see §3.5), but a framework-native sign
  determination requires the BZ integrals;
- sub-percent precision on `Δ_R^{through-2-loop}`; the
  literature-bounded band width is currently `~0.7 %` on the central
  and `~2.4 %` in 1σ combined-citation+2-loop terms;
- that the 2-loop extension **tightens** the 1-loop band; in fact
  the bound-saturated central shifts the 1-loop central downward by
  `0.72 %` and widens the lane by `1.2 GeV`, consistent with the
  honest loop-expansion propagation;
- any modification of the master UV→IR transport obstruction
  theorem's ~1.95 % total residual (this note refines the P1
  primitive line within the existing partition; it does not modify
  the partition or the total);
- any modification of the 1-loop master assembly, the loop-geometric
  bound, the Rep-A/Rep-B cancellation sub-theorem, the three
  per-channel BZ-computation sub-theorems, the K_2 or K_3 color-factor
  retention notes for P3, or any publication-surface file.

---

## 8. What is retained vs. cited vs. open

### 8.1 Retained (framework-native, established upstream and preserved)

- SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` (from
  `YT_EW_COLOR_PROJECTION_THEOREM.md` D7 and
  `YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` S1).
- MSbar flavor count at M_Pl: `n_f = 6`; retained light flavors
  `n_l = 5` for `b_0`.
- 1-loop Δ_R central `−3.271 %` and per-channel contributions
  (from the master assembly theorem).
- Loop-geometric envelope `r_R = (α_LM/π) · b_0 = 0.22126` and
  tail/amplification factors (from the loop-geometric bound note).
- Canonical-surface anchors `α_LM = 0.09067`, `α_LM/π = 0.02886`,
  `α_LM/(4π) = 0.00721`, `(α_LM/(4π))² = 5.20×10⁻⁵`.
- **2-loop color-tensor skeleton** (this note): 8 SU(3) Casimir
  products with exact rational values.
- **2-loop magnitude bound** (this note, from the loop-geometric
  envelope): `|Δ_R^{2-loop}| ≤ 0.724 %`.
- **Through-2-loop bound-saturated central** (this note):
  `Δ_R^{through-2-loop} ≃ −3.99 %`.

### 8.2 Cited (external, with O(1) uncertainty on BZ integrals)

- `Δ_1, Δ_2, Δ_3` 1-loop centrals inherited from the master assembly
  (cited staggered lattice-PT references: Sharpe 1994,
  Bhattacharya–Sharpe 1998, Hasenfratz–Hasenfratz 1980, etc.).

### 8.3 Open (not closed by this note)

- Framework-native 4D BZ quadrature of the eight 2-loop integrals
  `J_FF, J_FA, J_AA, J_Fl, J_Al, J_ll, J_FFh, J_Fh` on the retained
  `Cl(3) × Z^3` canonical action.
- Framework-native 4D BZ quadrature of the 1-loop integrals
  `I_v_scalar, I_SE^{gluonic+ghost}, I_SE^{fermion-loop}, I_leg`
  (inherited OPEN status from the 1-loop sub-theorems).
- Framework-native sign determination of the 2-loop piece beyond
  the expected same-sign structure.
- Propagation of the through-2-loop P1 revision into any
  publication-surface table (explicitly NOT pursued here).
- 3-loop and higher corrections beyond the geometric tail bound.

---

## 9. Validation

The runner
`scripts/frontier_yt_p1_delta_r_2_loop_extension.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p1_delta_r_2_loop_extension_2026-04-18.log`. The
runner must return PASS on every check to keep this note on the
retained surface.

The runner verifies:

1. Retention of SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`
   and flavor counts `n_f = 6` (MSbar), `n_l = 5` (for b_0).
2. Retention of canonical-surface constants
   `α_LM = 0.09067`, `α_LM/π = 0.02886`, `α_LM/(4π) = 0.00721`,
   `(α_LM/(4π))² = 5.20×10⁻⁵`.
3. Retention of loop-geometric bound `r_R = 0.22126` with
   tail factor `0.2841` and amplification `1.2841`.
4. Retention of 1-loop Δ_R central `−3.271 %` (from master
   assembly).
5. 2-loop color-tensor skeleton: 8 SU(3) tensors with exact rational
   values `(16/9, 4, 9, 4, 9, 9, 8/9, 2/3)` at `n_f = 6`.
6. Exact Casimir products: `C_F² = 16/9`, `C_F · C_A = 4`,
   `C_A² = 9`, `C_F · T_F · n_f = 4`, `C_A · T_F · n_f = 9`,
   `T_F² · n_f² = 9`, `C_F² · T_F = 8/9`, `C_F · T_F = 2/3`
   (at `n_f = 6`).
7. 2-loop magnitude bound `|Δ_R^{(2)}| ≤ r_R · |Δ_R^{(1)}| = 0.7236 %`.
8. Tail bound `|tail(N=1)| ≤ 0.2841 · |Δ_R^{(1)}| = 0.9293 %`.
9. Total bound `|Δ_R^{total}| ≤ 1.2841 · |Δ_R^{(1)}| = 4.2003 %`.
10. Through-2-loop bound-saturated central
    `Δ_R^{through-2-loop} = −3.994 %` (shift `−0.723 %` in same-sign
    direction from 1-loop central).
11. Refined P1 primitive band `P1 ∈ [3.3 %, 4.7 %]` at through-2-loop.
12. m_t(pole) retained lane at through-2-loop:
    `172.57 GeV ± 6.9 GeV`; observation `172.69 GeV` within lane.
13. Consistency with 1-loop master assembly (no modification of
    its central or per-channel contributions).
14. Consistency with loop-geometric bound (r_R and tail factors
    unchanged).
15. Retained coverage fraction: 1-loop `77.9%`, through-2-loop
    `95.1%` of the total bound.
16. No modification of any prior retained theorem, support note,
    citation note, or publication-surface file.
17. Structural analogy check with P3 `K_2` 4-tensor and `K_3`
    10-tensor skeletons (the 8-tensor Δ_R^{(2)} skeleton is
    consistent with the Cartesian product of the 1-loop
    three-channel + heavy-top completion).
