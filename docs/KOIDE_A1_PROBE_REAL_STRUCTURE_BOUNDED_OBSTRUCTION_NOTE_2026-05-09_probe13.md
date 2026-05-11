# Koide A1 Probe 13 — Real-Structure / Antilinear-Involution Sharpened Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure; no new admission)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 13 of the Koide
A1-condition closure campaign. Tests the **real-structure /
antilinear-involution mechanism** identified by Probe 12 as the
precisely-localized missing primitive — specifically, whether any
retained antilinear involution on `M_3(ℂ)` canonically combines `ω`
and `ω̄` characters into the real doublet that would force ℝ-isotype
counting (`(1,1)`) over ℂ-character counting (`(1,2)`) on
`M_3(ℂ)_Herm` under `C_3`-isotype decomposition.
**Status:** source-note proposal for a **sharpened** bounded obstruction.
The Probe 12 residue is **refined further**: K-real-structure (entry-wise
complex conjugation, retained as the T factor of CPT_EXACT_NOTE) DOES
supply the Z_2 part of ℝ-isotype counting (combining `ω` and `ω̄`
characters via `χ_ω ↔ χ_ω̄`), but does NOT supply the SO(2)-angular
quotient on the doublet (the U(1)_b symmetry of the Brannen δ-readout)
required for the (1, 1) weighting on the reduced two-slot carrier
`(ρ_+, ρ_⊥)` of MRU. The A1 admission count is UNCHANGED. The
sharpened residue is genuinely smaller than Probe 12's "ℝ-isotype
counting principle".
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-real-structure-20260509
**Primary runner:** [`scripts/cl3_koide_a1_probe_real_structure_2026_05_09_probe13.py`](../scripts/cl3_koide_a1_probe_real_structure_2026_05_09_probe13.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_real_structure_2026_05_09_probe13.txt`](../logs/runner-cache/cl3_koide_a1_probe_real_structure_2026_05_09_probe13.txt)

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

## Phase 1 — Time-Lane Retained Content Survey

The framework retains the following antilinear / antiunitary content:

- **Reflection positivity** ([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)):
  the temporal-link reflection `Θ` is an **antilinear involution** on
  the gauge-field algebra: `Θ² = id`, `Θ(αU + βV) = ᾱΘ(U) + β̄Θ(V)`.
- **CPT_EXACT_NOTE** ([`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)): on
  even periodic `Z³` lattices, `T` (time reversal) acts as **complex
  conjugation `K`** (since the staggered Hamiltonian `H` is real).
  `C` (sublattice parity) and `P` (spatial inversion) are retained as
  real involutions; CPT = C·P·K is antiunitary, with `(CPT)² = id`
  ([`CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md`](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md)).
- **Physical Hermitian Hamiltonian bridge**
  ([`PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md)):
  on `H = iD`, the antiunitary representative is `Θ_H = P K`; this is
  retained as the framework's antiunitary time-reversal on the physical
  Hilbert space, satisfying `Θ_H H Θ_H^{-1} = H`.
- **Single-clock structure**
  ([`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)):
  the framework has a unique time direction (no second clock).

Key takeaways for Probe 13:

- `K` (entry-wise complex conjugation) IS retained as the `T` factor
  of CPT.
- `Θ_H = CK` is the retained antiunitary on physical Hilbert space.
- All retained antilinear/antiunitary operators are **discrete** (Z_2
  generators).
- **No retained CONTINUOUS U(1)** acts on the matter-sector `M_3(ℂ)`
  on `hw=1` except the `C_3`-cyclic shift (discrete order 3).

## Question

