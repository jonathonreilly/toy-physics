# Koide BAE Probe 18 — F1 Canonical Q-Functional Sharpened Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; partial closure: F2 ruled out; no positive closure of F1 vs F3)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 18 of the Koide
**BAE-condition** closure campaign. Tests whether the canonical
Q-functional choice F1 (block-total Frobenius, multiplicity-(1,1)
weighted) is forced from cited source-stack content, distinguishing it from
F2 (angular-averaged determinant squared) and F3 (rank-weighted
(1,2)). After Probe 16's identification of three surviving candidates
on the (a, |b|)-plane, this probe enumerates seven attack vectors
against the F1 canonicality question.
**Status:** source-note proposal for a **partially-closing sharpened**
bounded obstruction. F2 is **structurally ruled out** as not in the
retained additive log-isotype-functional class (attack vector AV5).
The discrete F1-vs-F3 residue is unchanged from Probes 12, 13 — same
"R-isotype vs C-character counting" trap. Net effect: discrete
functional ambiguity narrowed from 3 candidates to 2. The BAE
admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-bae-probe-f1-canonical-functional-20260509
**Primary runner:** [`scripts/cl3_koide_bae_probe_f1_canonical_functional_2026_05_09_probe18.py`](../scripts/cl3_koide_bae_probe_f1_canonical_functional_2026_05_09_probe18.py)
**Cache:** [`logs/runner-cache/cl3_koide_bae_probe_f1_canonical_functional_2026_05_09_probe18.txt`](../logs/runner-cache/cl3_koide_bae_probe_f1_canonical_functional_2026_05_09_probe18.txt)

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
- **"BAE-condition" (Brannen Amplitude Equipartition)** = the
  amplitude-ratio constraint `|b|²/a² = 1/2` for the
  `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` on
  `hw=1 ≅ ℂ³`. Per the rename announced in PR #790 (2026-05-09),
  **BAE is the primary name**; the legacy alias **"A1-condition"**
  remains valid in landed PRs (e.g., Probes 1–17 + the eleven-probe
  campaign synthesis) and is preserved here when cross-referencing
  those PRs without rewriting them.

These are distinct objects despite the legacy shared label. This probe
concerns the BAE-condition only; framework axiom A1 is retained and
untouched.

## Question

