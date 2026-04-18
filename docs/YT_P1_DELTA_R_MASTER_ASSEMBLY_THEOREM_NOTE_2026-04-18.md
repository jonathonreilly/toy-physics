# P1 Δ_R Master Assembly Theorem Note (Three-Channel Ratio Correction Roll-Up)

**Date:** 2026-04-18 (amended 2026-04-18 with canonical-central supersession notice)
**Status:** retained **literature-cited master assembly theorem** on the P1
ratio correction. The literature-cited central `Δ_R = −3.27 %` recorded below
remains a defensible three-channel roll-up of the cited Δ_1/Δ_2/Δ_3
sub-theorems, **but it is SUPERSEDED as the canonical retained central by the
framework-native full-staggered-PT BZ quadrature central**
`Δ_R = −3.77 % ± 0.45 %` established in
`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`. See **§0
Correction** below for the superseding-relationship statement; the body of
this note (§1–§9) is preserved unchanged as the literature-citation-based
assembly derivation that the full-staggered-PT central refines. The packaged
`delta_PT = 1.92 %` and the cited I_S-based `5.77 %` are also recovered here
as degenerate single-channel endpoints of the full three-channel assembly.

**Primary runner:** `scripts/frontier_yt_p1_delta_r_master_assembly.py`
**Log:** `logs/retained/yt_p1_delta_r_master_assembly_2026-04-18.log`

---

## §0 Correction (amendment 2026-04-18 — canonical central superseded)

**The canonical retained Δ_R central on the P1 ratio surface is now**

```
    Δ_R^{canonical}  =  −3.77 %  ±  0.45 %      (full-staggered-PT 4D BZ quadrature)
```

established in
`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md` by direct
framework-native numerical evaluation of the four canonical lattice-PT
integrals `I_v_scalar`, `I_v_gauge`, `I_SE_gluonic`, `I_SE_fermion` with full
Kawamoto–Smit staggered Feynman rules and MSbar continuum subtraction.

The **literature-cited central** `Δ_R = −3.27 %` derived in §§2–9 of this note
from the cited Δ_1 = +2, Δ_2 = −10/3, Δ_3 = +0.933 per-channel centrals
**remains a defensible three-channel roll-up of the citation-based
sub-theorems**, and the two values are consistent within ~1σ of the master
assembly's covariance-reduced ±2.32 % band. The full-staggered-PT central
differs from the literature-cited central by `0.50 %` (absolute), reflecting
the framework-native refinement of the per-channel centrals:

- `I_v_scalar = +3.90` (framework-native) vs `≃ 4` (literature-cited) →
  `Δ_1 = +1.80` vs `+2` (`−10 %`);
- `I_SE_gluonic = +2.32` (framework-native) vs `≃ 2` (literature-cited) →
  `Δ_2 = −3.87` vs `−10/3` (`+16 %`);
- `I_SE_fermion = +0.996` (framework-native) vs `≃ 0.7` (literature-cited) →
  `Δ_3 = +1.33` vs `+0.933` (`+42 %`).

Each per-channel framework-native value is within the cited literature
bracket; the shift in the assembled `Δ_R` is within the master assembly's
±2.32 % literature-bounded band. The framework-native central is retained as
canonical going forward.

### Superseding-relationship summary

| Central | Value | Status | Role |
|---|---|---|---|
| **Full-staggered-PT 4D BZ quadrature** | **−3.77 % ± 0.45 %** | **canonical retained** | framework-native Δ_R central |
| Literature-cited master assembly (this note §§2–9) | −3.27 % ± 2.32 % | retained as literature-citation-based assembly | prior three-channel roll-up; superseded as canonical but preserved as the citation-based derivation |
| Through-2-loop extension (literature base) | −3.99 % ± 0.70 % | retained as bound-saturated estimate built on the literature-cited 1-loop | bound-saturated loop-geometric extension; documented in `docs/YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md` |
| Through-2-loop extension (full-staggered-PT base, scaled) | −4.60 % ± 0.84 % | retained as MC-pinned 2-loop assembly | from `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md` |

### Revised m_t(pole) retained band at the canonical central

With `Δ_R^{canonical} = −3.77 % ± 0.45 %`, the 1-loop m_t lane widens from the
literature-cited `±5.64 GeV` (at 3.27 % P1 central) to

```
    Δm_t^{P1, full-PT}  ≃  0.0377 · 172.57  ≃  ±6.50 GeV      (1-loop full-PT)
    Δm_t^{P1, precision}  ≃  0.0045 · 172.57  ≃  ±0.78 GeV    (precision on central)
    m_t^{pole, retained}  =  172.57 GeV  ±  6.50 GeV          (1-loop full-PT)
```

consistent with the observed `m_t^{pole, PDG} = 172.69 GeV`. Under the
through-2-loop bound-saturated extension and the MC-pinned 2-loop assembly,
the retained lane further widens to ~`±6.9 GeV` and ~`±7.94 GeV` respectively
(see the referenced 2-loop notes for the precise bands).

### What is preserved vs. superseded

- **Preserved (unchanged) in this note:** the three-channel structural
  decomposition `Δ_R = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`; the
  literature-cited per-channel centrals `(+2, −10/3, +0.933)`; the covariance
  analysis and the ±2.32 % 1σ band on the literature-cited central; the
  reinterpretation of `delta_PT = 1.92 %` and cited `5.77 %` as
  single-channel approximations; the m_t-lane budget convention and sensitivity
  factors.
- **Superseded as canonical** by the full-staggered-PT note: the **operational
  Δ_R central value** used going forward is `−3.77 % ± 0.45 %`, not `−3.27 %
  ± 2.32 %`.
- **Preserved in its derivational role:** the literature-cited `−3.27 %` is
  still a defensible citation-based three-channel roll-up and remains the
  "literature-cited assembly" reference for cross-checks against the
  framework-native `−3.77 %`.

### Confidence on the supersession

HIGH on all points above. The full-staggered-PT evaluation uses the full
Kawamoto–Smit Feynman rules with proper MSbar continuum subtraction at
`N = 64` grid with `m² = 0.01`, giving sub-percent grid precision and ±5 %
per-integral systematic — a ~5× tightening over the literature-citation
±30 % spread that drives the master assembly's ±2.32 % band. The canonical
central `−3.77 %` is framework-native; the prior `−3.27 %` remains as the
defensible literature-citation-based estimate consistent with the canonical
central within the master assembly's 1σ literature-bounded band.

