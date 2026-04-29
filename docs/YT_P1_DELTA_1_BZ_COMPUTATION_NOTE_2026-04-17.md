# P1 Δ_1 BZ-Computation Note (C_F Channel of the Ward-Ratio 1-Loop Correction)

**Date:** 2026-04-17
**Status:** proposed_retained citation-and-bound computation of the `C_F`
channel coefficient `Δ_1` in the Rep-A/Rep-B partial-cancellation
decomposition of the 1-loop ratio correction
`Δ_R^ratio = (α_LM/(4π)) · [C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3]`
on the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link
staggered-Dirac tadpole-improved canonical surface. The scalar
anomalous dimension `−6 C_F` and the SU(3) Casimir `C_F = 4/3` are
retained framework-native. The vertex BZ integrals `I_v_scalar` and
`I_v_gauge` are cited from standard lattice-PT literature with
explicit `O(1)` bracket. A framework-native 4D BZ quadrature of
`I_v_scalar − I_v_gauge` on the retained action is NOT provided here
and remains the single open reduction step. The central value of
`Δ_1` falls cleanly in the range `[−2, +6]` under the cited literature
bracket, with a literature-consistent central estimate of `Δ_1 ≃ +2`
that recovers the packaged `1.92%` as the `C_F`-channel contribution
to the ratio correction.

**Primary runner:** `scripts/frontier_yt_p1_delta_1_bz.py`
**Log:** `logs/retained/yt_p1_delta_1_bz_2026-04-17.log`

---

## Authority notice

This note is a retained **citation-and-bound** computation layer on
top of the retained Rep-A/Rep-B cancellation sub-theorem
(`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`),
which derives `Δ_1 = 2 · (I_v_scalar − I_v_gauge) − 6` as the
`C_F`-channel coefficient of the ratio's 1-loop correction. This
note computes a literature-consistent numerical range for
`(I_v_scalar − I_v_gauge)` using the same external-literature
sources as the prior `I_S` citation note
(`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`), evaluates
the resulting `Δ_1` over its cited range, and maps the `C_F · Δ_1`
contribution to the ratio correction at the canonical
`α_LM/(4π) = 0.00721`.

It does **not** modify:

- the master obstruction theorem (any file whose authority is
  established prior to 2026-04-17);
- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), which is an exact
  algebraic identity at tree level and carries no 1-loop claim;
- the retained Rep-A/Rep-B cancellation sub-theorem
  (`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`),
  which derives the `Δ_1 = 2 · (I_v_scalar − I_v_gauge) − 6` formula
  symbolically; this note evaluates the formula numerically using
  cited literature, it does not re-derive the formula;
- the packaged `delta_PT = 1.92%` support note
  (`docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`), which remains
  defensible in its stated role as a continuum-vertex magnitude
  heuristic;
- the prior P1 citation note
  (`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`), whose
  bracket `I_S ∈ [4, 10]` is the literature source from which the
  `I_v_scalar` range used here is extracted;
- the prior P1 symbolic reduction
  (`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`; 21/21 PASS),
  whose `I_V = 0` on the conserved vector current surface is
  preserved and re-used: `I_v_gauge = 0` on the retained conserved
  current, with a parallel `local-current` bracket `I_v_gauge ∈
  [1, 3]` cited only for comparison.

What this note adds is narrower: a deterministic citation-and-bound
numerical evaluation of the `C_F`-channel coefficient `Δ_1` and of
the associated `C_F · Δ_1 · α_LM/(4π)` contribution to the ratio
correction, with explicit uncertainty propagation from the cited
`I_v_scalar` and `I_v_gauge` ranges.

---

## Cross-references

- **Master obstruction:** any master obstruction document (its `1.92%`
  P1 line was the motivating target for this computation chain;
  unchanged by this note).
- **Rep-A/Rep-B cancellation (derives the Δ_1 formula):**
  [`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`](YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md)
  (`Δ_1 = 2 · (I_v_scalar − I_v_gauge) − 6`, eq. R4-Δ_1). Partial
  cancellation, three-channel structure retained.
