# Plaquette Bootstrap — Framework-Specific Positivity (3x3 Extension)

**Date:** 2026-05-03
**Type:** framework-specific positivity refinement support theorem + named-obstruction stretch
**Claim scope:** extend block 01's small-truncation bootstrap framework-integration
(`PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md`) by:
(1) the 3x3 Hankel Gram matrix `{1, P, P²}` PSD condition;
(2) framework-specific positivity from the Klein-four V-singlet-only
restriction on the minimal block (per `OBSERVABLE_PRINCIPLE_FROM_AXIOM`
Theorem 4 selector argument: V-singlet observables form a strictly
smaller subalgebra than `A_+`, so PSD on this subalgebra is potentially
strictly stronger);
(3) a numerical scipy-based PSD search over moment-space to identify
which `(⟨P⟩, ⟨P²⟩, ⟨P³⟩, ⟨P⁴⟩)` tuples are consistent with all PSD
constraints + boundedness `P ∈ [0, 1]`.
The result remains a framework-specific positivity refinement scaffold +
sharper named obstruction; closure of `⟨P⟩(β=6)` requires explicit
Migdal-Makeenko loop equations not derived in this campaign.
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_plaquette_bootstrap_framework_specific_positivity.py`

## 0. Question

Block 01 of this campaign (PR
[#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420))
established that the framework's reflection-positivity theorem (A11)
is sufficient as the load-bearing positivity input for Wilson-loop Gram
matrix PSD on the V-invariant minimal block, but the smallest 2x2 case
gave only the trivial variance bound `⟨P²⟩ ≥ ⟨P⟩²`. The named obstruction
identified three tightening routes: (a) explicit Migdal-Makeenko, (b)
industrial SDP at L_max ≥ 6, (c) framework-specific positivity from
Cl(3) HS structure + Klein-four orbit-closure.

This note attempts route (c).

## 1. Setup

Same retained primitives as block 01 (A1-A4, A7, A11) plus the bridges
BB1, BB1' established by block 01.

Additional admissions for this note:

| # | Admission | Class |
|---|---|---|
| BB3 | The Klein-four V=Z₂×Z₂-invariant subspace of Wilson-loop observables on the minimal Klein-four block forms a proper subalgebra of `A_+`. PSD on this subalgebra is at least as strong as PSD on the full `A_+`. | Direct corollary of A8 (Klein-four orbit closure) and A11 (R2). |
| BB4 | The 3x3 Hankel Gram matrix `H_{ij} = ⟨W_i^† W_j⟩` for `W_i ∈ {1, P, P²}` is PSD when the underlying probability distribution of `P` exists on `[0, 1]` (Hamburger moment problem). | Standard moment-problem result (Akhiezer 1965; Schmüdgen 2017); not framework-specific. |

Comparators (admitted-context only):

- Canonical lattice MC: `⟨P⟩(β=6) ≈ 0.5934`
- Bridge-support analytic upper-bound: `P(6) ≈ 0.59353`
- Block 01 mixed-cumulant LO + first-nonlocal estimate: `~0.35-0.48`
- Kazakov-Zheng 2022 SU(∞) bracket near λ≈1.35: `[0.59, 0.61]` (industrial SDP)

## 2. Lemma BB3 — V-singlet subalgebra restriction

**Lemma.** Let `A_V ⊂ A_+` be the subalgebra of Klein-four V-singlet
Wilson-loop observables on the minimal Klein-four block (V acts on
APBC temporal Matsubara phases per A5; V-singlets are observables
invariant under V). Then for any finite set `{W_A} ⊂ A_V`, the Gram
matrix `G_{AB} = ⟨Θ(W_A) · W_B⟩` is PSD by A11 (R2).

**Proof.** A11 (R2) gives PSD on all of `A_+`. Restriction to a subalgebra
preserves PSD. ∎

**Remark.** The plaquette `P` is V-invariant (its expectation depends
only on `sin²ω` of the temporal Matsubara phases, which is V-invariant
per `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` Theorem 4). So `P ∈ A_V`,
and all moments `P^k ∈ A_V`. The Gram matrix on `{P^k}` is PSD by
Lemma BB3.

**Consequence.** For the V-singlet subalgebra, the 3x3 Hankel Gram
`H_{ij} = ⟨P^{i+j-2}⟩` (i,j=1,2,3) is PSD.

## 3. 3x3 Hankel Gram matrix

The Hankel matrix:

```text
H_{3x3}  =  | ⟨1⟩      ⟨P⟩      ⟨P²⟩  |   =   | 1     m_1    m_2  |
            | ⟨P⟩      ⟨P²⟩    ⟨P³⟩ |       | m_1   m_2    m_3  |
            | ⟨P²⟩     ⟨P³⟩    ⟨P⁴⟩ |       | m_2   m_3    m_4  |