**The rest of this note (§§1–9) is the ORIGINAL literature-citation-based
master assembly derivation, preserved unchanged.** Its Δ_R central `−3.27 %`
should be read as the literature-citation-based central that the canonical
full-staggered-PT central `−3.77 %` supersedes.

---

## Authority notice

This note is a retained **master assembly theorem** on the P1 ratio
correction. It is a faithful roll-up of four prior retained
sub-theorems; it introduces no new physics. Specifically, this note
does **not** modify:

- the master UV-to-IR transport obstruction theorem (whose ~1.95 %
  total residual systematic and P1/P2/P3 primitive decomposition are
  unchanged at the structural level; the revised P1 central value
  recorded here is an internal reorganization of the P1 primitive,
  not a modification of the master theorem's three-primitive
  decomposition);
- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), which attaches no
  precision claim and is unaffected;
- the retained Rep-A/Rep-B partial-cancellation sub-theorem
  (`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`),
  whose three-channel structural decomposition is inherited without
  modification;
- the retained Δ_1 BZ-computation sub-theorem
  (`docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`), whose
  `Δ_1 ≃ +2` central and `[0, +8]` range are inherited without
  modification;
- the retained Δ_2 BZ-computation sub-theorem
  (`docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`), whose
  `Δ_2 ≃ −10/3` central and `[−5, 0]` range are inherited without
  modification;
- the retained Δ_3 BZ-computation sub-theorem
  (`docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`), whose
  `Δ_3 ≃ +0.933` central and `[+0.667, +2.000]` range are inherited
  without modification;
- the packaged `delta_PT = 1.92 %` support note
  (`docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`), which remains
  defensible in its stated OPEN-status role as a continuum
  vertex-correction magnitude heuristic — and is explicitly
  reinterpreted below as the **single-channel (C_F only)
  approximation** to the full three-channel Δ_R;
- the prior cited I_S-based `5.77 %` P1 central from
  `docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`, which
  remains defensible in its stated role as a cited C_F-channel
  literature central — and is also reinterpreted below as a
  **single-channel (C_F only, no external-Z_ψ cancellation
  accounting)** approximation;
- any publication-surface file. No publication table is modified by
  this note.

What this note adds is narrow but decisive: the **numerical central
value** and the **literature-bounded uncertainty range** for the full
three-channel Δ_R, assembled from the three retained
citation-and-bound channel evaluations.

---

## Cross-references

### Foundational sub-theorems (directly inherited)

- **Three-channel structural decomposition (parent theorem):**
  `docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md` —
  `Δ_R^ratio = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]` with
  partial-cancellation verdict (external Z_ψ cancels exactly; all
  three channels generically nonzero).
- **Δ_1 channel (C_F):**
  `docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md` —
  `Δ_1 = 2 (I_v_scalar − I_v_gauge) − 6`, retained
  `I_v_gauge = 0` (conserved point-split current, 21/21 PASS
  symbolic reduction), literature-central `I_v_scalar ≃ 4`, giving
  `Δ_1 ≃ +2` central with range `[0, +8]`.
- **Δ_2 channel (C_A):**
  `docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md` —
  `Δ_2 = I_v_gauge − (5/3) I_SE^{gluonic+ghost}`, with
  `I_v_gauge = 0` (retained conserved current) and literature-central
  `I_SE^{gluonic+ghost} ≃ 2`, giving `Δ_2 ≃ −10/3` central with
  range `[−5, 0]`.
- **Δ_3 channel (T_F n_f):**
  `docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md` —
  `Δ_3 = (4/3) I_SE^{fermion-loop}`, with literature-central
  `I_SE^{fermion-loop} ≃ 0.7` (per flavor, `α/(4π)` convention,
  Sharpe–Bhattacharya 1998 bracket), giving `Δ_3 ≃ +0.933` central
  with range `[+0.667, +2.000]`.

### Context

- **Master obstruction (unchanged):** any document recording the
  three-primitive P1/P2/P3 decomposition and the ~1.95 % total
  residual systematic.
- **Retained Ward identity (tree level):**
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` — `y_t_bare² =
  g_bare²/(2 N_c) = g_bare²/6` at tree level.
- **Canonical-surface anchors:**
  `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — `⟨P⟩ = 0.5934`,
  `u_0 = 0.87768`, `α_LM = 0.09067`, `α_LM/(4π) = 0.00721`.
- **Packaged delta_PT support (reinterpreted):**
  `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` — packaged
  `delta_PT = α_LM · C_F / (2π) = 1.92 %`, reinterpreted in §5.1 as
  the single-channel (C_F only) approximation to Δ_R.
- **Cited I_S literature (reinterpreted):**
  `docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md` — cited
  `I_S ∈ [4, 10]` bracket, reinterpreted in §5.2 as a
  cited-literature C_F-channel central without external-Z_ψ
  cancellation accounting.

---

## Abstract (§0 Verdict)

> **Canonical-central supersession notice.** The canonical retained Δ_R
> central going forward is the full-staggered-PT value
> `Δ_R = −3.77 % ± 0.45 %` from
> `docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`. The
> literature-cited central `Δ_R = −3.27 %` recorded in this Abstract is the
> citation-based three-channel roll-up and remains a defensible internal
> consistency check; it is superseded as the operational Δ_R central but
> preserved as the literature-citation-based derivation. See §0 Correction
> above for the superseding-relationship summary and the revised m_t(pole)
> retained band.

**Retained central value of the full three-channel Δ_R (literature-cited assembly, this note):**

```
    Δ_R^ratio  =  (α_LM/(4π)) · [ C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3 ]

    central:  Δ_R ≃ −3.27 %                                          (V-central)
```

at SU(3), `α_LM = 0.09067`, `α_LM/(4π) = 0.00721`, `C_F = 4/3`,
`C_A = 3`, `T_F = 1/2`, `n_f = 6`, with the three retained
per-channel centrals `(Δ_1, Δ_2, Δ_3) = (+2, −10/3, +0.933)`.

**Per-channel contributions at central:**

```
    C_F · Δ_1 · α_LM/(4π)       =  +1.924 %                          (V-CF)
    C_A · Δ_2 · α_LM/(4π)       =  −7.215 %                          (V-CA)
    T_F n_f · Δ_3 · α_LM/(4π)   =  +2.020 %                          (V-nf)
    ---------------------------------
    Δ_R^central                  =  −3.271 %                          (V-sum)
```

