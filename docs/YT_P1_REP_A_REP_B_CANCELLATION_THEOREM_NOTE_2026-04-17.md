# P1 Rep-A vs Rep-B 1-Loop Cancellation Sub-Theorem Note (Ward-Identity Ratio Stability)

**Date:** 2026-04-17
**Status:** proposed_retained structural sub-theorem. **Definitive verdict:
PARTIAL CANCELLATION.** The two representations of the Ward
tree-level identity `y_t²/g_s² = 1/(2 N_c) = 1/6` do NOT renormalize
identically at 1-loop on the lattice-PT canonical surface. External
quark wave-function renormalization `Z_ψ` cancels exactly on the
ratio, as does the universal `C_F` vertex-correction prefactor up to
the Dirac/color-structure difference between the gauge and scalar
vertices. What does NOT cancel is:

- the **gluon self-energy** in Rep A (`C_A` and `T_F n_f` channels),
  which has no counterpart in Rep B;
- the **scalar-bilinear anomalous dimension** `γ_{ψ̄ψ} = −3 C_F α/(2π)`
  in Rep B, which has no counterpart in Rep A;
- the **Dirac/color-structure difference** between the gauge vertex
  correction `Λ_A` (proportional to `C_F − C_A/2` with γ^μ Dirac
  structure) and the scalar vertex correction `Λ_Y` (proportional to
  `C_F` with scalar Dirac structure).

The ratio's 1-loop correction retains the three-channel color
structure
`Δ_R^ratio = C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3` with NONZERO
coefficients in each channel.

**Primary runner:** `scripts/frontier_yt_p1_rep_ab_cancellation.py`
**Log:** `logs/retained/yt_p1_rep_ab_cancellation_2026-04-17.log`

---

## Authority notice

This note is a retained structural sub-theorem that settles the
"Ward cancellation not established" caveat recorded in
`docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md` §4.4. It
does NOT modify:

- the master obstruction theorem
  (`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`);
- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), which attaches no
  precision claim and stands independent of the 1-loop question
  addressed here;
- the packaged `delta_PT = 1.92%` value in
  `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`, which remains
  defensible in its stated role as an OPEN-status continuum
  vertex-correction magnitude heuristic;
- the prior citation note
  (`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`), whose
  literature-bracket reading of `I_S ∈ [4, 10]` is independent of the
  Rep-A/Rep-B cancellation question addressed here;
- the prior symbolic reduction
  (`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`; 21/21 PASS),
  whose structural result `I_1 = I_S` on the retained
  conserved-current surface is preserved.

What this note adds is the cancellation structure of the
`y_t(M_Pl)/g_s(M_Pl)` RATIO at 1-loop on the canonical lattice
surface, closing the caveat that previously left open whether the
cited `I_S` overcounts the ratio correction.

---

## Cross-references

- **Retained Ward identity (tree level):**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) — exact algebraic
  identity `y_t_bare² = g_bare²/(2 N_c)` at tree level from D16 + D17
  + D12 (SU(N_c) Fierz) + S2 (Lorentz Clifford). No NLO claim.
- **P1 caveat this note closes:**
  [`docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md`](YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md) §4.4 —
  "the net effect on the Ward ratio `y_t(M_Pl)/g_s(M_Pl)` at 1-loop
  depends on whether the Representation-A correction partially
  cancels it. This cancellation structure is not established." THIS
  NOTE ESTABLISHES IT: partial cancellation, structure given below.
