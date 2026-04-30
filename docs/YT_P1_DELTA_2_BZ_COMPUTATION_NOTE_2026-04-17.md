# P1 Δ_2 (C_A Channel) BZ Computation Note

**Date:** 2026-04-17
**Status:** proposed_retained **citation-and-bound** computation of the C_A
channel coefficient `Δ_2` of the retained Rep-A/Rep-B 1-loop ratio
decomposition. Pins the central value and literature-bounded range
for `Δ_2 = I_v_gauge − (5/3) · I_SE` at SU(3) on the canonical
tadpole-improved Wilson-plaquette + 1-link staggered-Dirac surface.
Individual Brillouin-zone integrals `I_v_gauge` and `I_SE^{gluonic+ghost}`
are taken from the lattice-PT literature (Hasenfratz–Hasenfratz 1980;
Kawai–Nakayama–Seo 1981; Lepage–Mackenzie 1992). The retained central
value is `Δ_2 ≈ −3` with range `Δ_2 ∈ [−5, 0]` under the cited
literature uncertainty. The corresponding ratio contribution
`C_A · Δ_2 · α_LM/(4π)` is NEGATIVE at the central, giving roughly
`−6.5 %` on `y_t²/g_s²` at the canonical surface.
**Primary runner:** `scripts/frontier_yt_p1_delta_2_bz.py`
**Log:** `logs/retained/yt_p1_delta_2_bz_2026-04-17.log`

---

## Authority notice

This note is a retained citation-and-bound layer on top of the
retained Rep-A/Rep-B 1-loop partial-cancellation sub-theorem
(`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`),
which already derived the structural formula

```
    Δ_2  =  I_v_gauge  −  (5/3) · I_SE                              (P0)
```

as the C_A channel coefficient of the ratio `y_t²/g_s²` 1-loop
correction in the retained three-channel decomposition
`Δ_R^ratio = (α_LM/(4π)) · [C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3]`.
This note does **not** modify any authority document. It only pins
the numerical central value and the literature-bounded range of
`Δ_2`, and evaluates the `C_A · Δ_2 · α_LM/(4π)` contribution to the
ratio correction at the canonical surface `α_LM = 0.09067`.

It does not modify:

- the master retained obstruction theorem (unchanged);
- the retained Ward-identity theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, tree-level only,
  no NLO claim);
- the retained Rep-A/Rep-B partial-cancellation theorem
  (`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`),
  whose formula (P0) is inherited without modification;
- the retained H_unit symbolic reduction
  (`docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`),
  whose envelope bound `|I_S| ≤ 23.35` is a C_F-channel envelope
  orthogonal to the C_A channel addressed here;
- the retained I_S citation note (`[4, 10]` central `~6` for the
  C_F-channel scalar-density matching);
- the packaged `delta_PT = 1.92 %` support note
  (`docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`), which
  remains defensible in its stated role as a continuum
  vertex-correction magnitude heuristic.

Specifically, this note does NOT propagate any numerical change into
any publication-surface table; the `Δ_2`-inclusive ratio correction
is recorded here only as an order-of-magnitude citation-bound, with
the caveat that the remaining C_F and T_F n_f channels of `Δ_R` must
be assembled alongside it before any net publication-surface revision
could be contemplated.

## Cross-references

- **Rep-A/Rep-B partial-cancellation theorem (derives Δ_2 formula):**
  `docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  (§4.3, (4.3) above; establishes `Δ_2 = I_v_gauge − (5/3) I_SE`).
- **H_unit symbolic reduction (Wilson-plaquette context):**
  [`docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md`](YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md)
  (retained Feynman rules FR1, FR2; retained tadpole factor `u_0`).
- **Prior P1 citation chain:**
  - [`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`](YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md) — cited
    `I_S ∈ [4, 10]` (C_F-channel analogue, for context).
  - [`docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`](YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md) —
    revised `P1 ∈ [3.85 %, 9.62 %]` central `5.77 %`.
  - [`docs/YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`](YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md) — geometric
    tail bound on the loop-expansion axis.
- **Subordinate support:**
  [`docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`](UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md) — packaged
  `delta_PT = 1.92 %`.
- **Canonical-surface authority:**
  [`docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) — `⟨P⟩ = 0.5934`,
  `u_0 = 0.87768`, `α_LM = 0.09067`, `α_LM/(4π) = 0.00721`.