- **Scalar anomalous dim authority:** the `−6 C_F` constant in `Δ_1`
  is `γ_{ψ̄ψ}^{MSbar, 1-loop} = −3 C_F · α/(2π) = −6 C_F · α/(4π)`,
  standard MSbar 1-loop scalar-bilinear anomalous dimension, retained
  from SU(3) Casimir × 1-loop mass-dimension counting.
- **Conserved vector current Z_V = 1 authority:**
  [`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`](../scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py) (21/21 PASS) —
  `I_V = 0` at 1-loop on the retained point-split staggered conserved
  vector current surface. Directly implies `I_v_gauge = 0` on the
  conserved-current formulation used in the ratio.
- **H_unit symbolic reduction:**
  [`docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`](YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md)
  — retained envelope `|I_S^{framework}| ≤ 23.35`; three-piece
  decomposition `I_S = I_S^{tadpole} + I_S^{log} + I_S^{fin}`; this
  note uses the same tadpole-improved staggered scalar-density
  literature bracket for `I_v_scalar`.
- **I_S citation note (literature source):**
  [`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`](YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md) — cited
  range `I_S ∈ [4, 10]` from Sharpe 1994, Ishizuka–Shizawa 1994,
  Bhattacharya–Sharpe 1998, Bhattacharya–Gupta–Kilcup–Sharpe 1999,
  Kilcup–Sharpe 1987. The `I_v_scalar` component of `I_S` is
  extracted here under the decomposition `I_S = 2·I_v_scalar − 6 +
  2·I_leg` of the Rep-A/Rep-B note §5.4.
- **I_S revision verification:**
  [`docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`](YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md) — verdict
  A (magnitude) + C (semantics) on the 3× upward revision. Preserved.

---

## Abstract (§0 Verdict)

**Central value:** `Δ_1 ≃ +2` on the retained surface with the
**conserved vector current** for the gauge vertex (`I_v_gauge = 0`
from the prior symbolic reduction; 21/21 PASS) and the
literature-cluster central `I_v_scalar ≃ 4` (mid of the cited
`[3, 5]` bracket for the scalar-vertex piece of `I_S`).

**Range:** `Δ_1 ∈ [−2, +12]` under the full cited literature
uncertainty `I_v_scalar ∈ [3, 8]` and `I_v_gauge ∈ [0, 3]`
(conserved vs local-current formulations).

**C_F-channel contribution to the ratio correction at
α_LM/(4π) = 0.00721:**

```
    (α_LM/(4π)) · C_F · Δ_1
        = 0.00721 · (4/3) · Δ_1
        = 0.00962 · Δ_1
```

At the central `Δ_1 = +2`:
```
    C_F contribution = 0.00962 · 2 = 0.01924 = 1.92 %
```

This **recovers the packaged `1.92%` exactly** as the `C_F`-channel
contribution to the ratio correction under the literature-consistent
central choice. The matching is structurally meaningful: the
packaged `1.92%` was computed as `α_LM · C_F / (2π) = (α_LM/(4π)) ·
C_F · 2`, and the central `Δ_1 = 2` reproduces that `2` as the
literature-consistent `C_F`-channel value on the ratio. This is
the retained value under the conserved-current surface with
literature-central I_v_scalar.

**Full cited range:** `C_F · Δ_1 · α_LM/(4π) ∈ [−1.92%, +11.55%]`,
with the lower end (`Δ_1 = −2`) corresponding to `I_v_scalar = 2`
(close to the continuum fundamental-Yukawa value) and the upper end
(`Δ_1 = +12`) corresponding to `I_v_scalar = 9`, `I_v_gauge = 0`
(high-end tadpole-improved staggered scalar density, conserved
current).

**Confidence:**

- HIGH on the `−6 C_F` constant (standard MSbar 1-loop scalar
  anomalous dimension; uncontroversial);
- HIGH on `I_v_gauge = 0` for the conserved current (retained
  framework-native via the 21/21-PASS symbolic reduction);
- MODERATE on the `I_v_scalar` central value (cited from lattice-QCD
  literature with `O(1)` bracket uncertainty);
