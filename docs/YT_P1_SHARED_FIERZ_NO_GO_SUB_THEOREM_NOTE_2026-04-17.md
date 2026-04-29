# P1 Shared-Fierz Shortcut No-Go Sub-Theorem Note

**Date:** 2026-04-17
**Status:** proposed_retained structural sub-theorem — **definitive no-go
verdict** on reducing the 1-loop ratio correction
`Δ_R ≡ Δ_y − Δ_g` on the Ward ratio `y_t²/g_s²` at M_Pl to an
algebraic shortcut via a shared Fierz identity combining the
Ward-theorem SU(N_c) color Fierz (D12) with the Lorentz Clifford
Fierz (S2). The two representations (Rep-A = one-gluon-exchange
extraction of `g_s²`; Rep-B = `H_unit` matrix-element extraction of
`y_t²`) are STRUCTURALLY DIFFERENT at 1-loop: Rep-A has vertex,
gluon self-energy, ghost, quark self-energy, and tadpole pieces;
Rep-B has scalar-operator dressing and quark self-energy only. The
external quark self-energy (`2 C_F · I_leg`) cancels exactly on the
ratio because both representations share the same physical external
legs. All other pieces have no counterpart across the Rep-A/Rep-B
divide and cannot be mapped to each other by any algebraic
rearrangement. Closes `Δ_R` as a **genuine lattice-PT computation
requiring channel-by-channel BZ evaluation**, not an algebraic
shortcut.

**Primary runner:** `scripts/frontier_yt_p1_shared_fierz_no_go.py`
**Log:** `logs/retained/yt_p1_shared_fierz_no_go_2026-04-17.log`

---

## Authority notice

This note is a retained structural sub-theorem on the P1 primitive
of the master UV-to-IR transport obstruction theorem
(`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`).
It does NOT modify:

- the master obstruction theorem's three-primitive decomposition;
- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), which holds at
  tree level and attaches no NLO claim;
- the retained Rep-A/Rep-B partial cancellation sub-theorem
  (`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`),
  which establishes the PARTIAL cancellation verdict on the ratio
  — the shortcut no-go here is the structural prerequisite behind
  that verdict;
- the retained color-factor retention note
  (`docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`), which
  retains the three-channel color decomposition independent of any
  Fierz question;
- any publication-surface file.

What this note adds is narrow: the **formal no-go verdict** that
the shared Ward-theorem Fierz (D12 + S2) does not algebraically
reduce Rep-A's structure to Rep-B's structure, or vice versa, on the
1-loop ratio correction. The practical implication is that `Δ_R`
**must be computed channel by channel** via lattice-PT BZ
evaluation; no algebraic shortcut collapses it to a pre-Fierz
one-liner.

---

## Cross-references

- **Master obstruction (parent):**
  [`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`](YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
  — names P1 as the 1-loop lattice-to-MSbar matching primitive on
  the Ward ratio.
- **Ward-identity tree-level theorem (source of D12 + S2):**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) —
  D16 (composite H_unit), D17 (H-unit normalization), D12 (SU(N_c)
  color Fierz), S2 (Lorentz Clifford Fierz); together establish
  `y_t_bare² = g_bare²/(2 N_c)` at tree level.
- **Color-factor retention (structural decomposition):**
  [`docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md) —
  retained three-channel form
  `Δ_R = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]`.
- **Rep-A/Rep-B partial cancellation (uses this no-go as prerequisite):**
  [`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`](YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md)
  — establishes the PARTIAL cancellation verdict on the ratio
  (external Z_ψ cancels; all three channels generically nonzero).
- **Color-projection correction note:**
  [`docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md`](YT_COLOR_PROJECTION_CORRECTION_NOTE.md) — retained
  H_unit/H_bar projection + SU(N_c) Fierz structure.
- **I_1 symbolic decomposition (Ward `I_V = 0`):**
  `docs/YT_P1_I1_LATTICE_PT_SYMBOLIC_DECOMPOSITION_NOTE_2026-04-17.md`
  — conserved-current reduction on retained point-split vector
  current.

---

## Abstract (§0 Verdict)

**Verdict: SHORTCUT NO-GO on the 1-loop Δ_R computation.**

Define the 1-loop ratio correction

```
    Delta_R  :=  delta_y  -  delta_g