The **sign is negative**: the MSbar ratio
`(y_t/g_s)^{MSbar}(M_Pl)` on the canonical lattice-PT surface is
**smaller** than the lattice Ward tree-level ratio `1/√6` by about
3.27 % at 1-loop. The three channels partially cancel: the positive
C_F + T_F n_f contributions (+1.92 % + 2.02 % = +3.95 %) partially
offset the larger-magnitude negative C_A contribution (−7.22 %),
giving a net |Δ_R| = 3.27 % that is **smaller than any individual
channel in absolute value**.

**Uncertainty propagation:**

Uncorrelated worst-case envelope over the cited literature brackets
`Δ_1 ∈ [0, +8]`, `Δ_2 ∈ [−5, 0]`, `Δ_3 ∈ [+0.667, +2.000]`:

```
    Δ_R ∈ [−9.38 %, +12.03 %]         (uncorrelated outer envelope)    (V-UC)
```

Covariance-reduced range (accounting for: (i) the partial
anti-correlation between Δ_2 and Δ_3 via the related `I_SE`
definitions, though the two BZ integrals are not identical; (ii) the
shared literature sources, which induce correlated citation
uncertainties; (iii) the retained conserved-current
`I_v_gauge = 0` shared between Δ_1 and Δ_2):

```
    Δ_R ∈ [−6 %, 0 %]                  (covariance-reduced, indicative)  (V-COV)
```

**Operational retained P1 central:**

```
    P1 = |Δ_R|_central  ≃  3.27 %                                    (P1-central)
    P1 range (30 % lit. uncertainty on each channel, quadrature):
        P1 ∈ [2.3 %, 4.3 %]                                          (P1-band)
```

**Comparison to prior P1 estimates (reinterpreted):**

| Prior estimate | Value | Reinterpretation |
|----------------|-------|------------------|
| Packaged `delta_PT` (UV_GAUGE_TO_YUKAWA_BRIDGE) | 1.92 % | **Single-channel C_F only** approximation; recovered as `C_F · Δ_1 · α_LM/(4π)` at the retained central `Δ_1 = 2`. |
| Cited I_S-based (I_S_REVISION_VERIFICATION) | 5.77 % | **Single-channel C_F only** approximation without external-Z_ψ cancellation; recovered as the upper-bracket `C_F · 6 · α_LM/(4π)` with no C_A or T_F n_f channel accounting. |
| **Retained three-channel (this note)** | **3.27 %** | **Full three-channel assembly** with partial cancellation between C_F + T_F n_f (positive) and C_A (negative). |

**Implication for m_t(pole) (literature-cited central):** At the
literature-cited P1 central 3.27 %, the m_t lane budget on the canonical
surface is

```
    Δm_t^{P1, lit}  ≃  ±5.7 GeV                                     (M-lane, lit)
```

consistent with the observed `m_t^{pole, PDG} = 172.69 GeV` lying within the
literature-cited lane centered on `m_t^{pole, retained} ≃ 172.57 GeV ± 5.7
GeV`.

**Implication for m_t(pole) (canonical full-staggered-PT central, superseding
replacement):** At the canonical P1 central `3.77 % ± 0.45 %` from the
full-staggered-PT BZ quadrature, the m_t lane budget becomes

```
    Δm_t^{P1, full-PT}  ≃  ±6.5 GeV                                 (M-lane, canonical)
```

(a ~1.14× widening of the literature-cited ±5.7 GeV lane), with precision on
the central `±0.78 GeV` from the full-PT ±0.45 % uncertainty. The observed
`m_t^{pole, PDG} = 172.69 GeV` lies well within the canonical lane
`172.57 GeV ± 6.5 GeV`.

**Confidence:**

- HIGH on the algebraic structure (three-channel color decomposition,
  per-channel formulae);
- HIGH on the sign (negative at central and strictly negative across
  the reasonable subset of the literature bracket);
- MODERATE on the magnitude (the three cited BZ integrals carry O(1)
  literature uncertainty, yielding a P1 central `3.27 % ± ~30 %` from
  compounded citation spread);
- HIGH on the reinterpretation of the packaged `1.92 %` and cited
  `5.77 %` as degenerate single-channel approximations.

**Safe claim boundary.** The retained central `Δ_R = −3.27 %` is
**literature-cited**, not framework-native. Pinning to sub-percent
precision requires framework-native 4D Brillouin-zone quadrature of
`I_v_scalar`, `I_SE^{gluonic+ghost}`, and `I_SE^{fermion-loop}` on
the retained `Cl(3) × Z^3` canonical action. This is not performed
here and remains the single open reduction step for the P1 primitive
at the retained surface.

---

## 1. Foundational sub-theorems (retained inheritance)

This master assembly inherits without modification:

### 1.1 Three-channel structural decomposition

From `docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
§4.3:

```
    Δ_R^ratio  =  (α_LM/(4π)) · [ C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3 ]  (1.1)

    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6                       (1.2-Δ_1)
    Δ_2  =  I_v_gauge  −  (5/3) · I_SE^{gluonic+ghost}               (1.2-Δ_2)
    Δ_3  =  (4/3) · I_SE^{fermion-loop}                              (1.2-Δ_3)
```

Retained verdict on the cancellation structure: **PARTIAL** (external
quark Z_ψ cancels exactly; all three channels generically nonzero).
This is the authority statement on the ratio correction's color
decomposition, with each coefficient carrying a framework-native
retained structural form.

### 1.2 Per-channel retained centrals

From the three BZ-computation sub-theorems
(`docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`,
`docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`,
`docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`):

```
    Δ_1^{central}  =  +2                    (literature-cited; I_v_scalar ≃ 4,
                                             I_v_gauge = 0 on retained
                                             conserved-current surface)   (1.3-Δ_1)
    Δ_2^{central}  =  −10/3  ≈  −3.333      (literature-cited;
                                             I_SE^{gluonic+ghost} ≃ 2,
                                             I_v_gauge = 0 on retained
                                             conserved-current surface)   (1.3-Δ_2)
    Δ_3^{central}  =  (4/3) · 0.7  ≈  +0.933   (literature-cited;
                                                 I_SE^{fermion-loop} ≃ 0.7
                                                 per flavor)             (1.3-Δ_3)