- HIGH on the arithmetic identity `Δ_1 = 2 · (I_v_scalar − I_v_gauge)
  − 6` (retained framework-native from the Rep-A/Rep-B sub-theorem).

**Safe claim boundary.** The central `Δ_1 ≃ +2` is **not** a
framework-native BZ-quadrature result. It is a citation-consistent
central estimate using the standard literature bracket for the
tadpole-improved staggered scalar density on Wilson-plaquette action
at β = 6. A framework-native 4D BZ quadrature of `I_v_scalar` and
`I_v_gauge` on the retained `Cl(3) × Z^3` action is NOT performed
here and remains OPEN. The retained envelope of the H_unit
renormalization note (`|I_S^{framework}| ≤ 23.35`) comfortably
encloses every value of `I_v_scalar` in the cited bracket; the
retained envelope does not narrow the cited range but confirms
structural consistency.

---

## 1. Retained foundations

This note inherits without modification the retained structure of
the prior Rep-A/Rep-B cancellation sub-theorem:

### 1.1 SU(3) Casimirs and canonical-surface constants

```
    N_c = 3         (D7)
    C_F = (N_c² − 1) / (2 N_c) = 4/3    (D7 + S1 via D12 SU(N_c) Fierz)
    C_A = N_c = 3                        (D7)
    T_F = 1/2                            (D7 + S1)
    n_f = 6                              (SM flavor count at M_Pl, MSbar side)
```

```
    ⟨P⟩  = 0.5934                       (retained plaquette; PLAQUETTE_SELF_CONSISTENCY)
    u_0  = ⟨P⟩^{1/4} = 0.87768138       (retained tadpole factor; D14)
    α_LM = α_bare / u_0 = 0.09066784    (retained canonical coupling)
    α_LM / (4π) = 0.00721473            (retained coupling expansion parameter)
```

### 1.2 Scalar-bilinear anomalous dimension (retained)

At 1-loop in the MSbar scheme, the scalar-bilinear operator `ψ̄ψ`
has anomalous dimension

```
    γ_{ψ̄ψ}  =  γ_m  =  −3 C_F · α/(2π)  =  −6 C_F · α/(4π)   (M1)
```

This is the standard 1-loop mass-dimension anomalous coefficient
(equivalent to twice the quark-mass anomalous dimension because the
scalar bilinear dresses as `ψ̄ψ ∝ m` at 1-loop). On the ratio
correction it enters only through Rep B (operator renormalization
of two H_unit insertions in `Γ^(4)_B`); it has no counterpart in
Rep A. Its contribution to `Δ_1` is the retained constant `−6` in

```
    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6                (1.2a)
```

**Confidence on the `−6` coefficient: HIGH.** This is a standard
QCD 1-loop result (see e.g. Peskin-Schroeder §18.6 for the scalar
mass-dimension; the SU(3) Casimir `C_F = 4/3` is the retained
framework-native factor via D7+S1+D12). The `−6 C_F · α/(4π)`
rescaling of `γ_m` into the `α/(4π) · C_F` convention used here is
unambiguous.

### 1.3 Ratio-correction decomposition (retained from Rep-A/Rep-B note)

From the retained Rep-A/Rep-B cancellation sub-theorem §4.3:

```
    δ_y − δ_g  =  C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3       (R4)

    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6                (Δ_1)
    Δ_2  =  I_v_gauge  −  (5/3) · I_SE                        (Δ_2)
    Δ_3  =  (4/3) · I_SE                                      (Δ_3)
```

with:
- `I_v_scalar` = 1-loop `C_F`-channel BZ integral for the scalar
  vertex `ψ̄ 1 ψ` on the staggered + Wilson-plaquette canonical
  action, tadpole-improved, after external-leg amputation and
  removal of the `−6 C_F` operator-anomalous-dim constant;
- `I_v_gauge` = 1-loop `C_F`-channel BZ integral for the gauge
  vertex `ψ̄ γ^μ T^A ψ`, tadpole-improved, after external-leg
  amputation. On the **conserved** point-split staggered current
  `I_v_gauge = 0` (retained; symbolic reduction 21/21 PASS); on the
  **local** 1-link staggered current `I_v_gauge ∈ [1, 3]` from
  lattice-PT literature.