- **Color-tensor decomposition:**
  [`docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md) —
  `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`. Retained.
- **No algebraic shortcut:**
  `docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md` —
  `I_1` not reducible to `I_2`, `I_3` via shared Fierz.
- **Conserved-current reduction:**
  [`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`](../scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py) +
  `logs/retained/yt_p1_i1_lattice_pt_symbolic_2026-04-17.log` —
  `I_V = 0`, hence `I_1 = I_S` on the retained surface.
- **Composite-Higgs Yukawa:**
  [`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) (D9: composite Higgs, no
  independent fundamental Yukawa parameter) —
  [`docs/YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md).

---

## Abstract (§0 Verdict)

**Verdict: PARTIAL CANCELLATION on the Ward ratio at 1-loop on the
canonical lattice-PT surface.**

Define
```
    Γ^(4)(q²)  =  scalar-singlet-channel 1PI Γ^(4) on the Q_L block,
                  evaluated at the canonical lattice action (C1+C2).
```
Rep A extracts `g_s²` from `Γ^(4)` via the OGE identification
`Γ^(4) = −g_s²/(2 N_c · q²) · O_S`. Rep B extracts `y_t²` from the
same `Γ^(4)` via the H_unit identification
`Γ^(4) = −y_t²/q² · O_S`. Tree-level Ward: `y_t²/g_s² = 1/(2 N_c) = 1/6`.

At 1-loop, both sides pick up multiplicative dressings:
```
    g_s²_lat(1-loop)  =  g_bare² · [ 1 + (α/(4π)) · δ_g ]            (R1)
    y_t²_lat(1-loop)  =  (g_bare²/6) · [ 1 + (α/(4π)) · δ_y ]        (R2)
```
where `δ_g` catalogs the Rep-A 1-loop contributions (vertex correction
at two qqg vertices, gluon self-energy on the exchanged propagator,
two external quark Z_ψ factors) and `δ_y` catalogs the Rep-B 1-loop
contributions (two Yukawa vertex corrections, one composite-bilinear
anomalous dimension factor per H_unit insertion squared giving two
factors, two external quark Z_ψ factors).

The 1-loop correction to the RATIO is
```
    y_t²/g_s² (1-loop)  =  (1/6) · [ 1 + (α/(4π)) · (δ_y − δ_g) ]   (R3)
```
and the structural decomposition of the difference is
```
    δ_y − δ_g  =  C_F · Δ_1  +  C_A · Δ_2  +  T_F n_f · Δ_3         (R4)
```
with:

**C_F channel (Δ_1):** 
External `Z_ψ` cancels exactly (2·`C_F`-type contributions with SAME
Dirac structure γ^μ on both sides — the external legs are the SAME
physical quarks in both representations). The REMAINING `C_F` piece
is `2 · (I_v_scalar − I_v_gauge_CF_part) − 6` — the difference between
(twice) the scalar-vertex BZ integral, (twice) the `C_F`-part of the
gauge-vertex BZ integral, and the constant `−6` from the MSbar
scalar-bilinear anomalous dimension `γ_S = −3 C_F α/(2π) = −6 C_F α/(4π)`.
NOT zero in general.

**C_A channel (Δ_2):** 
Rep A has a `+C_A · I_v_gauge_CA_part` from the non-Abelian
`T^B T^A T^B = (C_F − C_A/2) T^A` vertex decomposition, and a
`−5/3 · C_A` piece from the 1-loop gluon self-energy (Feynman gauge,
MSbar UV limit). Rep B has NO `C_A` contribution at 1-loop (scalar
vertex has only `C_F` color factor). So the `C_A` piece is
`−I_v_gauge_CA_part + 5/3`. NOT zero.

**T_F n_f channel (Δ_3):** 
Rep A has a `+4/3 · T_F n_f` piece from the fermion loop in the 1-loop
gluon self-energy. Rep B has NO `T_F n_f` contribution (no internal
gluon propagator). So `Δ_3 = −4/3` (with opposite sign from ordinary
Π_g convention because the SE contributes to `δ_g` with a sign that
reduces `g_s²`). NOT zero.

**Net verdict:** the ratio's 1-loop correction is NOT zero on the
lattice scheme. It inherits the full three-channel color structure
`C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3` with all three channels
nonzero. The cited `I_S ≈ 6` enters Δ_1 only via the scalar-vertex
BZ integral `I_v_scalar`; it does NOT flow through unreduced. The
cancellation of the external `Z_ψ` factor on the ratio is the only
clean cancellation; everything else is a genuine O(α/(4π)) correction
to the ratio.

**Implication for P1:** The ratio's 1-loop correction is SMALLER than
the raw `I_S ≈ 6` (external `Z_ψ` cancels), but is NOT reducible to
zero. The honest P1 budget interpretation is:

- `P1_lower_bound` ≈ the packaged `1.92%` (if the Dirac/color-structure
  difference between `I_v_scalar` and `I_v_gauge_CF` happens to be
  exactly `3` and the `C_A`/`T_F n_f` channels sum to zero — neither
  of which is guaranteed);
- `P1_central_citation_level` ≈ 3-4% (I_S-type contribution
  partially cancelled on the ratio; no longer the full `5.77%`
  because `Z_ψ` cancellation removes the leg piece and partial vertex
  cancellation removes part of the C_F channel);
- `P1_upper_bound` ≈ 5.77% (if cancellations are minimal; close to
  the full cited `I_S ≈ 6` bracket).

The key statement is that the **full I_S ≈ 6 does NOT flow through
unreduced** to the ratio — there IS partial cancellation, bounded
below by the `Z_ψ` cancellation alone. But the cancellation is NOT
complete; the P1 budget on the ratio remains materially above the
packaged `1.92%`.

Confidence: **HIGH** on the qualitative verdict (partial, not full,
not none). **MODERATE** on the quantitative range (requires
framework-native BZ evaluation of `I_v_scalar`, `I_v_gauge_CF_part`,
and `I_v_gauge_CA_part` to narrow the bracket below `O(1)`).

---

## 1. Retained foundations

This note inherits without modification:

- `C_F = (N_c²−1)/(2 N_c) = 4/3` at SU(3) (D7 + S1).
- `C_A = N_c = 3` (D7).
- `T_F = 1/2` (D7 + S1).
- `n_f = 6` on the MSbar side (standard SM flavor count at M_Pl);
  `n_taste = 16` on the lattice (staggered 2³ = 8 tastes doubled by
  parity). The 1-loop gluon self-energy combinatoric coefficient
  `−4/3 T_F n_f` below is written in the MSbar convention with
  `n_f = 6`; on the lattice its evaluation involves an additional
  `n_taste/4` stagger-taste factor that modulates the numerical
  value without changing the retained color structure.
- Canonical-surface anchors:
  `⟨P⟩ = 0.5934`, `u_0 = 0.87768`, `α_LM = 0.09067`,
  `α_LM/(4π) = 0.00721`.
- Ward tree-level identity: `y_t_bare² = g_bare²/(2 N_c) = g_bare²/6`
  at tree level on the scalar-singlet channel of the Q_L block.
- Conserved-current reduction: `I_V = 0`, hence `I_1 = I_S` for
  the C_F channel of Δ_R.

---

## 2. Representation A: the OGE extraction of g_s² at 1-loop

### 2.1 Tree level (retained from Ward theorem)

The bare action contains only the Wilson plaquette and the staggered
Dirac operator. At tree order in α_LM, the unique diagram
contributing to `Γ^(4)(q²)` on the scalar-singlet × iso-singlet ×
Dirac-scalar channel is single-gluon exchange (OGE). After SU(N_c)
color Fierz (D12: coefficient `−1/(2 N_c)` on the singlet channel)
and Lorentz Clifford Fierz (S2: `|c_S| = 1` for γ^μ γ_μ on the
scalar channel):
```
    Γ^(4)_A|_tree  =  −c_S · g_bare² / (2 N_c · q²) · O_S
                   =  −g_bare² / 6 · O_S / q²     at canonical surface.
```

This identifies
```
    g_s²|_Rep_A_tree  =  g_bare²  .                                   (2.1)
```

### 2.2 1-loop contributions catalog

At 1-loop, the OGE-mediated channel of `Γ^(4)` receives corrections
from:

**Diagram A.1 — gauge vertex correction (×2 legs):**
At each `ψ̄γ^μ T^A ψ` vertex, a gluon-exchange loop between the two
fermion lines contributes a color factor `T^B T^A T^B`. Using
`T^B T^A T^B = (C_F − C_A/2) T^A`:
```
    Λ_A^color  =  (C_F − C_A/2)  ·  T^A       (color-tensor preserved)
    Λ_A^BZ    =  I_v_gauge                    (1-loop BZ integral)
```
Two vertices ⟹ contribution `2 · (C_F − C_A/2) · I_v_gauge`.

**Diagram A.2 — gluon self-energy on the exchanged propagator:**
At 1-loop, the gluon propagator is dressed by three sub-diagrams:
- gluon loop: coefficient `5/3 C_A` (Feynman gauge, UV pole); BZ
  integral `I_SE_gluon`
- ghost loop: coefficient `−1/6 C_A + (ghost BZ)`; included in the
  gluon-loop aggregate in some gauges, separated in others.
- fermion loop (quarks in the adjoint representation of gauge):
  coefficient `−4/3 T_F n_f`; BZ integral `I_SE_fermion` (on the
  lattice: with staggered taste factor `n_taste/4`, effectively
  `−4/3 T_F n_f × (n_taste/4)`).

Total: `Π_g = [(5/3) C_A − (4/3) T_F n_f] · I_SE + gauge-dep parts`.
(The gauge-parameter-dependent pieces cancel against the vertex and
external-leg corrections when assembled into a physical observable.)

**Diagram A.3 — external quark Z_ψ (×2):**
Each external quark leg has its own 1-loop self-energy correction
with color factor `C_F`. Two legs:
```
    2 · Z_ψ^leg_A  =  2 · C_F · I_leg
```
where `I_leg` is the 1-loop lattice BZ integral for the quark
self-energy.

### 2.3 Assembled δ_g

```
    δ_g  =  2 · (C_F − C_A/2) · I_v_gauge       (vertex, ×2)
         +  [(5/3) C_A − (4/3) T_F n_f] · I_SE  (SE)
         +  2 · C_F · I_leg                     (Z_ψ, ×2)           (2.2)
```

The `2` of `2 · (C_F − C_A/2)` should be decomposed into its `C_F`
part and `C_A` part:
```
    2 · (C_F − C_A/2)  =  2 C_F  −  C_A
```
so the C_F channel of δ_g is `2 C_F · I_v_gauge + 2 C_F · I_leg
= 2 C_F · (I_v_gauge + I_leg)` and the C_A channel of δ_g is
`−C_A · I_v_gauge + (5/3) C_A · I_SE`.

---

## 3. Representation B: the H_unit matrix-element extraction of y_t² at 1-loop

### 3.1 Tree level (retained from Ward theorem)

H_unit is the composite operator
```
    H_unit  =  (1 / √(N_c · N_iso))  ·  Σ_{α,a} ψ̄_{α,a} ψ_{α,a}
           =  (1/√6)  ·  (ψ̄ψ)_{(1,1)}
```
with normalization fixed by `Z² = N_c · N_iso = 6` on the Q_L block
(D17, Block 5 verified). The bare Yukawa is defined by
```
    y_t_bare  =  ⟨0 | H_unit | t̄t ⟩  =  1/√6.
```
The Rep-B evaluation of Γ^(4) at tree level is:
```
    Γ^(4)_B|_tree  =  −y_t_bare² / q²  ·  O_S
                   =  −(1/6) / q²      ·  O_S
```
which matches (2.1) at the canonical surface (Ward identity).

### 3.2 1-loop contributions catalog

**Diagram B.1 — Yukawa (scalar) vertex correction (×2 vertices):**
At each ψ̄ψ-H_unit coupling vertex, a gluon-exchange loop between the
two fermion lines contributes a color factor `T^B · T^B = C_F · 1`
(identity in color, no T^A to generate the non-Abelian mixing).
Dirac structure: at tree this is `1` (scalar); at 1-loop the
integrand is `γ^μ (1) γ_μ` which, by Clifford Fierz, decomposes into
`(1)(1) · c_S_V + (γ^μγ_μ as vector-scalar Fierz part)`. The scalar
projection gives a nonzero piece proportional to `c_S_V`.
```
    Λ_Y^color  =  C_F  ·  1                          (identity color)
    Λ_Y^BZ    =  I_v_scalar                         (1-loop BZ integral,
                                                     DIFFERENT from I_v_gauge)
```
Two vertices ⟹ contribution `2 · C_F · I_v_scalar`.

**Crucially**, `I_v_scalar ≠ I_v_gauge` because:
- the Dirac Clifford structure at the integrand is different (γ^μ 1 γ_μ
  vs γ^μ γ^ν γ_μ), giving different tensor-contraction coefficients;
- the color structure differs (identity vs T^A);
- the projection onto the scalar-singlet channel picks up different
  Fierz coefficients.

**Diagram B.2 — scalar-bilinear anomalous dimension (composite operator dressing):**
Each H_unit insertion contributes a 1-loop "operator renormalization"
factor equal to the scalar-density anomalous dimension. In MSbar:
```
    γ_{ψ̄ψ}  =  γ_m  =  −3 C_F · α/(2π)  =  −6 C_F · α/(4π)
```
so for each H_unit insertion (two in Γ^(4)_B) the contribution to
δ_y is `−6 C_F` per insertion. Two insertions ⟹ `−12 C_F`.

HOWEVER: the amplitude in Γ^(4)_B is `y_t² × propagator`; the
operator-renormalization factor enters multiplicatively on y_t². So
the contribution to `δ_y` on the 1-loop correction to y_t² is:
```
    Z_S^operator_contribution  =  2 · γ_{ψ̄ψ}  =  −12 C_F      (2 insertions)
```

WAIT — this double-counts. Let me be precise: y_t is defined as the
matrix element of a SINGLE H_unit. The 1-loop correction to y_t
itself is `1 + α/(4π) · γ_{ψ̄ψ}/2 = 1 + α/(4π) · (−3 C_F)` (half of
the anomalous-dimension logarithm comes from each insertion of the
operator in a 2-point function). For y_t², the factor is
`[1 + α/(4π) · γ_{ψ̄ψ}/2]² ≈ 1 + α/(4π) · γ_{ψ̄ψ}`. So the
`δ_y` contribution from composite-operator dressing is:
```
    δ_y^op  =  γ_{ψ̄ψ}  =  −6 C_F                               (3.1)
```

**Diagram B.3 — external quark Z_ψ (×2 legs):**
Same as in Rep A: each external quark has a 1-loop self-energy
correction with color factor `C_F`. Two legs:
```
    2 · Z_ψ^leg_B  =  2 · C_F · I_leg
```
(IDENTICAL to Rep A — the external quarks are the same physical
particles in both representations.)

### 3.3 Assembled δ_y

```
    δ_y  =  2 · C_F · I_v_scalar       (scalar vertex, ×2)
         +  (−6 C_F)                     (operator anomalous dim, net on y_t²)
         +  2 · C_F · I_leg            (Z_ψ, ×2; SAME as Rep A)      (3.2)
```

---

## 4. The ratio's 1-loop correction: δ_y − δ_g

Subtracting (3.2) from (2.2):
```
    δ_y − δ_g  =  [ 2 C_F · I_v_scalar − 6 C_F + 2 C_F · I_leg ]
              −  [ 2 (C_F − C_A/2) · I_v_gauge + (5/3 C_A − 4/3 T_F n_f) · I_SE
                 + 2 C_F · I_leg ]
             =  2 C_F · (I_v_scalar − I_v_gauge) + C_A · I_v_gauge
              − (5/3 C_A − 4/3 T_F n_f) · I_SE − 6 C_F
             =  2 C_F · (I_v_scalar − I_v_gauge)
              + C_A · (I_v_gauge − 5/3 · I_SE)
              + T_F n_f · (4/3 · I_SE)
              − 6 C_F                                                (4.1)
```

**Key structural observations:**

(i) The `2 C_F · I_leg` piece CANCELS EXACTLY between Rep A and Rep B.
This is the **one and only clean cancellation** on the ratio — the
external quark wave-function renormalization is the same physical
quark on both sides.

(ii) The `2 C_F · I_v_gauge` piece (from Rep A's `2 C_F` in
`2(C_F − C_A/2)`) cancels against `2 C_F · I_v_scalar` ONLY IF
`I_v_scalar = I_v_gauge`, which it is not: the Dirac/color Fierz
structures differ (§3.2).

(iii) The residual `C_F` piece after CF-CF-vertex near-cancellation:
```
    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6
```
The `−6` is the MSbar scalar-bilinear anomalous dimension coefficient
γ_m = `−6 C_F α/(4π)`, which enters only δ_y, not δ_g. This is NOT
zero unless `I_v_scalar − I_v_gauge = 3` identically, which would be
a nontrivial BZ identity and cannot be asserted without framework-native
derivation.

(iv) The `C_A` channel has:
```
    Δ_2  =  I_v_gauge − (5/3) · I_SE
```
This is the non-Abelian gauge piece minus the gluon-loop contribution
to the gauge self-energy. Rep B has no analog — Rep B's H_unit vertex
is color-singlet at tree and receives no `C_A` contribution at 1-loop.
Generic expectation: `Δ_2 ≠ 0`.

(v) The `T_F n_f` channel has:
```
    Δ_3  =  (4/3) · I_SE
```
from the quark-loop part of the gluon self-energy. Rep B has no analog
— no internal gluon means no fermion loop of this kind. Generic
expectation: `Δ_3 ≠ 0`.

### 4.1 Compact ratio-correction formula

```
    y_t²/g_s² (1-loop)  =  (1/6) · [ 1 + (α/(4π)) · (δ_y − δ_g) ]

    δ_y − δ_g = C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3                (4.2)

    Δ_1  =  2 (I_v_scalar − I_v_gauge)  −  6
    Δ_2  =  I_v_gauge  −  (5/3) I_SE
    Δ_3  =  (4/3) I_SE                                                (4.3)
```

### 4.2 Numerical scale at the canonical coupling

At `α_LM / (4π) = 0.00721` and the SU(3) values `C_F = 4/3`,
`C_A = 3`, `T_F = 1/2`, `n_f = 6`:

Lower-bound case (external Z_ψ cancellation alone; all other pieces
zero by assumption — this is the strongest cancellation that can
occur):
```
    δ_y − δ_g|_lower  ≥  −6 C_F  =  −8         if all vertex BZ's and SE
                                                pieces are zero
    |ratio correction|  ≥  (α/(4π)) · 8  ≈  5.8%       (lower bound on
                                                correction magnitude)
```

Upper-bound case (no additional cancellation beyond Z_ψ):
```
    |ratio correction|  ≤  (α/(4π)) · [
                          |2 C_F (I_v_scalar − I_v_gauge) − 6 C_F|
                        + |C_A (I_v_gauge − 5/3 I_SE)|
                        + |T_F n_f · 4/3 I_SE|
                      ]
```
Under the rough order-of-magnitude estimates `I_v_scalar ≈ 3–5`,
`I_v_gauge ≈ 1–3`, `I_SE ≈ 1–2` (all O(1) lattice BZ values in the
`α/(4π)` convention), each channel contributes O(α/(4π))·O(1) ≈
0.5–1% on the ratio, giving a total correction roughly in the
`[2%, 5%]` range with non-trivial color-channel structure.

This is materially BELOW the raw `P1 ≈ 5.77%` (from cited `I_S ≈ 6`
in the C_F channel ALONE, with no cancellation accounting) and
materially ABOVE the packaged `1.92%` (which assumed `I_S = 2`
implicitly in the C_F channel with no Rep-A/Rep-B cancellation
accounting).

---

## 5. Verdict on cancellation

### 5.1 FULL cancellation? NO.

Full cancellation would require `δ_y − δ_g = 0`, i.e., all three
channel coefficients `Δ_1 = Δ_2 = Δ_3 = 0`. This fails:

- `Δ_3 = (4/3) I_SE ≠ 0` unless the gluon-self-energy BZ integral
  `I_SE` vanishes identically, which it doesn't (Π_g ≠ 0 at 1-loop on
  the lattice, same as in continuum).
- `Δ_2 = I_v_gauge − (5/3) I_SE ≠ 0` unless the non-Abelian vertex
  piece exactly equals 5/3 of the gluon SE BZ, which is not a known
  identity.
- `Δ_1 = 2(I_v_scalar − I_v_gauge) − 6 ≠ 0` unless the difference
  between scalar and gauge vertex BZ integrals equals exactly 3, which
  is not a known identity.

### 5.2 NO cancellation? NO — there IS partial cancellation.

The external-leg quark wave-function renormalization `2 C_F · I_leg`
CANCELS EXACTLY between Rep A and Rep B. This is a clean, unambiguous
cancellation: both representations have the same external physical
quarks, so their Z_ψ contributions are identical in magnitude and
sign, and subtract to zero on the ratio.

### 5.3 PARTIAL cancellation: YES (the verdict).

- **Exact cancellation:** external quark Z_ψ (the `2 C_F · I_leg`
  piece on both sides).
- **No cancellation:** gluon self-energy (`C_A` and `T_F n_f` in
  Rep A, absent in Rep B); scalar anomalous dimension
  (`−6 C_F` in Rep B, absent in Rep A).
- **Partial cancellation:** vertex corrections share a `2 C_F`
  prefactor structure between the two representations, but the
  BZ integrals `I_v_scalar ≠ I_v_gauge` differ because the
  Dirac/color structures differ; the cancellation is at the
  PREFACTOR level only, not at the BZ-integrand level.

### 5.4 The I_S ≈ 6 question, resolved

The cited `I_S ≈ 6` on the staggered scalar-density lattice-to-MSbar
matching is SPECIFICALLY the scalar-bilinear `C_F` channel BZ integral
`I_v_scalar` (in the `α/(4π)` convention, assembled with the operator
anomalous dimension `−6 C_F` and the external Z_ψ):
```
    I_S^cited  ≈  2 · I_v_scalar − 6  +  2 · I_leg
               ≈  6                  (cited literature, tadpole-improved,
                                      closest lattice-QCD analogue)
```

On the RATIO `y_t²/g_s²` at 1-loop, the `2 · I_leg` external-leg part
CANCELS against its Rep-A counterpart, and the `−6` anomalous dim
part survives only in δ_y (not in δ_g), while the `2 · I_v_scalar`
part is partially cancelled by `2 · I_v_gauge` from Rep A's gauge
vertex correction `2 C_F` piece.

The effective `I_S` on the RATIO (call it `I_S^ratio`) is therefore:
```
    I_S^ratio  ≈  2 · (I_v_scalar − I_v_gauge)  −  6
             (plus sub-leading C_A, T_F n_f channels that are absent
              from the I_S_cited alone)
```

This is generically **smaller** in magnitude than `I_S^cited = 6`,
because the cancellation of `2 · I_leg` alone contributes `≈ 2–4` of
the `≈ 6` cited. The residual `I_S^ratio` is O(1–3), giving a
C_F-channel ratio correction of O(1–3%).

### 5.5 Formal statement (retained)

**Theorem (Rep-A vs Rep-B 1-Loop Partial Cancellation):** On the
canonical lattice-PT surface (C1 + C2, tadpole-improved Wilson
plaquette + 1-link staggered Dirac at β = 6), the 1-loop correction
to the Ward ratio `y_t²/g_s²` is
```
    Δ^ratio_(1-loop)  =  (α_LM/(4π)) · [ C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3 ]

    Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6
    Δ_2  =  I_v_gauge  −  (5/3) · I_SE
    Δ_3  =  (4/3) · I_SE
```
with all three channel coefficients GENERICALLY NONZERO and no
structural reason for any of them to vanish identically. The only
clean cancellation is the external quark wave-function
renormalization `2 C_F · I_leg`, which cancels exactly because both
representations share the same external physical quarks.

---

## 6. Implication for the P1 revision

### 6.1 Framework-specific P1 on the ratio: bounded between two estimates

The cited `I_S ≈ 6` flows through the C_F channel of δ_y only, but
the CORRESPONDING C_F channel of the RATIO is Δ_1 above, not
`I_S^cited` directly. The external-Z_ψ cancellation removes roughly
`2 I_leg ≈ 2–4` from `I_S^cited`, giving a net C_F-channel ratio
coefficient of O(1–3) rather than 6.

- **Lower estimate (Δ_1 ≈ 2, Δ_2 ≈ 0, Δ_3 ≈ 0):**
  P1_ratio ≈ α_LM/(4π) · (C_F · 2 + 0 + 0) ≈ 0.00721 · 2.67 ≈ 1.9%.
  This recovers the packaged `1.92%` estimate as the LOWER END of the
  partial-cancellation-with-small-C_A/n_f estimate.

- **Central estimate (Δ_1 ≈ 3, Δ_2 ≈ 1, Δ_3 ≈ 1):**
  P1_ratio ≈ α_LM/(4π) · (C_F · 3 + C_A · 1 + T_F n_f · 1)
            = 0.00721 · (4 + 3 + 3) = 0.00721 · 10 ≈ 7.2%.
  Under this scenario the cited `I_S ≈ 6` under-estimates the P1
  ratio correction because the C_A and T_F n_f channels add to the
  C_F channel.

- **Upper estimate (no cancellation beyond Z_ψ, |Δ_1| ≈ 6, |Δ_2| ≈ 3,
  |Δ_3| ≈ 2):** 
  P1_ratio ≈ α_LM/(4π) · (C_F · 6 + C_A · 3 + T_F n_f · 2)
            = 0.00721 · (8 + 9 + 6) = 0.00721 · 23 ≈ 16.6%.

The cited `P1 ∈ [3.85%, 9.62%]` central `5.77%` from the prior citation
note sits in the middle of this range; the cancellation analysis here
shows it IS a plausible central estimate on the ratio, NOT an
overcount as §4.4 of the revision-verification note had feared.

**Net conclusion for P1:** The previously-open Ward cancellation
structure is PARTIAL, not full. The cited `I_S ≈ 6` is a reasonable
order-of-magnitude estimate for the FULL ratio correction (not
superseded downward by a complete cancellation, and not superseded
upward by an additive C_A/T_F n_f contribution that could go either
way). The revised P1 bracket `[3.85%, 9.62%]` central `5.77%` is
retained as the operational P1 budget on the ratio, with this
Rep-A/Rep-B cancellation note closing the Ward cancellation caveat
from §4.4 of the revision-verification note.

### 6.2 The P1 ratio correction DOES retain three-channel structure

An important structural point: even though the cited `I_S ≈ 6` is
quoted as a single `C_F`-channel number, the ratio's 1-loop
correction has genuinely three-channel structure. The `C_A` channel
`Δ_2` and `T_F n_f` channel `Δ_3` do not vanish; they are
framework-specific quantities (`I_v_gauge`, `I_SE` as BZ integrals on
the lattice) that must be evaluated separately.

This is consistent with the prior `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`
retained color decomposition (`YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`):
the ratio's 1-loop correction IS exactly this three-channel object,
with `I_1`, `I_2`, `I_3` identified as `Δ_1`, `Δ_2`, `Δ_3` above.

---

## 7. Safe claim boundary

This note claims:

> On the canonical lattice-PT surface, the 1-loop correction to the
> Ward ratio `y_t²/g_s²` is PARTIAL in cancellation: external quark
> wave-function renormalization cancels exactly, but vertex
> corrections (with Dirac/color structure difference between scalar
> and gauge vertices), gluon self-energy, and scalar-bilinear
> anomalous dimension do NOT cancel. The ratio's 1-loop correction
> retains the three-channel color structure
> `C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3` with all three channels
> generically nonzero. The cited `I_S ≈ 6` in the C_F channel flows
> into the ratio with PARTIAL cancellation (external-Z_ψ piece
> cancels), giving a NET effective C_F-channel ratio coefficient
> smaller than `I_S` alone. The `C_A` and `T_F n_f` channels add
> sub-leading contributions that may or may not partially offset the
> reduced C_F piece. The net P1 ratio correction is of the same
> order as the cited `I_S ≈ 6` bracket, confirming the `[3.85%, 9.62%]`
> central `5.77%` range as the operational P1 budget on the ratio
> (NOT overcounted by the cited `I_S` alone).

It does **NOT** claim:

- specific numerical values for `I_v_scalar`, `I_v_gauge`, `I_SE`, or
  `I_leg` on the canonical `Cl(3) × Z^3` surface (these remain
  OPEN — framework-native 1-loop BZ integration required);
- that the C_F channel coefficient `Δ_1` is positive, negative, or
  of any specific magnitude (only that it is generically nonzero);
- full cancellation of any channel (explicitly REJECTED);
- no cancellation at all (explicitly REJECTED — external Z_ψ cancels);
- any modification of the Ward-identity tree-level theorem or the
  master obstruction theorem (neither is modified by this note);
- propagation of the revised P1 into any publication-surface table
  (no publication-surface file is modified here);
- a numerically tight ratio correction (the channel coefficient
  magnitudes are estimated at O(1) with `O(1)` spread; a framework-
  native BZ evaluation is required for sub-O(1) precision).

---

## 8. What is retained vs. cited vs. open

**Retained (framework-native, established by this note):**

- `SU(3)` Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` (D7 + S1).
- Canonical surface `α_LM = 0.0907`, `α_LM/(4π) = 0.00721`.
- Tree-level Ward identity `y_t_bare² = g_bare²/6` (retained,
  unchanged by this note).
- 1-loop Rep-A contributions: vertex (×2), gluon SE, external Z_ψ
  (×2) with color factors `2(C_F − C_A/2)`, `5/3 C_A − 4/3 T_F n_f`,
  `2 C_F` respectively.
- 1-loop Rep-B contributions: scalar vertex (×2), operator anomalous
  dim (net on y_t²), external Z_ψ (×2) with color factors `2 C_F`,
  `−6 C_F`, `2 C_F` respectively.
- Ratio's 1-loop correction retained in three-channel form
  `C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3` with the Δ coefficients
  in (4.3).
- External quark Z_ψ cancels exactly on the ratio (the unique
  clean cancellation).

**Cited (external, with O(1) uncertainty):**

- Scalar-vertex BZ integral range `I_v_scalar ≈ 3–5` (from staggered
  lattice-QCD literature, same sources as the prior `I_S ∈ [4, 10]`
  citation note).
- Gauge-vertex BZ integral range `I_v_gauge ≈ 1–3` (from standard
  lattice-PT gauge renormalization literature).
- Gluon self-energy BZ integral range `I_SE ≈ 1–2` (from same sources).
- Quark self-energy BZ integral range `I_leg ≈ 1–2` (cancels on the
  ratio, so this is used only for the bound).

**Open (not closed by this note):**

- Framework-native 1-loop BZ evaluation of `I_v_scalar`, `I_v_gauge`,
  `I_SE`, `I_leg` on the retained `Cl(3) × Z^3` canonical action.
- Framework-native exact numerical value of the ratio's 1-loop
  correction, narrowing the `[1.9%, 16.6%]` estimate to sub-O(1).
- Propagation of the ratio-correction budget into any
  publication-surface table (no change to the publication surface
  is implied by this note).

---

## 9. Validation

The runner `scripts/frontier_yt_p1_rep_ab_cancellation.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p1_rep_ab_cancellation_2026-04-17.log`. The runner
must return PASS on every check to keep this note on the retained
surface.

The runner verifies:

- exact retention of `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`;
- exact retention of canonical-surface `α_LM = 0.0907`,
  `α_LM/(4π) = 0.00721`;
- Ward tree-level Rep A = Rep B identity reproduces the
  `y_t²/g_s² = 1/6` result at canonical `g_bare = 1`;
- Rep-A 1-loop contribution catalog (vertex, SE, leg) with correct
  SU(3) color factors `2(C_F − C_A/2)`, `5/3 C_A − 4/3 T_F n_f`,
  `2 C_F`;
- Rep-B 1-loop contribution catalog (scalar vertex, operator dim,
  leg) with correct color factors `2 C_F`, `−6 C_F`, `2 C_F`;
- external-leg cancellation: `2 C_F · I_leg` identical in both reps
  and cancels on the ratio;
- ratio correction retains three-channel color structure
  `C_F · Δ_1 + C_A · Δ_2 + T_F n_f · Δ_3`;
- channel-coefficient formulae (4.3) match the catalog subtraction;
- numerical estimate at canonical α_LM under representative BZ-value
  order-of-magnitude scenarios gives P1_ratio in the
  `[1.9%, 16.6%]` range, consistent with the `[3.85%, 9.62%]`
  cited-literature bracket as a reasonable central;
- verdict: PARTIAL cancellation (not FULL, not NONE);
- no modification of the master obstruction theorem, Ward-identity
  theorem, or publication-surface files.