```

where `delta_g` is the 1-loop correction to `g_s²` extracted from
Rep-A (OGE identification of `g_s²` from `Γ^(4)`) and `delta_y` is
the 1-loop correction to `y_t²` extracted from Rep-B (`H_unit`
matrix-element identification of `y_t²` from the same `Γ^(4)`).

**At tree level** (Rep-A = Rep-B): the Ward identity
`y_t_bare² = g_bare²/(2 N_c)` follows from:

- **D12** (SU(N_c) color Fierz): singlet-channel coefficient
  `−1/(2 N_c)` on the Q_L block;
- **S2** (Lorentz Clifford Fierz): coefficient `c_S = 1` on the
  scalar-singlet channel;
- **D16** + **D17**: composite H_unit with normalization `Z² = N_c · N_iso = 6`.

**At 1-loop** (the question): can a shared Fierz identity
(combining D12 + S2, or any algebraic rearrangement of D12 and S2)
reduce Rep-A's 1-loop structure to Rep-B's 1-loop structure (or
vice versa) on the ratio `Δ_R`?

**Answer: NO.**

The structural reason is as follows:

- **Rep-A 1-loop piece list** (dressing `g_s²`):
  1. Vertex correction at each qqg vertex (×2); color factor
     `T^B T^A T^B = (C_F − C_A/2) T^A`.
  2. Gluon self-energy on the exchanged propagator; color factors
     `(5/3) C_A − (4/3) T_F n_f`.
  3. Ghost-loop contribution (in Feynman gauge: absorbed into the
     gluon SE total; in other gauges: separate diagram).
  4. External quark self-energy (Z_ψ) on each external leg (×2);
     color factor `C_F` per leg.
  5. Tadpole diagrams (retained → 0 on dimensional grounds in
     continuum MSbar; on the lattice retained into the tadpole-
     improvement factor u_0).

- **Rep-B 1-loop piece list** (dressing `y_t²` through H_unit):
  1. Scalar vertex correction at each H_unit insertion (×2);
     color factor `T^B T^B = C_F` (identity color, no non-Abelian
     T^A to generate C_A mixing).
  2. Composite-operator anomalous dimension
     `γ_{ψ̄ψ} = −6 C_F · (α/(4π))` per H_unit insertion (net on
     y_t² after squaring).
  3. External quark self-energy (Z_ψ) on each external leg (×2);
     color factor `C_F` per leg (IDENTICAL to Rep-A).

**Structural divide:**

| Piece | Rep-A | Rep-B |
|-------|-------|-------|
| External Z_ψ (×2) | `2 C_F · I_leg` | `2 C_F · I_leg` (IDENTICAL) |
| Vertex correction | `2 (C_F − C_A/2) · I_v_gauge` | `2 C_F · I_v_scalar` (different BZ) |
| Gluon SE | `(5/3 C_A − 4/3 T_F n_f) · I_SE` | ABSENT (no internal gluon) |
| Ghost loop | Absorbed in gluon SE | ABSENT |
| Tadpoles | Absorbed in u_0 improvement | Absorbed in u_0 improvement |
| Scalar-operator anom. dim. | ABSENT | `−6 C_F` |

**Key structural observations:**

(i) The **external Z_ψ piece cancels exactly** on `Δ_R`. This is
the one and only clean cancellation. Both representations share the
same external physical quarks, so their Z_ψ contributions are
identical and subtract to zero.

(ii) The **gluon self-energy (C_A and T_F n_f channels) in Rep-A
has no counterpart in Rep-B**. Rep-B's H_unit is a color-singlet
operator (identity color in the color indices) and has no internal
gluon line to dress. No Fierz rearrangement can generate a gluon-
self-energy diagram from a color-singlet scalar insertion.

(iii) The **scalar-operator anomalous dimension in Rep-B has no
counterpart in Rep-A**. Rep-A's OGE extraction of `g_s²` does not
include an operator-renormalization factor, because `g_s²` is a
Lagrangian parameter, not a composite operator matrix element.

(iv) The **vertex correction BZ integrals differ**: `I_v_gauge`
(Dirac `γ^μ γ^ν γ_μ` structure, color `T^A`) vs `I_v_scalar`
(Dirac `γ^μ 1 γ_μ` structure, color identity). No Fierz identity
(Clifford or color) maps these to each other, because their Dirac
Clifford structures differ at the integrand level.

**Consequence.** The ratio correction `Δ_R` retains the
three-channel form

```
    Delta_R  =  (alpha_LM/(4 pi)) · [C_F · Delta_1 + C_A · Delta_2 + T_F n_f · Delta_3]
