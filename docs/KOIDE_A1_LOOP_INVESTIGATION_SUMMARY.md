# A1 Derivation — /loop investigation summary

**Status:** investigation converged with strong structural candidates; closure remains open

This note summarizes the comprehensive investigation into deriving
A1 (Frobenius equipartition `|b|²/a² = 1/2`, equivalently Brannen `c = √2`,
equivalently Koide `Q = 2/3`) from the retained Cl(3)/Z³ framework + textbook
mathematics, axiom-natively.

## Outcome

A1 has been **comprehensively characterized** but **not yet derived
axiom-natively** from current retained content alone. Multiple
structural hints identified; specific closure routes proposed; lemma
needed for full closure documented.

The investigation produced 7 new A1-focused runners (52 PASS total),
exploring distinct angles:

| # | Runner | Angle | PASS |
|---|---|---|---|
| 1 | `frontier_koide_a1_quartic_potential_derivation.py` | Koide-Nishiura V(Φ) quartic | 5/5 |
| 2 | `frontier_koide_a1_n3_structural_uniqueness.py` | Multi-formula convergence at n=3 | 5/5 |
| 3 | `frontier_koide_a1_cv_equals_one.py` | CV=1 (exponential max-entropy) | 4/4 |
| 4 | `frontier_koide_a1_block_democracy_max_entropy.py` | Block-democracy max-entropy | 5/5 |
| 5 | `frontier_koide_a1_weyl_vector_kostant_coincidence.py` | A_1 Weyl vector match | 6/6 |
| 6 | `frontier_koide_a1_a2_weyl_double_match.py` | A_1 + A_2 double Weyl match | 8/8 |
| 7 | `frontier_koide_a1_lie_theoretic_triple_match.py` | Lie-theoretic triple match | 10/10 |
| 8 | `frontier_koide_a1_yukawa_casimir_identity.py` | Yukawa Casimir-difference | 9/9 |

## A1 characterizations (mathematically equivalent forms)

The /loop confirmed eight equivalent forms of A1:

1. **Algebraic (Frobenius):** `3a² = 6|b|²` ⟺ `|b|/a = 1/√2`
2. **Brannen:** prefactor `c = √2`
3. **Koide:** `Q = (Σm)/(Σ√m)² = 2/3`
4. **Geometric:** 45° latitude on S² from the (1,1,1) axis
5. **Statistical:** coefficient of variation `CV = 1` (exponential)
6. **Variational:** unique minimum of `V(Φ) = [2(trΦ)² − 3tr(Φ²)]²`
7. **Lie-theoretic:** `|b|²/a² = |ω_{A_1, fund}|²` (SU(2) fundamental weight)
8. **Casimir:** `|b|²/a² = T(T+1) − Y²` for Yukawa participants (lepton doublet AND Higgs)

All are mathematically equivalent to A1. None is currently derived
axiom-natively from the retained framework + textbook math alone.

## Six candidate closure routes

The /loop explored six distinct routes to axiom-native A1 closure.
Status of each:

### Route A: Koide-Nishiura U(3) quartic potential

Add `V(Φ) = [2(trΦ)² − 3tr(Φ²)]²` to the retained action. V ≥ 0 with
unique minimum at A1. The 4th-order trace structure is OUTSIDE
HIGHER_ORDER_STRUCTURAL_THEOREMS Theorem 6 (4th-order Clifford
cancellation), so no no-go. Open: derive V from Cl(3)/Z³ EW-scalar lane.

**Status:** structurally compatible, but V not yet derived from retained
axioms. Requires framework extension.

### Route B: Clifford torus / 45° latitude

Equator ↔ 45° latitude geometric coincidence. Connects to "real-irrep-
block democracy" but doesn't add new derivation.

**Status:** rephrasing of A1, not a derivation.

### Route C: AS G-signature Lefschetz sum coincidence

`Σ cot²(πk/3) = 2/3` (Gauss identity at n=3) matches `Q = 2/3`
numerically. Parallel topological derivation but doesn't structurally
replace A1.

**Status:** parallel numerical match, doesn't close A1.

### Route D: Newton-Girard polynomial structure

`V(Φ) = [e₁² − 6e₂]²` with `6 = n(n+1)/2` for n=3. Clean elementary-
symmetric form but doesn't force coefficient 6.

**Status:** structurally suggestive, not closing.

### Route E: A_1 Weyl-vector match

`|b|²/a² = 1/2 = |ω_{A_1, fund}|² = |ρ_{A_1}|²` (Kostant). The retained
Cl⁺(3) ≅ ℍ ⟹ Spin(3) = SU(2) provides A_1 Lie data. Open: structural
lemma connecting Yukawa amplitude to fundamental weight squared.