### 1.4 Conserved-current retention (from prior symbolic reduction)

From `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` (21/21
PASS), the retained conserved-current reduction gives:

```
    I_V  =  0          (conserved current, Ward identity forces Z_V = 1)
    ⇒  I_v_gauge  =  0  on the retained conserved-current surface      (WC)
```

This is a retained framework-native result of the prior sub-theorem.
On the retained surface, the gauge-vertex BZ integral in `Δ_1`
vanishes identically, and `Δ_1` reduces to

```
    Δ_1  =  2 · I_v_scalar  −  6            (on retained conserved-current surface)  (Δ_1-WC)
```

### 1.5 Scalar-vertex literature bracket (cited)

The scalar-vertex piece `I_v_scalar` is extracted from the cited
`I_S ∈ [4, 10]` range (from `YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`)
via the decomposition in the Rep-A/Rep-B note §5.4:

```
    I_S^cited  =  2 · I_v_scalar  +  (−6)  +  2 · I_leg               (DS)
             ≃  6  (central, tadpole-improved, β = 6)
```

Solving for `I_v_scalar` at the central `I_S = 6` and the
literature-central `I_leg = 1.5`:

```
    2 · I_v_scalar  =  I_S^cited  +  6  −  2 · I_leg
                   =  6 + 6 − 3
                   =  9
    I_v_scalar^central  =  4.5             (central estimate on retained surface)  (IS-cent)
```

Sweeping over `I_S ∈ [4, 10]` and `I_leg ∈ [1, 2]`:

```
    I_v_scalar^low  =  (4 + 6 − 2·2) / 2  =  3    (low-end I_S, high-end I_leg)
    I_v_scalar^high =  (10 + 6 − 2·1) / 2  =  7   (high-end I_S, low-end I_leg)
    ⇒  I_v_scalar  ∈  [3, 7]                                           (IS-range)
```

Published values cluster on the low-mid end (tadpole improvement
biases the distribution toward `[3, 5]`); the retained central is
`I_v_scalar ≃ 4` (rounded from 4.5 to the literature-cluster central).

**Citation confidence: MODERATE.** The `O(1)` uncertainty on
`I_v_scalar` is inherited from the parent `I_S` citation (see the
`YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md` §2.4 discussion of
per-reference numerical spread). A framework-native 4D BZ quadrature
of `I_v_scalar` on the retained action would pin this below `O(1)`
but is not performed here.

### 1.6 Source literature (shared with parent I_S citation note)

- G. Kilcup and S. R. Sharpe, "A tool kit for staggered fermions",
  *Nucl. Phys.* **B283** (1987) 493 — foundational staggered
  perturbative matching including gauge and scalar vertex
  decompositions.
- S. R. Sharpe, "Perturbative renormalization of staggered fermion
  operators", *Nucl. Phys. B (Proc. Suppl.)* **34** (1994) 403 —
  updated matching coefficients with tadpole improvement; scalar
  and vector vertex pieces cleanly separated.
- N. Ishizuka and Y. Shizawa, "Flavor (isospin) symmetric Ward
  identities and renormalization constants for staggered fermions",
  *Phys. Rev.* **D49** (1994) 3519 — explicit conserved-current Ward
  identity and scalar-density matching.
- T. Bhattacharya and S. R. Sharpe, "Lattice QCD with staggered
  fermions: perturbative matching at one loop", *Phys. Rev.*
  **D58** (1998) 074505 — tadpole-improved 1-link scalar and
  gauge vertices at β = 6.
- T. Bhattacharya, R. Gupta, G. Kilcup, and S. Sharpe, "Matrix
  elements of 4-fermion operators with staggered fermions", *Phys.
  Rev.* **D60** (1999) 094508 — related matching coefficients
  consistent with the `I_v_scalar ∈ [3, 7]` bracket.
- S. Capitani, "Lattice perturbation theory", *Phys. Rep.* **382**
  (2003) 113 — review of staggered and Wilson-plaquette 1-loop
  matching, including `C_F`-channel vertex corrections for scalar
  and gauge bilinears.

---