```

with all three channel coefficients generically nonzero and no
algebraic shortcut that collapses any channel to zero or relates
channels to each other. `Δ_R` MUST be computed channel by channel
via lattice-PT BZ evaluation; no shared Fierz reduction exists.

**Confidence: HIGH** on the no-go verdict. The Fierz identities
D12 and S2 are prerequisites for the tree-level Ward identity, not
constraints on the 1-loop structure. At tree level the Ward
identity is exact; at 1-loop the Rep-A and Rep-B diagrammatic
structures diverge qualitatively and no Fierz rearrangement closes
the gap.

---

## 1. Retained foundations

This note inherits without modification:

- **SU(N_c) color Fierz (D12):**
  On the Q_L block `|ψ|₁ ⊗ |ψ̄|₁ + |ψ|₂ ⊗ |ψ̄|₂ + ...`, the
  Fierz identity for the scalar-singlet channel has coefficient
  `−1/(2 N_c)`. This is the color content of the tree-level Ward
  identity `y_t_bare² = g_bare²/(2 N_c) = 1/6` at SU(3).
- **Lorentz Clifford Fierz (S2):**
  On the scalar-singlet `c_S` channel, the Clifford Fierz
  coefficient is `c_S = 1`. This is the Dirac content of the
  tree-level identity.
- **D16 (composite Higgs):**
  `H_unit = (1/√(N_c · N_iso)) · Σ_{α,a} ψ̄_{α,a} ψ_{α,a}`
  = `(1/√6) · (ψ̄ψ)_{(1,1)}` on the Q_L block.
- **D17 (H-unit normalization):**
  `Z² = N_c · N_iso = 6` on the Q_L block.
- **SU(3) Casimirs:** `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`.
- **Canonical-surface anchors:** `α_LM = 0.09067`,
  `α_LM/(4π) = 0.00721`.

---

## 2. The Ward-theorem Fierz (D12 + S2) is a TREE-LEVEL constraint only

At tree level on the canonical lattice surface:

- The unique diagram contributing to `Γ^(4)(q²)` on the
  scalar-singlet × iso-singlet × Dirac-scalar channel is
  single-gluon exchange (OGE).
- After SU(N_c) color Fierz (D12, coefficient `−1/(2 N_c)`) and
  Lorentz Clifford Fierz (S2, coefficient `c_S = 1`):

```
    Gamma^(4)|_tree  =  -c_S · g_bare^2 / (2 N_c · q^2) · O_S
                     =  -g_bare^2 / 6 · O_S / q^2
                     (at canonical surface)                              (W-tree)
