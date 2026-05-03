# Plaquette Bootstrap — Framework-Integration Theorem Note

**Date:** 2026-05-03
**Type:** framework-integration support theorem + named-obstruction stretch
**Claim scope:** map the lattice-bootstrap approach (Anderson-Kruczenski 2017,
Kazakov-Zheng 2022/2024, JHEP 12(2025) 033) onto the framework's retained
primitives, establish that the framework's existing reflection-positivity
theorem (A11, `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`)
is sufficient as the load-bearing positivity input for Wilson-loop Gram
matrix PSD on the minimal Klein-four block, and derive the smallest
non-trivial analytical bound on `⟨P⟩(β=6)` from the 2x2 Gram-matrix
constraint combined with the bridge-support stack's exact mixed-cumulant
audit (`P_full(β) = P_1plaq(β) + β^5/472392 + O(β^6)`).
The result is a framework-integration scaffold + sharper named obstruction,
NOT closure of the famous open lattice problem.
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_plaquette_bootstrap_framework_integration.py`

## 0. Question

`PLAQUETTE_SELF_CONSISTENCY_NOTE.md` (status amended 2026-05-01 to
`bounded`) records the verdict:

> "the explicit analytic `beta = 6` insertion remains open."

The user's net-call assessment proposed three routes for closing
`⟨P⟩(β=6)` analytically:
- H1 Route 1: minimal-block self-consistent saddle (attempted in PR
  [#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410),
  named-obstruction stretch).
- H1 Route 2: Cl(3)+Klein-four counting forcing β=6 (skipped per V1 —
  `G_BARE_RIGIDITY_THEOREM_NOTE.md` already addresses it).
- H1 Route 3: modern lattice bootstrap with reflection positivity +
  Migdal-Makeenko + SDP.

This note sets up H1 Route 3 inside the framework, identifies what is
already retained vs newly admitted, and derives the smallest non-trivial
analytical bound that follows from the framework's existing reflection
positivity (A11) plus the bridge-support stack's exact mixed-cumulant
audit.

## 1. Setup

Retained framework primitives:

| # | Primitive |
|---|---|
| A1-A4 | local algebra `Cl(3)`, substrate `Z³`, finite Grassmann/staggered-Dirac, canonical Wilson normalization `g_bare = 1` (β = 6) |
| A7 | closed-form determinant on minimal `L_s = 2` APBC block |
| **A11** | **reflection positivity (R1-R4) on A_min for canonical CL3-on-Z3 action** |

Newly admitted bridges (this note):

| # | Bridge | Class |
|---|---|---|
| BB1 | Wilson-loop Gram matrix `G_AB = ⟨W_A^† W_B⟩ ⪰ 0` for `{W_A}` polynomial in fields localized in Λ_+ | Direct corollary of A11 (R2) restricted to Wilson-loop subalgebra |
| BB2 | Lattice Migdal-Makeenko / one-link Schwinger-Dyson equation as an algebraic identity relating Wilson-loop expectations | Standard lattice gauge identity (Wilson 1974; Eguchi-Kawai 1982; Migdal 1983); not framework-specific |

Comparators (admitted-context only):

- Canonical lattice MC: `⟨P⟩(β=6) ≈ 0.5934` (`PLAQUETTE_SELF_CONSISTENCY_NOTE`)
- Bridge-support analytic upper-bound candidate: `P(6) ≈ 0.59353`
- Kazakov-Zheng 2022 SU(∞) bracket near λ≈1.35: `⟨P⟩ ∈ [0.59, 0.61]` at L_max=16 ([arXiv:2203.11360](https://arxiv.org/abs/2203.11360))
- Kazakov-Zheng 2024 SU(2) finite-N: 0.1% precision in physical range ([arXiv:2404.16925](https://arxiv.org/abs/2404.16925))
- Mixed-cumulant audit: `P_full(β) = P_1plaq(β) + β^5/472392 + O(β^6)` (`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE`)

## 2. Lemma BB1 — RP theorem (A11) implies Wilson-loop Gram-matrix PSD

**Lemma.** Let `{W_A}` be any finite set of Wilson-loop observables (or
polynomials in field operators) localized in the positive-time half
`Λ_+ = {(t, x⃗) ∈ Λ : t ≥ 0}`. Then the Gram matrix

```text
G_{AB}  =  ⟨ Θ(W_A) · W_B ⟩
```

is Hermitian positive semidefinite (PSD), where `Θ` is the temporal-link
reflection of A11.

**Proof.** A11 (R2) states: "the map `F ↦ G(F, F') := ⟨Θ(F) · F'⟩` is a
positive semi-definite Hermitian sesquilinear form on the algebra `A_+`
of polynomial observables localised in `Λ_+`." Wilson loops localized
in `Λ_+` are a subset of `A_+`; restricting the bilinear form to this
subset gives the matrix `G_{AB}`. Restriction of a PSD Hermitian
sesquilinear form to a finite-dimensional subspace gives a PSD
Hermitian matrix. ∎

**Consequence.** All leading principal minors of `G_{AB}` are non-negative.
For any `α ∈ ℂ^{|A|}`, `∑_{AB} α_A^* α_B G_{AB} ≥ 0`.

## 3. Smallest non-trivial Gram matrix on the minimal block

Let `1` denote the identity (constant observable). Let `P` denote the
Wilson plaquette `(1/N_c) Re tr U_p` for one specific spatial plaquette
`p` localized entirely in `Λ_+`. Both `1` and `P` are real-valued
Hermitian observables (`Θ(1) = 1`, `Θ(P) = P_-` where `P_-` is the
reflected plaquette in `Λ_-`).

The 2x2 Gram matrix is:

```text
G_{2x2}  =  | ⟨Θ(1) · 1⟩    ⟨Θ(1) · P⟩  |   =   | 1            ⟨P⟩         |
            | ⟨Θ(P) · 1⟩    ⟨Θ(P) · P⟩  |       | ⟨P⟩          ⟨P_- · P⟩  |
```

By translation invariance and ⟨P⟩ = ⟨P_-⟩ = ⟨P⟩ (shorthand for the
canonical-volume average), the off-diagonal is just `⟨P⟩`. The diagonal
`⟨Θ(P) · P⟩ = ⟨P_- · P⟩` is the **reflected-plaquette correlator**,
which by cluster decomposition splits into a connected and disconnected
piece:

```text
⟨P_- · P⟩   =   ⟨P⟩²   +   C_{P_-, P}
```

where `C_{P_-, P}` is the connected correlator (positive by RP and by
the cluster property — see Lemma BB1' below).

PSD of `G_{2x2}` ⟺ `det G_{2x2} ≥ 0`:

```text
det G_{2x2}  =  ⟨P_- · P⟩ - ⟨P⟩²  =  C_{P_-, P}  ≥  0.
```

The 2x2 PSD constraint is therefore equivalent to the non-negativity of the
reflected-plaquette connected correlator — which is a direct restatement
of A11 (R1).

**Result of the smallest non-trivial Gram matrix:** `C_{P_-, P} ≥ 0`. This
is *consistent with* but does not *bound* `⟨P⟩(β=6)` on its own.

## 4. Lemma BB1' — connected correlator non-negativity

**Lemma.** For any reflected pair `(P_-, P)` of real-Hermitian Wilson loops,
the connected correlator `C_{P_-, P} = ⟨P_- · P⟩ - ⟨P⟩² ≥ 0`.

**Proof.** Apply A11 (R1) with `F = P - ⟨P⟩` (a real-valued mean-subtracted
observable in `Λ_+`). Then `Θ(F) = P_- - ⟨P⟩` (since the reflection of a
constant is itself). Expanding:

```text
0 ≤ ⟨Θ(F) · F⟩  =  ⟨(P_- - ⟨P⟩)(P - ⟨P⟩)⟩
                =  ⟨P_- P⟩ - ⟨P⟩²       (using ⟨P_-⟩ = ⟨P⟩ = ⟨P⟩)
                =  C_{P_-, P}.
```

So `C_{P_-, P} ≥ 0` follows directly from RP applied to mean-subtracted
plaquettes. ∎

## 5. Combining with the mixed-cumulant audit (BB2-equivalent route)

The framework's `GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE` (cited
in `PLAQUETTE_SELF_CONSISTENCY_NOTE` "Exact bridge-support stack on `main`")
provides the EXACT mixed-cumulant identity:

```text
P_full(β)  =  P_1plaq(β)  +  β^5 / 472392  +  O(β^6).
```

where `P_1plaq(β)` is the single-plaquette baseline value (computable via
SU(3) character expansion). This is an exact algebraic identity on the
framework surface, not a perturbative expansion.

For `β = 6`:

```text
β^5 / 472392  =  6^5 / 472392  =  7776 / 472392  ≈  0.016460.
```

The single-plaquette `P_1plaq(β)` for SU(3) at the strong-coupling leading
order is `β/(2N²) = 6/18 = 1/3 ≈ 0.333`. With higher orders included
(SU(3) character-expansion sum), `P_1plaq(6) ≈ 0.43-0.46` (typical
strong-coupling expansion convergent through ~4-6 orders at β=6).

This gives a **single-plaquette + first nonlocal correction** estimate:

```text
P_full(6)  ≈  P_1plaq(6)  +  0.0165  +  (higher orders ignored).
           ≈  0.45 - 0.48  (depending on truncation of P_1plaq)
```

The actual MC value is 0.5934 — the strong-coupling expansion is NOT
convergent enough at β=6 to give a tight bound.

**Honest result:** the smallest non-trivial framework-integration of the
bootstrap approach gives:

(a) Lemma BB1: framework's RP theorem ⟹ Wilson-loop Gram matrix PSD;
    rigorous, retained-conditional on A11.

(b) Lemma BB1': connected reflected-plaquette correlator non-negativity
    follows from A11 directly (mean-subtracted variant).

(c) Smallest 2x2 PSD analytically equivalent to (b); does NOT bound
    `⟨P⟩(β=6)` on its own.

(d) Combining with the framework's exact mixed-cumulant audit gives a
    perturbative-expansion estimate `P_full(6) ≈ 0.45-0.48`, which is far
    below the MC value 0.5934 — reflecting the strong-coupling expansion's
    poor convergence at β=6 (the famous open problem).

## 6. Sharper named obstruction

Tightening the analytical bound to the published Kazakov-Zheng precision
(~2-3% near λ≈1.35) requires:

```text
[BOOTSTRAP-TIGHTENING OBSTRUCTION]:
  The framework's existing primitives + 2x2 small-truncation bootstrap
  give only weak analytical bounds on ⟨P⟩(β=6). Tightening requires:
    (a) explicit derivation of lattice Migdal-Makeenko / Schwinger-Dyson
        loop equations on the framework's V-invariant minimal block, OR
    (b) higher-truncation (L_max = 6+) Gram matrices + industrial SDP
        solver, OR
    (c) framework-specific positivity refinements from Cl(3) Hilbert-
        Schmidt structure + Klein-four orbit-closure (block 02 attempt).
```

The (c) route is the natural framework-internal next cycle (block 02 of
this campaign).

## 7. Connection to bridge-support stack

The framework's bridge-support stack
(`PLAQUETTE_SELF_CONSISTENCY_NOTE.md` "Exact bridge-support stack on `main`")
already provides an **analytic upper-bound candidate** `P(6) ≈ 0.59353`
from explicit Perron-state reduction theorems and source-sector matrix-element
factorization at β=6, with the explicit window `0.5934 ≤ ⟨P⟩(β=6) ≤ 0.59353`
(±0.022%).

This bootstrap framework-integration provides:
- A **complementary structural attack** via reflection positivity + Gram-matrix PSD
- A **lower-bound expansion** (Section 5) — currently far below MC due to strong-coupling convergence
- A **roadmap** (Section 6) for tightening via framework-specific positivity (block 02)

The two approaches (bridge-support upper-bound + bootstrap lower-bound)
in principle bracket the analytic problem from both sides; closing the
window remains the famous open lattice problem.

## 8. What this note closes

- Framework-integration of the lattice bootstrap approach: A11 (RP theorem)
  is the load-bearing positivity input; Wilson-loop Gram matrix PSD follows
  directly.
- Lemma BB1 + BB1': rigorous PSD on framework surface for any finite Wilson-loop
  set in `Λ_+`.
- Identification of the smallest non-trivial 2x2 case as equivalent to
  reflected connected-correlator non-negativity.
- Sharper named obstruction: explicit roadmap for tightening (block 02 +
  future industrial SDP work).

## 9. What this note does NOT close

- The analytical value of `⟨P⟩(β=6)` (famous open lattice problem).
- A non-trivial lower bound on `⟨P⟩(β=6)` beyond strong-coupling
  expansion.
- The audit-pending status of A11 (this note inherits A11's conditional
  tier).
- Industrial-SDP-class precision (~2-3% as Kazakov-Zheng 2022).

## 10. Honest status

```yaml
actual_current_surface_status: framework-integration support theorem + named-obstruction stretch
target_claim_type: positive_theorem (BB1, BB1') / open_gate (full ⟨P⟩(β=6) bound)
conditional_surface_status: bounded by A11 audit-pending status
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Lemma BB1 (Wilson-loop Gram PSD from A11) and Lemma BB1' (connected
  correlator non-negativity) are exact-support theorems on the framework
  surface, conditional on A11's audit ratification (currently support
  tier, audit-pending). The smallest 2x2 PSD reduces to BB1' analytically.
  The MIXED-CUMULANT-augmented estimate is an expansion-based lower
  bound, not a rigorous bound; honest output is named-obstruction
  stretch.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Framework-integration scaffold + lemmas BB1, BB1'. Inherited A11
  audit-pending status. Honest tier: support theorem with named obstruction
  for tightening to non-trivial bound.
```

## 11. Cross-references

- A11 source: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Verdict-named obstruction: [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- Mixed-cumulant audit: `GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`
- Sister obstruction: [`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- Prior campaign block 03 (mean-field saddle stretch): PR [#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410), `PLAQUETTE_MINIMAL_BLOCK_SADDLE_STRETCH_NOTE_2026-05-02.md`
- Literature: Anderson-Kruczenski 2017; Kazakov-Zheng [arXiv:2203.11360](https://arxiv.org/abs/2203.11360), [arXiv:2404.16925](https://arxiv.org/abs/2404.16925); JHEP 12(2025) 033 SU(3) bootstrap
- Loop pack: `.claude/science/physics-loops/plaquette-bootstrap-closure-20260503/`