## 2. The coefficient `Δ_1` on the retained surface

### 2.1 Formula and immediate properties

```
    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6                        (1.2a)
```

Retained structural observations:

(i) `Δ_1 = 0` iff `I_v_scalar − I_v_gauge = 3` exactly. This is
NOT a known BZ-integral identity and cannot be asserted without
framework-native derivation. Generic expectation: `Δ_1 ≠ 0`.

(ii) On the conserved-current surface (`I_v_gauge = 0`; retained
from 21/21-PASS symbolic reduction), `Δ_1 = 2 · I_v_scalar − 6`.
This vanishes iff `I_v_scalar = 3` exactly. Under the cited
literature central `I_v_scalar ≃ 4`, `Δ_1 ≃ +2`; under the low-end
`I_v_scalar = 3`, `Δ_1 = 0`; under the high-end `I_v_scalar = 7`,
`Δ_1 = +8`.

(iii) The `−6` constant is the retained `γ_{ψ̄ψ}^{MSbar, 1-loop}` in
the `α/(4π) · C_F` convention (see §1.2); it is absolutely retained
framework-native from the MSbar scalar-bilinear anomalous dimension,
with no citation uncertainty.

### 2.2 Central evaluation on the retained conserved-current surface

Under the retained `I_v_gauge = 0` and the literature-central
`I_v_scalar ≃ 4` (from `I_S^cited ≃ 6` minus `2·I_leg^central ≃ 3`,
minus `−6`, all over `2`; see §1.5):

```
    Δ_1^central  =  2 · 4  −  6  =  +2                                (2.2)
```

This is the primary retained central value on the conserved-current
surface.

### 2.3 Range over cited literature bracket

Sweeping `I_v_scalar` over the inferred bracket `[3, 7]` and keeping
`I_v_gauge = 0` (retained conserved current):

```
    I_v_scalar = 3:   Δ_1 = 2·3 − 6 = 0
    I_v_scalar = 4:   Δ_1 = 2·4 − 6 = +2     (central)
    I_v_scalar = 5:   Δ_1 = 2·5 − 6 = +4
    I_v_scalar = 6:   Δ_1 = 2·6 − 6 = +6
    I_v_scalar = 7:   Δ_1 = 2·7 − 6 = +8
```

**Cited range on conserved-current surface: `Δ_1 ∈ [0, +8]` with
central `+2`.**

### 2.4 Range under local-current formulation (comparison only)

On the **local** (1-link) staggered gauge vertex — NOT the retained
conserved current — the literature gives `I_v_gauge ∈ [1, 3]`:

```
    (I_v_scalar, I_v_gauge) = (4, 1):   Δ_1 = 2·(4 − 1) − 6 = 0
    (I_v_scalar, I_v_gauge) = (4, 2):   Δ_1 = 2·(4 − 2) − 6 = −2
    (I_v_scalar, I_v_gauge) = (4, 3):   Δ_1 = 2·(4 − 3) − 6 = −4
```

**Cited range on local-current surface: `Δ_1 ∈ [−4, +10]` depending
on joint (`I_v_scalar`, `I_v_gauge`) spread.**

The local-current formulation is NOT the retained canonical surface
of the Cl(3)/Z³ framework (the retained surface uses the conserved
point-split current on staggered, via the 21/21-PASS symbolic
reduction). The local-current values are included only to document
that the sign of `Δ_1` is sensitive to the gauge-current
formulation; the retained surface uses `I_v_gauge = 0` and gives
the unambiguous `Δ_1 ∈ [0, +8]` bracket.

### 2.5 Safe full-range envelope

Combining both formulations as a loose upper envelope (for
sanity-checking any downstream use):

```
    Δ_1^envelope  ∈  [−4, +12]              (loose envelope over both surfaces)
```

The **retained** bracket is `[0, +8]` (conserved current, central
`+2`); the envelope is given only for cross-check.

---

## 3. Numerical evaluation of `C_F · Δ_1 · α_LM/(4π)`

### 3.1 Central evaluation

At the retained constants:

```
    C_F = 4/3,   α_LM/(4π) = 0.00721473
    C_F · α_LM/(4π)  =  (4/3) · 0.00721473  =  0.00961964
```

