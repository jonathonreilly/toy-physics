# BAE Max-Entropy Retained Bounded Obstruction

**Date:** 2026-05-10
**Type:** bounded_theorem (sharpened obstruction; no positive closure;
new positive content: Born-rule operationalism is NOT a candidate path
to BAE closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — additional probe of the
Brannen Amplitude Equipartition (BAE) closure question, attacking the
**information-theoretic / Jaynes max-entropy class** specifically
grounded in retained physical-lattice baseline (PR #725) and retained
Born-rule operationalism (PR #729) + retained C_3 symmetry on hw=1.
This is the class that the 30-probe campaign treated only at literature-
survey level (Surveys 1, 4) and that Probe 18 AV4 touched conditionally;
this note executes it as a derivation.
**Status:** source-note proposal for a sharpened bounded obstruction.
The proposed Born-rule operationalism + physical-lattice baseline + Jaynes
max-entropy attack does NOT close BAE. On the contrary, every Born-rule-
canonical measure points AWAY from BAE. The BAE admission count is
UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** bae-max-entropy-retained-20260510
**Primary runner:** [`scripts/cl3_bae_max_entropy_retained_2026_05_10_baemaxent.py`](../scripts/cl3_bae_max_entropy_retained_2026_05_10_baemaxent.py)
**Cache:** [`logs/runner-cache/cl3_bae_max_entropy_retained_2026_05_10_baemaxent.txt`](../logs/runner-cache/cl3_bae_max_entropy_retained_2026_05_10_baemaxent.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming

- **physical `Cl(3)` local algebra** (legacy minimal-axiom alias:
  `A1`) = the repo's retained local algebra baseline per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename in
  [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md),
  **BAE is the primary name**; the legacy alias **"A1-condition"** remains
  valid in landed PRs.

## Question

The 30-probe BAE closure campaign reached terminal bounded-obstruction
state per
[`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md).
The campaign tested many structural classes but treated the
information-theoretic / Jaynes max-entropy class only at literature-survey
level (Surveys 1, 4 of the external A1 survey) and at conditional level
within Probe 18 AV4.

**This note executes that class as a derivation, specifically grounded
in retained physical-lattice baseline + retained Born-rule operationalism
+ retained C_3 symmetry of hw=1.**

The hypothesis tested:

> "Could a Jaynes max-entropy attack on the (a, |b|)-plane, where the
> max-entropy measure is canonically pinned by retained Born-rule
> operationalism (PR #729) + retained physical-lattice baseline
> (PR #725) + retained C_3 symmetry, give BAE uniquely?"

## Answer

**No.** Born-rule operationalism + physical-lattice baseline + Jaynes
max-entropy do NOT canonically give BAE. On the contrary, every
Born-rule-canonical measure points AWAY from BAE:

| Measure | Description | Max-ent point | Verdict |
|---|---|---|---|
| **M1** = block-democracy | uniform on `(p_+, p_⊥) = (E_+/N, E_⊥/N)` | BAE (κ=2) | not Born-canonical |
| **M2** = Born eigenvalue | `p_k = λ_k² / Σ λ_j²` | degenerate triplet (\|b\|=0) | NOT BAE |
| **M3** = real-dim Gaussian | dE_+ × √E_⊥ dE_⊥ (Probe 25) | κ=1 | NOT BAE |
| **vN entropy** | `S = -Tr(ρ log ρ)` on C_3-invariant ρ | ρ = I/3 (degenerate) | NOT BAE |
| **C_3-Plancherel** | uniform on `Ĉ_3 = {χ_1, χ_ω, χ_ω̄}` | κ=1 (Probe 12) | NOT BAE |

Only M1 (block-democracy) gives BAE — but M1 is NOT a Born-rule
operationalism. It treats isotypes as discrete bins (multiplicity count),
not as Born amplitudes on physical observables. M1 was already proposed
as a candidate NEW primitive in
[`KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`](KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md);
it remains outside the retained stack.

**Verdict: SHARPENED bounded obstruction with new positive content.** The
Jaynes prior-choice convention-trap identified by Probe 18 AV4 is
REINFORCED by this probe: Born-rule operationalism does not pin a
canonical max-ent measure. The BAE admission count is UNCHANGED.

## Setup

### Premises (A_min for this probe)

| ID | Statement | Class |
|---|---|---|
| Cl3 | physical `Cl(3)` local algebra | repo baseline; legacy alias `A1` in [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Z3 | `Z³` spatial substrate | repo baseline; legacy alias `A2` in the same source |
| PhysLat | physical-lattice baseline (Cl(3) on Z^3 is physical, not regulator) | repo baseline; see [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md) |
| ConvUnif | labeling and unit conventions are convention bookkeeping | repo baseline; see [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |
| C3Pres | `C_3[111]` on hw=1 is preserved framework symmetry | repo baseline; see [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md) |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | source dependency; see [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRU | `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; see [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ \|b\|²/a² = 1/2` (BAE) | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Probe12 | Plancherel-uniform on `Ĉ_3` gives (1, 2) → F3 | source dependency; see [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) |
| Probe18 | F1 vs F3 residue on (a, |b|)-plane | source dependency; see [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md) |
| Probe25 | Gaussian path-integral measure → F3 (real-dim weighting) | source dependency; see [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md) |
| Probe28 | Full retained interactions preserve F3 | source dependency; see [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md) |
| BlockDem | block-democracy primitive (already proposed; outside retained stack) | source dependency; see [`KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`](KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms or imports — primitives are derivations from the repo
  baseline or retained work only (per user 2026-05-09 clarification)

## The five candidate max-entropy measures

The probe enumerates five candidate max-entropy measures on the
(a, |b|)-plane. Each measure is "natural" from a different physical
principle. The question is whether retained Born-rule operationalism +
physical-lattice baseline pin one canonically.

### M1 — block-democracy (uniform on isotype bins)

Block probabilities `(p_+, p_⊥) = (E_+/N, E_⊥/N)` where
`E_+ = 3a²`, `E_⊥ = 6|b|²`, `N = E_+ + E_⊥`.

Max `H = -p_+ log p_+ - p_⊥ log p_⊥` over `(a, |b|)` is at
`p_+ = p_⊥ = 1/2 ↔ E_+ = E_⊥ ↔ 3a² = 6|b|² ↔ BAE`.

**Status:** gives BAE, but M1 is the BLOCK-DEMOCRACY primitive — it
treats each ℝ-isotype as a single bin (multiplicity count). M1 was
already proposed in
[`KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`](KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md);
it remains a CANDIDATE primitive outside the retained stack.

### M2 — Born-rule on hw=1 eigenvalues

Born-rule says `p = |amplitude|²` on physical observables. The natural
physical observables on `hw=1 ≅ ℂ³` are eigenvalues
`λ_k = a + 2|b| cos(θ + 2πk/3)` of `H = aI + bC + b̄C²`.

Born-rule probability: `p_k = λ_k² / Σ_j λ_j²`. With cited identity
`Σ_k λ_k² = 3a² + 6|b|²` (verified algebraically), Born-rule on
eigenvalues defines a 3-bin probability distribution.

Max `H = -Σ p_k log p_k` over `(a, |b|, θ)` is at `λ_0 = λ_1 = λ_2`
(degenerate triplet). For the Brannen circulant this means `|b| = 0`,
NOT BAE.

**Status:** Born-rule eigenvalue max-ent → degenerate triplet, NOT BAE.

### M3 — real-dim Gaussian (Probe 25 baseline)

Per Probe 25 (PHYS-AV1), the canonical retained Gaussian path-integral
measure on `Herm_circ(3)` is
`dE_+ × √E_⊥ dE_⊥` (1-real-dim trivial × 2-real-dim doublet).

Max-ent on `(E_+, E_⊥)` with this measure and constraint `E_+ + E_⊥ = N`
maximizes `F3 = log E_+ + 2 log E_⊥`, giving `E_+ = N/3, E_⊥ = 2N/3`,
i.e. `κ = 1`, NOT BAE.

**Status:** matches retained physical-lattice baseline + Gaussian
dynamics; gives F3/κ=1, NOT BAE.

### M4 — von Neumann entropy on C_3-invariant density operator

`ρ` on hw=1 with `[ρ, C_3] = 0` forces `ρ = aI + bC + b̄C²` (same circulant
form as `H`). `Tr(ρ) = 1` gives `a = 1/3`. `ρ ≥ 0` constrains `|b|`.

Max von Neumann entropy `S = -Tr(ρ log ρ) = -Σ p_k log p_k` (with `p_k` =
eigenvalues of `ρ`, which sum to 1) is at all `p_k` equal: `p_k = 1/3`,
forcing `|b| = 0`. `ρ = I/3` (maximally mixed).

**Status:** standard quantum max-ent → `ρ = I/3`, NOT BAE.

### M5 — C_3-character Plancherel-uniform (cited Probe 12)

Plancherel-uniform on `Ĉ_3 = {χ_1, χ_ω, χ_ω̄}` gives `(1/3, 1/3, 1/3)`.
Restricted to ℝ-isotypes (combining `χ_ω`, `χ_ω̄` into a single doublet)
gives `(1, 2)` weighting → F3 → `κ = 1`, NOT BAE. Cited from Probe 12.

**Status:** Plancherel-canonical, gives F3/κ=1, NOT BAE.

## Why Born-rule operationalism does NOT pin M1

The hypothesis was that retained Born-rule operationalism (PR #729)
canonically pins the M1 measure (block-democracy) as the natural
physical max-ent measure on the (a, |b|)-plane. The probe disconfirms
this hypothesis on three grounds:

1. **Born-rule applies to observables, not parameters.** Per the
   Conventions Unification Note (PR #729), `(a, |b|)` are
   operator-coefficient parameters — convention bookkeeping, not
   physical Born amplitudes. Applying Born-rule to `(a, |b|)` is a
   category error.

2. **Born-rule on the physical observables (eigenvalues) gives M2.**
   Eigenvalues of `H` on hw=1 are the natural Born observables.
   Born-rule + max-ent on eigenvalues forces all eigenvalues equal
   (degenerate triplet, `|b|=0`), NOT BAE.

3. **Block probabilities `(p_+, p_⊥)` are not Born amplitudes.** They
   are normalized isotype Frobenius norms, treating each isotype as a
   single "bin". The (1, 1) bin-per-isotype weighting is a multiplicity
   count, not a Born amplitude on a physical observable. The retained
   Conventions Unification Note explicitly distinguishes structural
   prediction from convention bookkeeping; the choice of "bin per
   isotype" is convention bookkeeping, not retained Born structure.

The retained physical-lattice baseline (PR #725) similarly does NOT
pin M1. The closest match is M3 (real-dim Gaussian), which is what
the Probe 25 retained Gaussian path-integral analysis gives. M3 selects
F3/κ=1, NOT BAE.

## The constraint trap

Even granting a canonical measure, Jaynes max-ent requires CONSTRAINTS.
The probe tests three retained constraints:

- **C1: ⟨Tr(H²)⟩ = N (Frobenius scale).** Probe 18 AV4's constraint.
  Under M1 → BAE. Under M3 → κ=1.
- **C2: ⟨Tr(H⁴)⟩ = N4 (quartic moment).** Algebraically nonconstant in
  `(a², |b|²)`; adds a separate constraint surface.
- **C3: ⟨det(H)⟩ or ⟨det²(H)⟩.** Polynomial in `(a, |b|)`; pins yet
  another moment-related (a, |b|) value.

Each retained moment gives a different max-ent point. Retained content
(Hamiltonian dynamics, Wilson coefficient, spectral-action couplings)
does NOT canonically privilege any one moment. This is the SAME class
of trap as Probe 18 AV4 + Probe 25 PHYS-AV1–AV7.

## Theorem (BAE max-entropy retained sharpened bounded obstruction)

**Theorem.** On A1 + A2 + retained physical-lattice baseline (PR #725) +
retained Conventions Unification (PR #729) + retained C_3 symmetry on
hw=1 + retained Block-Total Frobenius + retained MRU + retained
Probe 12 + retained Probe 18 + retained Probe 25:

```
(a) The Jaynes max-entropy attack on the (a, |b|)-plane requires
    BOTH a measure and a constraint. Five natural max-ent measures
    are enumerated:
      M1 — block-democracy
      M2 — Born-rule on hw=1 eigenvalues
      M3 — real-dim Gaussian (Probe 25)
      M4 — von Neumann entropy on C_3-invariant ρ
      M5 — C_3-character Plancherel-uniform
    Of these, only M1 gives BAE. M2, M3, M4, M5 give NON-BAE max-ent
    points (degenerate triplet or κ=1).
    [Verified Sections 1, 3, 5; runner 33/33 PASS.]

(b) Born-rule operationalism (PR #729) most directly supports M2
    (Born-rule on eigenvalues of physical observables on hw=1).
    M2 gives degenerate triplet, NOT BAE.
    [Verified Sections 1.3, 1.4, 2.1.]

(c) (a, |b|) are operator-coefficient parameters (convention
    bookkeeping per PR #729), not Born amplitudes. Block probabilities
    (p_+, p_⊥) are normalized isotype Frobenius norms (multiplicity
    count), not Born amplitudes on physical observables.
    [Section 2.2, 2.3.]

(d) Retained physical-lattice baseline (PR #725) + Gaussian
    path-integral measure (Probe 25) → M3 = real-dim weighting.
    M3 gives κ=1, NOT BAE.
    [Section 1.5, 2.4; Probe 25 cited.]

(e) Standard quantum von Neumann entropy on C_3-invariant density
    operator (M4) gives ρ = I/3 (maximally mixed, degenerate triplet).
    NOT BAE.
    [Section 3.3, 3.4.]

(f) C_3-character Plancherel-uniform max-ent (M5) gives F3 → κ=1,
    NOT BAE (cited from Probe 12).
    [Section 3.1.]

(g) Even granting a measure, the choice of constraint (Tr(H²) vs
    Tr(H⁴) vs det(H) vs det²(H)) is conventional. Different retained
    moments give different max-ent points.
    [Section 4.]

Therefore: Born-rule operationalism + physical-lattice baseline +
Jaynes max-entropy do NOT canonically give BAE. The Jaynes prior-choice
convention-trap identified by Probe 18 AV4 is REINFORCED — Born-rule
operationalism does not pin M1, and on the contrary, every Born-rule-
canonical measure points AWAY from BAE.

The BAE admission count is unchanged. No new admission is proposed.
```

**Proof.** Items (a)–(g) verified by the paired runner (33 PASS / 0 FAIL).
(a) constructs each measure explicitly and computes its max-ent point.
(b) computes Born-rule eigenvalue probabilities and shows max-ent is at
degenerate triplet. (c) cites the retained Conventions Unification Note
(PR #729). (d) cites Probe 25 PHYS-AV1. (e) computes von Neumann entropy
on the C_3-invariant density operator parametrized by `(a, |b|, θ)` with
`Tr(ρ) = 1`. (f) cites Probe 12. (g) computes ⟨Tr(H²)⟩, ⟨Tr(H⁴)⟩,
⟨det(H)⟩, ⟨det²(H)⟩ symbolically and shows each pins a different
(a, |b|) ratio. ∎

## Convention-robustness check

The runner verifies (Section 5):

- For each candidate measure, the max-ent point on the constraint surface
  `E_+ + E_⊥ = 6` is computed numerically. M1 gives `t = 1/2` (BAE);
  M2 (Born) gives `t ≈ 1` or `t ≈ 0` (degenerate); M3 gives `t = 2/3`
  (κ=1); M5 gives `t = 2/3` (κ=1).

- Generic weighting `(μ, ν)`: max at `t* = ν/(μ+ν)`. BAE corresponds to
  `(μ, ν) = (1, 1)`; real-dim/Plancherel correspond to `(μ, ν) = (1, 2)`.

- Born-rule numerical max-ent over the constraint sweep returns
  `t ≈ {0, 1}` (boundary), confirming that Born-rule eigenvalue max-ent
  does NOT achieve BAE in the interior.

## Three honest outcomes (assessed)

The user identified three honest outcomes for this probe at the start.
Assessment:

1. **CLOSURE** — DISCONFIRMED. Born-rule + physical-lattice baseline +
   Jaynes max-entropy do NOT uniquely give BAE.
2. **STRUCTURAL OBSTRUCTION** — CONFIRMED. The Jaynes prior-choice
   convention-trap (Probe 18 AV4) persists under the Born-rule grounding.
3. **SHARPENED** — CONFIRMED. New positive content beyond Probe 18 AV4
   and Probe 25:
   - Born-rule on hw=1 eigenvalues (M2) gives degenerate triplet, NOT BAE.
   - Standard QM von Neumann entropy on C_3-invariant ρ (M4) gives `ρ = I/3`,
     NOT BAE.
   - Retained content (M3 = Gaussian, M5 = Plancherel) all converge on κ=1.
   - The block-democracy primitive (M1) is identified as the SOLE max-ent
     measure that gives BAE, but it is OUTSIDE retained content (already
     so identified by `KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18`).

Outcome class for this probe: **STRUCTURAL OBSTRUCTION (Outcome 2)**
with **SHARPENED content (Outcome 3)** as new positive contribution.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction with new
  positive content; no positive closure of BAE)
- `audit-derived effective status`: set only by the independent audit
  lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with this probe's
  sharpening: "Born-rule operationalism (PR #729) + physical-lattice
  baseline (PR #725) + Jaynes max-entropy do NOT canonically give BAE.
  Every Born-rule-canonical measure points AWAY from BAE; the SOLE
  max-ent measure that gives BAE is block-democracy, which is NOT a
  Born-rule operationalism and remains a candidate primitive outside
  the retained stack."

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Executes the information-theoretic / Jaynes max-entropy class
   (treated only at survey level by Surveys 1, 4 of the 30-probe
   campaign, and at conditional level by Probe 18 AV4) as a derivation.
2. Enumerates five candidate max-entropy measures grounded in retained
   content.
3. Establishes that Born-rule operationalism (PR #729) + physical-
   lattice baseline (PR #725) + retained C_3 symmetry do NOT canonically
   pin the M1 (block-democracy) measure required for BAE.
4. Shows that Born-rule on hw=1 eigenvalues (M2) gives degenerate triplet,
   NOT BAE.
5. Shows that standard QM von Neumann entropy on C_3-invariant ρ (M4)
   gives ρ = I/3 (maximally mixed), NOT BAE.
6. Reinforces Probes 25, 28, 29 by demonstrating that Born-rule
   operationalism + retained content go in the SAME direction (κ=1 or
   degenerate triplet, NOT BAE).
7. Provides a paired runner (33 PASS / 0 FAIL).

### What this probe DOES NOT do

1. Does NOT close BAE.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT promote external surveys to retained authority.

## Honest assessment

The probe was given the explicit task of testing whether Born-rule
operationalism + physical-lattice baseline + Jaynes max-entropy could
close BAE. The hypothesis was that grounding the Jaynes prior choice in
retained Born-rule + physical-lattice content would canonically pin the
M1 (block-democracy) measure required for BAE.

**The probe disconfirms this hypothesis.** Five natural max-entropy
measures grounded in retained content are enumerated, and only one (M1
= block-democracy) gives BAE. M1 is not a Born-rule operationalism; it
treats isotypes as discrete bins (multiplicity count), which is a
convention choice ABOVE Born-rule + physical-lattice content. The
remaining four measures (M2 = Born eigenvalue, M3 = real-dim Gaussian,
M4 = vN entropy, M5 = C_3-Plancherel) all give NON-BAE max-ent points.

The result is consistent with the 30-probe campaign's terminal state:
within the retained stack, every canonical measure converges on F3 or
on a degenerate point, and the F1/(1,1) multiplicity weighting needed
for BAE remains structurally absent. Born-rule operationalism, far from
breaking the obstruction, reinforces it.

This sharpens the campaign's terminal residue from "F1 vs F3 within
the retained additive log-isotype-functional class" (Probe 18) to
"every Born-rule-canonical max-entropy measure on hw=1 points AWAY
from BAE; the SOLE max-ent measure that gives BAE (block-democracy /
M1) is not a Born-rule operationalism."

This is a **negative result** in the strongest sense the campaign has
produced for the information-theoretic class: not just "Born-rule does
not close BAE", but "Born-rule + retained content actively points away
from BAE", consistent with Probes 25, 28, 29.

## Cross-references

### Foundational baseline
- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Physical-lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Conventions unification: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- C_3 symmetry preserved: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained provenance of the C_3 / circulant structure
- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure
- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- Block-democracy candidate primitive: [`KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md`](KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md)

### BAE campaign
- 30-probe campaign synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- BAE rename: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 18 (F1 vs F3): [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- Probe 25 (physical extremization): [`KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md`](KOIDE_BAE_PROBE_PHYSICAL_EXTREMIZATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe25.md)
- Probe 28 (interacting dynamics): [`KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md`](KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md)
- Probe 29 (κ-prediction test): [`KOIDE_BAE_PROBE_KAPPA_PREDICTION_TEST_PARTIAL_FALSIFICATION_NOTE_2026-05-09_probe29.md`](KOIDE_BAE_PROBE_KAPPA_PREDICTION_TEST_PARTIAL_FALSIFICATION_NOTE_2026-05-09_probe29.md)

## Validation

```bash
python3 scripts/cl3_bae_max_entropy_retained_2026_05_10_baemaxent.py
```

Expected: `PASSED: 33/33`

The runner verifies:

1. Section 0 — Retained inputs hold (eigenvalue formula, Block-Total
   Frobenius, MRU weight class, BAE point identification).
2. Section 1 — Three candidate measures M1, M2, M3 explicitly
   constructed; M1 → BAE; M2 → degenerate triplet; M3 → κ=1.
3. Section 2 — Born-rule canonicality analysis: Born-rule most directly
   supports M2 (eigenvalue Born); (a, |b|) are not Born amplitudes;
   block probabilities are not Born amplitudes; M3 = retained physics
   measure; Born-rule + retained content does NOT pin M1.
4. Section 3 — Born-rule + retained C_3 + max-ent: Plancherel-uniform
   gives F3 (Probe 12); ℝ-isotype vs ℂ-character is the (1,1) vs (1,2)
   trap; vN entropy on C_3-invariant ρ gives I/3 (degenerate); numerical
   verification.
5. Section 4 — Constraint trap: Tr(H²), Tr(H⁴), det(H), det²(H) each
   give different max-ent points.
6. Section 5 — Numerical sweep over measure × constraint matrix.
7. Section 6 — Sharpened verdict.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The fact that uniform-on-(p_+, p_⊥) max-entropy gives BAE is a
  consistency equality conditional on the M1 measure choice; the
  underlying structural derivation (forcing M1 from Born-rule
  operationalism + physical-lattice baseline) is what fails.
- `feedback_hostile_review_semantics.md`: stress-tests the semantic
  claim "Born-rule operationalism canonically gives BAE" by enumerating
  five candidate Born-rule + max-ent paths and showing every
  Born-rule-canonical path goes AWAY from BAE.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction with new
  positive content; no retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: this is NOT a one-step
  relabeling of Probe 18 AV4. New content: explicit Born-rule M2
  failure mode (degenerate triplet); explicit von Neumann entropy M4
  failure mode (ρ = I/3); explicit alignment with Probes 25, 28, 29
  showing Born-rule + retained content goes against BAE. Five-measure
  enumeration with paired runner verification.
- `feedback_compute_speed_not_human_timelines.md`: results characterized
  in terms of WHAT additional content would be needed to close BAE
  (a non-Born-rule, non-Gaussian, non-Plancherel max-ent measure with
  cited canonical justification — none currently retained).
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five candidate measures) on a single
  load-bearing structural hypothesis (Born-rule operationalism canonically
  pins block-democracy), with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a source
  theorem note; the paired runner produces cached output; no
  output-packets, lane promotions, or synthesis notes are introduced.

## Review-loop rule

This note records a sharpened bounded obstruction within the BAE
closure campaign's terminal state. New BAE-closure attempts should
explicitly identify why they're outside the structural class
"Born-rule + retained content + Jaynes max-entropy" — since this probe
has structurally established that every Born-rule-canonical max-ent
measure on hw=1 points AWAY from BAE.