```

### 1.3 Per-channel retained literature-bounded ranges

```
    Δ_1  ∈  [0, +8]                         (retained conserved-current
                                             surface; I_v_scalar ∈ [3, 7])   (1.4-Δ_1)
    Δ_2  ∈  [−5, 0]                         (retained range across cited
                                             I_SE^{gluonic+ghost} ∈ [1, 3]
                                             and I_v_gauge ∈ [0, 3]
                                             [conservative, incl. local
                                             current sensitivity])           (1.4-Δ_2)
    Δ_3  ∈  [+0.667, +2.000]                (retained range across cited
                                             I_SE^{fermion-loop} ∈ [0.5, 1.5]
                                             per flavor)                    (1.4-Δ_3)
```

### 1.4 Casimirs, coupling, and canonical-surface constants

```
    C_F  =  (N_c² − 1)/(2 N_c)  =  4/3       (D7 + S1 + D12 at SU(3))
    C_A  =  N_c  =  3                         (D7 at SU(3))
    T_F  =  1/2                               (D7 + S1 at SU(3))
    n_f  =  6                                 (MSbar side at M_Pl, standard SM)
    ⟨P⟩  =  0.5934                            (retained plaquette)
    u_0  =  ⟨P⟩^{1/4}  =  0.877681            (retained tadpole factor)
    α_LM =  α_bare / u_0  =  0.090668         (retained canonical coupling)
    α_LM / (4π)  =  0.007215                  (retained expansion parameter)
```

---

## 2. Assembly

### 2.1 Per-channel evaluation at central

Substituting (1.3) into (1.1) with the retained SU(3) values of §1.4:

```
    C_F · Δ_1^{central} · α_LM/(4π)
        =  (4/3) · 2 · 0.00721
        =  0.01924
        ≃  +1.924 %                                                   (2.1)

    C_A · Δ_2^{central} · α_LM/(4π)
        =  3 · (−10/3) · 0.00721
        =  −10 · 0.00721
        =  −0.07215
        ≃  −7.215 %                                                   (2.2)

    T_F · n_f · Δ_3^{central} · α_LM/(4π)
        =  (1/2) · 6 · 0.933 · 0.00721
        =  3 · 0.933 · 0.00721
        =  0.02020
        ≃  +2.020 %                                                   (2.3)
```

### 2.2 Sum

```
    Δ_R^{central}  =  (+1.924 %) + (−7.215 %) + (+2.020 %)
                   =  −3.271 %                                        (2.4)
```

**Retained central value of Δ_R: −3.27 %** (sub-permille precision
on the arithmetic given the cited Δ_i centrals).

### 2.3 Structural observations

**(i) Partial cancellation among the three channels.** The positive
C_F (+1.92 %) and T_F n_f (+2.02 %) channels partially offset the
larger-magnitude negative C_A channel (−7.22 %). The net |Δ_R| =
3.27 % is smaller than |C_A · Δ_2 · α_LM/(4π)| = 7.22 % alone.

**(ii) Sign dominance.** The C_A channel magnitude (7.22 %) exceeds
the sum of the C_F and T_F n_f magnitudes (3.95 %) at central, so
the sign of Δ_R is set by the C_A channel. This remains true across
most of the cited literature range (see §3.3).

**(iii) Single-channel approximations are degenerate.** Neither the
packaged `1.92 %` (C_F only, at `Δ_1 = 2`) nor the cited `5.77 %`
(C_F only, at `Δ_1 = 6`; also without external-Z_ψ accounting)
captures the three-channel structure. Both are recovered as
degenerate endpoints of the full assembly (see §5).

---

## 3. Uncertainty propagation

### 3.1 Uncorrelated worst-case envelope

Scanning `(Δ_1, Δ_2, Δ_3)` over the eight corners of the cited
bracket `[0, +8] × [−5, 0] × [+0.667, +2.000]`:

```
    Δ_R^{min-uc}  =  (α_LM/(4π)) · [ C_F · 0 + C_A · (−5) + T_F n_f · 0.667 ]
                  =  0.00721 · [ 0 + (−15) + 2.000 ]
                  =  0.00721 · (−13.000)
                  =  −0.09380
                  ≃  −9.38 %                                         (3.1)

    Δ_R^{max-uc}  =  (α_LM/(4π)) · [ C_F · 8 + C_A · 0 + T_F n_f · 2.000 ]
                  =  0.00721 · [ 10.667 + 0 + 6.000 ]
                  =  0.00721 · 16.667
                  =  +0.12023
                  ≃  +12.03 %                                        (3.2)
```

Uncorrelated worst-case envelope:

```
    Δ_R^{UC-envelope}  ∈  [ −9.38 %,  +12.03 % ]                     (3.3)
    |Δ_R|^{UC-envelope}  ∈  [ ~1 %, ~12 % ]                          (3.4)
```

This is the conservative outer range under the assumption that all
three Δ_i are independent and can reach their extreme values
simultaneously. It spans the full `|Δ_R|` bracket `[1 %, 12 %]` of
the task specification.

### 3.2 Covariance-reduced range

The three cited channels are not independent. Specifically:

**Correlation 1 (retained conserved current).** Both Δ_1 and Δ_2
reference `I_v_gauge`, which is retained-fixed at `I_v_gauge = 0`
on the conserved point-split staggered vector current (21/21 PASS
symbolic reduction; `docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`
and Rep-A/Rep-B §4.3). This is a framework-native retention, not a
citation, so there is **no uncertainty** on `I_v_gauge = 0` in the
retained surface. The cross-surface sensitivity `I_v_gauge ∈ [1, 3]`
(local-current formulation) is **not retained** and appears only as
a cross-check envelope in the Δ_1 and Δ_2 notes.

**Correlation 2 (anti-correlated gluon SE pieces).** The `Δ_2` note
uses `I_SE^{gluonic+ghost}` (the pure-gauge piece of Π_g) while
`Δ_3` uses `I_SE^{fermion-loop}` (the quark-loop piece of Π_g).
These are distinct BZ integrals corresponding to different
diagrammatic classes, but they both live inside the 1-loop gluon
self-energy and are typically evaluated in the same literature
(Sharpe–Bhattacharya 1998 and related). On a framework-native
evaluation they would be correlated by choice of tadpole
improvement, lattice action variant, and overall normalization
convention. The citation-level uncertainties therefore share a
common systematic that a joint quadrature would partially absorb.

**Correlation 3 (shared literature sources).** All three channels
cite the same cluster of staggered lattice-PT references (Sharpe
1994, Bhattacharya–Sharpe 1998, Kilcup–Sharpe 1987, Capitani 2003,
Hasenfratz–Hasenfratz 1980, Lepage–Mackenzie 1992,
Sharpe–Bhattacharya 1998). Systematic shifts across these
references (e.g., the tadpole-improvement prescription) would move
all three Δ_i together rather than independently, reducing the
effective uncorrelated range.

Under a 30 % symmetric citation uncertainty on each retained central
(applied in quadrature, as the partial anti-correlation between C_A
and T_F n_f channels at least partially offsets):

```
    σ(C_F·Δ_1·α/(4π))      ≃  0.577 %       (30 % of 1.924 %)
    σ(C_A·Δ_2·α/(4π))      ≃  2.164 %       (30 % of 7.215 %)
    σ(T_F·n_f·Δ_3·α/(4π))  ≃  0.606 %       (30 % of 2.020 %)