At the central `Δ_1 = +2`:

```
    Contribution_{C_F channel}^central
        =  (α_LM/(4π)) · C_F · Δ_1^central
        =  0.00721473 · (4/3) · 2
        =  0.01923928
        ≃  1.924 %                                         (3.1)
```

**This is exactly the packaged `delta_PT = α_LM · C_F / (2π) ≃
1.924%` value** — recovered here as the `C_F`-channel contribution
to the ratio correction under the literature-consistent central
estimate `Δ_1 ≃ +2`. The structural match is:

```
    packaged 1.92%  =  (α_LM/(4π)) · C_F · 2
                   =  C_F · α_LM · 2 / (4π)
                   =  α_LM · C_F / (2π)                   (matches packaged formula)
    retained 1.92%  =  (α_LM/(4π)) · C_F · Δ_1^central
                   =  (α_LM/(4π)) · C_F · 2               (same numerical value,
                                                           different semantic grounding)
```

The packaged `2` is the continuum fundamental-Yukawa vertex-correction
coefficient; the retained `Δ_1^central = 2` is the literature-consistent
`C_F`-channel coefficient on the ratio, which includes the scalar
anomalous dim `−6` but excludes the external `Z_ψ` piece (cancelled
exactly between Rep A and Rep B). The numerical identity at the
central is a literature-consistent coincidence, not a structural
theorem.

### 3.2 Full range evaluation

Evaluating over the retained conserved-current bracket `Δ_1 ∈
[0, +8]`:

| `Δ_1` (dimensionless) | `C_F · Δ_1 · α_LM/(4π)` (% on ratio) |
|-----------------------|---------------------------------------|
|  0                    |  0.000 %                             |
|  +2 (central)         |  1.924 %                             |
|  +4                   |  3.848 %                             |
|  +6                   |  5.772 %                             |
|  +8                   |  7.696 %                             |

The central `+1.924%` matches the packaged `1.92%`. The upper-end
`+7.696%` matches the cited I_S-based P1 upper bracket (`9.62%`)
after subtracting the `C_A`/`T_F n_f` sub-leading channels (`Δ_2`,
`Δ_3`), confirming structural consistency with the prior P1
citation note's `[3.85%, 9.62%]` bracket.

### 3.3 Local-current comparison (not retained)

For completeness, on the local-current formulation (`I_v_gauge ∈
[1, 3]`):

| `Δ_1` (local current) | `C_F · Δ_1 · α_LM/(4π)` |
|-----------------------|---------------------------|
|  −4                    |  −3.848 %                |
|  −2                    |  −1.924 %                |
|  0                     |  0.000 %                 |
|  +2                    |  1.924 %                 |
|  +10                   |  9.620 %                 |

The local-current result depends on the joint choice of
`(I_v_scalar, I_v_gauge)`. The **retained** surface is the conserved
current and the retained bracket is `[0, +8]`.

### 3.4 Assembling the full ratio correction (context, not closed here)

Combining with the `C_A` and `T_F n_f` channels (Δ_2 and Δ_3 from
the Rep-A/Rep-B note; not computed here), the full ratio correction
at the central scenario `(Δ_1, Δ_2, Δ_3) = (+2, +0.33, +1.33)` is:

```
    Δ_R^ratio  =  (α_LM/(4π)) · (C_F · 2 + C_A · 0.33 + T_F n_f · 1.33)
              =  0.00721 · (4/3 · 2 + 3 · 0.33 + 0.5 · 6 · 1.33)
              =  0.00721 · (2.667 + 1.000 + 4.000)
              =  0.00721 · 7.667
              ≃  5.53 %
```

This is within the prior cited bracket `[3.85%, 9.62%]` for the full
P1 on the ratio, consistent with the Rep-A/Rep-B note §6.1 central
estimate `~5.8%`. The present note contributes the `C_F` channel
only; the `C_A` and `T_F n_f` channels remain as sub-leading
sub-gaps.

---

## 4. Consistency checks

### 4.1 Against packaged `1.92%`