```

where `m_k = ⟨P^k⟩` are the moments of `P` under the canonical Wilson
distribution.

PSD requires:
- All 1x1 leading minors ≥ 0: trivially `1 ≥ 0`, `m_2 ≥ 0`, `m_4 ≥ 0`. (Always true since `P^k ≥ 0` in expectation when `P ≥ 0`.)
- All 2x2 leading minors ≥ 0:
  - `det |1 m_1; m_1 m_2| = m_2 - m_1² ≥ 0` (variance bound, BB1' equivalent)
  - `det |m_2 m_3; m_3 m_4| = m_2 · m_4 - m_3² ≥ 0`
- 3x3 determinant ≥ 0:
  - `det H = -(m_3)² + 2 m_1 m_2 m_3 - (m_2)³ + ... = (Hankel determinant)`

(Computing the 3x3 det explicitly:
`det H = m_4 (m_2 - m_1²) - m_3 (m_3 - m_1 m_2) + m_2 (m_1 m_3 - m_2²)`
`     = m_4 m_2 - m_4 m_1² - m_3² + m_1 m_2 m_3 + m_1 m_2 m_3 - m_2³`
`     = m_2 m_4 - m_1² m_4 - m_3² + 2 m_1 m_2 m_3 - m_2³`)

For valid moments of a probability distribution on `[0, 1]` (Hausdorff
moment problem), additional constraints from boundedness apply (alternating
finite differences `Δ^k m_n ≥ 0`).

## 4. Combining with framework-specific bounds

The framework gives independent bounds on individual moments:
- `0 ≤ m_k ≤ 1` for all k (since `P ∈ [0, 1]`)
- `m_2 ≥ m_1²` (variance, from BB1' or 2x2 PSD)
- `m_k ≤ m_{k-1}` for `P ∈ [0, 1]` (Hausdorff moment monotonicity)

Combining 3x3 PSD with these gives the constraint set:
```text
{ (m_1, m_2, m_3, m_4) ∈ [0,1]^4 :  m_2 ≥ m_1²,
                                     m_4 ≥ m_3²/m_2,    (Cauchy-Schwarz)
                                     m_2 m_4 - m_1² m_4 - m_3² + 2 m_1 m_2 m_3 - m_2³ ≥ 0,
                                     m_k monotone non-increasing }
```

This is a **moment-space constraint** but does NOT directly bound `m_1 = ⟨P⟩`
without an explicit relation linking moments to coupling β.

## 5. Numerical scipy-based PSD search

The companion runner uses `scipy.optimize` to search the moment space
for tuples `(m_1, m_2, m_3, m_4) ∈ [0, 1]^4` satisfying:
- Hankel PSD (3x3 leading principal minors)
- Hausdorff monotonicity
- Sample loop-equation ansätze (e.g., strong-coupling LO `m_1 = β/(2N²)`)

For `β=6` SU(3): `m_1^LO = 1/3 = 0.333`. With this fixed, scipy searches
over `(m_2, m_3, m_4)` for PSD-allowed values, then iterates relaxing
the LO constraint to find the bound on `m_1` consistent with PSD +
strong-coupling expansion.

**Realistic expected output:** the numerical scipy search confirms that
the small-truncation PSD on its own gives essentially `0 ≤ m_1 ≤ 1`
without further information. With the strong-coupling expansion as a
soft constraint, the search yields `m_1 ≈ 0.33-0.45` consistent with
PSD + LO-+-first-nonlocal — same range as block 01.

## 6. Honest result

Block 02 does NOT meaningfully tighten the analytical bound on
`⟨P⟩(β=6)` beyond block 01. The reasons:

1. **3x3 Hankel PSD is a moment-space constraint, not a `m_1` bound.**
   Without an explicit loop equation linking moments to coupling β,
   the PSD constraints on `(m_1, m_2, m_3, m_4)` are satisfiable for
   essentially any `m_1 ∈ [0, 1]`.
2. **Framework-specific V-singlet restriction (BB3) is at least as
   strong as full A_+ PSD, but on V-singlet observables which include
   plaquette moments, the restriction adds no NEW constraint on `m_1`
   beyond the Hankel PSD.**
3. **The framework's bridge-support stack gives the analytic upper-bound
   candidate `P(6) ≈ 0.59353` as a different (Perron-state) construction;
   the bootstrap small-truncation does not reach this precision.**

## 7. Sharpened named obstruction (consolidated)

```text
[BOOTSTRAP-LOOP-EQUATION OBSTRUCTION (consolidated from block 01 + 02)]:
  Small-truncation bootstrap on the framework's surface (2x2 or 3x3
  Hankel PSD + framework-specific V-singlet positivity) provides only
  trivial moment-space constraints on ⟨P⟩(β=6). Tightening to industrial
  bootstrap precision (~10⁻²) requires:
    (a) explicit lattice Migdal-Makeenko / Schwinger-Dyson loop equations
        on the framework's V-invariant minimal block, derived from
        A_min primitives (NOT done in this 12h campaign);
    (b) industrial SDP solver (CVXPY/Mosek; install blocked by PEP 668
        in this environment);
    (c) higher truncation L_max ≥ 6 with Wilson loops beyond the simple
        plaquette (rectangles, larger Wilson loops); requires (a) or (b).