The eleven-probe campaign synthesis
([`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md))
identified the missing primitive, and Probes 12–13 sharpened it to:

> "the canonical SO(2) phase quotient on the non-trivial doublet of
> `A^{C_3}` = the U(1)_b symmetry of the Brannen δ-readout."

Probe 16 (PR #789) then **eliminated the U(1)_b angular ambiguity**
by pivoting to the Q-functional level — the Brannen Q-functional is
U(1)_b-invariant by construction. This collapses the residue to the
discrete (a, |b|)-plane, with three admissible Q-functional candidates:

```
F1 = log E_+ + log E_⊥             (block-total, mult (1,1))   → κ = 2 = BAE  ✓
F2 = log ⟨det²⟩_{arg(b)}            (angular-averaged det²)     → boundary, NOT BAE
F3 = log E_+ + 2·log E_⊥            (rank-weighted (1,2))       → κ = 1, NOT BAE
```

where `E_+ = ‖π_+(H)‖²_F = 3a²` and `E_⊥ = ‖π_⊥(H)‖²_F = 6|b|²`.

**Question:** Does any cited source-stack content canonically distinguish F1
from F2 and F3?

## Answer

**Partial closure.** F2 is **structurally ruled out** as not in the
retained additive log-isotype-functional class. F1 vs F3 ambiguity
**remains** and is the same residue identified by Probes 12, 13.

**Verdict: SHARPENED bounded obstruction with partial closure.** The
discrete functional ambiguity is narrowed from `{F1, F2, F3}` to
`{F1, F3}`. The remaining BAE residue is unchanged; the campaign's
terminal residue acquires its sharpest characterization to date as:

```
"Within the retained canonical class of additive log-isotype-
functionals on the (a, |b|)-plane, F1 (multiplicity (1,1)) vs F3
(rank/dimension (1,2)) selection is not forced by cited source-stack content."
```

The BAE admission count is UNCHANGED. No new admission is proposed.

## Setup

### Premises (A_min for probe 18)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | source dependency; see [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm`; §4 enumerates F1 and F3 (det carrier) as the two natural retained log-laws | source dependency; see [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| FrobIsoSplit | Frobenius pairing is the unique Ad-invariant inner product on `M_3(ℂ)_Herm` (up to overall positive scalar) | source dependency; see [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1` | source dependency; see [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2` | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Q-readout | Q-functional factors through diagonal-species returned operator (rank-3 quotient) | source dependency; see [`KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md) |
| HSRig | Hilbert–Schmidt rigidity: `B_HS = Tr(XY)` is unique Ad-invariant on `su(3)` up to scalar | source dependency; see [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) |
| Probe1 | RP/GNS does not force `(1,1)` Frobenius pairing on hw=1 from cited source-stack content | source dependency; see [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md) |
| Probe12 | Plancherel-uniform on `Ĉ_3` gives `(1,2)` weighting; `(1,1)` requires combining ω, ω̄ | source dependency; see [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) |
| Probe13 | K-real-structure supplies Z_2 part of (1,1) but not SO(2) | source dependency; see [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms or imports — primitives are derivations from axioms or
  retained work only (per user 2026-05-09 clarification)

## The three candidate Q-functionals (restated)

After Probe 16's pivot to the Q-functional level (eliminating
U(1)_b angular ambiguity), the surviving candidates on the
(a, |b|)-plane are:

```
F1(H) = log E_+(H) + log E_⊥(H)       weights (1, 1)
F2(H) = log ⟨det(H)²⟩_{arg(b)}         weights (1, 1, 1) on eigenvalues, multiplicative
F3(H) = log E_+(H) + 2·log E_⊥(H)      weights (1, 2)
```

with `E_+(H) = ‖π_+(H)‖²_F = 3a²` and `E_⊥(H) = ‖π_⊥(H)‖²_F = 6|b|²`.

**Extremization under `E_+ + E_⊥ = const`:**

| Functional | Extremum location | κ = a²/|b|² | BAE? |
|---|---|---|---|
| F1 | E_+ = E_⊥ = N/2 | 2 | ✓ |
| F2 | boundary (E_⊥ → 0 or E_+ → 0) | undefined / 0 | ✗ |
| F3 | E_+ = N/3, E_⊥ = 2N/3 | 1 | ✗ |

(All three verified algebraically by the runner Sections 1, 6, 9.)

## Per-attack-vector analysis

### AV1 — Conditional-expectation pairing on `A^{C_3}`

**Status: SELECTS F3, NOT F1.**

The canonical conditional expectation `E: M_3(ℂ) → M_3(ℂ)^{C_3}`
defined by `E(X) = (1/3) Σ_g g · X · g^*` (Probe 12 sub-derivation b)
gives an `A^{C_3}`-valued pairing `⟨X, Y⟩_E = E(X^* Y)`. To extract a
scalar, one needs a state on `A^{C_3}`. Probe 12 establishes that the
**canonical (Plancherel-uniform) state** on `A^{C_3}` gives:

```
ω_Planch(⟨H, H⟩_E) = (1/3) Tr(H^* H) = (1/3)(3a² + 6|b|²) = a² + 2|b|²
```

This is the **(1, 2)** weighting → **κ = 1 = F3, NOT F1**. (Runner
Section 2.)

**AV1 outcome:** AV1's canonical scalarizer selects F3, not F1. F1
would require a non-Plancherel state on `A^{C_3}` that is not retained.

### AV2 — Plancherel-canonical state on bimodule

**Status: SELECTS F3, NOT F1.**

Direct restatement of AV1 in Plancherel/Peter-Weyl language: applied
to the eigenvalues of `H` over `Ĉ_3 = {χ_1, χ_ω, χ_ω̄}`,

```
ω_Planch(H^*H) = (1/3)(|λ_1|² + |λ_ω|² + |λ_ω̄|²) = a² + 2|b|²
```

(Runner Section 3.) Same conclusion as AV1: Plancherel-canonical
state gives F3 weighting, NOT F1.

### AV3 — HS-rigidity propagation

**Status: PINS INNER PRODUCT, NOT LOG-FUNCTIONAL.**

The retained Hilbert–Schmidt rigidity theorem
([`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md))
shows `B_HS(X, Y) = Tr(XY)` is the unique Ad-invariant symmetric
bilinear form on `su(3)` up to overall positive scalar. The matter-
sector analogue
([`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md))
shows the Frobenius pairing on `M_3(ℂ)_Herm` is uniquely Ad-invariant
up to overall positive scalar.

**The CHOICE between F1, F2, and F3 is downstream of the inner
product.** All three log-functionals use the SAME canonical Frobenius
inner product when measuring isotype norms `E_+` and `E_⊥`. They
differ only in the **log-functional weighting** applied to those
norms. HS-rigidity / Frobenius-uniqueness pins the inner product, not
the log-functional. (Runner Section 4.)

**AV3 outcome:** AV3 does NOT select F1 over F3 (or F2). Inner-product
canonicality is one structural level above the question.

### AV4 — C_3-invariant maximum-entropy on (E_+, E_⊥)

**Status: REQUIRES CONVENTIONAL MEASURE-AND-CONSTRAINT CHOICE.**

Maximum-entropy on the (E_+, E_⊥)-plane with the constraint
`E_+ + E_⊥ = N` (Pythagoras of `Tr(H^*H)`) and the **uniform measure
on (E_+, E_⊥)** gives the F1 extremum at `E_+ = E_⊥ = N/2` (BAE).

But the choice of:
- (a) measure (uniform on `(E_+, E_⊥)` vs uniform on `(a², |b|²)` vs uniform on the
  isotype eigenvalue tuples), and
- (b) constraint (which conserved quantity?)

is itself conventional. A maximum-entropy framing requires fixing
both, and the framework's cited source-stack content does not pin both choices
canonically. (Runner Section 5.)

**AV4 outcome:** AV4 reaches F1 only conditionally on a specific
measure-and-constraint convention; it does not force F1 from retained
content.

### AV5 — Additive vs multiplicative aggregation (RULES OUT F2)

**Status: STRUCTURALLY RULES OUT F2.**

The retained Block-Total Frobenius theorem (§4 of
[`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md))
operates on the canonical class

```
S_{μ,ν}(H) = μ · log E_+(H) + ν · log E_⊥(H)         (additive log-isotype class)
```

and explicitly enumerates only **two natural retained log-laws** in
this class: F1 = (μ, ν) = (1, 1) (block-total) and F3 = (μ, ν) = (1, 2)
(det carrier). The retained MRU weight-class theorem
([`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md))
classifies all functionals in this class by the formula `κ = 2μ/ν`.

**F2 = `log ⟨det²⟩_{arg(b)}` is NOT in this class.** It is a
multiplicative aggregate over eigenvalues followed by angular
averaging, structurally distinct from any additive function of
isotype Frobenius norms.

**Numerical confirmation (runner Sections 6, 9):**

- F2's extremum on the constraint `E_+ + E_⊥ = N = 6` lies at the
  **boundary** (`E_⊥ = 0.5` in the swept range, near the lower edge),
  NOT at `E_+ = E_⊥ = 3` (the F1 extremum / BAE point).
- F2 evaluated at the BAE point: `F2(BAE) = -0.6931`; F2 at `E_⊥ = 0.5`:
  `F2 = 1.5255`. F2 is genuinely larger near the boundary.
- F2 differs from F1 and F3 by a non-constant function of `(a, |b|)`
  (`std(F2 − F1) ≈ 1.80`, `std(F2 − F3) ≈ 0.98` across the test sweep),
  confirming F2 is not just an additive shift of either.

**AV5 outcome:** F2 is structurally outside the retained canonical
log-isotype-functional class. The 3-candidate ambiguity {F1, F2, F3}
narrows to the 2-candidate ambiguity {F1, F3}. **This is the new
positive partial-closure contribution of Probe 18.**

### AV6 — (1,1) vs (1,2) multiplicity weighting

**Status: UNRESOLVED — same residue as Probes 12, 13.**

Within the retained additive log-isotype-functional class, the
remaining choice is between F1 = (1,1) and F3 = (1,2). Per the
retained Block-Total Frobenius theorem at d = 3, the real-irrep
multiplicity of `Herm_circ(3)` is `(1 trivial + 1 doublet)`, and
`mult(ρ, Herm_circ(3)) = (1, 1)` is the Frobenius-reciprocity-native
**ℝ-isotype** count.

But Probes 12, 13 establish that cited source-stack content does not select
ℝ-isotype counting `(1, 1)` over ℂ-character counting `(1, 1, 1) →
(1, 2)`:

- **Probe 12** (Plancherel/Peter-Weyl): the canonical Plancherel state
  on `Ĉ_3` is uniform `(1/3, 1/3, 1/3)`, which collapses on real
  isotypes to `(1, 2)`, NOT `(1, 1)`.
- **Probe 13** (real-structure / antilinear involution): K-real-
  structure (entry-wise complex conjugation, retained as the T factor
  of CPT) supplies the Z_2 part of ℝ-isotype counting (combining
  `χ_ω ↔ χ_ω̄`) but NOT the SO(2) angular quotient on the doublet.

**AV6 outcome:** F1 vs F3 ambiguity unchanged from Probes 12, 13.
This is the same residue, lifted to the Q-functional level.

### AV7 — RP/GNS canonical pairing (lifted to functional level)

**Status: INHERITS PROBE 1 BARRIER B3.**

Probe 1
([`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md))
established five barriers (B1–B5) blocking the RP/GNS chain. **Barrier
B3** is precisely the log-functional choice issue: even granting
tracial vacuum `ρ_Ω = I/3`, the GNS inner product becomes
`⟨A, B⟩_GNS = (1/3) ⟨A, B⟩_Frobenius`, preserving the (1,1) at the
**inner product** level. But the open residue (Probe 1 §B3) is the
choice of LOG-FUNCTIONAL on the Frobenius geometry — `S_block` (1,1)
vs `S_det` (1,2) — and the GNS inner product alone does NOT select
between them.

At the Q-functional level (this probe's setting), B3 still applies:
F1 vs F3 is exactly the log-functional choice that B3 names as
unresolved.

**AV7 outcome:** Probe 18 inherits Probe 1 Barrier B3. The lifted
question (functional choice on the (a, |b|)-plane) is the same
mathematical question already barred at the algebra level.

## Theorem (Probe 18 sharpened bounded obstruction)

**Theorem.** On A1 + A2 + retained C_3-action on `hw=1` + retained
`M_3(ℂ)` on `hw=1` + retained Block-Total Frobenius + retained
Frobenius Isotype-Split Uniqueness + retained MRU + retained Probe 1
+ retained Probe 12 + retained Probe 13 + retained HS-rigidity:

```
(a) F2 (log <det^2>_{arg(b)}) is structurally NOT in the retained
    canonical class of additive log-isotype-functionals. The retained
    Block-Total Frobenius theorem §4 enumerates only F1 and F3 in
    this class.
    [Closes; runner AV5 Section 6.]

(b) F2's extremum on the constraint E_+ + E_⊥ = const lies at the
    boundary (E_⊥ → 0 or E_+ → 0), NOT at the BAE interior point
    E_+ = E_⊥ = N/2.
    [Closes; runner Sections 6, 9.]

(c) Within the retained canonical class {F1, F3}, the conditional-
    expectation / Plancherel-canonical state route (AV1, AV2) selects
    F3, NOT F1.
    [Closes per Probe 12; runner Sections 2, 3.]

(d) HS-rigidity / Frobenius-uniqueness (AV3) pins the inner product
    on M_3(ℂ)_Herm but is one structural level too coarse to select
    F1 over F3 — both use the same canonical Frobenius inner product.
    [Closes; runner Section 4.]

(e) Maximum-entropy on (E_+, E_⊥) with the (E_+ + E_⊥ = const)
    constraint and uniform measure (AV4) reaches F1's BAE extremum,
    but the measure-and-constraint choice is conventional, not
    cited-source-stack-forced.
    [Closes (conditional); runner Section 5.]

(f) RP/GNS (AV7) inherits Probe 1 Barrier B3: GNS inner product alone
    does not select the log-functional choice F1 vs F3.
    [Closes per Probe 1; runner Section 8.]

(g) The R-isotype counting (1, 1) → F1 vs C-character counting
    (1, 1, 1) ↦ (1, 2) → F3 trap (AV6) is unresolved by retained
    content. This is the SAME residue as Probes 12, 13 lifted to
    the Q-functional level.
    [Probe 12, 13 residue carried forward unchanged; runner Section 7.]

Therefore: F2 is structurally ruled out (AV5 partial closure). The
remaining F1 vs F3 ambiguity is unchanged from Probes 12, 13 and
cannot be derived from cited source-stack content alone. The discrete
functional ambiguity is narrowed from {F1, F2, F3} to {F1, F3}.

The BAE admission count is unchanged. No new admission is proposed.
```

**Proof.** Each item is verified algebraically by the runner (40 PASS /
0 FAIL). (a) verifies F2 is not of the form `μ log E_+ + ν log E_⊥`
by explicit non-coincidence with any (μ, ν) (Section 6, 9). (b)
maximizes F2 on the constraint and demonstrates the boundary location
(Sections 6, 9). (c)–(g) are imports of Probes 1, 12, 13 results
applied at the Q-functional level. ∎

## Convention-robustness check

The runner verifies (Section 10):

- **Scale-invariance of κ ratio** under `H → cH`: F1 and F3 shift by
  additive constants; F2 by `4 log c²`. All preserve extremization
  location.
- **Basis change** `C → C^{-1} = C²` preserves the C_3-isotype
  decomposition.
- **F2's exclusion is independent of arg(b) sampling**: the angular
  average in F2 has been verified to converge under different
  discretization counts (n_φ = 256 used; convergence check holds at
  n_φ = 64, 128).

The bimodule frame and inner product structure remain canonically
pinned by cited source-stack content. What is **not pinned** is the choice
between F1 and F3 within the retained additive log-isotype-functional
class.

## Attack-vector enumeration

| AV | Mechanism | Outcome |
|---|---|---|
| AV1 | Conditional-expectation pairing on A^{C_3} | selects F3 (Plancherel-canonical → (1, 2)) |
| AV2 | Plancherel-canonical state on bimodule | selects F3 (same as AV1, Probe 12 mechanism) |
| AV3 | HS-rigidity propagation (Killing form) | pins inner product, not log-functional |
| AV4 | C_3-invariant max-entropy on (E_+, E_⊥) | reaches F1 conditionally on measure-and-constraint convention |
| AV5 | Additive vs multiplicative aggregation | **rules out F2 structurally** (partial closure) |
| AV6 | (1,1) vs (1,2) multiplicity weighting | unresolved (Probe 12, 13 residue carried forward) |
| AV7 | RP/GNS canonical pairing at functional level | inherits Probe 1 Barrier B3 |

**Net: 3-candidate ambiguity narrowed to 2-candidate ambiguity.**

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction with partial
  closure of F2 exclusion)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["BAE-condition: |b|²/a² = 1/2 (legacy:
  A1-condition)"]` — the residual admission, with the Probe 18
  sharpening: "F1 vs F3 selection within the retained additive
  log-isotype-functional class on the (a, |b|)-plane is not forced
  by cited source-stack content"

**No new admissions added by this probe. The BAE admission count is
UNCHANGED.**

### What this probe DOES

1. Closes the discrete F2 candidate as structurally outside the
   retained canonical class (AV5 partial closure).
2. Lifts Probes 1, 12, 13 obstructions to the Q-functional level,
   confirming the residue persists.
3. Verifies that HS-rigidity / Frobenius-uniqueness is one structural
   level too coarse to address F1 vs F3 (AV3).
4. Sharpens the campaign's terminal residue from "U(1)_b angular
   quotient" (Probe 13) to "F1 vs F3 selection within the retained
   additive log-isotype-functional class on the (a, |b|)-plane".
5. Provides a paired runner verifying each attack vector with explicit
   numerical/algebraic counterexamples.

### What this probe DOES NOT do

1. Does NOT close the BAE-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   eleven-probe campaign synthesis (admit / derive / pivot).
7. Does NOT promote external surveys to retained authority.

## Honest assessment

This probe was given the F1-vs-F2-vs-F3 framing identified by Probe 16
as the campaign's terminal residue at the Q-functional level. The
hypothesis was that the discrete-3-candidate ambiguity (smaller than
prior continuous-symmetry residues) might be addressable from retained
content alone.

**What the probe finds:**

1. **F2 is structurally excluded** (positive partial closure). This is
   the new contribution. The retained canonical class of log-laws is
   the additive class `μ log E_+ + ν log E_⊥`; F2's multiplicative
   det²-aggregate falls outside this class. Numerically, F2's
   extremum on the constraint is at the boundary, not at BAE.

2. **F1 vs F3 within the canonical class is unchanged** from Probes
   12, 13. The Plancherel-canonical state route (AV1, AV2) selects
   F3; the (1,1) ℝ-isotype weighting that gives F1 requires a
   non-canonical state on `A^{C_3}` not pinned by cited source-stack content.

3. **HS-rigidity + Frobenius-uniqueness** (AV3) is structurally
   relevant but operates at the inner-product level, not the log-
   functional level. F1, F2, F3 all use the same canonical Frobenius
   inner product when computing E_+ and E_⊥; they differ only in the
   log-functional weighting on top.

4. **Max-entropy** (AV4) reaches F1 only conditionally on a specific
   measure-and-constraint convention. Without cited source-stack content
   pinning both the prior measure and the conserved constraint, the
   max-entropy framing does not force F1.

5. **The campaign's terminal residue acquires its sharpest
   characterization to date**: "F1 vs F3 selection within the retained
   additive log-isotype-functional class on the (a, |b|)-plane".

This is a **2-candidate discrete ambiguity** within an explicitly
enumerated structural class, sharper than any prior characterization
in the campaign. It does NOT close BAE, but it sharpens the residue
to the smallest structural ambiguity yet identified.

What this probe contributes to the campaign:

1. **Positive partial closure**: F2 is ruled out structurally. The
   campaign's terminal residue is now `{F1, F3}` only — the smallest
   discrete residue identified.
2. **Sharpened residue characterization**: the campaign's open piece
   is the `(μ, ν) = (1, 1)` vs `(1, 2)` weight-class choice within
   the retained `S_{μ,ν}` canonical class. This is the same residue
   as the retained Block-Total Frobenius theorem §4's "minor named
   residue".
3. **Confirmation of campaign terminal state**: an eighteenth
   independent attack now returns the same structural obstruction at
   the F1-vs-F3 level, with F2 partially closed. The structural locus
   is fully consistent with the eleven-probe campaign's synthesis.

The remaining residue is now **maximally sharp**: a single binary
choice between two retained natural log-laws on the same canonical
inner-product geometry, both algebraically clean, neither pinned by
cited source-stack content.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Physical-lattice baseline interpretation: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Preserved-`C_3` interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained provenance of the C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius (with §4 explicit F1/F3 enumeration): [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness (Frobenius is canonical inner product): [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- Q-readout factorization: [`KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)
- HS-rigidity (matter-sector parallel): [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)

### Probe campaign

- Eleven-probe synthesis (campaign terminal state): [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 1 (RP/GNS): [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
- Route D (Newton-Girard, (1,1) vs (1,2) weight-class): [`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure / antilinear involution): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)

### Naming convention

- BAE rename note (announced PR #790 / 2026-05-09): "Brannen Amplitude
  Equipartition (BAE)" is the primary name; "A1-condition" is the
  legacy alias used in landed PRs through Probe 17.

## Validation

```bash
python3 scripts/cl3_koide_bae_probe_f1_canonical_functional_2026_05_09_probe18.py
```

Expected: `=== TOTAL: PASS=40, FAIL=0 ===`

The runner verifies:

1. Section 0 — Retained inputs hold (C unitary, order 3; E_+ = 3a²;
   E_⊥ = 6|b|²; equipartition at BAE).
2. Section 1 — F1, F2, F3 definitions; F1 extremum at BAE (κ=2);
   F3 extremum at κ=1.
3. Section 2 — AV1: conditional expectation E pairing; Plancherel-
   canonical state gives (1, 2) weighting → F3, NOT F1.
4. Section 3 — AV2: Plancherel-uniform on `Ĉ_3` gives `a² + 2|b|²`,
   reproducing AV1.
5. Section 4 — AV3: Frobenius is Ad-invariant; pins inner product,
   not log-functional.
6. Section 5 — AV4: max-entropy reaches F1 conditionally on uniform-
   on-(E_+, E_⊥) measure plus E_+ + E_⊥ = const constraint.
7. Section 6 — AV5: F2 is not in retained additive class; F2's max
   on constraint at boundary, not at BAE.
8. Section 7 — AV6: (1,1) vs (1,2) unresolved per Probes 12, 13.
9. Section 8 — AV7: tracial GNS = (1/3) Frobenius preserves (1, 1) at
   inner product level; log-functional choice still unpinned.
10. Section 9 — F2 robustness: F2 differs from F1 and F3 by
    non-constant function; max at boundary not BAE.
11. Section 10 — Convention robustness (scale-invariance, basis
    change).
12. Section 11 — Verdict synthesis (3 → 2 candidates; F1 vs F3 same
    residue as Probes 12, 13).

Total: 40 PASS / 0 FAIL.

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The fact that uniform-on-(E_+, E_⊥) max-entropy gives F1's
  BAE point is a consistency equality conditional on the measure-and-
  constraint convention; the underlying structural derivation
  (forcing the convention from cited source-stack content) is what fails.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim "F1 is canonical" by showing each attack vector's
  action-level identification fails at a different structural locus
  (inner product vs log-functional vs measure vs canonical state).
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction with
  partial closure; the parent BAE admission remains at its prior
  bounded status; no retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the seven-vector
  attack with explicit numerical counterexamples and the new
  positive partial closure (F2 exclusion via AV5) is substantive new
  structural content, not a relabel of any prior probe.
- `feedback_compute_speed_not_human_timelines.md`: alternative
  routes characterized in terms of WHAT additional content would be
  needed (a non-Plancherel state on `A^{C_3}`, a measure-and-
  constraint principle, a log-functional selector), not how-long-they-
  would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a multi-angle attack (seven independent vectors) on a
  single load-bearing structural hypothesis, with sharp PASS/FAIL
  deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: this note is a
  source theorem note; the paired runner produces cached output;
  no output-packets, lane promotions, or synthesis notes are
  introduced.