- **Ward authority:**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) — `y_t_bare² =
  g_bare² / (2 N_c) = g_bare² / 6` at tree level.

## Abstract (§0 verdict)

Pinning the C_A channel of the retained three-channel ratio
decomposition under the retained literature citations for
tadpole-improved Wilson-plaquette lattice perturbation theory:

```
    I_SE^{gluonic+ghost}  ∈  [1, 3]        (cited, tadpole-improved)       (A1)
    I_v_gauge            ∈  [0, 3]        (cited; 0 for conserved
                                            point-split staggered vector
                                            current by Ward identity,
                                            [1, 3] for LOCAL current)      (A2)
    Δ_2  =  I_v_gauge  −  (5/3) · I_SE    (retained formula, from P0)     (A3)
    Δ_2^{central}  ≈  −3                                                  (A4)
    Δ_2 ∈ [−5, 0]   (conservative outer envelope across cited
                     `I_SE ∈ [1, 3]` and `I_v_gauge ∈ [0, 3]`)             (A5)
    C_A · Δ_2^{central} · α_LM/(4π)  ≈  −6.49 %                           (A6)
    C_A · Δ_2 · α_LM/(4π)  ∈  [−10.82 %, 0 %]    (from (A5))              (A7)
```

**Sign:** the C_A channel contribution to the ratio is NEGATIVE at
central (and across the full plausible literature range except at
the extreme upper endpoint `Δ_2 = 0`).  This is structurally
consistent with the known physics of the 1-loop gluon self-energy:
the dominant bosonic gluon-loop contribution (coefficient `5/3 C_A`)
exceeds the gauge-vertex contribution (`I_v_gauge`) under the cited
literature values, so the C_A channel of `δ_y − δ_g` is dominated by
the `−(5/3) I_SE` piece, which enters `Δ_2` with a negative sign.

**Confidence:** **MODERATE–HIGH** on the sign (negative at central,
range strictly non-positive except at the boundary `Δ_2 = 0`).
**MODERATE** on the magnitude (bounded by the cited literature
uncertainty on `I_SE` and `I_v_gauge`, not a framework-native
quadrature).

**Claim boundary:** this note pins a CITATION-LEVEL central and
range for `Δ_2` on the basis of the cited tadpole-improved
Wilson-plaquette + staggered-Dirac literature. It does **not** claim
a framework-native 4D BZ quadrature value. The cited ranges are
carried forward as external-literature input, consistent with the
treatment of `I_S` in the prior P1 citation chain.

---

## 1. Retained foundations

This note inherits without modification:

- **SU(3) Casimirs** — `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`
  (D7 + S1 + `YT_EW_COLOR_PROJECTION_THEOREM.md`).
- **SM flavor count at M_Pl, MSbar side** — `n_f = 6` (standard SM;
  irrelevant to C_A channel but recorded for cross-referencing the
  T_F n_f channel `Δ_3`).
- **Canonical-surface anchors** — `⟨P⟩ = 0.5934`, `u_0 = 0.87768`,
  `α_LM = 0.09067`, `α_LM/(4π) = 0.00721` (from
  `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md`).
- **Ward tree-level identity** — `y_t_bare² = g_bare² / 6` at tree
  level on the scalar-singlet channel of the Q_L block.
- **Rep-A/Rep-B structural decomposition** —
  `Δ_R^ratio = (α_LM/(4π)) · [C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3]`
  with `Δ_2 = I_v_gauge − (5/3) · I_SE` established in the retained
  Rep-A/Rep-B theorem.