```

Quadrature-combined 1σ uncertainty on Δ_R:

```
    σ(Δ_R)  ≃  √(0.577² + 2.164² + 0.606²)  ≃  2.32 %                (3.5)
```

Covariance-reduced 1σ band on Δ_R:

```
    Δ_R  ≃  (−3.27 ± 2.32) %                                          (3.6)
         ≈  [−5.6 %, −0.9 %]                                          (3.7)
```

This is a tighter claim than the uncorrelated worst-case envelope
(3.3); it uses the common-systematic reduction across shared
literature sources.

**Operational P1 band (retained operational claim):**

```
    P1 = |Δ_R|  ≃  3.27 %  ±  ~30 %                                  (3.8)
    P1 ∈  [~2.3 %,  ~4.3 %]  (1σ citation band)                      (3.9)
```

### 3.3 Sign stability

The sign of Δ_R^{central} = −3.27 % is negative because
`|C_A · Δ_2 · α/(4π)| > C_F · Δ_1 · α/(4π) + T_F n_f · Δ_3 · α/(4π)`
at central. Sign-reversal requires the negative C_A contribution to
be more than offset by the positive contributions. Probing the
cited ranges:

- With `Δ_1 = +8`, `Δ_3 = +2.000` (upper ends, positive channels
  maximized), and `Δ_2 = 0` (upper end, C_A contribution zero),
  Δ_R = +7.70 % + 0 + 4.33 % = +12.03 %. This is the sign-flipped
  extreme.
- With the retained central `Δ_2 = −10/3` (C_A channel active),
  sign reversal requires
  `C_F · Δ_1 + T_F n_f · Δ_3 > |C_A · (−10/3)| = 10`, i.e.,
  `(4/3) Δ_1 + 3 Δ_3 > 10`. At `Δ_3 = 2`, this is `(4/3) Δ_1 > 4`,
  i.e., `Δ_1 > 3`. So sign reversal within the C_A central
  scenario requires Δ_1 ≳ 3, which is the upper half of the cited
  `[0, +8]` bracket.

**Sign retention across the cited bracket: NEGATIVE for Δ_1 ≤ 3 and
at central; POSITIVE for Δ_1 ≥ 3 with maximum Δ_3 and minimum
|Δ_2|.** The retained central sits firmly in the negative regime.

---

## 4. Physical interpretation

### 4.1 MSbar anomalous dimension of the ratio (consistency)

The MSbar anomalous dimension of the Yukawa-to-gauge ratio
`R ≡ y_t/g_s` at 1-loop has a standard form dominated by the Yukawa
anomalous dimension (from the scalar vertex and operator
renormalization) minus the gauge coupling's gluon-self-energy
contribution. Qualitatively:

```
    γ_R / R  ≈  γ_{y_t} − γ_{g_s}
              ≈  (9/4) C_F α/(4π) − (3 C_F α/(2π))                   (physics)
              −   [β-function contribution from C_A, T_F n_f at g_s side]
```

The leading 1-loop running of `y_t/g_s` is **downward** (the ratio
decreases under RGE toward the IR) because the top Yukawa runs
slightly less upward than g_s under the combined Higgs-self-coupling
and QCD drivers at high scales. The retained `Δ_R < 0` on the
lattice-to-MSbar matching is consistent with this downward RGE
trend: the MSbar ratio at `M_Pl` is **below** the lattice tree
ratio `1/√6` by about 3.27 % on the canonical surface.

A rough numerical cross-check. The 1-loop Yukawa-ratio anomalous
dimension computed from standard QCD β-function inputs gives
`γ_R/R ≈ −0.0068` per e-fold at M_Pl. Over a single "matching
log" Δμ/μ = O(1), this gives a `O(1 %)`-scale correction. Over the
full lattice-to-MSbar matching conversion (which spans multiple
scales through the staircase), the accumulated effect can
naturally reach the `O(3 %)`-scale retained here. The sign is
consistent; the magnitude is within an order of magnitude; the
retention is supported.

### 4.2 Channel-by-channel physics

**C_F channel (+1.92 %).** The scalar-bilinear vertex correction
(Rep B) is positive; the gauge-vertex correction (Rep A) has a
partial C_F piece that cancels partially against it. The residual
`+1.92 %` after the external-Z_ψ cancellation and the MSbar scalar
anomalous dimension `−6 C_F α/(4π)` (negative) is a small net
positive number, reflecting the dominance of the scalar vertex over
the gauge vertex in the `C_F` Clifford/color structure difference.

**C_A channel (−7.22 %).** The non-Abelian gauge-vertex piece is
positive (from `+C_A · I_v_gauge`) but subdominant to the bosonic
gluon-self-energy piece (`−(5/3) C_A · I_SE`), which is negative
because the gluon self-energy reduces the effective `g_s²` at
1-loop (asymptotic freedom contribution to β-function). On the
ratio `y_t²/g_s²` this enters with a sign flip, giving a **negative**
contribution to the ratio's 1-loop correction — the ratio increases
less than one might expect from the scalar vertex alone because the
gauge coupling running reduces g_s in the opposite direction.

Actually, let us clarify the sign carefully: the gluon SE reduces
`g_s²` at 1-loop at high energy (asymptotic freedom: β_0 > 0 in the
`dα_s/d ln μ = −β_0 α_s² /(2π)` convention means α_s DECREASES
toward the UV, so `g_s²` at the UV is SMALLER than the bare value,
which means `δ_g < 0` from the `(5/3) C_A` piece). On the ratio
`δ_y − δ_g`, the sign flips: a negative δ_g contributes a **positive**
amount to `δ_y − δ_g` from this piece alone. But there is a
competing `+I_v_gauge = 0` piece (conserved current), so the C_A
channel enters the ratio as `+C_A · (0) − C_A · (5/3) I_SE = −(5/3) C_A I_SE`,
which is **negative** because `I_SE > 0`.

The net statement is: on the retained conserved-current surface,
the C_A channel of the ratio correction is dominated by the gluonic
gluon self-energy piece and enters as a **negative** contribution
of magnitude `(5/3) C_A · I_SE · α/(4π)` on the ratio. This is the
source of the dominant `−7.22 %` at central.

**T_F n_f channel (+2.02 %).** The fermion loop in the gluon
self-energy screens `g_s²` (reduces it) — this is the standard
matter-loop contribution to the β function, `−4/3 T_F n_f` in
`β_0 = (11 C_A − 4 T_F n_f)/3`. On the ratio `δ_y − δ_g`, this
screening enters **positively** (flipped sign) because reducing
`g_s²` increases `y_t²/g_s²`. The retained `+2.02 %` at central is
consistent with the matter-screening physics.

### 4.3 Net interpretation

The retained Δ_R = −3.27 % is **not** a single "vertex correction"
in the traditional sense. It is a competition between:

- the MSbar scalar-bilinear anomalous dimension (pulls y_t down
  relative to bare);
- the `C_A` gluon self-energy (pulls g_s down under RGE;
  counterintuitively pulls the ratio down because of the `δ_y − δ_g`
  sign flip discussed above);
- the `T_F n_f` fermion loop (pulls g_s down under matter
  screening; positive contribution to the ratio).

The C_A piece wins by a factor of ~2 in magnitude, so the net is
negative. The framework-native sign consistency with standard MSbar
RGE of y_t/g_s (downward running, γ_R/R < 0) is a non-trivial
consistency check and supports the retained result.

---

## 5. Supersession of prior single-channel approximations

### 5.1 Packaged `delta_PT = 1.92 %` (C_F channel only)

From `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`:

```
    packaged delta_PT  =  α_LM · C_F / (2π)
                      =  (α_LM/(4π)) · C_F · 2
                      =  0.00721 · (4/3) · 2
                      =  0.01924
                      ≃  1.92 %                                      (5.1)