The eleven-probe campaign synthesis
([`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md))
named the precisely-localized missing primitive as the canonical
`(1,1)`-multiplicity-weighted Frobenius pairing on `M_3(ℂ)_Herm`
under `C_3`-isotype decomposition. Probe 12
[KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md]
sharpened this to:

> The retained-content principle that selects ℝ-isotype counting
> (gives `(1,1)` → κ = 2 = A1) over ℂ-character counting (gives
> `(1,2)` → κ = 1) is NOT supplied by Plancherel/Peter-Weyl alone.
> An additional **real-structure / antilinear-involution** principle
> is needed to combine `ω` with `ω̄` into a real doublet.

**Question:** Does any retained antilinear involution (or product of
retained involutions) supply this real-structure principle, and if
so does it close the A1-condition?

## Answer

**Mixed.** K-real-structure (retained as the `T` factor of CPT)
**DOES** supply the Z_2 part of ℝ-isotype combination (`χ_ω ↔ χ_ω̄`),
but **DOES NOT** supply the SO(2) angular quotient on the doublet
required for the `(1, 1)` weighting on the reduced two-slot carrier
`(ρ_+, ρ_⊥)` of MRU
([`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)).

**Verdict: SHARPENED bounded obstruction.** The A1 admission count is
UNCHANGED. The Probe 12 residue is refined further:

```
the canonical SO(2) phase quotient on the non-trivial doublet of
A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout.
```

This is a **smaller** named primitive than Probe 12's "ℝ-isotype
counting principle" because the Z_2 part of ℝ-isotype counting
(`χ_ω ↔ χ_ω̄`) IS supplied by retained K. What's missing is precisely
the **angular** U(1)_b — the continuous 1-dim Lie-algebra extension of
K, NOT the full real-structure principle.

## Setup