```

- Rep-A identification: `Γ^(4) = −g_s²/(2 N_c · q²) · O_S` ⟹
  `g_s²|_Rep-A_tree = g_bare²`.
- Rep-B identification: `Γ^(4) = −y_t²/q² · O_S` ⟹
  `y_t²|_Rep-B_tree = g_bare²/(2 N_c) = g_bare²/6`.

The tree-level Ward identity is therefore `y_t² · 2 N_c = g_s²`
at canonical bare coupling.

**Role of D12 + S2:** these are the Fierz identities used to derive
the tree-level identity. They express the algebraic equivalence of
the color-singlet and the SU(N_c) color decomposition of the OGE
amplitude at tree level. They are NOT a general principle that
extends to arbitrary 1-loop diagrams.

---

## 3. Why D12 + S2 do not extend to the 1-loop ratio

### 3.1 Rep-A 1-loop structure

Rep-A's 1-loop correction to `g_s²` is the sum of five diagrammatic
categories on the OGE channel:

**A.1 Vertex correction (×2):** 
At each `ψ̄γ^μ T^A ψ` vertex, the 1-loop correction has color factor

```
    T^B T^A T^B  =  (C_F - C_A/2) · T^A
```

which decomposes into a C_F piece and a C_A piece. The BZ integral
is `I_v_gauge`. Dirac structure: `γ^μ γ^ν γ_μ` (projected onto the
scalar-singlet channel).

**A.2 Gluon self-energy on the exchanged propagator:** 
Three sub-diagrams at 1-loop:
- gluon-loop: color `(5/3) C_A` (Feynman-gauge UV pole);
- ghost-loop: color `(−1/6) C_A` (absorbed in gluon-loop aggregate);
- fermion-loop: color `(−4/3) T_F n_f`.

Total color structure: `(5/3) C_A − (4/3) T_F n_f`. BZ integral
`I_SE`.

**A.3 External quark Z_ψ (×2):** 
Each external leg carries a self-energy correction with color
factor `C_F` per leg. BZ integral `I_leg`.

**A.4 Tadpole:** 
On the lattice, absorbed into the tadpole-improvement factor
`u_0 = <P>^{1/4}`. On the retained canonical surface this is
already accounted for in the `α_LM = α_bare / u_0` renormalization.

**A.5 Ghost:** 
Absorbed into the gluon SE aggregate in Feynman gauge.

### 3.2 Rep-B 1-loop structure

Rep-B's 1-loop correction to `y_t²` extracted via H_unit is the sum
of three diagrammatic categories:

**B.1 Scalar vertex correction (×2):** 
At each `H_unit = (1/√6) (ψ̄ψ)_{(1,1)}` insertion, the 1-loop
correction has color factor

```
    T^B · 1 · T^B  =  C_F · 1    (identity color on scalar vertex)
```

which has only a C_F piece, NO C_A mixing. The BZ integral is
`I_v_scalar` (Dirac `γ^μ 1 γ_μ` structure, DIFFERENT from Rep-A's
`I_v_gauge`).

**B.2 Scalar-operator anomalous dimension:** 
Each H_unit insertion contributes a composite-operator renormalization
factor given by the MSbar scalar-density anomalous dimension

```
    gamma_{psi-bar psi}  =  -3 C_F · alpha / (2 pi)
                         =  -6 C_F · alpha / (4 pi)