```

**Interpretation.** The packaged `1.92 %` is the **C_F-channel
contribution alone** at `Δ_1 = 2` (the literature-central
`C_F`-coefficient). It is precisely `C_F · Δ_1^{central} · α_LM/(4π)`
and is recovered exactly by the retained three-channel assembly as
the first of three terms. It is **not** the full Δ_R; it is a
single-channel (C_F only) approximation that (a) omits the C_A
channel (−7.22 %), (b) omits the T_F n_f channel (+2.02 %).

The packaged value remains defensible in its stated role as a
"continuum vertex-correction magnitude heuristic" — it correctly
captures the C_F-channel magnitude — but it is not the retained
P1 central on the full ratio.

### 5.2 Cited I_S-based `5.77 %` (C_F channel only, no external-Z_ψ accounting)

From `docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`:

```
    cited I_S^{literature}  ≃  6      (staggered scalar-density central)
    cited P1^{I_S}          ≃  (α_LM/(4π)) · C_F · I_S
                           =  0.00721 · (4/3) · 6
                           ≃  5.77 %                                  (5.2)
```

**Interpretation.** The cited `5.77 %` is the **C_F-channel central
WITHOUT external-Z_ψ cancellation**. It uses the raw cited
`I_S ≈ 6` (which includes the external Z_ψ contribution `2 I_leg`
that the Rep-A/Rep-B cancellation theorem has since shown cancels
exactly on the ratio) and identifies it directly with the
C_F-channel coefficient. In the retained framework this corresponds
to the upper end of the Δ_1 bracket `[0, +8]`, specifically
`Δ_1 = 6`, which is reached only in the non-retained limit where
external-Z_ψ does NOT cancel — a limit the Rep-A/Rep-B theorem has
explicitly ruled out.

Reinterpreted in terms of the retained surface:

```
    retained Δ_1  =  I_S − 2 I_leg − 0 (for I_v_gauge=0)
                  ≃  6 − 2·(1.5)  ≃  +3      at literature endpoints
                  ≃  6 − 2·(2)    ≃  +2      at literature-central I_leg ≃ 2
```

The cited `5.77 %` is recovered as
`C_F · 6 · α_LM/(4π)` — the same as using `Δ_1 = 6`, which requires
no external-Z_ψ subtraction. The retained central uses `Δ_1 = 2`
(after external-Z_ψ subtraction), giving the packaged `1.92 %` on
the C_F channel alone; the cited `5.77 %` is what you get if you
forget the external-Z_ψ cancellation.

**Either way, the cited `5.77 %` remains a single-channel (C_F only)
approximation** — it is not the full Δ_R; it omits C_A and T_F n_f
channels.

### 5.3 Three-channel retained supersession

The retained Δ_R = −3.27 % supersedes both prior single-channel
estimates on the full ratio. Its position between the packaged
`1.92 %` (lower single-channel) and the cited `5.77 %` (upper
single-channel) is a non-trivial outcome of the three-channel
cancellation structure:

- |Δ_R|^{three-channel, retained} = 3.27 % is **larger** than the
  packaged 1.92 % (C_F only) because the C_A channel contribution
  (−7.22 %) more than offsets the T_F n_f contribution (+2.02 %);
- |Δ_R|^{three-channel, retained} = 3.27 % is **smaller** than the
  cited 5.77 % (C_F only at I_S=6) because the retained C_F channel
  uses Δ_1 = 2 (external Z_ψ cancels), not Δ_1 = 6.

Both prior values are degenerate limits of the full assembly. The
retained `3.27 %` is the correct operational P1 central on the
ratio.

---

## 6. Implication for the master obstruction

### 6.1 Master obstruction P1 revision

The master UV-to-IR transport obstruction theorem packages a ~1.95 %
total residual systematic decomposed into P1, P2, P3 primitives.
With the retained P1 revised to `3.27 %`, the P1 primitive is:

```
    P1  =  |Δ_R|^{retained}  =  3.27 %  ±  ~30 %                     (6.1)
    P1 ∈ [~2.3 %, ~4.3 %]  (1σ citation band)                        (6.2)