### Premises (A_min for probe 13)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | retained per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained per [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| BlockTotalFrob | `E_+ = 3a²`, `E_⊥ = 6\|b\|²` on `M_3(ℂ)_Herm` | retained per [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRU | Weight-class theorem: `κ = 2μ/ν`; `(1,1) → κ=2`; `(1,2) → κ=1`; reduced two-slot carrier `(ρ_+, ρ_⊥)` requires SO(2) quotient | retained per [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2` | retained per [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| RP | Antilinear involution `Θ` on gauge algebra (`Θ² = id`) | retained per [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| CPT | T = K (complex conjugation), CPT antiunitary, `(CPT)² = id` | retained per [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), [`CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md`](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md) |
| Theta_H | Antiunitary `Θ_H = CK` on physical `H = iD` | retained per [`PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md) |
| Probe12 | Plancherel-uniform on `Ĉ_3` gives `(1,2)` weighting; `(1,1)` requires combining `ω` and `ω̄` | retained per [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new admissions added by this probe (verdict: SHARPENED, no closure
  achieved without admission, and no admission proposed)

## Candidate antilinear involutions

The retained involutions to test are:

1. **K** = entry-wise complex conjugation (retained as T factor of CPT,
   per [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md): "T operator: complex
   conjugation K (since H is real)").
2. **T_alg** = transposition `X → X^T` extended antilinearly (the
   real-form transposition; on real-coefficient matrices same as K).
3. *** = Hermitian conjugation `X → X^†` (= K∘T_alg, antilinear,
   anti-multiplicative, `*² = id`).
4. **Θ_H = CK** = retained antiunitary on physical Hilbert space.
5. **CPT = C·P·K** = retained antiunitary, `(CPT)² = id`.

### Test 1 (existence)

All five candidates are well-defined antilinear involutions on
`M_3(ℂ)`. (Runner Section 2.1, 4.1-4.3.)

### Test 2 (compatibility with C_3)

K, T_alg commute with the C_3-action on M_3(C) by conjugation
(since C is real, `K(αg(X)) = αg(K(X))`). T_H and CPT contain
sublattice parity `C` and spatial inversion `P`, both unitary on
`M_3(ℂ)` matter sector; their composition with K still commutes
with the matter-sector `C_3[111]`-action. (Runner Section 2.4, 4.)

### Test 3 (ℝ-isotype forcing)

**K combines `ω` and `ω̄` characters into a real doublet.**

Concretely: under K, `χ_1` is K-fixed (as a character of `A^{C_3}`
applied to a real circulant gives a real number), and
`χ_ω ↔ χ_ω̄` are swapped by K (since
`χ_ω(K(H)) = χ_{ω̄}(H)` as can be verified directly).

The K-orbit structure on `Ĉ_3 = {χ_1, χ_ω, χ_ω̄}`:

```
{χ_1}  (singleton, K-fixed)
{χ_ω, χ_ω̄}  (doublet, K-swapped pair)
```

This **IS** the ℝ-isotype combination identified by Probe 12 as
needed. K-real-structure DOES provide it. (Runner Section 3.)

### Test 4 (uniqueness of (1, 1) weighting)

**FAIL.** K-orbit-based weight on `Ĉ_3` gives **(1, 2) ratio, not
(1, 1)**. Explicitly:

- **Real-Plancherel weight on K-orbits**: `w_orbit = (Σ_{χ ∈ orbit} (dim χ)²) / |G|`.
  For `{χ_1}`: `w = 1/3`.
  For `{χ_ω, χ_ω̄}`: `w = 2/3`.
  Ratio `1 : 2` — **same as complex Plancherel** (1, 2).

- **K-orbit-uniform weight** (each orbit gets equal weight):
  `w({χ_1}) = w({χ_ω, χ_ω̄}) = 1/2`.
  Inside doublet: split equally `w(χ_ω) = w(χ_ω̄) = 1/4`.
  This is a different state, but it is **NOT** the (1, 1) weighting
  on `(E_+, E_⊥)` blocks of `M_3(ℂ)_Herm`.

  Specifically, applied to `H^*H` for circulant `H = aI + bC + b̄C²`,
  K-orbit-uniform gives `(e_1²)/2 + (e_ω² + e_ω̄²)/4` where
  `e_χ = χ(H)` are the eigenvalues of `H`. This is NOT `(E_+ + E_⊥)/2`.
  The extremization over `(a, b)` at fixed `E_+ + E_⊥` gives
  `|b|² = a²/4` (κ = 4, NOT A1), as verified by runner T5.6 Lagrange
  computation:

  ```
  Maximize w(H^*H) = (a + 2b)²/2 + (a − b)²/2  (b real, K-fixed)
  subject to 3a² + 6b² = const.
  Lagrangian gives: (a + 2b)(a − b) = 0, i.e., a = −2b or a = b.
  At a = b: trivial. At a = −2b: |b|² = a²/4, κ = 4, NOT A1 (κ = 2).
  ```

(Runner Sections 5, 7.)

### Test 5 (closure of A1)

**FAIL.** The reduced two-slot carrier `(ρ_+, ρ_⊥)` of MRU requires
the SO(2)-INVARIANT radius:

```
ρ_⊥ = √((Re b)² + (Im b)²) / √6 = |b| / √6
```

K alone supplies only the **Z_2 reflection** `(Re b, Im b) → (Re b, −Im b)`,
since `K(b) = b̄`. The Z_2 quotient gives a **half-plane** `(Im b ≥ 0)`,
NOT the SO(2)-quotient = single radius `|b|`.

Concretely: `K(B_0) = B_0`, `K(B_1) = B_1` (real), `K(B_2) = −B_2` (pure
imaginary), where `B_0 = I`, `B_1 = C + C²`, `B_2 = i(C − C²)`. So K acts
on the `(B_0, B_1, B_2)`-coordinate system as `(+, +, −)` — a
reflection in `B_2`-direction, not a rotation.

The (1, 1) weighting on `(ρ_+, ρ_⊥)` requires the **SO(2)**-symmetry
`(B_1, B_2) → (cos θ B_1 − sin θ B_2, sin θ B_1 + cos θ B_2)`, which is
**continuous**. **No retained antilinear involution is continuous.**

(Runner Sections 6, 8.)

## Theorem (Probe 13 sharpened bounded obstruction)

**Theorem.** On A1 + A2 + retained C_3-action on `hw=1` + retained
M_3(ℂ) on `hw=1` + retained Frobenius block-total + retained K (CPT)
+ retained `Θ_H = CK` + retained CPT + retained MRU
weight-class structure:

```
(a) K (entry-wise complex conjugation) is retained as the T factor of
    CPT. K is well-defined, antilinear, K² = id, commutes with the
    C_3-action.
    [Closes from retained content; runner Sections 2, 4.]

(b) K combines χ_ω and χ_ω̄ characters into a real doublet via the
    K-orbit structure on Ĉ_3:
        {χ_1} (singleton)  ⊕  {χ_ω, χ_ω̄} (K-swapped pair).
    This IS the Z_2 part of ℝ-isotype counting.
    [Closes from retained content; runner Section 3.]

(c) K-orbit-uniform state on A^{C_3} = circulants gives the K-orbit
    weighting (w_+, w_doublet) = (1/2, 1/2). Applied to H^*H, the
    Lagrangian extremum is at |b|² = a²/4 (κ = 4), NOT A1 (κ = 2).
    Real-Plancherel weight on K-orbits = (1/3, 2/3), same (1, 2) ratio
    as complex Plancherel.
    [Failure mode; runner Sections 5, 7.]

(d) The (1, 1) weighting on the reduced two-slot carrier (ρ_+, ρ_⊥)
    requires the SO(2)-INVARIANT radius ρ_⊥ = |b|. K alone supplies
    only the Z_2 reflection (Re b, Im b) → (Re b, −Im b). The Z_2
    quotient of the (b complex)-plane gives a half-plane, NOT the
    SO(2)-quotient = single radius.
    [Failure mode; runner Sections 6, 8.]

Therefore: no retained antilinear involution closes the A1-condition.
The real-structure mechanism supplies the Z_2 part of ℝ-isotype
counting (combining χ_ω and χ_ω̄) but does NOT supply the SO(2) angular
quotient on the doublet. The A1-condition closure attempt via
real-structure / antilinear-involution returns SHARPENED bounded
obstruction. The remaining residue is named precisely:

  "the canonical SO(2) phase quotient on the non-trivial doublet of
   A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout."

The A1 admission count is unchanged. No new admission is proposed by
this probe.
```

**Proof.** (a) and (b) are explicit constructions verified
algebraically by the runner (PASS in Sections 2-4). (c) computes the
K-orbit-uniform Lagrangian extremum and shows it gives κ = 4, not A1
(PASS in Sections 5, 7). (d) verifies that K acts on the
`(B_1, B_2)`-plane as a reflection (det = −1), not as a rotation
(SO(2)), so the K-quotient is Z_2 (half-plane), not SO(2) (radius);
no composition of retained discrete antilinear involutions generates
SO(2) (PASS in Sections 6, 8). ∎

## Convention-robustness check

Probe 12 verified: any framework that gives independent normalizations
to trivial vs non-trivial isotypes will fail, *unless* the (rho_+, rho_⊥)
two-slot carrier is canonical. Probe 13 confirms:

- **Scale-invariance** of `|b|²/a²` is preserved under `H → cH`. ✓
- **Basis change** `C → C^{-1} = C²` preserves C_3-action and isotype
  structure. ✓
- **K-action consistency** with C_3: `K(α_g(X)) = α_g(K(X))` ✓ (since
  C is real).

The bimodule frame is canonically pinned by retained content (per
Probe 12 sub-derivations a, b). What is **not pinned** is the
**angular U(1)_b** quotient on the doublet — the surviving
convention-trap.

## Attack-vector enumeration

Per the eleven-probe campaign + Probe 12 synthesis, this is the
thirteenth attack vector:

| # | Attack vector | Outcome |
|---|---|---|
| 13 | Real-structure / antilinear-involution mechanism (K, T_alg, *, T_H, CPT) | sharpened obstruction; supplies Z_2 part of ℝ-isotype counting (χ_ω ↔ χ_ω̄) but NOT SO(2) angular quotient |

This refines the residue from Probe 12. Specifically:

- **Probe 12 §3** said "real-structure mechanism is needed to combine ω
  with ω̄". Probe 13 verifies: K **DOES** combine them — but only as Z_2,
  not SO(2).
- **Probe 12 closure-step c** identified `(1, 2) → κ = 1` as the
  obstruction. Probe 13 confirms: even after K-real-structure-quotient,
  real-Plancherel on K-orbits still gives `(1/3, 2/3) = (1, 2)` ratio.
- **MRU note §4** identified the SO(2)-angular-quotient inside the
  doublet as the "missing object". Probe 13 verifies: this SO(2) is
  NOT supplied by any retained antilinear involution.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction; no closure)
- `effective_status`: `retained_bounded` (after audit review)
- `admitted_context_inputs`: `["A1-condition: |b|²/a² = 1/2"]` —
  the residual admission, with the Probe 13 sharpening:
  "the canonical SO(2) phase quotient on the non-trivial doublet of
   A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout"

**No new admissions added by this probe.**

### What this probe DOES

1. Verifies that K (entry-wise complex conjugation) IS retained as
   the T factor of CPT_EXACT_NOTE.
2. Verifies that K combines `χ_ω` and `χ_ω̄` characters into a real
   doublet (Z_2 part of ℝ-isotype counting).
3. Verifies that no retained antilinear involution (K, T_alg, *, Θ_H,
   CPT, or any product) supplies the SO(2) angular quotient on the
   doublet.
4. Sharpens the residue from Probe 12's "ℝ-isotype counting principle"
   to the smaller "SO(2)/U(1)_b angular quotient on the doublet" — the
   Z_2 part is now supplied by retained K.

### What this probe DOES NOT do

1. Does NOT close the A1-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem (BZ, 3GenObs, Circulant,
   BlockTotalFrob, MRU, KoideAlg, RP, CPT, Θ_H, Probe1, Probe7,
   Probe12, Campaign).
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   eleven-probe campaign synthesis or Probe 12 (admit/derive/pivot).

## Honest assessment

Probe 13 was given the freedom to **propose new primitives** if needed.
It does not exercise that freedom because:

- The **Z_2 part** of the missing ℝ-isotype counting principle IS already
  retained (as `K = T` in CPT_EXACT_NOTE).
- The **remaining residue** (SO(2)/U(1)_b angular quotient) is a
  **continuous** symmetry, which is qualitatively different from any
  retained antilinear involution (all of which are discrete Z_2 generators).
  A new "SO(2) primitive" would not be a small extension of K — it would
  be a fresh continuous symmetry on the doublet.

Three possible options for closing the U(1)_b residue (none endorsed
by this probe):

1. **Admit U(1)_b as a NEW small continuous primitive.** A 1-dim
   Lie-algebra extension of K, scoped to the non-trivial doublet
   inside `A^{C_3}`. This would be a fresh continuous symmetry, not
   derivable from the discrete retained involutions.

2. **Derive U(1)_b from a retained continuous symmetry.** The framework
   has retained continuous symmetries (lattice translations, gauge
   U(1)_em, U(1)_Y), but none acts on the matter-sector M_3(C) on
   hw=1 with the right angular structure on (B_1, B_2).

3. **Pivot to the SO(2)-quotient at the readout level (functional, not
   algebraic).** The Brannen Q-functional IS U(1)_b-invariant
   (Q depends only on `|b|²/a²`, not arg(b)). So the SO(2)-quotient
   could be enforced AT THE Q-READOUT STEP, not at the algebra level.
   This would be a different framing: not "M_3(C) has a canonical
   SO(2) symmetry", but "the Koide functional Q(H) factors through the
   SO(2)-quotient of H".

What this probe contributes to the campaign:

1. **Confirmation** that the K-real-structure (retained as T in CPT)
   does supply the Z_2 part of the missing principle. So the residue
   is genuinely smaller than Probe 12's "ℝ-isotype counting principle".
2. **Sharpened residue characterization**: the open piece is the
   continuous U(1)_b angular quotient, NOT the discrete real-structure.
   This is a Lie-algebra-1 extension residue, not a finite-group residue.
3. **Confirmation of campaign terminal state**: thirteen independent
   attacks now return the same structural obstruction, strengthening
   the conclusion that the missing primitive cannot be derived from
   generic algebraic/discrete-symmetry content alone.

The campaign's residue is now: **a continuous U(1)_b angular quotient
on the non-trivial doublet of A^{C_3}**. This is more precisely
localized than Probe 12's phrasing (which left the entire ℝ-isotype
principle open), and could plausibly be the target of a future Probe 14
if such a U(1)_b is identifiable from a retained continuous symmetry
or admittable as a small new primitive.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained antilinear / antiunitary content (time-lane survey)

- RP: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- CPT exact: [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
- (CPT)² = id: [`CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md`](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md)
- Physical Hermitian Hamiltonian + Θ_H = CK: [`PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md)
- Single-clock structure: [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
- Anomaly forces time: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)