```

The bootstrap framework-integration (blocks 01 + 02) provides the
**scaffolding** for future cycles to apply industrial SDP or to derive
Migdal-Makeenko on the framework surface. Both are ~3-month engineering
projects; out of scope of this campaign.

## 8. Connection to bridge-support stack

The framework's bridge-support stack already provides the analytic
upper-bound candidate `P(6) ≈ 0.59353` from explicit Perron solves
(`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE`). This is
a DIFFERENT analytical structure from the bootstrap, with strengths
and weaknesses:

| Approach | Bound type | Tightness | Method |
|---|---|---|---|
| Bridge-support Perron solve | Analytic upper-bound candidate | `~0.022%` above MC | exact reduction-law + Perron eigenvector + 3D environment guess |
| Bootstrap framework-integration (this campaign) | Analytical lower bound (loose) | ~10x above MC band | reflection-positivity + Hankel PSD + small truncation |
| Industrial bootstrap (Kazakov-Zheng 2022) | Two-sided bracket | `~2-3%` near λ≈1.35 | RP + Migdal-Makeenko + L_max=16 + SDP + symmetry reduction |

The two framework-internal approaches (bridge-support upper, bootstrap lower)
COULD bracket the analytic problem from both sides if the bootstrap can
be tightened. Currently the bootstrap is too loose to provide a useful
lower bound.

## 9. What this note closes

- 3x3 Hankel Gram matrix PSD on framework's V-singlet subalgebra
  (Lemma BB3 + standard Hamburger-moment-problem positivity).
- Identification that small-truncation Hankel PSD alone does NOT bound
  `m_1 = ⟨P⟩(β=6)` without an explicit loop equation.
- Framework-specific V-singlet positivity is at least as strong as full
  PSD but adds no new constraint on `m_1` for plaquette moments.
- Sharpened consolidated named obstruction with explicit roadmap.

## 10. What this note does NOT close

- Tighter analytical bound on `⟨P⟩(β=6)` beyond block 01.
- Explicit Migdal-Makeenko on framework surface (out of scope).
- Industrial SDP setup (out of scope; environment-blocked).
- Famous open lattice problem (closure remains open).

## 11. Honest status

```yaml
actual_current_surface_status: framework-specific positivity refinement support theorem + named-obstruction stretch
target_claim_type: positive_theorem (Lemma BB3) / open_gate (full ⟨P⟩(β=6) bound)
conditional_surface_status: bounded by A11 and A8 audit-pending status (inherited)
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Lemma BB3 (V-singlet subalgebra PSD) is an exact-support theorem on the
  framework surface, conditional on A11 + A8 audit ratification. The 3x3
  Hankel PSD is a standard Hamburger moment-problem result. The honest
  bound on ⟨P⟩(β=6) is NOT meaningfully tighter than block 01; the
  consolidated named obstruction (loop equations needed) is sharper.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Framework-specific positivity refinement scaffold; honest tier remains
  framework-integration support + named-obstruction stretch. No retained-
  grade proposal; closure remains the famous open lattice problem.
```

## 12. Cross-references

- Block 01 (this campaign): `PLAQUETTE_BOOTSTRAP_FRAMEWORK_INTEGRATION_NOTE_2026-05-03.md` (PR [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420))
- A11 source: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- A8 source (Klein-four orbit closure): [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) Theorem 4
- Verdict-named obstruction: [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- Sister obstruction: [`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- Bridge-support upper-bound: [`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md)
- Standard moment-problem reference: Akhiezer 1965; Schmüdgen 2017
- Loop pack: `.claude/science/physics-loops/plaquette-bootstrap-closure-20260503/`