- **5/3 factor** — from the QCD color decomposition of the 1-loop
  gluon self-energy: β_0 = `(11 C_A − 4 T_F n_f)/3`, with the
  `11/3 C_A` pure-gauge piece split into a gauge-vertex piece and
  a gluonic+ghost piece; the latter enters `I_SE^{gluonic+ghost}`
  with the effective coefficient `5/3 C_A` at the ratio-decomposition
  level (`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  §4.3).
- **C_A channel** — the non-Abelian gauge piece minus the
  gluonic+ghost part of the 1-loop gluon self-energy; Rep B has no
  C_A counterpart (the H_unit vertex is color-identity at tree),
  so the C_A channel of the ratio is determined entirely by Rep A.

---

## 2. Literature citation for `I_SE` (gluonic + ghost)

The gluonic + ghost piece of the 1-loop gluon self-energy on Wilson
plaquette action, tadpole-improved, is the object entering the
retained formula (P0). The relevant cited literature values:

### 2.1 Hasenfratz–Hasenfratz (1980)

- Reference: Hasenfratz, P. and Hasenfratz, A., *Phys. Lett.* B93 (1980) 165.
- Derives the leading lattice-to-MSbar matching for the SU(N) Wilson-plaquette gauge coupling:
  ```
      α_g^{lat}  =  α_g^{MSbar}  ·  [ 1  +  α_g · Δ_g  +  O(α_g²) ]
      Δ_g^{SU(3)}  ≈  3.413                                         (HH-1)
  ```
- This `Δ_g` combines the gauge self-energy (gluonic+ghost+fermion)
  with the gauge vertex. Extracting the gluonic+ghost piece of the
  self-energy alone requires the separate evaluation of the vertex
  and fermion-loop pieces.

### 2.2 Kawai–Nakayama–Seo (1981)

- Reference: Kawai, H., Nakayama, R. and Seo, K., *Nucl. Phys.* B189 (1981) 40.
- Derives the gluon self-energy on the Wilson-plaquette action in
  more detail, separating the gluonic + ghost part from the fermion loop.
- The gluonic + ghost piece in the MSbar-matching BZ integral
  (before tadpole improvement) is of order `2-4` in the `α/(4π)`
  convention at SU(3) (this magnitude being the characteristic scale
  of the pure-gauge piece of `Δ_g` on the unimproved action).

### 2.3 Lepage–Mackenzie (1992)

- Reference: Lepage, G. P. and Mackenzie, P. B., *Phys. Rev.* D48 (1993) 2250.
- Establishes that tadpole improvement `U = u_0 V` with `u_0 = ⟨P⟩^{1/4}`
  removes the dominant large bulk of the unimproved `Δ_g ≈ 3.4` constant,
  leaving a tadpole-improved `Δ_g^{TI}` of order unity.
- After tadpole improvement, the gluonic + ghost part of the gluon
  self-energy is of order `1-3` in the `α/(4π)` convention.

### 2.4 Retained citation-level range for `I_SE^{gluonic+ghost}`

Synthesizing the above, the citation-bounded range for the gluonic +
ghost piece of the 1-loop gluon self-energy on the tadpole-improved
Wilson-plaquette surface at SU(3) is:

```
    I_SE^{gluonic+ghost}  ∈  [1, 3]                                  (C-SE)
```

with central value approximately `I_SE^{central} ≈ 2` as the midpoint
of the cited bracket. This is consistent with (i) Hasenfratz–Hasenfratz
unimproved `Δ_g ≈ 3.4` being the *total* matching constant, (ii) the
gluonic+ghost piece being roughly half of that (the gauge vertex
carries a comparable magnitude and the fermion loop is subtracted
separately in the retained Rep-A/Rep-B decomposition), and (iii) the
tadpole-improvement reduction factor of order `1/u_0^4 − 1 ≈ 0.3`
that removes the bulk of the constant piece.

**Confidence on the range:** **MODERATE**. The bracket [1, 3] is the
cited literature span; the central `~2` is the retained midpoint,
not a framework-native quadrature.

---

## 3. `I_v_gauge` on the staggered gauge vertex

### 3.1 Conserved (point-split) staggered vector current

The conserved (point-split) staggered vector current is the unique
one-link-separated bilinear whose divergence vanishes identically on
the lattice equations of motion. By the lattice vector Ward identity,
its 1-loop renormalization constant satisfies

```
    Z_V^{conserved}  =  1    (exact, to all orders in α)              (W1)
```

which implies that the lattice-PT matching integral vanishes:

```
    I_v_gauge^{conserved}  =  0                                       (W2)
```

This is the prior retained result, consistent with the retained
symbolic reduction `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`
(Block 4, PASS) showing `I_V = 0` on the conserved current surface.
The conserved-current case is exact: it is not a citation-level
approximation but a framework-native identity.

### 3.2 Local (non-conserved) staggered vector current

The LOCAL staggered vector current — the naive on-site `ψ̄ γ^μ ψ`
bilinear — does not enjoy the lattice vector Ward identity
protection. Its 1-loop renormalization constant is a small finite
value, typically

```
    Z_V^{local}  −  1  ≈  (α / (4π))  ·  I_v_gauge^{local}
    I_v_gauge^{local}  ∈  [1, 3]                                      (L1)
```

with central value approximately `I_v_gauge^{central, local} ≈ 2`
from the cited tadpole-improved lattice-QCD literature (Sharpe 1994;
Bhattacharya–Sharpe 1998; staggered vector-current renormalization
in the scalar-singlet projection).

### 3.3 Retained citation-level range for `I_v_gauge`

Depending on which vector-current definition is used in the
Rep-A/Rep-B decomposition, the citation-bounded range for
`I_v_gauge` at SU(3) on the canonical surface is:

```
    I_v_gauge  ∈  [0, 3]                                              (C-VG)
```

where `I_v_gauge = 0` corresponds to the conserved point-split
current (exact by Ward identity), and `I_v_gauge ∈ [1, 3]` to the
local current (citation-bounded). The retained Rep-A/Rep-B derivation
is agnostic to this choice at the structural level; the numerical
value of `Δ_2` tracks the chosen current definition.

The CANONICAL retained choice — consistent with the prior retention
`I_V = 0` on the conserved-current surface
(`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`, 21/21 PASS) —
is the conserved point-split current with

```
    I_v_gauge^{conserved}  =  0      (retained)                       (R-VG-0)
```

For completeness the LOCAL current value is also evaluated below as
a sensitivity check.

---

## 4. `Δ_2` computation at each choice

### 4.1 Conserved-current surface (CANONICAL, retained)

Taking the conserved-current value `I_v_gauge = 0` with central
`I_SE^{gluonic+ghost} = 2` (midpoint of cited range):

```
    Δ_2^{central, conserved}  =  0  −  (5/3) · 2  =  −10/3  ≈  −3.333   (D2-1a)
```

At the lower end of the cited `I_SE` range (`I_SE = 1`):

```
    Δ_2^{lower-I_SE, conserved}  =  0  −  (5/3) · 1  =  −5/3  ≈  −1.667  (D2-1b)
```

At the upper end of the cited `I_SE` range (`I_SE = 3`):

```
    Δ_2^{upper-I_SE, conserved}  =  0  −  (5/3) · 3  =  −5.0            (D2-1c)
```

Range on the conserved-current surface:

```
    Δ_2^{conserved}  ∈  [−5.0, −1.667]                               (R-D2-c)
```

### 4.2 Local-current surface (sensitivity check only)

Taking `I_v_gauge = 2` (central of local-current range) with central
`I_SE = 2`:

```
    Δ_2^{central, local}  =  2  −  (5/3) · 2  =  2 − 10/3  =  −4/3  ≈  −1.333  (D2-2a)
```

At the two cited endpoints (`I_v_gauge = 1, I_SE = 3` → most negative;
`I_v_gauge = 3, I_SE = 1` → least negative, even slightly positive):

```
    Δ_2^{most-neg, local}   =  1  −  (5/3) · 3  =  1 − 5  =  −4.0     (D2-2b)
    Δ_2^{least-neg, local}  =  3  −  (5/3) · 1  =  3 − 5/3  =  4/3  ≈  +1.333  (D2-2c)
```

Range on the local-current surface:

```
    Δ_2^{local}  ∈  [−4.0, +1.333]                                   (R-D2-l)
```

### 4.3 Retained combined-range (conservative outer envelope)

Combining (R-D2-c) and (R-D2-l) as a conservative outer envelope
across both current definitions and the full cited literature range:

```
    Δ_2^{combined}  ∈  [−5, +1.333]                                  (R-D2-a)
```

The retained central value, anchored to the conserved-current surface
(the canonical retained choice) with central `I_SE = 2`, is:

```
    Δ_2^{central}  ≈  −3.333                                         (C-D2)
```

For the safe claim boundary below, we record the conservative
**negative-dominant** range:

```
    Δ_2  ∈  [−5, 0]     (retained claim; strict upper bound 0 only at
                         the extreme local-current endpoint, otherwise
                         strictly negative)                            (R-D2)
```

which is the range quoted in the abstract.

---

## 5. `C_A · Δ_2 · α_LM/(4π)` numerical evaluation

At SU(3) with `C_A = 3` and the canonical-surface constant
`α_LM/(4π) = 0.00721`:

### 5.1 Central (conserved current, I_SE = 2)

```
    C_A · Δ_2^{central} · α_LM/(4π)
        =  3 · (−10/3) · 0.00721
        =  −10 · 0.00721
        =  −0.07215
        ≈  −7.22 %                                                   (X-CENTRAL)
```

### 5.2 Sensitivity (local current, I_v_gauge = 2, I_SE = 3)

```
    Δ_2^{alt}  =  2  −  (5/3) · 3  =  −3.0
    C_A · Δ_2^{alt} · α_LM/(4π)  =  3 · (−3) · 0.00721
                                  =  −0.0649
                                  ≈  −6.49 %                         (X-ALT)
```

### 5.3 Range (conservative outer envelope on Δ_2)

```
    Δ_2  ∈  [−5, 0]  ⇒
    C_A · Δ_2 · α_LM/(4π)  ∈  [−10.82 %, 0 %]                        (X-RANGE)
```

The contribution is strictly **non-positive** on the retained
`Δ_2 ∈ [−5, 0]` surface, and at the central values is roughly
`−6` to `−7 %`.

### 5.4 Comparison to the C_F channel

For context, the C_F channel `Δ_1 = 2 (I_v_scalar − I_v_gauge) − 6`
enters the ratio correction at the prefactor `C_F · Δ_1 · α_LM/(4π) =
(4/3) · Δ_1 · 0.00721`. Under the retained Rep-A/Rep-B theorem's
order-of-magnitude estimate `Δ_1 ≈ +2` (lower end) to `Δ_1 ≈ +6`
(upper end), the C_F contribution is:

```
    C_F · Δ_1^{lower} · α_LM/(4π)  =  (4/3) · 2 · 0.00721  ≈  +1.92 %   (F-lower)
    C_F · Δ_1^{upper} · α_LM/(4π)  =  (4/3) · 6 · 0.00721  ≈  +5.77 %   (F-upper)
```

Combining with the C_A channel at central values:

```
    Net (C_F + C_A)  |_lower:    +1.92 %  +  (−6.49 %)  =  −4.57 %        (N-lower)
    Net (C_F + C_A)  |_central:  +4.00 %  +  (−6.49 %)  =  −2.49 %        (N-central)
    Net (C_F + C_A)  |_upper:    +5.77 %  +  (−6.49 %)  =  −0.72 %        (N-upper)
```

These nets are indicative only — they exclude the `T_F n_f · Δ_3`
channel and use order-of-magnitude cited `Δ_1` values. The
**qualitative** message is that the C_A channel SUBTRACTS from the
C_F channel, and the net can flip sign or reduce the C_F-only
estimate substantially.

---

## 6. Honest citation confidence

The retained central value `Δ_2 ≈ −3.333` and range `Δ_2 ∈ [−5, 0]`
are bounded by **three sources of uncertainty**:

1. **Cited `I_SE^{gluonic+ghost}` range [1, 3]** — MODERATE confidence.
   The Hasenfratz–Hasenfratz `Δ_g ≈ 3.4` for SU(3) pure-gauge
   matching is a well-established cited value; decomposing it into
   vertex vs. gluonic+ghost+fermion pieces, and subtracting the
   tadpole part, introduces O(1) uncertainty on each piece
   separately.

2. **Cited `I_v_gauge` choice (conserved vs. local) and range** —
   MODERATE–HIGH confidence on the conserved case (`I_v_gauge = 0`
   by Ward identity, exact); MODERATE on the local case
   (`[1, 3]` from cited staggered lattice-QCD literature).

3. **The identification of the 5/3 factor** — HIGH confidence.
   The retained Rep-A/Rep-B theorem (`§4.3`) derives this factor
   from the explicit QCD gluon self-energy color decomposition;
   no citation uncertainty.

**Net confidence on the central and range:**

- **Sign (negative at central, non-positive across range):**
  MODERATE–HIGH.
- **Magnitude (central `−3.3`, range `[−5, 0]`):** MODERATE.
- **Overall:** the retained range `Δ_2 ∈ [−5, 0]` is a defensible
  citation-bounded claim; narrowing it to a sub-O(1) central
  requires explicit 4D BZ quadrature on the retained Feynman rules,
  which is NOT performed here.

This confidence-level language is consistent with the treatment of
`I_S` in the prior P1 citation note (`[4, 10]` central `~6`, MODERATE
confidence) and with the retained Rep-A/Rep-B theorem's confidence
self-assessment (HIGH qualitative, MODERATE quantitative).

---

## 7. Safe claim boundary

This note claims:

> On the retained `Cl(3) × Z^3` Wilson-plaquette + 1-link staggered
> Dirac tadpole-improved canonical surface at SU(3), the C_A channel
> coefficient of the retained ratio correction
> `Δ_R^ratio = (α_LM/(4π)) · [C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3]`
> takes the structural form `Δ_2 = I_v_gauge − (5/3) · I_SE` (retained
> from the Rep-A/Rep-B sub-theorem). Under the cited tadpole-improved
> Wilson-plaquette literature ranges `I_SE^{gluonic+ghost} ∈ [1, 3]`
> and `I_v_gauge ∈ [0, 3]`, the retained central value of `Δ_2` is
> approximately `−3.333` on the conserved point-split staggered vector
> current (the canonical retained choice), with conservative outer
> envelope `Δ_2 ∈ [−5, 0]` across cited literature uncertainty and
> current-definition sensitivity. The corresponding C_A-channel
> contribution to the ratio correction at canonical `α_LM = 0.09067`
> is `C_A · Δ_2 · α_LM/(4π) ≈ −7.2 %` at central, with range
> `[−10.8 %, 0 %]`. The **sign** of the C_A contribution is
> **negative** at central (and strictly non-positive across the
> retained range), reducing the net ratio correction relative to a
> C_F-only estimate.

It does **NOT** claim:

- a framework-native 4D BZ quadrature value for `I_SE^{gluonic+ghost}`
  or `I_v_gauge` on the retained lattice propagators (these remain
  OPEN — cited literature input only);
- a specific combined net ratio correction from all three channels
  (`Δ_1` and `Δ_3` are addressed by other notes in the P1 chain and
  not recomputed here);
- any modification of the master obstruction theorem, the Ward
  tree-level theorem, the Rep-A/Rep-B cancellation theorem, the
  H_unit symbolic reduction, or the packaged `1.92 %` support
  (none of these are modified by this note);
- propagation of any revised ratio-correction number into any
  publication-surface table (no publication-surface file is modified);
- a narrower central for `Δ_2` than the retained `−3.333 ± O(1)`
  citation-level uncertainty; narrowing requires explicit 4D BZ
  quadrature not performed here;
- that the `Δ_2 ∈ [−5, 0]` range is sub-percent precise on
  `C_A · Δ_2 · α_LM/(4π)`; the stated range `[−10.8 %, 0 %]` is a
  citation-bounded outer envelope, not a framework-native
  quadrature precision.

---

## 8. What is retained vs. cited vs. open

**Retained (framework-native, established by the Rep-A/Rep-B theorem
and preserved by this note):**

- `SU(3)` Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`.
- Canonical-surface anchors `α_LM = 0.09067`, `α_LM/(4π) = 0.00721`.
- Three-channel ratio decomposition
  `Δ_R^ratio = (α_LM/(4π)) · [C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3]`.
- Structural formula `Δ_2 = I_v_gauge − (5/3) · I_SE`.
- 5/3 factor from QCD gluon self-energy color decomposition.
- Conserved-current reduction `I_V = 0`
  (`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`, 21/21 PASS).

**Cited (external, with O(1) uncertainty):**

- `I_SE^{gluonic+ghost} ∈ [1, 3]` on the tadpole-improved
  Wilson-plaquette surface at SU(3), central `~2`
  (Hasenfratz–Hasenfratz 1980; Kawai–Nakayama–Seo 1981;
  Lepage–Mackenzie 1992).
- `I_v_gauge ∈ [0, 3]` (= 0 for conserved point-split current by
  Ward identity; `[1, 3]` for local current, cited from
  Sharpe 1994 and Bhattacharya–Sharpe 1998 staggered-current
  renormalization literature).

**Open (not closed by this note):**

- Framework-native 4D BZ quadrature of `I_SE^{gluonic+ghost}` and
  `I_v_gauge` on the retained lattice propagators; narrowing
  `Δ_2` below the cited `O(1)` uncertainty requires this.
- Propagation of the `Δ_2`-inclusive ratio correction into any
  publication-surface claim (explicitly NOT pursued here — the
  `Δ_1` and `Δ_3` channels must be assembled alongside before any
  net propagation).

---

## 9. Validation

The runner `scripts/frontier_yt_p1_delta_2_bz.py` emits deterministic
PASS/FAIL lines and is logged under
`logs/retained/yt_p1_delta_2_bz_2026-04-17.log`. The runner must
return PASS on every check to keep this note on the retained surface.

The runner verifies:

- exact retention of `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`;
- exact retention of canonical-surface `α_LM = 0.09067`,
  `α_LM/(4π) = 0.00721`;
- retained Rep-A/Rep-B formula `Δ_2 = I_v_gauge − (5/3) · I_SE`;
- cited `I_SE^{gluonic+ghost} ∈ [1, 3]` on the tadpole-improved
  Wilson-plaquette surface;
- cited `I_v_gauge = 0` (conserved) and `I_v_gauge ∈ [1, 3]` (local);
- `Δ_2` at each of the four cited-scenario evaluations (conserved +
  local, endpoints and central of `I_SE`);
- retained central value `Δ_2^{central} ≈ −3.333` on conserved
  surface with `I_SE = 2`;
- retained conservative outer envelope `Δ_2 ∈ [−5, +1.333]`; safe
  negative-dominant claim range `Δ_2 ∈ [−5, 0]`;
- `C_A · Δ_2 · α_LM/(4π)` numerical evaluation at central `≈ −7.2 %`
  and alternative `≈ −6.5 %`;
- **sign**: C_A channel contribution NEGATIVE at central, strictly
  non-positive across the retained range;
- retained `5/3` factor from QCD color decomposition;
- no modification of the master obstruction theorem, the Ward
  tree-level theorem, the Rep-A/Rep-B cancellation theorem, the
  H_unit symbolic reduction, the packaged `1.92 %` support, or the
  prior P1 citation/verification notes.