### Retained provenance of the C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class + reduced two-slot carrier `(ρ_+, ρ_⊥)`: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Eleven-probe campaign + Probe 12

- Synthesis (campaign terminal state): [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 1 (RP/GNS): [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
- Route D (Newton-Girard): [`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md)
- Probe 12 (Plancherel/Peter-Weyl, immediate predecessor): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md) (PR pending merge)

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_real_structure_2026_05_09_probe13.py
```

Expected: `=== TOTAL: PASS=57, FAIL=0 ===`

The runner verifies:

1. Retained inputs (Section 1): C is unitary, order 3, eigenvalues
   `{1, ω, ω̄}`; H = aI + bC + b̄C² is Hermitian and circulant.
2. K (Section 2): entry-wise complex conjugation is well-defined,
   antilinear, K² = id, commutes with C_3-action, preserves
   Hermiticity, maps circulants to circulants, acts on (a, b) as
   (a, b̄).
3. K's action on isotypes (Section 3): K combines χ_ω and χ_ω̄
   characters into K-doublet; χ_1 is K-fixed; K-orbit structure on
   `Ĉ_3` is `{χ_1} ⊕ {χ_ω, χ_ω̄}`.
4. Other antilinear involutions (Section 4): T_alg, *, Θ_H, CPT all
   reduce to K (or identity) on Hermitian circulants. Group generated
   on this set: just Z_2.
5. K-orbit weighting (Section 5): Plancherel-uniform = (1/3, 1/3, 1/3);
   K-orbit-uniform = (1/2, 1/4, 1/4); real-Plancherel on K-orbits =
   (1/3, 2/3). Lagrangian extremum of K-orbit-uniform on H^*H gives
   |b|² = a²/4, NOT A1.
6. Reduced (+, ⊥) carrier of MRU (Section 6): B_0 = I, B_1 = C+C²,
   B_2 = i(C−C²); ||B_0||² = 3, ||B_1||² = ||B_2||² = 6; K acts as
   (B_0, B_1, B_2) → (B_0, B_1, −B_2) (Z_2 reflection).
7. K-symmetric state freedom (Section 7): K alone does not pin a
   unique state; multiple K-symmetric states give different scalars.
8. SO(2)/U(1)_b is the missing piece (Section 8): SO(2) preserves
   |b|², K only Z_2; no retained discrete involution generates SO(2).
9. Verdict (Section 9): SHARPENED bounded obstruction; A1 admission
   count UNCHANGED.
10. Convention robustness (Section 10): scale-invariance, basis change.
