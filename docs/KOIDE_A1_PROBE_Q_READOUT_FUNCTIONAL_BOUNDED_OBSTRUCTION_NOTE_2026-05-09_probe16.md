# Koide A1 Probe 16 — Q-Readout / Functional-Level Pivot, Sharpened Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction at the functional level; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 16 of the Koide
A1-condition closure campaign. Pivots from algebra-level closure
(Probes 1-14) to the **Q-functional / Koide-readout level**, exploiting
the fact that under the retained P1 identification `λ_k = √m_k`, the
Brannen Koide ratio `Q = Σm_k / (Σ√m_k)²` reduces to
`Q(a, |b|) = (a² + 2|b|²)/(3a²)` and is **U(1)_b-invariant by
construction** (depends only on `|b|²/a²`, not on `arg(b)`).
**Status:** source-note proposal for a **sharpened** bounded obstruction.
The Probe 13/14 algebra-level residue (U(1)_b angular quotient on the
b-doublet) is **automatically erased** at the Q-functional level — Q
factors through the U(1)_b-quotient as a function of `|b|²/a²` alone.
However, **the closure of A1 does not follow** from this U(1)_b-erasure:
the residue is sharpened to a **functional-choice ambiguity on the
post-quotient (a, |b|)-plane** between admissible extremization
functionals. The A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe16-q-readout-functional-20260509
**Primary runner:** [`scripts/cl3_koide_a1_probe_q_readout_functional_2026_05_09_probe16.py`](../scripts/cl3_koide_a1_probe_q_readout_functional_2026_05_09_probe16.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_q_readout_functional_2026_05_09_probe16.txt`](../logs/runner-cache/cl3_koide_a1_probe_q_readout_functional_2026_05_09_probe16.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"A1-condition"** = the Brannen-Rivero amplitude-ratio constraint
  `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian circulant
  `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`.

These are distinct objects despite the shared label. This probe
concerns the A1-condition only; framework axiom A1 is retained and
untouched.

## Pivot motivation

All 14 prior probes attacked closure at the **algebra level** —
identifying an operator-level mechanism that fixes `(a, |b|)` such
that `|b|²/a² = 1/2`. Probe 13 (real-structure / antilinear
involution) and Probe 14 (retained-U(1) hunt) sharpened the missing
primitive to:

> "The canonical SO(2) phase quotient on the non-trivial doublet of
> A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout."

This is a **continuous** symmetry, qualitatively different in kind
from any retained algebra symmetry. Probe 14 ruled out 9 retained
U(1) candidates; none projects to U(1)_b on the b-doublet.

Probe 13 §"Honest assessment" listed three options:

> 3. **Pivot to the SO(2)-quotient at the readout level (functional,
>    not algebraic).** The Brannen Q-functional IS U(1)_b-invariant
>    (Q depends only on `|b|²/a²`, not arg(b)). So the SO(2)-quotient
>    could be enforced AT THE Q-READOUT STEP, not at the algebra
>    level.

This probe takes that option. The hypothesis is: **at the Q-readout
level, U(1)_b-invariance is automatic** (Q factors through the
quotient), so the algebra-level residue is **erased by construction**.
The question becomes: does the framework's retained matter-sector
content force `Q = 2/3` at the readout level?

## Phase 1 — Q-functional U(1)_b-invariance under retained P1 identification

Under the retained P1 identification (per
[`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
§1.2):

```text
v_k = √m_k = λ_k     (eigenvalues of H = aI + bC + b̄C² on hw=1)
```

so `λ_k = a + 2|b|cos(arg(b) + 2πk/3)`. Then:

```text
Σ √m_k    =  Σ λ_k     =  Tr(H)         =  3a
Σ m_k     =  Σ λ_k²    =  ‖H‖_F²        =  3a² + 6|b|²
Q         =  Σm_k/(Σ√m_k)²              =  (a² + 2|b|²)/(3a²)
```

Both numerator and denominator depend on `(a, |b|²)` only, hence:

```text
Q(a, b) = Q(a, |b|) ;     Q is U(1)_b-invariant on Herm_circ(3).
```

Equivalently: the **Brannen square-root mass carrier** `√m_k = V₀(1 +
c·cos(δ + 2πk/3))` (per [`KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md`](KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md))
is the same parameterization with `V₀ = a`, `c = 2|b|/a`, `δ = arg(b)`,
and `Q = (c² + 2)/6 = (a² + 2|b|²)/(3a²)`.

**Consequence**: `Q = 2/3 ⇔ a² = 2|b|² ⇔ |b|²/a² = 1/2 = A1`.

## Phase 2 — What U(1)_b-erasure gains at the functional level

The Q-functional **erases** all U(1)_b-non-invariant cited source-stack content
on `Herm_circ(3)`. Concretely, on the post-U(1)_b-quotient (a, |b|)-
plane:

| Functional | U(1)_b-invariant? | Survives quotient |
|---|---|---|
| `Tr(H) = 3a` | ✓ | yes |
| `Tr(H²) = ‖H‖_F² = 3a² + 6|b|²` | ✓ | yes |
| `E_+(H) = ‖π_+(H)‖_F² = 3a²` | ✓ | yes |
| `E_⊥(H) = ‖π_⊥(H)‖_F² = 6|b|²` | ✓ | yes |
| `Tr(H³)` (carries `cos(3 arg b)`) | ✗ | erased after averaging |
| `det(H) = a³ - 3a|b|² + 2|b|³ cos(3 arg b)` | ✗ | erased after averaging |
| `log|det(H)|` (carries `cos(3 arg b)`) | ✗ | erased after averaging |

**Crucial finding**: the **det-carrier law `log|det|`** that the campaign
synthesis identified as the **competing extremization functional**
(landing at `(1,2)` weighting → κ=1, NOT A1) is **NOT** U(1)_b-
invariant. It is **eliminated** by the Q-functional U(1)_b-quotient.

This is genuinely new content of the functional pivot: the algebra-
level closure attempt was barred because of a competition between
multiple admissible carrier functionals, and the **angular-non-invariant
functional (det)** dropped out at the U(1)_b-quotient.

## Phase 3 — The remaining residue at the functional level

Even after U(1)_b-quotient, multiple admissible extremization
functionals survive on the (a, |b|)-plane. We tested three:

### Functional F1: Block-total Frobenius equipartition

```text
S_block(a, |b|) = log E_+ + log E_⊥ = log(3a²) + log(6|b|²)
                = log 3 + log 6 + 2 log a + 2 log |b|
```

Constraint: `E_+ + E_⊥ = 3a² + 6|b|² = const`.
Lagrange extremum: `1/E_+ = 1/E_⊥ → E_+ = E_⊥ → a² = 2|b|² → κ = 2 = A1`. ✓

This is the (1,1)-multiplicity-weighted Frobenius pairing identified
by the campaign synthesis as the missing primitive, realized
explicitly by the retained block-total Frobenius theorem (see
[`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)).

### Functional F2: Angular-averaged log-det

```text
⟨det(H)⟩_arg(b) = a³ - 3a|b|²       (cos(3 arg b) averages to zero)
S_avgdet(a, |b|) = log ⟨det⟩²
```

Constraint: `E_+ + E_⊥ = const`.
Lagrange extremum (numerical): boundary `|b| = 0`, `a → max` → `κ = ∞`,
**NOT** A1. ✗

### Functional F3: Standard log|det|² extremum on (a², |b|²)-plane (rank-weighted)

The (1,2) weighting that the campaign synthesis identified as the
algebra-level competitor. After U(1)_b-quotient, the angular-
non-invariant `cos(3 arg b)` term is averaged out, but the rank-
weighted form survives in modified form:

```text
S_rank(a, |b|) = log a² + 2 log |b|²    (1:2 multiplicity from rank P_+ = 1, P_⊥ = 2)
```

Constraint: `E_+ + E_⊥ = const`.
Lagrange extremum: `1/a² · 2a = 2λ · 6a` and `2/|b|² · |b| = 2λ · 12|b|`
→ `E_+ = (1/3) E_total`, `E_⊥ = (2/3) E_total` → `κ = 1`, NOT A1. ✗

**Verdict on functional-choice**: among the admissible post-U(1)_b-
quotient extremization functionals, **only F1 (block-total Frobenius
equal-weight, (1,1)-multiplicity)** lands at A1. F2 (angular-averaged
det) and F3 (rank-weighted) do not.

## Phase 4 — The sharpened residue

The functional-level pivot **does erase** the U(1)_b angular
ambiguity (Probe 13/14 residue) by construction. The remaining
ambiguity is **the choice of extremization functional** on the
(a, |b|)-plane, among the admissible candidates surviving U(1)_b-
quotient.

The cited source-stack content currently provides:

- `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM` — proved exact,
  but `proposed_retained` (status not yet ratified by independent
  audit). It exhibits F1 with `d = 3` uniqueness and the (1,1)
  multiplicity reading from Frobenius reciprocity.
- The MRU demotion note explicitly flags that the (1,1) weighting
  vs (1,2) weighting choice is **not pinned by cited source-stack content**;
  it is "minor and equivalent in scale to MRU-as-observable-principle".
- No cited matter-sector dynamics extremizes `log E_+ + log E_⊥`
  at the physical point (`V(m)` minimum is `m_V ≈ -0.433`, NOT
  the physical `m_* ≈ -1.161` per
  [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
  §5).

**Sharpened residue at functional level**:

> "The canonical extremization functional on the (a, |b|) post-U(1)_b-
> quotient carrier — selecting `F1 = log E_+ + log E_⊥` (block-total
> Frobenius, (1,1)-multiplicity weighting) over admissible competitors
> `F2 = log⟨det⟩²` (angular-averaged) and `F3 = log E_+ + 2 log E_⊥`
> (rank-weighted) — that lands the extremum at A1 (κ=2)."

This is **strictly smaller** than the Probe 13/14 algebra-level residue:

- Probe 13/14 residue: "U(1)_b angular quotient on the b-doublet" — a
  **continuous** Lie-algebra-1 extension of retained discrete C_3.
- Probe 16 residue: "(1,1) multiplicity weighting selection on the
  post-quotient (a, |b|) plane" — a **discrete** functional-choice
  among finitely many admissible extremization principles.

The functional pivot **converts a continuous-symmetry residue into a
discrete-functional-choice residue**. This is genuine progress, even
though A1 is still not closed.

## Phase 5 — Honest scope: does the polynomial cone identity propagate to closure?

The retained `KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM`
(positive_theorem) gives the polynomial identity:

```text
3(u² + v² + w²) = 2(u + v + w)²    (cone identity)
  ⇔  Q = 2/3
  ⇔  4(uv + uw + vw) - (u² + v² + w²) = 0
```

for any positive triple `(u, v, w) ∈ R³`. This is **purely polynomial**;
the (u, v, w) are abstract coordinates. The retained
`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE` extends the
identity to the C_3-Plancherel components: `Q = 2/3 ⇔ a₀² = 2|z|²`.

**The propagation question**: does the framework's retained matter-
sector √m-vector `v = (√m_e, √m_μ, √m_τ)` lie on the cone?

- **At algebra level (Probes 1-14)**: the closure target is "derive
  `|b|²/a² = 1/2` from cited source-stack content". Result: not closeable —
  needs U(1)_b primitive.
- **At functional level (this probe)**: the closure target is "derive
  the (1,1)-multiplicity-weighting extremum convention from retained
  content". Result: not closeable — convention layer remains.

In **both** framings, the polynomial cone identity is the right
backbone but is **not load-bearing on closure**. It tells us that
"if `(a, |b|)` lies at A1, then `(λ_0, λ_1, λ_2)` lies on the cone
and Q = 2/3", but it does not tell us **why** the framework selects
A1.

## Setup

### Premises (A_min for probe 16)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | source dependency; see [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6|b|²` on `Herm_circ(3)` | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| ConeAlg | Koide `Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2` | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| ConePoly | Polynomial cone three-form equivalence | source dependency; see [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md) |
| P1 | `λ_k = √m_k` (P1 square-root identification) | source dependency; see [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md) §1.2 |
| BrannenSO2 | `Q = (c²+2)/6` U(1)_b-invariant on Brannen carrier | source dependency; see [`KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md`](KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md) |
| Probe13 | Algebra-level residue: U(1)_b SO(2) phase quotient on b-doublet | source dependency; see [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) |
| Probe14 | No retained U(1) projects onto U(1)_b on b-doublet | source dependency; see [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new admissions added by this probe (verdict: SHARPENED, no
  closure achieved without admission, and no admission proposed)
- NO **import of empirical Koide match Q ≈ 2/3 as derivation input**
  (this would be the substep-4 AC narrowing rule violation; instead
  this probe operates entirely in the algebra-form `Q(a, |b|) =
  (a² + 2|b|²)/(3a²)` without instantiating numerical Q values)

## Theorem (Probe 16 sharpened functional-level bounded obstruction)

**Theorem.** On A1 + A2 + retained C_3-action on `hw=1` + retained
`M_3(ℂ)` on `hw=1` + retained Hermitian circulant + retained
block-total Frobenius + retained cone-algebraic equivalence +
retained polynomial cone three-form equivalence + retained P1
identification + retained Brannen-SO(2) phase-erasure support:

```
(a) Q-functional U(1)_b-invariance (closes from cited source-stack content).
    Under P1, Q(a, b) = (a² + 2|b|²)/(3a²) depends only on (a, |b|),
    not arg(b). The Q-functional factors through the U(1)_b-quotient
    of the (a, b) plane.

(b) Det-carrier law erasure under U(1)_b-quotient (closes).
    log|det(H)| carries the U(1)_b-non-invariant cos(3 arg b) term.
    Under U(1)_b-quotient (angular average over arg(b) ∈ [0, 2π)),
    ⟨det(H)⟩ = a(a² - 3|b|²) and ⟨det²⟩ = a^6 - 6a^4|b|² + 9a²|b|^4
    + 2|b|^6. The angular-averaged det-carrier extremum lands at the
    boundary |b|=0 (κ=∞), NOT A1.

(c) Block-total Frobenius equipartition is the canonical extremum
    candidate at functional level (retained-grade candidate, not
    closure).
    log E_+ + log E_⊥ at fixed E_+ + E_⊥ = const has its
    Lagrange extremum exactly at E_+ = E_⊥ ⇔ a² = 2|b|² ⇔ A1.
    F1 lands at A1.

(d) Functional-choice ambiguity persists at functional level.
    Multiple post-U(1)_b-quotient functionals on (a, |b|) plane
    are admissible:
    - F1 = log E_+ + log E_⊥ (block-total Frobenius, (1,1)-mult)
      → extremum at A1 (κ=2).
    - F2 = log⟨det⟩² (angular-averaged det)
      → extremum at |b|=0 boundary (κ=∞), NOT A1.
    - F3 = log E_+ + 2 log E_⊥ (rank-weighted, (1,2)-mult)
      → extremum at κ=1, NOT A1.
    No retained extremization principle pins F1 over F2, F3.

Therefore: the functional-level pivot **erases the U(1)_b angular
ambiguity** (Probes 13/14 residue) by construction, but **does not
close the A1-condition**. The new sharpened residue is a discrete
functional-choice ambiguity among admissible post-U(1)_b-quotient
functionals on (a, |b|), strictly smaller than (and qualitatively
different from) the algebra-level continuous-symmetry residue.

The A1 admission count is unchanged. No new admission is proposed by
this probe.
```

**Proof.** (a) Direct algebraic computation of Q under P1 (runner
Sections 2-3). (b) Direct symbolic computation of det(H) showing the
`cos(3 arg b)` dependence (runner Sections 4.1-4.4). (c) Explicit
Lagrange extremum on F1 (runner Sections 5.1-5.4). (d) Explicit
Lagrange/numerical extrema on F2 and F3 with verification that they
land away from A1 (runner Sections 5.5-5.8). ∎

## Phase 6 — Honest assessment

### Does the functional-level pivot actually work?

**Partially, but not for closure.** It correctly **erases** the
U(1)_b angular component of the algebra-level residue. The Q-
functional automatically respects U(1)_b — that is a fact, not a
postulate. This is genuine progress over Probes 13/14.

But it does **not close A1**. The substantive question — "what
forces `Q = 2/3`?" — moves from "what fixes `(a, |b|)` such that
`|b|²/a² = 1/2` at algebra level" to "what selects the (1,1)-
multiplicity extremum convention F1 over admissible competitors F2,
F3 at the post-quotient functional level". The substantive content
of the residue is **not eliminated**, only **reshaped**.

### Did the retained Koide-cone polynomial identity propagate cleanly to closure?

**No.** The polynomial identity (`KOIDE_CONE_THREE_FORM_EQUIVALENCE`)
provides the **algebraic backbone** linking `Q = 2/3` to `|b|²/a² =
1/2` to the cone equation `3(u² + v² + w²) = 2(u + v + w)²`, but
all three forms are **equivalent under retained algebra**. The
question of whether the framework's matter-sector √m-vector
**lies on** the cone is not closed by the polynomial identity alone;
that would require an independent forcing principle that selects A1
over the continuum of off-cone (a, |b|) pairs.

The retained polynomial cone three-form equivalence is purely
polynomial algebra over abstract `(u, v, w) ∈ R³`. It does **not**
identify `(u, v, w)` with charged-lepton √m amplitudes (per the note's
own `## What this does NOT claim` section). Identifying `(u, v, w) =
(√m_e, √m_μ, √m_τ)` and forcing the cone is precisely the A1
admission this campaign is trying to derive.

### What specifically blocks the functional-level approach?

The block is the **functional-choice convention**. Even after U(1)_b-
quotient, three admissible extremization functionals survive on the
(a, |b|)-plane:

1. **F1** (block-total Frobenius, (1,1)-multiplicity): lands at A1.
2. **F2** (angular-averaged det): lands at boundary, NOT A1.
3. **F3** (rank-weighted, (1,2)-multiplicity): lands at κ=1, NOT A1.

The retained `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM` is
`proposed_retained` but the canonicality of F1 over F2, F3 is exactly
what the campaign synthesis flagged as the missing primitive.

The retained `KOIDE_MRU_DEMOTION_NOTE` explicitly says the (1,1) vs
(1,2) choice is "minor and equivalent in scale to MRU-as-observable-
principle" but **not derivable from cited source-stack content alone**. This
probe verifies that the same kind of choice persists at the functional
level, in modified form — the (1,1)-multiplicity vs angular-averaged-
det convention.

### Critical circularity check

**Does this probe smuggle in the empirical Q ≈ 2/3 match?**

No. The probe operates entirely on the algebraic Q-functional `Q(a,
|b|) = (a² + 2|b|²)/(3a²)` without instantiating numerical PDG mass
values. The runner verifies:

- F1 extremum at `a² = 2|b|²` (algebraic, no PDG input).
- F2, F3 extrema at boundaries / `κ = 1` respectively (algebraic).

The retained PDG numerical realization (`PDG E_+/E_⊥ ≈ 1.000018` per
the block-total Frobenius theorem §5.2) is an **audit-comparator
observation only**, never load-bearing on the in-scope content. It
appears in the retained block-total theorem note for falsification
purposes but is not used here as a derivation input.

This satisfies the substep-4 AC narrowing rule.

## Convention-robustness check

- **Scale-invariance** of `|b|²/a²` is preserved under `H → cH`. ✓
- **Basis change** `C → C^{-1} = C²` preserves C_3-action and isotype
  structure. ✓
- **U(1)_b-invariance** of Q is convention-independent (depends on
  P1 identification only, which is retained). ✓

The post-U(1)_b-quotient (a, |b|)-plane is canonically pinned by
cited source-stack content. What is **not pinned** is the **canonical
extremization functional on that plane** — the surviving
convention-trap.

## Attack-vector enumeration

This is the sixteenth attack vector in the campaign:

| # | Attack vector | Outcome |
|---|---|---|
| 16 | Q-functional / Koide-readout level pivot | sharpened obstruction; erases U(1)_b angular ambiguity by construction; remaining residue is functional-choice convention on (a, \|b\|) plane |

This refines the residue from Probe 13/14:

- **Probe 13/14 residue**: U(1)_b angular quotient on b-doublet
  (continuous Lie-algebra-1 extension).
- **Probe 16 residue**: discrete functional-choice convention on
  (a, |b|) plane (block-total Frobenius vs angular-averaged det
  vs rank-weighted).

The qualitative shift from continuous-symmetry residue to discrete-
functional-choice residue is genuine progress in the campaign, even
though A1 is not closed.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction; no closure)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["A1-condition: |b|²/a² = 1/2"]` —
  the residual admission, with the Probe 16 sharpening:
  "the canonical extremization functional on the (a, |b|) post-U(1)_b-
   quotient carrier — block-total Frobenius (1,1)-multiplicity over
   angular-averaged det or rank-weighted competitors — that lands the
   extremum at A1 (κ=2)"

**No new admissions added by this probe.**

### What this probe DOES

1. Verifies that under retained P1 identification `λ_k = √m_k`, the
   Brannen Koide ratio `Q(a, b) = (a² + 2|b|²)/(3a²)` is U(1)_b-
   invariant by construction.
2. Verifies that the **det-carrier law** (campaign synthesis's
   competing functional for κ=1) is **NOT** U(1)_b-invariant and is
   **eliminated** by the U(1)_b-quotient.
3. Verifies that the block-total Frobenius equipartition F1 = log E_+
   + log E_⊥ has its Lagrange extremum at A1 (κ=2) on the (a, |b|)-
   plane.
4. Verifies that admissible competitors F2 (angular-averaged det)
   and F3 (rank-weighted) land **away** from A1.
5. Sharpens the residue from Probes 13/14's "U(1)_b angular quotient"
   (continuous) to "(1,1)-multiplicity functional convention"
   (discrete).

### What this probe DOES NOT do

1. Does NOT close the A1-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem (BZ, 3GenObs, Circulant,
   BlockTotalFrob, ConeAlg, ConePoly, P1, BrannenSO2, Probe13,
   Probe14).
4. Does NOT promote any downstream theorem (the block-total Frobenius
   measure theorem remains `proposed_retained`).
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   eleven-probe campaign synthesis (admit/derive/pivot).

## Strategic options remaining

This probe **does not select** an option. Three options remain after
16 probes:

1. **Continue derivation hunt**. The residue is now precisely
   characterized at functional level: (1,1)-multiplicity functional
   selection convention. A future probe might find a derivation of
   F1 canonicality from cited source-stack content (e.g., max-entropy
   principle on isotypic decomposition, Gibbs-state argument, or a
   variational principle internal to retained `Cl(3)` structure).

2. **Admit the (1,1)-multiplicity functional convention**. With user
   approval, add a single line: "the canonical extremization
   functional on the (a, |b|) post-U(1)_b-quotient carrier is the
   block-total Frobenius (1,1)-multiplicity-weighted log-law." Under
   such an admission, A1 follows immediately. The cost is one named
   admission; the rest of the framework is unchanged.

3. **Pivot to other bridge work**. The A1-condition is one named
   target among multiple bridge-gap admissions. The audit lane and
   the user may classify A1 as a parameter/readout target and
   prioritize independent bridge work over A1-closure attempts.

## Honest note on the polynomial identity

The retained `KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM` is
positive_theorem and provides the polynomial backbone:

- `(F_orbit)`: `4(uv + uw + vw) - (u² + v² + w²) = 0`
- `(F_ratio)`: `(u² + v² + w²)/(u + v + w)² = 2/3`
- `(F_cyclic)`: `2 r₀² = r₁² + r₂²` (in cyclic basis)

These are equivalent for any abstract (u, v, w). The probe verifies
that under the retained P1 identification (v_k = √m_k = λ_k = a +
2|b|cos(arg(b) + 2πk/3)), the (F_ratio) form gives `Q = (a² +
2|b|²)/(3a²)` (post-U(1)_b-erasure). The polynomial identity is
correctly applied; it does not, by itself, force A1.

The functional-level pivot's contribution is to make the U(1)_b-
erasure manifest at the readout level (rather than requiring an
algebra-level continuous symmetry, which Probe 14 ruled out from
cited source-stack content). This **clears one obstruction** but uncovers a
second discrete one (functional-choice convention).

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained polynomial Koide-cone identities

- Three-form equivalence: [`KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_THREE_FORM_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md)
- Completing-root narrow: [`KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md`](KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02.md)
- Algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Retained spectrum-operator bridge and P1 identification

- Spectrum-operator bridge: [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
- Block-total Frobenius (proposed_retained): [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU demotion (functional-choice convention status): [`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md)

### Retained Brannen-carrier U(1)_b-erasure support

- Brannen Q SO(2) phase erasure: [`KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md`](KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md)
- Q readout factorization: [`KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)
- Brannen phase reduction: [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)

### Sister Koide-A1 probes

- Probe 13 (real-structure / antilinear involution): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) — sharpened residue: U(1)_b angular quotient
- Probe 14 (retained-U(1) hunt) — see [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md)

### Eleven-probe campaign baseline

- Synthesis (campaign terminal state, pre-Probe 12): [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_q_readout_functional_2026_05_09_probe16.py
```

Expected: `=== TOTAL: PASS=N, FAIL=0 ===`

The runner verifies:

1. Retained inputs (Section 1): C unitary, order 3, eigenvalues
   `{1, ω, ω̄}`; H = aI + bC + b̄C² is Hermitian and circulant.
2. P1 identification under retained spectrum-operator bridge:
   `λ_k = √m_k` (Section 2).
3. Q-functional under P1: Q(a, b) = (a² + 2|b|²)/(3a²) is U(1)_b-
   invariant (Section 3).
4. Det carrier carries cos(3 arg b) and is NOT U(1)_b-invariant
   (Section 4).
5. Block-total Frobenius F1 extremum at A1 (Section 5.1).
6. Angular-averaged det F2 extremum at boundary, NOT A1 (Section 5.2).
7. Rank-weighted F3 extremum at κ=1, NOT A1 (Section 5.3).
8. Functional-choice ambiguity verified explicitly (Section 6).
9. No PDG numerical input is load-bearing (Section 7).
10. Polynomial cone identity applied correctly under P1 (Section 8).
11. Convention-robustness checks (Section 9).
12. Verdict: SHARPENED bounded obstruction; A1 admission count
    UNCHANGED (Section 10).