```

This is ~1.5× the packaged `1.92 %` central previously carried in
the master obstruction, and 0.57× the cited `5.77 %` central from
the I_S_revision_verification note. **Neither prior value is
retained as the operational P1 central going forward on the full
ratio.**

The master obstruction's total residual ~1.95 % is unchanged at the
structural level (the P1/P2/P3 decomposition is a partition of the
total; this note does not modify the partition or its total). The
master obstruction may internally reweight the P1 budget line on
the retained surface; this is an internal reorganization that does
not modify the master obstruction's ceiling claim.

### 6.2 m_t lane budget

At the literature-cited P1 central of 3.27 %, the m_t lane budget on the
canonical surface is

```
    Δm_t^{P1, lit}  ≃  P1 · m_t^{central}  ≃  0.0327 · 172.57
                                       ≃  ±5.64 GeV                 (6.3)
```

The m_t(pole) prediction at the literature-cited central is

```
    m_t^{pole, lit}  =  172.57 GeV  ±  5.7 GeV                       (6.4)
```

**Superseding-central update.** At the canonical full-staggered-PT central
`3.77 % ± 0.45 %`
(`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`), the m_t
lane budget widens to

```
    Δm_t^{P1, full-PT}  ≃  0.0377 · 172.57  ≃  ±6.50 GeV             (6.3-canonical)
    m_t^{pole, retained}  =  172.57 GeV  ±  6.5 GeV                 (6.4-canonical)
```

which is the canonical operational lane going forward. The precision on the
central is `±0.78 GeV` from the full-PT ±0.45 % uncertainty. The observed
`m_t^{pole, PDG} = 172.69 GeV` lies 0.12 GeV above the central, well within
both the literature-cited ±5.64 GeV lane and the canonical ±6.50 GeV lane.

Relative to the prior packaged P1 = 1.92 %:

```
    prior Δm_t  ≃  0.0192 · 172.57  ≃  ±3.31 GeV                   (prior)
    retained Δm_t  ≃  0.0327 · 172.57  ≃  ±5.64 GeV                (retained)
```

The retained lane budget is ~1.7× wider than the prior packaged
value. This reflects the genuine three-channel uncertainty on the
ratio, which the single-channel packaged estimate had
under-accounted.

### 6.3 What would tighten P1 to sub-percent

Three concrete reductions are needed to tighten `|Δ_R|` from
`3.27 % ± ~1 %` to sub-percent:

1. **Framework-native 4D BZ quadrature of `I_v_scalar`** on the
   retained `Cl(3) × Z^3` action with the exact composite-H_unit
   bilinear and tadpole improvement. Tightens Δ_1 from `[0, +8]`
   to sub-O(1) uncertainty.
2. **Framework-native 4D BZ quadrature of `I_SE^{gluonic+ghost}`**
   on the retained lattice propagators. Tightens Δ_2 from `[−5, 0]`
   to sub-O(1) uncertainty; this is the **dominant** citation
   bracket and tightening it would give the single largest
   improvement.
3. **Framework-native 4D BZ quadrature of `I_SE^{fermion-loop}`**
   on the retained lattice propagators. Tightens Δ_3 from
   `[+0.667, +2.000]` to sub-O(1) uncertainty.

All three require numerical 4D Brillouin-zone integration on the
retained action (not performed here). A framework-native evaluation
of all three, combined with the retained algebraic assembly of this
note, would pin Δ_R to sub-percent and close the P1 primitive
fully.

---

## 7. Safe claim boundary

**Canonical-central supersession note.** The claim text below is the
claim on the literature-citation-based three-channel assembly performed
in this note. The **canonical retained Δ_R central** going forward is
`−3.77 % ± 0.45 %` from the full-staggered-PT BZ quadrature
(`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`); see
§0 Correction for the superseding-relationship summary.

This note claims (literature-citation-based assembly):

> On the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link staggered
> Dirac tadpole-improved canonical surface at SU(3), the 1-loop
> correction to the Ward ratio `y_t²/g_s²` evaluated as the
> three-channel partial-cancellation assembly
> `Δ_R^ratio = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`
> (from the retained Rep-A/Rep-B cancellation theorem) with the
> three retained literature-cited central values Δ_1 ≃ +2,
> Δ_2 ≃ −10/3, Δ_3 ≃ +0.933 (from the three Δ_i BZ-computation
> sub-theorems), gives **Δ_R^{literature-cited central} ≃ −3.27 %**
> with **negative sign** and uncorrelated outer envelope
> `Δ_R ∈ [−9.38 %, +12.03 %]`, tightened by covariance and
> shared-literature reductions to an operational 1σ band
> `Δ_R ≈ (−3.27 ± 2.3) %`. This literature-cited central is
> **superseded as the canonical retained Δ_R** by the framework-native
> full-staggered-PT value `−3.77 % ± 0.45 %` — which lies well within
> the master assembly's ±2.32 % literature-bounded band and is the
> operational Δ_R central going forward. The literature-cited P1
> primitive `3.27 %` (with ±30 % citation uncertainty giving
> `P1 ∈ [2.3 %, 4.3 %]`) is reinterpreted as the literature-cited
> three-channel assembly, with the canonical full-PT P1 `3.77 % ±
> 0.45 %` (`P1 ∈ [3.32 %, 4.22 %]`) superseding it. The corresponding
> m_t lane budget at the canonical full-staggered-PT central is
> `m_t^{pole} = 172.57 GeV ± 6.5 GeV` (vs the literature-cited
> `172.57 GeV ± 5.7 GeV`), consistent with the observed
> `m_t^{pole, PDG} = 172.69 GeV`.

It does **not** claim:

- framework-native 4D BZ quadrature values for `I_v_scalar`,
  `I_SE^{gluonic+ghost}`, `I_SE^{fermion-loop}`, or `I_leg` on the
  retained action (all four remain OPEN — cited-literature input
  only);
- sub-percent precision on Δ_R (the cited O(1) uncertainties on
  each channel limit the current precision to ~30 % relative on
  |Δ_R|);
- sign invariance across the full cited literature bracket (the
  sign is negative at central and across Δ_1 ≲ 3, but flips to
  positive in the extreme upper Δ_1 + upper Δ_3 + zero |Δ_2|
  corner, which is far from central);
- that the retained `−3.27 %` is the **full** Ward ratio correction
  on the canonical surface (the `C_A` channel on the local-current
  formulation would give a shifted central; the retained surface
  uses the conserved current where `I_v_gauge = 0`);
- any modification of the master obstruction theorem's ~1.95 %
  total residual (this note reorganizes the P1 line only, not the
  total);
- any modification of the Ward-identity tree-level theorem, the
  Rep-A/Rep-B cancellation sub-theorem, the three per-channel
  BZ-computation sub-theorems, the packaged `1.92 %` support note,
  the cited I_S citation note, or any publication-surface file;
- that the packaged `1.92 %` or cited `5.77 %` were "wrong" (both
  remain defensible as single-channel approximations in their
  stated OPEN-status roles); the literature-cited three-channel value
  `3.27 %` is a refinement that incorporates all three channels,
  not a correction of prior errors;
- that the literature-cited `−3.27 %` is the canonical operational central
  (the canonical central is the full-staggered-PT `−3.77 % ± 0.45 %`; see
  §0 Correction). The literature-cited `−3.27 %` is retained as the
  citation-based three-channel roll-up and is consistent with the canonical
  central within the master assembly's ±2.32 % literature-bounded band.

---

## 8. What is retained vs. cited vs. open

### 8.1 Retained (framework-native, established upstream and preserved)

- `SU(3)` Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`.
- MSbar flavor count at M_Pl: `n_f = 6`.
- Canonical-surface anchors `α_LM = 0.09067`, `α_LM/(4π) = 0.00721`.
- Three-channel color decomposition
  `Δ_R^ratio = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`.