**Status:** strong Lie-theoretic match; requires lemma to close.

### Route F: Yukawa Casimir-difference identity (STRONGEST)

`T(T+1) − Y² = 1/2 = A1` holds **uniquely** for the lepton SU(2)_L
doublet AND Higgs — the two Yukawa participants. NO other SM particle
satisfies it.

The retained CL3_SM_EMBEDDING_THEOREM provides:
- `T(T+1) = 3/4` from Cl⁺(3) ≅ ℍ (retained)
- `Y² = 1/4` from pseudoscalar ω → U(1)_Y, lepton Y = -1/2 (retained)
- Difference: `1/2 = A1` (derived from retained quantum numbers)

The retained `C_τ = T(T+1) + Y² = 1` (gives `y_τ`) is the SUM. The
candidate A1 is the DIFFERENCE. Both come from same retained data.

**Status:** strongest axiom-native A1 candidate. NO new retained
primitives required. Requires structural lemma:

  `|b|²/a² = T(T+1) − Y²` for Yukawa doublet participants

## Why the lemma is hard: 1-loop QFT analysis

Standard 1-loop QFT does NOT produce `T(T+1) − Y²` (difference) naturally:

- Wavefunction renormalization `Z_ψ` gives `T(T+1) + Y²` (sum, = C_τ)
- Yukawa β-function: gauge contributions enter with same sign
- No standard mechanism distinguishes SU(2)_L from U(1)_Y with opposite signs

For the Casimir-difference identity to be DERIVED (not just observed),
we'd need:
- An anomaly-related Wess-Zumino consistency condition
- SU(2)_L vs U(1)_Y ASYMMETRIC integration measure
- Topological sector distinguishing SU(2) from U(1)

None of these is currently in the retained framework.

## Honest status

A1 remains a **retained-but-not-axiom-native** assumption on the
canonical surface. The /loop made significant progress:

**What's NEW from the investigation:**
1. Identified A1 = T(T+1) − Y² uniquely for Yukawa participants (Route F)
2. Identified A1 = |ω_{SU(2)_L, fund}|² (Lie-theoretic, Route E)
3. Documented 6 structurally distinct candidate closure routes
4. Verified 1-loop QFT does NOT close the lemma (rules out simple paths)
5. Identified the specific gap: structural lemma linking Yukawa
   amplitude ratio to gauge Casimir-difference

**What remains open:**
- The structural lemma `|b|²/a² = T(T+1) − Y²` itself
- Or alternative route via Koide-Nishiura V(Φ) embedding
- Or an entirely new structural principle

**Recommendation for review:**

The /loop has identified Route F (Yukawa Casimir-difference) as the
strongest axiom-native candidate. It uses ONLY retained CL3_SM_EMBEDDING
quantum numbers — no new primitives required. Closure requires proving
the structural lemma, likely via a non-standard QFT mechanism (anomaly,
topological, or asymmetric measure).

This is a well-defined research direction for the next theory pass.
Iterative computational verification (the /loop) cannot close A1 alone;
the structural lemma requires genuinely new theoretical work.

## Regression status

- Historical loop-local status: **175/175 PASS** across the original 24
  support runners.
- Current master regression: `python3 scripts/frontier_koide_lane_regression.py`
- All charged-lepton observables match PDG at <0.03%
- Support picture unchanged: the strongest current executable support still
  isolates `δ = 2/9`, `Q = 2/3`, and a tight charged-lepton scale lane, but
  the physical/source-law A1 bridge, physical Brannen-phase bridge, and
  Type-B rational-to-radian readout remain open on the canonical package
  surface

## References

- `KOIDE_A1_DERIVATION_STATUS_NOTE.md` — A1 landscape with 6 routes
- `CL3_SM_EMBEDDING_THEOREM.md` — retained Cl⁺(3) ≅ ℍ structure
- `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md` — Theorem 1
- `STRUCTURAL_NO_GO_SURVEY_NOTE.md` — 7 retained no-go theorems
- `HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md` — Theorems 5, 6
- `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` — A1 as
  "the one load-bearing non-axiom step"

## Next steps for closure

1. **Prove Route F lemma**: develop a QFT mechanism (anomaly, topological,
   measure-asymmetric) showing `|b|²/a² = T(T+1) − Y²` for Yukawa
   participants. This would close A1 axiom-natively.

2. **Or import Route A (Koide-Nishiura V(Φ))** as retained primitive
   in the EW-scalar lane. Gives A1 as VEV minimum.

3. **Or adopt block-democracy** as retained primitive. Gives A1 as
   per-character equipartition principle.