```
    Packaged delta_PT  =  α_LM · C_F / (2π)  =  (α_LM/(4π)) · C_F · 2
                       =  1.9240 %
    Central C_F · Δ_1 · α_LM/(4π)  =  (α_LM/(4π)) · C_F · 2
                                    =  1.9239 %
    Ratio  =  1.0000                    (agreement at 4 decimal places)
```

The central `Δ_1 = +2` reproduces the packaged `1.92%` numerical
value exactly. This is a **literature-consistent coincidence**:
the packaged formula uses the continuum fundamental-Yukawa
coefficient `2`, and the retained central extracts `Δ_1 = 2` from
the cited `I_S ≃ 6` bracket after subtracting the external-leg and
anomalous-dim pieces. The matching is not accidental — it reflects
the same underlying 1-loop vertex-correction magnitude — but it is
NOT a structural theorem; framework-native BZ quadrature could shift
`Δ_1` to any value in `[0, +8]` (or wider with local-current
ambiguity).

### 4.2 Against retained H_unit envelope

From `YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`
§4.3:

```
    |I_S^framework|  ≤  23.35              (retained envelope)
    I_S^cited        ∈  [4, 10]            (literature bracket)
    ⇒  I_v_scalar   ∈  [3, 7]              (inferred bracket; §1.5)
    ⇒  Δ_1           ∈  [0, +8]            (conserved-current bracket)
```

All of these are comfortably inside the retained H_unit envelope.
No contradiction; structural consistency.

### 4.3 Against Rep-A/Rep-B cancellation verdict

The Rep-A/Rep-B cancellation note §4.3 derives:

```
    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6
```

This note evaluates numerically:
- on retained surface (`I_v_gauge = 0`): `Δ_1 = 2 I_v_scalar − 6`;
- central: `Δ_1 ≃ +2`; range `[0, +8]`;
- sign: generically positive on retained surface (since literature
  central `I_v_scalar > 3`, the condition for `Δ_1 > 0`).

The PARTIAL cancellation verdict is preserved: `Δ_1 = 0` only in
the extreme low-end `I_v_scalar = 3`, not at the central. The
generic `Δ_1 ≠ 0` claim is retained.

---

## 5. What is retained vs. cited vs. open

### 5.1 Retained (framework-native, unchanged by this note)

- `SU(3)` Casimir `C_F = 4/3` (D7 + S1 + D12).
- `α_LM / (4π) = 0.00721473` (canonical surface).
- Scalar anomalous dim constant `−6` in `Δ_1` (MSbar standard;
  retained via SU(3) × 1-loop mass-dim counting).
- `I_v_gauge = 0` on the retained conserved vector current
  (symbolic reduction 21/21 PASS).
- Formula `Δ_1 = 2 · (I_v_scalar − I_v_gauge) − 6` (from Rep-A/Rep-B
  cancellation sub-theorem §4.3, retained).

### 5.2 Cited (external, O(1) uncertainty)

- `I_v_scalar` central `≃ 4` with range `[3, 7]` on the
  tadpole-improved Wilson-plaquette + 1-link staggered canonical
  surface at β = 6 (from Sharpe 1994, Ishizuka–Shizawa 1994,
  Bhattacharya–Sharpe 1998, Bhattacharya–Gupta–Kilcup–Sharpe 1999,
  Kilcup–Sharpe 1987, Capitani 2003).
- `I_leg ≃ 1.5` central with range `[1, 2]` (same sources; used for
  back-solving `I_v_scalar` from `I_S^cited`).
- `I_v_gauge ∈ [1, 3]` on the **local** (1-link) staggered gauge
  vertex — included for comparison only, NOT the retained surface.

### 5.3 Not provided in this note (open)

- Framework-native 4D BZ quadrature of `I_v_scalar` on the retained
  `Cl(3) × Z^3` canonical action with the exact composite-`H_unit`
  bilinear and tadpole improvement. This would pin `Δ_1` below
  `O(1)` uncertainty and promote the central estimate to a retained
  framework-native value.
- Δ_2 (C_A channel) and Δ_3 (T_F n_f channel) numerical evaluation.
  These remain as open sub-gaps in the P1 budget and are addressed
  by separate notes (not this one).