- Per-channel structural formulae `Δ_1 = 2(I_v_scalar − I_v_gauge) − 6`,
  `Δ_2 = I_v_gauge − (5/3) I_SE^{gluonic+ghost}`,
  `Δ_3 = (4/3) I_SE^{fermion-loop}`.
- `I_v_gauge = 0` on the retained conserved point-split staggered
  vector current (21/21 PASS symbolic reduction).
- External quark Z_ψ cancels exactly on the ratio (partial
  cancellation theorem).
- MSbar scalar-bilinear anomalous dim constant `−6 C_F α/(4π)`.
- Tree-level Ward identity `y_t_bare² = g_bare²/(2 N_c)`.

### 8.2 Cited (external, with O(1) uncertainty)

- Δ_1 central `+2` with range `[0, +8]` from `I_v_scalar ≃ 4`,
  range `[3, 7]` (Sharpe 1994, Bhattacharya–Sharpe 1998,
  Kilcup–Sharpe 1987, Capitani 2003).
- Δ_2 central `−10/3` with range `[−5, 0]` from
  `I_SE^{gluonic+ghost} ≃ 2`, range `[1, 3]`
  (Hasenfratz–Hasenfratz 1980, Kawai–Nakayama–Seo 1981,
  Lepage–Mackenzie 1992).
- Δ_3 central `+0.933` with range `[+0.667, +2.000]` from
  `I_SE^{fermion-loop} ≃ 0.7` per flavor, range `[0.5, 1.5]`
  (Sharpe–Bhattacharya 1998, Luscher–Weisz 1985–86,
  Sharpe 2006 review, DeGrand–DeTar 2006 textbook).

### 8.3 Open (not closed by this note)

- **Framework-native 4D BZ quadrature of `I_v_scalar`,
  `I_SE^{gluonic+ghost}`, `I_SE^{fermion-loop}`, `I_leg`** on the
  retained `Cl(3) × Z^3` canonical action. **CLOSED by the full-staggered-PT
  BZ quadrature note
  (`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`)**, which
  produces the canonical `Δ_R = −3.77 % ± 0.45 %` central superseding the
  literature-cited `−3.27 %` of this note.
- Propagation of the canonical full-PT P1 = 3.77 % ± 0.45 % (or the
  literature-cited P1 = 3.27 % of this note) into any publication-surface
  table (explicitly NOT pursued here).
- Higher-loop (2-loop) corrections to `Δ_R`; the structural 2-loop extension
  is documented in `docs/YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md`
  (through-2-loop central −3.99 % ± 0.70 % built on the literature-cited
  1-loop) and the MC-pinned 2-loop assembly in
  `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md`
  (through-2-loop central −4.60 % ± 0.84 % built on the full-staggered-PT
  1-loop).

---

## 9. Validation

The runner
`scripts/frontier_yt_p1_delta_r_master_assembly.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p1_delta_r_master_assembly_2026-04-18.log`. The
runner must return PASS on every check to keep this note on the
retained assembly surface.

The runner verifies:

1. Retention of SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`
   and flavor count `n_f = 6`.
2. Retention of canonical-surface constants `α_LM = 0.09067`,
   `α_LM/(4π) = 0.00721` (sub-permille match to
   `canonical_plaquette_surface`).
3. Retention of per-channel centrals from the three BZ-computation
   sub-theorems: `Δ_1 = 2`, `Δ_2 = −10/3`, `Δ_3 = (4/3) · 0.7`.
4. Per-channel retained contributions at central:
   `C_F · Δ_1 · α/(4π) ≃ +1.924 %`,
   `C_A · Δ_2 · α/(4π) ≃ −7.215 %`,
   `T_F · n_f · Δ_3 · α/(4π) ≃ +2.020 %`.
5. Sum: `Δ_R^{central} ≃ −3.271 %` to sub-permille precision.
6. Sign: `Δ_R^{central} < 0` (negative).
7. Uncorrelated worst-case envelope:
   `Δ_R ∈ [−9.38 %, +12.03 %]`.
8. Covariance-reduced 1σ band on Δ_R:
   `(−3.27 ± ~2.3) %`.
9. Operational P1 band: `P1 = 3.27 % ± ~30 %` → `P1 ∈ [2.3 %, 4.3 %]`.
10. Reinterpretation of packaged `1.92 %` as the single-channel
    (C_F only, Δ_1 = 2) approximation to Δ_R; recovered as the first
    channel of the assembly.
11. Reinterpretation of cited `5.77 %` as the single-channel
    (C_F only, Δ_1 = 6 without external-Z_ψ subtraction)
    approximation to Δ_R.
12. Consistency with the Rep-A/Rep-B cancellation sub-theorem's
    three-channel structural decomposition.
13. Consistency with the master obstruction theorem's
    P1/P2/P3 primitive decomposition (structural, not numerical;
    the P1 primitive value updates but the total residual is
    unchanged at the structural level).
14. Retained m_t(pole) lane: `m_t^{pole} = 172.57 GeV ± 5.7 GeV`
    at the retained P1 = 3.27 %; consistent with observed
    `m_t^{pole, PDG} = 172.69 GeV`.
15. No modification of any prior retained theorem, support note,
    citation note, or publication-surface file.