```

On y_t² (two H_unit insertions), the net contribution is `−6 C_F`
per `(α/(4π))` (accounting for the squared matrix element). Rep-A
has NO analog; `g_s²` is a Lagrangian parameter, not a composite
operator matrix element.

**B.3 External quark Z_ψ (×2):** 
IDENTICAL to Rep-A A.3: `2 C_F · I_leg`. The external physical
quarks are the same in both representations.

### 3.3 Piece-by-piece comparison

| Piece | Rep-A | Rep-B | Shared Fierz? |
|-------|-------|-------|---------------|
| External Z_ψ | `2 C_F · I_leg` | `2 C_F · I_leg` | YES (identical, cancels on ratio) |
| Vertex | `2(C_F - C_A/2) · I_v_gauge` | `2 C_F · I_v_scalar` | NO (different Dirac, different BZ) |
| Gluon SE | `(5/3 C_A - 4/3 T_F n_f) · I_SE` | ABSENT | NO (no analog) |
| Ghost | Absorbed in gluon SE | ABSENT | NO |
| Tadpole | Absorbed in u_0 | Absorbed in u_0 | N/A (cancel) |
| Operator anom. dim. | ABSENT | `−6 C_F` | NO (no analog) |

**Three non-shared categories:**

1. **Gluon SE** (C_A and T_F n_f channels): Rep-A has it; Rep-B
   doesn't.
2. **Scalar-operator anomalous dimension**: Rep-B has it; Rep-A
   doesn't.
3. **Vertex BZ integrals** (`I_v_gauge` vs `I_v_scalar`): different
   Dirac/color structures, different numerical values.

**No Fierz identity maps these categories across Rep-A and Rep-B.**
D12 is a color identity on the SU(N_c) fundamental × anti-fundamental
product; it does not generate a gluon-self-energy diagram from a
scalar-vertex diagram (different diagrammatic topology). S2 is a
Clifford identity on bilinears; it does not convert a scalar-operator
anomalous dimension into a vertex correction (different renormalization
type).

### 3.4 Formal no-go statement

**Claim (shared Fierz shortcut no-go).** There is no algebraic
rearrangement of the color Fierz identity D12 with the Lorentz
Clifford Fierz S2 that maps the Rep-A 1-loop structure to the Rep-B
1-loop structure, or vice versa, on the ratio `Δ_R = δ_y − δ_g` at
the canonical lattice surface.

**Proof sketch.** Any such Fierz rearrangement must preserve the
diagrammatic topology (vertex vs self-energy vs external-leg) and
the renormalization type (Lagrangian parameter vs composite operator).
Fierz identities act on the Dirac/color Clifford structure of a FIXED
diagram; they do NOT convert one diagram topology to another. The
three categories that differ between Rep-A and Rep-B (gluon SE,
scalar-operator anom. dim., vertex BZ) differ in diagram topology
(respectively: SE, operator insertion, different Dirac-at-vertex).
Therefore no algebraic rearrangement of D12 + S2 can produce a
Rep-A-only piece from a Rep-B piece (or vice versa). QED.

---

## 4. Practical consequence: Δ_R is a lattice-PT computation

The shortcut no-go implies that `Δ_R` must be computed at the level
of **each BZ integral channel separately**:

- `Delta_1 = 2 · (I_v_scalar − I_v_gauge) − 6` — requires
  framework-native evaluation of both `I_v_scalar` (Rep-B vertex)
  and `I_v_gauge` (Rep-A vertex) on the retained staggered
  lattice-PT surface;
- `Delta_2 = I_v_gauge − (5/3) · I_SE^{gluonic+ghost}` — requires
  both `I_v_gauge` (Rep-A) and the gluon-SE BZ integral `I_SE`
  (Rep-A only; no Rep-B analog);
- `Delta_3 = (4/3) · I_SE^{fermion-loop}` — requires the fermion-loop
  piece of the gluon SE (Rep-A only).

Each channel coefficient is a genuine BZ integral on the
retained action. There is no shortcut.

**Alternative: cite the BZ integrals from the staggered lattice-QCD
literature.** This is the current operational approach in the
retained Δ_R stack:

- `I_v_scalar ≈ 3–5` (Sharpe 1994, Bhattacharya-Sharpe 1998);
- `I_v_gauge = 0` (retained, conserved point-split current;
  `docs/YT_P1_I1_LATTICE_PT_SYMBOLIC_DECOMPOSITION_NOTE_2026-04-17.md`);
- `I_SE^{gluonic+ghost} ≈ 1–3` (Hasenfratz-Hasenfratz 1980,
  Lepage-Mackenzie 1992);
- `I_SE^{fermion-loop} ≈ 0.5–1.5` (Sharpe-Bhattacharya 1998).

Using these brackets with the retained three-channel structure and
the exact color algebra gives the retained Δ_R central of −3.27 %
(`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`)
and framework-native BZ quadrature central of −3.77 ± 0.45 %
(`docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`).

The no-go closes the question of whether a simpler algebraic
route exists: it does not. `Δ_R` is an irreducibly multi-channel
quantity.

---

## 5. Safe claim boundary

This note claims:

> On the canonical lattice-PT surface (Wilson plaquette + 1-link
> staggered Dirac, tadpole-improved at β = 6), there is no algebraic
> rearrangement of the color Fierz identity D12 with the Lorentz
> Clifford Fierz S2 that maps the Rep-A 1-loop structure (vertex,
> gluon self-energy, ghost, quark self-energy, tadpoles) to the
> Rep-B 1-loop structure (scalar vertex, scalar-operator anomalous
> dimension, quark self-energy) on the ratio correction
> `Δ_R = δ_y − δ_g`. Rep-A has gluon-self-energy and tadpole pieces
> absent from Rep-B; Rep-B has scalar-operator anomalous dimension
> absent from Rep-A; the vertex corrections differ in Dirac
> Clifford structure and color structure (`C_F − C_A/2` in Rep-A vs
> `C_F` identity in Rep-B) with different BZ integral values. The
> only piece that matches between the two representations is the
> external quark Z_ψ, which cancels exactly on the ratio. Therefore
> `Δ_R` must be computed channel by channel via lattice-PT BZ
> evaluation; no Fierz shortcut collapses it.

It does **not** claim:

- that the retained tree-level Ward identity
  `y_t_bare² = g_bare²/(2 N_c)` (from D12 + S2 + D16 + D17) is in any
  way incorrect or incomplete at tree level — it is exact at tree;
- that any particular BZ integral (`I_v_scalar`, `I_v_gauge`,
  `I_SE`, `I_leg`) has a specific framework-native value on the
  retained canonical action (those are OPEN; this note states only
  that they are all needed);
- that the three-channel decomposition
  `Δ_R = (α_LM/(4π)) · [C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3]` is
  modified by this note (it is not; retained unchanged from
  `docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`);
- that any higher-order Fierz-type identity (e.g., Cvitanovic
  birdtrack identities, KLT relations) might provide a shortcut at
  higher loop order — those are different identities and their
  applicability is not addressed here;
- any modification of the master obstruction theorem or publication-
  surface files.

---

## 6. Validation

The runner
`scripts/frontier_yt_p1_shared_fierz_no_go.py` emits deterministic
PASS/FAIL lines and is logged under
`logs/retained/yt_p1_shared_fierz_no_go_2026-04-17.log`. The runner
must return PASS on every check to keep this note on the retained
surface.

The runner verifies:

1. Rep-A 1-loop piece list has vertex + gluon SE + ghost (absorbed)
   + quark SE + tadpole (absorbed); Rep-B 1-loop piece list has
   scalar vertex + scalar-op dressing + quark SE.
2. External Z_ψ is the only piece that matches exactly (both are
   `2 C_F · I_leg`); it cancels on the ratio.
3. Gluon SE (C_A channel and T_F n_f channel) has no counterpart
   in Rep-B (color-singlet scalar insertion has no internal gluon
   to dress).
4. Scalar-operator anomalous dimension (`−6 C_F`) has no counterpart
   in Rep-A (Lagrangian parameter vs composite operator
   renormalization types differ).

The total expected PASS count is 4 checks (one per structural
divide between Rep-A and Rep-B).

No publication-surface file is modified by this submission.

---

## Status

**RETAINED** — formal no-go verdict on the shared-Fierz shortcut
for the 1-loop ratio correction `Δ_R`. The two representations
(Rep-A = OGE extraction, Rep-B = H_unit matrix element) have
structurally different 1-loop piece lists with only the external
Z_ψ matching; the remaining pieces (gluon SE, scalar-op anom. dim.,
vertex BZ integrals) do not admit algebraic rearrangement. `Δ_R`
therefore must be computed channel by channel via lattice-PT BZ
evaluation, closing the "could there be a simpler route?" question
in the negative.
