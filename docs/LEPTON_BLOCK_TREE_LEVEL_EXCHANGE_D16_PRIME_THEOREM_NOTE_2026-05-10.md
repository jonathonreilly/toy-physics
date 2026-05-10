# Lepton Block Tree-Level Exchange Identification (D16-prime)

**Date:** 2026-05-10

**Status:** proposed_retained narrow positive theorem on the lepton (2,1)
block. Establishes the analog of the YT-lane's D16 (tree-level
Feynman-rule completeness on the Q_L = (2,3) block) for the L_L = (2,1)
lepton-doublet block. The theorem identifies the unique tree-level
Feynman diagram contributing to the 4-fermion 1PI Green's function
`Γ⁽⁴⁾(q²)` on the iso-singlet × Dirac-scalar channel of the lepton block:
**single-B-exchange** (U(1)_Y, hypercharge gauge boson).

The structural consequence is that the "Fierz-analog factor" entering
the lepton-block analog of the YT identity is a U(1) charge product
`Y(L_L) × Y(e_R)` (rational), NOT the sqrt-rational `1/sqrt(2 N_c)`
that the SU(N_c) color Fierz produces in the YT chain. This sharpens
and confirms the existing SA-A and SA-B obstructions documented in
`CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`.

**Primary runner:** `scripts/frontier_lepton_block_tree_level_exchange.py`

**Lane:** 6 — Charged-lepton mass retention (M5-a partial sharpening)

---

## 1. Theorem statement

**Theorem (D16-prime: lepton-block tree-level exchange identification).**

On the framework's bare action restricted to the lepton sector
(L_L = (2,1) lepton doublet + e_R = (1,1) right-handed charged lepton),
the unique tree-level Feynman diagram contributing to the 4-fermion
1PI Green's function `Γ⁽⁴⁾(q²)` on the **iso-singlet × Dirac-scalar
channel** at O(g_1² + g_2²) is **single-B-exchange** (U(1)_Y gauge
boson).

The other candidate single-particle exchanges are excluded:

| Mediator | Lepton-block contribution | Reason for exclusion |
|---|---|---|
| **Single-B (U(1)_Y)** | **YES** | both L_L and e_R have nonzero hypercharge |
| Single-W (SU(2)_L) | NO | e_R is iso-singlet → no T^a vertex |
| Single-gluon (SU(3)_c) | NO | both L_L and e_R are color-singlet → no T_color vertex |
| Higgs | NO | bare framework action has no fundamental scalar (D9 composite-Higgs) |

The structural consequence:

```text
   Fierz-analog factor on (2,1) = Y(L_L) × Y(e_R)   (rational, U(1) charge product)
                                ≠ 1/sqrt(2 N_c)     (sqrt-rational, SU(N_c) color Fierz)
```

## 2. Setup

### 2.1 Bare framework action ingredients

Per `MINIMAL_AXIOMS_2026-05-03.md` and the YT-lane chain (D1–D17), the
bare framework action contains:

- **Wilson plaquette terms** for SU(3)_c, SU(2)_L, U(1)_Y gauge sectors
- **Staggered Dirac fermion kinetic + gauge-coupling** terms
- **NO fundamental scalar** (no Higgs field as a primary degree of freedom)
- **NO bare Yukawa term** (the Yukawa coupling is what we're DERIVING)

The composite Higgs identification is via D9: `H_unit = (1/√Z²) Σ ψ̄ψ`
on the relevant block. On the L_L block, D17-prime
(`docs/LEPTON_BLOCK_SCALAR_SINGLET_COMPOSITE_UNIQUENESS_D17_PRIME_THEOREM_NOTE_2026-05-10.md`)
gives `H_unit^lep = (1/√2) Σ_α L̄_L^α H_α e_R` with Z² = 2.

### 2.2 Lepton-sector quantum numbers

| Field | Color SU(3) | Iso SU(2)_L | Hypercharge Y (std) | Hypercharge Y (doubled) |
|---|---|---|---|---|
| L_L = (ν_L, e_L)^T | singlet | doublet | -1/2 | -1 |
| e_R | singlet | singlet | -1 | -2 |

Gauge couplings:

- g_1: U(1)_Y coupling (B boson)
- g_2: SU(2)_L coupling (W bosons)
- g_3: SU(3)_c coupling (gluons)

### 2.3 The 4-fermion Green's function on the iso-singlet channel

The 1PI 4-fermion Green's function `Γ⁽⁴⁾(q²)` on the iso-singlet ×
Dirac-scalar channel is the same object computed in YT D16, projected
onto the appropriate iso × color × Lorentz channel:

```text
   Γ⁽⁴⁾_lep(q²) = <L̄_L^α L_L^α | iso-singlet × Dirac-scalar | ē_R e_R>
```

at the canonical evaluation surface (C1 + C2: `u_0 = ⟨P⟩^{1/4}`,
`g_bare = 1`).

## 3. Tree-level diagram enumeration

At O(g_i²) (single-particle exchange), the candidate diagrams are
single-particle exchanges between the L_L and e_R fields. Each
candidate must respect color, isospin, hypercharge, and Lorentz
conservation.

### 3.1 Single-gluon (G) exchange — EXCLUDED

The gluon couples via `g_3 ψ̄ T^a γ^μ ψ G_μ^a` where T^a are
SU(3)_c generators in the fundamental representation. Both L_L and
e_R are color singlets (T^a acts as zero on them). Therefore:

```text
   <L_L | g_3 T^a γ^μ | L_L> = 0   (L_L is color singlet)
   <e_R | g_3 T^a γ^μ | e_R> = 0   (e_R is color singlet)
```

Single-gluon exchange contributes **zero** to the lepton-block 4-fermion
Green's function.

### 3.2 Single-W (W^a) exchange — EXCLUDED

The W bosons couple via `g_2 ψ̄ T^a γ^μ ψ W_μ^a` where T^a are
SU(2)_L generators in the fundamental representation. e_R is an
SU(2) singlet (T^a acts as zero on e_R):

```text
   <e_R | g_2 T^a γ^μ | e_R> = 0   (e_R is iso singlet)
```

Therefore the W^a-e_R-e_R vertex is zero. Single-W exchange between
L_L and e_R is **forbidden** at tree level: there is no W^a vertex
on the e_R end.

### 3.3 Single-B (B) exchange — UNIQUE TREE CONTRIBUTION

The B boson couples via `g_1 ψ̄ Y γ^μ ψ B_μ` where Y is the
hypercharge (a number, not a matrix). Both L_L and e_R have nonzero
hypercharge:

```text
   <L_L | g_1 Y(L_L) γ^μ | L_L> = g_1 Y(L_L) γ^μ ≠ 0
   <e_R | g_1 Y(e_R) γ^μ | e_R> = g_1 Y(e_R) γ^μ ≠ 0
```

Single-B-exchange contributes:

```text
   M_B = g_1² × Y(L_L) × Y(e_R) × (γ^μ ⊗ γ_μ) / q²              (3.3.1)
```

Using S2 (Lorentz Clifford Fierz), the `γ^μ ⊗ γ_μ` structure projects
onto the Dirac-scalar channel with coefficient |c_S| = 1.

### 3.4 Higgs exchange — EXCLUDED (by D9)

The bare framework action has NO fundamental Higgs (per D9
composite-Higgs identification). The composite Higgs `H_unit` emerges
only at low energy as a fermion bilinear. Therefore there is no
tree-level Higgs propagator in `Γ⁽⁴⁾`.

### 3.5 Conclusion: single-B exchange is unique

Of the four single-particle-exchange candidates, only single-B-exchange
contributes nonzero to the iso-singlet × Dirac-scalar channel of the
lepton 4-fermion Green's function. Therefore:

**D16-prime:** at O(g_1²) on the lepton (2,1) block, the unique
tree-level contribution to `Γ⁽⁴⁾_lep(q²)` on the iso-singlet ×
Dirac-scalar channel is single-B-exchange (3.3.1).

## 4. Structural consequence: Fierz-analog is rational, not sqrt-rational

### 4.1 YT chain (Q_L block) Fierz factor

On the Q_L block, the unique tree-level contribution is
single-gluon-exchange. The SU(N_c) color Fierz identity (D12) projects
this onto the color-singlet channel with coefficient

```text
   C_color = 1/(2 N_c) = 1/6                   (YT D12, sqrt-rational^2)
```

producing the YT identity `y_t² = g_s²/(2 N_c)` after integration with
S2 (Lorentz) and D17 (composite uniqueness). The square root
`y_t = g_s/sqrt(2 N_c) = g_s/sqrt(6)` is **sqrt-rational with
non-square radicand 6**.

### 4.2 Lepton block (this theorem D16-prime) Fierz-analog factor

On the L_L block, the unique tree-level contribution is single-B-exchange.
The U(1)_Y "Fierz-analog factor" (charge product) is

```text
   C_Y = Y(L_L) × Y(e_R) = (-1/2) × (-1) = 1/2     (D16-prime, RATIONAL)
```

Note this is a **rational** number, NOT sqrt-rational. The U(1) charge
product is multiplicative; there is no SU(N) trace identity producing a
square-root factor.

### 4.3 Why this matters

The `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
specifically required a Ward identity of the form

```text
   y_τ_bare = G × C   with C structurally sqrt-rational
```

D16-prime sharpens this: the natural lepton-block analog of YT's
sqrt-rational color Fierz factor is the U(1)_Y charge product, which
is rational. So the lepton-block "Ward identity" candidate has the
form

```text
   y_τ_bare ≈ g_1 × Y(L_L) Y(e_R) × (kinematic)
            = g_1 × (1/2) × (kinematic)
```

This is structurally **different** from YT's sqrt-rational form. It
does NOT satisfy the sqrt-rational requirement of the combined no-go.

## 5. Comparison to YT D16 (Q_L block)

| | Q_L block (D16) | L_L block (D16-prime, this note) |
|---|---|---|
| Mediator | single-gluon (SU(3)_c) | single-B (U(1)_Y) |
| Coupling | g_s | g_1 |
| Structural factor | `1/(2 N_c) = 1/6` (sqrt-rational²) | `Y_LL × Y_eR = 1/2` (rational) |
| Sqrt-rational? | YES (1/sqrt(6)) | NO (1/2 = 1/sqrt(4), perfect square) |
| Source identity | SU(N_c) trace `Tr(T^a T^b) = (1/2) δ^{ab}` | U(1)_Y charge product |
| Reflects | non-abelian Fierz with N_c = 3 | abelian charge multiplication |

## 6. Significance

### 6.1 What this theorem closes

D16-prime identifies the unique tree-level contribution to the
lepton-block scalar-singlet 4-fermion Green's function, completing
the analog of the YT-chain step D16 on the lepton block. Combined
with D17-prime (just landed at PR #1018), this provides TWO of the
three structural primitives that an analogous y_τ derivation would
need.

### 6.2 What this theorem does NOT close

- Does NOT complete a y_τ Ward identity. The remaining piece
  (D12-prime: integration of the U(1) charge factor through S2 +
  the H_unit^lep matrix element) requires the actual matching
  computation.
- Does NOT falsify the
  `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`.
  In fact, D16-prime CONFIRMS the no-go by showing that the natural
  lepton-block "Ward identity" candidate has a RATIONAL (not
  sqrt-rational) structural factor — explicitly outside the no-go's
  sqrt-rational requirement.
- Does NOT predict any lepton mass or Yukawa value.

### 6.3 What this theorem enables

- **Sharper SA-B obstruction:** the Cycle 3 SA-B note's claim that
  "U(1)_Y is abelian → no Fierz sqrt-rational factor" is now
  CONCRETIZED by identifying the SPECIFIC tree-level diagram and
  showing its structural factor.
- **M5-a route progress:** combined with D17-prime (#1018), this
  closes 2 of the 3 structural primitives needed for a full
  lepton-block chain analog. The remaining piece (the matching
  computation) would EITHER produce a rational `y_τ ≈ g_1 × const`
  identity (which is a different KIND of Ward identity than YT-T1),
  OR confirm that the matching fails for structural reasons.
- **Cross-confirmation of the combined no-go:** D16-prime confirms
  from a sharper angle that the YT chain doesn't extend in the
  same sqrt-rational form.

## 7. Falsifiers

The theorem is falsified by any one of:

1. A demonstrated tree-level non-B exchange (other than gluon, W, or
   Higgs) that contributes to the lepton iso-singlet 4-fermion channel.
2. A demonstration that single-W-exchange CAN connect L_L to e_R via
   a vertex that the standard SU(2)_L generators forbid (which would
   require new structural content).
3. A demonstration that the bare framework action contains a
   fundamental Higgs (which would contradict D9).
4. A correction to the lepton-sector hypercharge assignments
   (which would change the U(1) charge product).

## 8. What this note does NOT claim

- A `y_τ` Ward identity on the framework surface.
- A Lane 6 closure.
- A prediction of `m_τ`, `m_e`, `m_μ`, or any Yukawa eigenvalue.
- A falsification of the
  `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10` no-go
  (in fact CONFIRMS the no-go from a sharper structural angle).
- An analog of D12 (SU(N_c) Fierz integration) on the (2,1) block —
  D16-prime only identifies the diagram; the integration is separate.

## 9. Cross-references

- D17-prime (lepton-block scalar-singlet uniqueness):
  `docs/LEPTON_BLOCK_SCALAR_SINGLET_COMPOSITE_UNIQUENESS_D17_PRIME_THEOREM_NOTE_2026-05-10.md`
  (PR #1018)
- YT D16 (Q_L block, retained):
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` row D16
- YT D17 (Q_L block, retained):
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` row D17
- Combined no-go (citing M5-a):
  `docs/CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
- SA-A SU(2) anchor exclusion:
  `docs/CHARGED_LEPTON_Y_TAU_WARD_IDENTITY_SU2_ANCHOR_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
- SA-B U(1) anchor exclusion:
  `docs/CHARGED_LEPTON_Y_TAU_WARD_IDENTITY_U1_ANCHOR_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
- Hypercharge bookkeeping:
  `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
- Minimal axioms substrate:
  `docs/MINIMAL_AXIOMS_2026-05-03.md`
- Composite Higgs D9:
  `docs/YUKAWA_COLOR_PROJECTION_THEOREM.md`

## 10. Boundary

This is a narrow positive structural theorem on the lepton (2,1) block,
identifying which single-particle exchange uniquely mediates the
iso-singlet × Dirac-scalar 4-fermion 1PI Green's function. Combined
with D17-prime (PR #1018), it closes 2 of the 3 structural primitives
needed for a full lepton-block analog of the YT chain. The third
primitive (D12-prime: U(1) charge integration through S2 + H_unit^lep)
remains to be computed; this is the next research-level step.

This theorem does NOT close Lane 6; it sharpens the existing
combined no-go by identifying the specific structural reason the
chain doesn't extend in YT's sqrt-rational form.

A class-A runner accompanies this note
(`scripts/frontier_lepton_block_tree_level_exchange.py`).