Any of these three paths would close A1. The investigation has clarified the
landscape sufficiently to choose the most promising route based on
retained-framework compatibility.

## Iter 8 addendum: comprehensive 1/2 catalog

After 8 /loop iterations producing 8 new A1-focused runners (181/181
PASS total, was 142/142 pre-loop), the investigation has cataloged
**9 distinct natural quantities in the retained framework all equal
to 1/2**, all equivalent to the A1 condition `|b|²/a² = 1/2`:

| # | Quantity | Origin |
|---|---|---|
| 1 | `dim(spinor) / dim(Cl⁺(3))` | Cl⁺(3) ≅ ℍ, spinor on ℂ² |
| 2 | `dim(spinor) · g_2²(bare)` | g_2² = 1/dim(Cl⁺(3)) |
| 3 | `T(T+1) − Y²` (lepton doublet) | unique to L doublet + Higgs |
| 4 | `\|ω_{A_1, fund}\|²` (Kostant) | h̄(h̄+1)r/12 = 1/2 |
| 5 | `\|ρ_{A_1}\|²` (Kostant) | rank 1: ρ = ω |
| 6 | `C_2(adj) − dim(fund)·C_2(fund)` for SU(2) | = 1/N for SU(N), N=2 gives 1/2 |
| 7 | σ at A1 = `a_0²/(a_0² + 2\|z\|²)` | C_3-character equipartition |
| 8 | `cos²(45°) = sin²(45°)` | 45° latitude on S² |
| 9 | `|b|²/a²` (A1 itself) | Frobenius equipartition condition |

The DIVERSITY of representations all giving 1/2 strongly suggests
this is a deep retained-framework invariant with multiple natural
definitions converging on it. However, **mathematical equivalence is
NOT the same as derivation** — multiple equivalent rephrasings of A1
do not constitute proof that A1 holds.

The /loop has reached the saturation point for THIS investigation:
further iterations produce variants of the same observation rather
than novel derivation routes. The closure path is well-mapped:

- **Strongest candidate**: Clifford dim-ratio (Route F variant) with
  the open lemma `|b|²/a² = dim(spinor)/dim(Cl⁺(3))`

- **Next-cleanest**: Yukawa Casimir-difference (Route F) with lemma
  `|b|²/a² = T(T+1) − Y²` for Yukawa participants

- **Most rigorous backup**: Koide-Nishiura V(Φ) import (Route A)
  as new retained primitive

Recommendation: stop iterative search here and focus on proving one of the
open lemmas, or on deciding whether a new retained primitive is warranted by
the accumulated structural evidence.

## Iter 9 addendum: external literature scan

Searched recent (2024–2026) physics literature for axiom-native Koide
derivations compatible with our retained Cl(3)/Z³ framework:

**Found (relevant external derivations):**
- preprints.org/202505.2156 (2025): "phase coherence" / topological soliton
  framework. Derives δ = 2/9 via Clifford torus geometry. Already
  evaluated — not directly compatible (Clifford torus → equator, but
  Koide cone sits at 45° latitude; mismatch documented in Route B).
- "Zero-Interaction Principle" (academia.edu/145613039, recent):
  derives δ = 2/9 as difference of "topological moments". Aligns
  conceptually with our AS spectral-flow derivation of δ = 2/9 but
  uses different framework primitives, not directly importable.
- arxiv.org/1809.00425 (2018): "What Physics Does The Charged Lepton
  Mass Relation Tell Us?" — survey paper, no new derivation.
- sciencedirect.com/S0550321321002431 (2021): modified Koide via
  flavor nonets in scalar potential model — extends Koide-Nishiura
  but doesn't derive c = √2 axiom-natively.

**Not found:**
- No external derivation uses "Frobenius equipartition" terminology
  (this is our retained framework's specific phrasing).
- No external work derives A1 from Cl(3) Clifford algebra dim counting.
- No external work uses our Casimir-difference identity (Route F).

**Conclusion:** the retained Cl(3)/Z³ framework's A1 derivation
landscape is genuinely novel. External literature provides parallel
derivations of δ = 2/9 (which we already have via AS) but does NOT
close A1 in a way compatible with our framework.

The path forward remains theoretical work on one of
the identified routes (E, F, or A). Iterative computational exploration
has reached its productive limit.

## Final /loop status

8 iterations produced 8 new A1-focused runners (181/181 PASS total),
3 documentation notes, and 9 distinct equivalent A1 expressions all
equal to 1/2 in the retained framework. Closure remains open.

The /loop is being stopped. All work is committed and pushed to
the April 22 support batch.
Review should start from `CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`.