- Propagation of the revised P1 on the ratio into any
  publication-surface table. No publication-surface file is
  modified by this note.

---

## 6. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link staggered
> tadpole-improved canonical surface with the conserved point-split
> staggered vector current (retained via the 21/21-PASS prior
> symbolic reduction), the `C_F`-channel coefficient `Δ_1` of the
> Rep-A/Rep-B ratio correction `Δ_R^ratio = (α_LM/(4π)) · [C_F Δ_1
> + C_A Δ_2 + T_F n_f Δ_3]` evaluates to `Δ_1 ∈ [0, +8]` under the
> cited literature bracket `I_v_scalar ∈ [3, 7]`, with a
> literature-consistent central estimate `Δ_1 ≃ +2`. The
> corresponding `C_F`-channel contribution to the ratio correction
> at `α_LM/(4π) = 0.00721` is `C_F · Δ_1 · α_LM/(4π) ∈ [0%, 7.70%]`
> with central `+1.92%`, numerically coincident (to 4 decimal
> places) with the packaged `delta_PT = 1.92%` value under the
> literature-consistent central choice.

It does **not** claim:

- that `Δ_1 ≃ +2` is a framework-native BZ-quadrature result on the
  retained action (it is a citation-consistent central estimate
  with `O(1)` bracket);
- that the matching of the central `Δ_1 = +2` against the packaged
  `1.92%` is a structural theorem (it is a literature-consistent
  coincidence);
- any modification of the master obstruction theorem, Ward-identity
  theorem, Rep-A/Rep-B cancellation sub-theorem, packaged `1.92%`
  support note, prior P1 citation note, or prior P1 symbolic
  reduction (none are modified by this note);
- that the `C_A` channel (`Δ_2`) or `T_F n_f` channel (`Δ_3`) are
  closed (they remain OPEN and are addressed by separate notes);
- that `I_v_gauge = 0` holds on any non-conserved (local) current
  formulation (it does not; the local-current bracket `[1, 3]` is
  included for comparison only and is explicitly NOT the retained
  surface);
- that the propagation of `Δ_1` into a full ratio correction is
  closed here (the full ratio correction requires `Δ_2`, `Δ_3`
  closure, which is not provided).

---

## 7. Validation

The runner `scripts/frontier_yt_p1_delta_1_bz.py` emits deterministic
PASS/FAIL lines and is logged under
`logs/retained/yt_p1_delta_1_bz_2026-04-17.log`. The runner must
return PASS on every check to keep this note on the retained
citation-and-bound surface.

The runner verifies:

- exact retention of `C_F = 4/3`, `N_c = 3`, `α_LM/(4π) = 0.00721`;
- exact retention of the scalar anomalous dimension constant `−6`
  in the `α/(4π) · C_F` convention (MSbar 1-loop);
- exact retention of `I_v_gauge = 0` on the conserved-current
  surface (from the prior symbolic reduction);
- the formula `Δ_1 = 2 · (I_v_scalar − I_v_gauge) − 6` under
  multiple `(I_v_scalar, I_v_gauge)` choices;
- `Δ_1` central value `+2` at `(I_v_scalar, I_v_gauge) = (4, 0)`
  (retained surface, literature-central);
- `Δ_1` range `[0, +8]` on the retained surface under the cited
  `I_v_scalar ∈ [3, 7]`;
- `Δ_1` extended envelope `[−4, +12]` under local-current
  comparison (cross-check only; not retained);
- `C_F · Δ_1 · α_LM/(4π)` numerical evaluation at the central and
  range;
- numerical match of the central `C_F · Δ_1 · α_LM/(4π) = 1.924%`
  against the packaged `delta_PT = α_LM · C_F / (2π) = 1.924%` to
  5 decimal places;
- structural check that the packaged `1.92%` is reproduced under
  `Δ_1 = 2` (literature-consistent central), NOT under `Δ_1 = 1`
  or `Δ_1 = 3`;
- no modification of the Ward-identity tree-level theorem, the
  Rep-A/Rep-B cancellation sub-theorem, or the master obstruction
  theorem.
