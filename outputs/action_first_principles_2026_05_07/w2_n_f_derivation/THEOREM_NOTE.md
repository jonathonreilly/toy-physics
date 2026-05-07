# N_F Derivation Status — Bounded Theorem with Definitive Z_2 Reduction

**Date:** 2026-05-07
**Type:** bounded_theorem candidate + structural barrier consolidation
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.
**Companion runner:** [`cl3_n_f_derivation_2026_05_07_w2_check.py`](cl3_n_f_derivation_2026_05_07_w2_check.py)
**Companion attack note:** [`ATTACK_RESULTS.md`](ATTACK_RESULTS.md)

## Executive summary

This note answers the W2 task: *"derive `N_F = 1/2` from Cl(3)
algebraic structure alone, eliminating the single remaining admitted
scalar in the bridge gap."*

**Verdict: bounded result, type (c) per task spec.** The seven-attack
analysis (full report in [`ATTACK_RESULTS.md`](ATTACK_RESULTS.md))
establishes:

> **(N_F-Bounded Theorem).** Cl(3) algebraic primitives plus the
> framework's fixed Hilbert-space embedding `V = C^8` and per-site
> Hilbert dim 2 reduce the L3 admission from a continuous family
> `N_F ∈ ℝ_+` to a discrete two-element set
>
> ```
> N_F ∈ { 1/2, 1 }                                          (T1)
> ```
>
> with the two values corresponding to the two natural Hilbert-
> Schmidt traces:
>
> - `N_F = 1/2` (canonical Gell-Mann): `Tr_{V_3}(T_a T_b) = (1/2) δ_{ab}`,
>   where V_3 ⊂ V is the 3D irreducible color triplet block;
> - `N_F = 1` (full Hilbert-Schmidt): `Tr_V(T_a^V T_b^V) = 1 · δ_{ab}`,
>   where T_a^V is the 8D embedding of the same generators.
>
> The ratio is exactly `Tr_V / Tr_{V_3} = 2 = dim(I_2)`, the fiber
> multiplicity of the taste-cube tensor decomposition `V = (3D ⊕ 1D)
> ⊗ C^2`. This factor of 2 is **structurally fixed** by the
> Cl(3)⊗Z³ substrate.
>
> The Z_2 → 1 reduction (selecting between `N_F = 1/2` and
> `N_F = 1`) is **not closed** by Cl(3) primitives alone; it
> requires the additional structural admission "use the irreducible
> carrier's trace as canonical."

The result is **type (c) bounded**: not a positive theorem
(`N_F = 1/2` not uniquely forced), not a definitive obstruction
(structural progress is genuine), but a sharpening of the L3
admission from continuous to discrete.

## What this means for the bridge gap

The four-layer stratification
([`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md))
becomes a **five-layer** stratification:

| Layer | Statement | Status | Authority |
|---|---|---|---|
| L1 | Cl(3) algebra structure on `V = C^8` | DERIVED (axiom A1) | minimal-axioms note |
| L2 | Hilbert–Schmidt form `B_HS` is unique up to scalar | DERIVED (Killing rigidity) | HS rigidity theorem (R1) |
| **L3a** | `N_F ∈ {1/2, 1}` (discrete Z_2 admission) | **DERIVED (this note, T1)** | Cl(3) primitives + fixed V embedding |
| **L3b** | Trace-space choice (V_3 vs V) selects `N_F = 1/2` vs `1` | **ADMITTED** (binary; was: continuous) | binary admission, not derivable from Cl(3) primitives alone |
| L4 | `g_bare = 1` (i.e. β = 6 at N_c = 3, given trace choice) | DERIVED (constraint) | Wilson matching algebra |

**Honest convention status:** **one binary admission** at L3b (which
trace space is canonical) — instead of the prior "any positive
scalar" continuous admission at L3.

The bridge gap shrinks from "one continuous admitted scalar" to
"one binary admitted choice." This is a substantive narrowing.

## What this means for "single-convention-free bridge"

Per the W2 task spec:

> *If derivable, the bridge becomes single-convention-free.*

`N_F = 1/2` is **not derivable** from Cl(3) primitives alone. So the
bridge does not become single-convention-free under this analysis.

However, the bridge becomes **discretely-admitted** rather than
**continuously-admitted**. The remaining admission is binary: pick
one of two structurally-permitted normalizations. This is a tier
strictly below "single-convention-free" but strictly above the
prior "one continuous scalar admitted."

The framework is therefore in a stable state where:
- Six structural barriers (Attacks 1-6) preclude the derivation of
  `N_F = 1/2` from group/algebra/topology arguments alone
- One sharp bivector argument (Attack 7) closes `N_F = 1/2` for
  SU(2) but does NOT extend to SU(3)
- The combined positive result (Attack 1 + Attack 7 substrate
  structure) gives the discrete Z_2 admission (T1)

## Claim scope

> **Theorem (N_F continuum-to-Z_2 reduction).** Let `V = C^8` be
> the framework's full Hilbert space (per
> [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
> and the taste-cube structure of `Z³`). Let
> `g_conc = su(3) ⊂ End(V)` be the derived gauge subalgebra in the
> canonical triplet block per
> [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](../../../docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
> Claim 1, with `V_3 ⊂ V` the 3D irreducible carrier of the
> fundamental rep per
> [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md).
>
> Then:
>
> **(T1)** Under the framework's fixed Hilbert-space inner product on
> V, the natural Hilbert–Schmidt trace forms on `g_conc` partition
> into exactly **two** structurally-distinguished representatives:
>
> - `B^{(3)}(X, Y) = Tr_{V_3}(X · Y)` — restricted trace on V_3,
>   giving `N_F^{(3)} = 1/2`;
> - `B^{(V)}(X, Y) = Tr_V(X · Y)` — full trace on V,
>   giving `N_F^{(V)} = 1`.
>
> The ratio `B^{(V)} / B^{(3)} = 2 = dim(I_2)` is structurally
> fixed by the Cl(3)⊗Z³ substrate's tensor-product decomposition
> `V = (V_3 ⊕ V_singlet) ⊗ I_2`, where `dim(I_2) = 2` is the fiber
> multiplicity.
>
> **(T2)** The continuous family of Ad-invariant inner products on
> `g_conc` (1-parameter family by Killing rigidity) is reduced to
> the discrete 2-element set `{B^{(3)}, B^{(V)}}` upon admission of
> the Cl(3) substrate primitives.
>
> **(T3)** Under canonical Gell-Mann assignment `N_F = 1/2`
> (= `B^{(3)}`-orthonormal basis), the framework's `g_bare = 1`
> chain follows as derived per the four-layer stratification's L4.
>
> **(T4)** Under alternative assignment `N_F = 1` (= `B^{(V)}`-
> orthonormal basis), the framework's β-matching gives
> `β = 2 N_c / g_bare² = 6/g_bare²`; the canonical (no-pre-factor)
> connection has `g_bare = √2`. (Equivalently, the algebraic
> identities under different basis normalizations.)
>
> **(T5)** The Cl(3)-primitive structure is **structurally silent**
> on the choice between `B^{(3)}` and `B^{(V)}`. Both are
> well-defined, both are Ad-invariant, both are Killing-class
> representatives. The choice is binary admitted.
>
> The theorem **does not** claim:
>
> - that `N_F = 1/2` is uniquely forced by `A1` (Cl(3)) and `A2`
>   (Z³) alone — the binary choice between V_3 and V remains;
> - that the Wilson plaquette action form is uniquely forced
>   (separate retention via A2.5);
> - closure of the deeper "absolute derivation of `g_bare = 1` from
>   A1+A2" Nature-grade target.

## Why the Z_2 reduction is structural (not coincidental)

The two natural representatives `B^{(3)}` and `B^{(V)}` arise from
**genuinely different** algebraic operations within Cl(3) primitives:

- `B^{(3)}` corresponds to "trace on the irreducible carrier of the
  fundamental rep." This is the standard mathematical trace used in
  representation theory (Slansky, Howe-Tan).
- `B^{(V)}` corresponds to "trace on the full Hilbert space of the
  framework." This is the standard physical trace used in lattice
  gauge theory and the framework's own Hamiltonian/Wilson-action
  formulation.

The ratio `2 = dim(I_2)` is *not* a degree of freedom — it is fixed
by the Cl(3)⊗Z³ substrate's natural tensor-product decomposition:

```
V = C^8 = (3D symmetric base ⊕ 1D antisymmetric base) ⊗ C²
        =       V_3            ⊕     V_singlet         ⊗ V_fiber
```

The 3D + 1D = 4D decomposes the Hamming-symmetric structure of the
taste cube, and the C² fiber is the b₃ axis (per
[`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md)
Step B). The factor `dim(I_2) = 2` is the fiber multiplicity, which
is *exactly* the ratio between the full-V trace and the V_3 trace.

So the Z_2 reduction is a **structural theorem about the natural
traces of the framework**, not a coincidental matching.

### Verification

The runner [`cl3_n_f_derivation_2026_05_07_w2_check.py`](cl3_n_f_derivation_2026_05_07_w2_check.py)
verifies all elements of (T1)-(T5) numerically:

- `N_F^{(3)} = 1/2` exactly (Section 0)
- `N_F^{(V)} = 1` exactly (Section 0)
- Ratio `N_F^{(V)} / N_F^{(3)} = 2` exactly (Section 0)
- Killing-form Ad-invariance under random SU(3) action (Section 1)
- Spin(6)/SU(4) embedding gives `N_F = 1/2` (Section 2;
  inherited convention)
- d-symbol values at canonical: `d_{118} = 1/√3` (Section 3)
- SU(2) bivector-to-vector forces `1/2` factor (Section 7)
- SU(3) generators are NOT Cl(3) bivectors (Section 7)
- 22/0 EXACT pass.

## Why the Z_2 → 1 reduction is *not* closed

The seven attack vectors (full analysis in
[`ATTACK_RESULTS.md`](ATTACK_RESULTS.md)) systematically probe
whether the framework's structure forces `B^{(3)}` over `B^{(V)}`.
All seven fail:

| Attack | Why it fails |
|---|---|
| 1 (Killing rigidity) | "Up to scalar" by classical theorem; silent on overall scale |
| 2 (Spin(6) inheritance) | Routes admission upstream to SU(4); same convention layer |
| 3 (anomaly cancellation) | Homogeneous in gauge-field power; invariant under `N_F` rescaling |
| 4 (representation integrality) | Invariant under integer rescaling; multiple integrality conventions |
| 5 (operational reconstruction) | Dimension-counting, scale-blind |
| 6 (literature consensus) | Uniformly admits `N_F = 1/2` as convention |
| 7 (Cl(3) bivector trace) | Works for SU(2); fails to extend to SU(3) (different rep mechanism) |

Three of these (Attacks 1, 5, 6) are **definitive** — they preclude
the derivation by classical theorems. The other four are **specific**
— they identify why a particular route fails but leave the meta-
question open.

The deepest finding is from **Attack 7**: SU(2)'s `N_F = 1/2`
*is* forced by Cl(3) bivector structure (Spin(3) → SO(3) double
cover), but SU(3)'s `N_F = 1/2` is NOT derivable the same way
because SU(3) generators are not Cl(3) bivectors. This is a
structural barrier specific to the SU(3) case.

## Where the structural barrier ultimately lies

The L3 admission's residual binary choice corresponds to a deep
question about which trace is "natural" in the framework:

```
Is the framework's natural Hilbert-Schmidt trace
   (a) the trace on the irreducible su(3) carrier V_3, or
   (b) the trace on the full taste cube V = C^8?
```

Cl(3) primitives provide **both** options:

- **(a) is natural mathematically.** In rep theory, the canonical
  trace is on the irreducible carrier. The fundamental rep of SU(3)
  is on V_3 = C^3 (the color triplet); restricting to V_3 gives the
  Killing-canonical trace structure.

- **(b) is natural physically.** In the framework's Hamiltonian
  formulation, the Hilbert space is V = C^8. The lattice action,
  Wilson loops, holonomies, and physical observables all live on V.
  The natural inner product structure is `Tr_V`, not `Tr_{V_3}`.

These two reflect a tension between **mathematical rep-theory
convention** and **physical Hilbert-space convention**. The
framework's load-bearing notes mostly use convention (a)
(canonical Gell-Mann `N_F = 1/2`), which agrees with the standard
particle-physics literature, but convention (b) is also valid and
would simply re-parametrize all the framework's gauge-coupling
predictions.

### Could a categorical / universal-property argument close this?

The single open route identified by this analysis is:

> **Categorical universality:** if one can show via universal-property
> argument that the trace on the *irreducible carrier* is uniquely
> "natural" (in the sense of category theory: a unique natural
> transformation between trace functors), then `N_F = 1/2` would be
> structurally forced.

Concretely: there is a natural *trace functor* on the category of
finite-dimensional `g`-modules, given by `Tr_V : End(V) → C`. The
question is whether the trace on the *irreducible* carrier is
"more canonical" (in some category-theoretic sense) than the trace
on a reducible carrier.

This is not closed here. It would be a Nature-grade research target
in its own right. The likely answer (based on standard rep theory):
the trace on each isotypic component is canonical, but the overall
combination is admitted. This is not a clean closure path.

## Cited authorities (one hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) | unaudited candidate (positive_theorem proposed) | Killing rigidity (R1) — uniqueness "up to scalar" |
| [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md) | unaudited candidate (positive_theorem proposed) | Four-layer stratification (parent of the L3 sharpening this note delivers) |
| [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](../../../docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) | proposed_retained (Claims 1, 2) | Cl(3) → End(V) embedding canonicity (Claim 1) |
| [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md) | bounded_theorem | SU(3) on V_3 (3D symmetric base subspace) embedding |
| [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) | positive_theorem (proposed) | Per-site Hilbert dim = 2 (Pauli rep on C²) |
| [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md) | retained_bounded | Casimir = 4/3 at canonical Gell-Mann |
| [`MINIMAL_AXIOMS_2026-05-03.md`](../../../docs/MINIMAL_AXIOMS_2026-05-03.md) | meta | Framework axiom set A1 + A2 |

### Two-hop dependencies (referenced for context)

- [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](../../../docs/G_BARE_RIGIDITY_THEOREM_NOTE.md)
  — sister Hamiltonian-level rigidity (V-trace explicit)
- [`A2_5_DERIVATION_ATTACK_RESULTS.md`](../A2_5_DERIVATION_ATTACK_RESULTS.md)
  — establishes foreclosed routes (Hochschild, polynomial-closure,
  Lieb-Robinson) that this analysis avoided

## Standard rep-theory references

(For attack 6 — the literature consensus argument)

- Slansky, R. (1981). "Group Theory for Unified Model Building."
  Physics Reports 79(1), 1-128.
- Greiner, W. & Müller, B. (1994). "Quantum Mechanics: Symmetries."
  Springer-Verlag, Berlin.
- Cvitanović, P. (2008). "Group Theory: Birdtracks, Lie's, and
  Exceptional Groups." Princeton University Press.
- Peskin, M. & Schroeder, D. (1995). "Introduction to Quantum
  Field Theory." Addison-Wesley, Section A.4.
- Howe, R. & Tan, E.-C. (1992). "Non-Abelian Harmonic Analysis."
  Springer Universitext.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Cl(3) primitives plus the framework's fixed Hilbert-space embedding
  V = C^8 reduce the L3 admission of the four-layer stratification
  from a continuous family N_F ∈ ℝ_+ to a discrete 2-element set
  N_F ∈ {1/2, 1}. The ratio 2 = dim(I_2) is structurally fixed by
  the Cl(3)⊗Z³ substrate's tensor-product decomposition (V_3 ⊕
  V_singlet) ⊗ I_2. The Z_2 → 1 reduction (selecting between
  N_F = 1/2 and N_F = 1) is NOT closed by Cl(3) primitives alone;
  it requires the additional binary admission "use the irreducible
  carrier's trace as canonical" (selects 1/2) vs "use the full
  Hilbert-space trace as canonical" (selects 1).
proposed_load_bearing_step_class: A
declared_one_hop_deps:
  - g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07
  - g_bare_constraint_vs_convention_restatement_note_2026-05-07
  - g_bare_structural_normalization_theorem_note_2026-04-18
  - cl3_color_automorphism_theorem
  - cl3_per_site_hilbert_dim_two_theorem_note_2026-05-02
audit_required_before_effective_retained: true
parent_update_allowed_only_after_retained: true
distinguishing_content_from_2026-05-07_four_layer:
  the four-layer stratification's L3 is "any positive scalar N_F
  ∈ ℝ_+". The present note sharpens this to "discrete N_F ∈ {1/2, 1}",
  with the binary choice corresponding to V_3 vs V trace. This is a
  substantive sharpening of the L3 admission tier (continuous to
  discrete) supported by structural identification of the two
  natural HS representatives.
admitted_context_inputs:
  - L3b binary admission: "trace space = V_3 (selects N_F = 1/2)"
    vs "trace space = V (selects N_F = 1)". This is the single
    remaining admission in the g_bare chain, replacing the prior
    continuous-scalar admission.
```

## What this candidate can support after retention

- **Sharpening of the four-layer stratification.** The L3 admission
  is reduced from continuous to binary. After retention, the
  parent restatement note should be cross-linked to cite this Z_2
  reduction explicitly.

- **Strengthening of bridge-gap closure.** The framework's
  `g_bare = 1` chain has an even tighter named admission (binary
  choice), making the bridge audit-defensibility one tier sharper.

- **Foreclosure of the Nature-grade target.** The seven attack
  vectors define what's foreclosed. Future attempts to derive
  `N_F = 1/2` should NOT retry these seven routes; they should
  pursue only the open route (categorical universality) or admit
  the Z_2 binary as definitive.

## What this theorem does NOT close

- **The Z_2 → 1 reduction.** The choice between `N_F = 1/2` (V_3
  trace) and `N_F = 1` (V trace) is not closed. Both are
  structurally admissible.

- **The deeper "absolute derivation of `g_bare = 1` from A1+A2"
  Nature-grade target.** This remains the deepest open foundational
  question. The Z_2 reduction is a sharpening, not a closure.

- **The action-form question.** The Wilson plaquette action form
  is a separate retention target (A2.5); not addressed here.

- **The Hamiltonian-Lagrangian dictionary.** Convention C-iso
  remains an O(g²) bounded admission; not addressed here.

## Cross-references

- [`G_BARE_AUDIT_RESIDUAL_CLOSURE.md`](../G_BARE_AUDIT_RESIDUAL_CLOSURE.md)
  — master synthesis of the audit-residual closure
- [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](../UNIFIED_BRIDGE_STATUS_2026_05_07.md)
  — bridge status note that lists W2 (this) as the single Nature-grade
  remaining open target
- [`A2_5_DERIVATION_ATTACK_RESULTS.md`](../A2_5_DERIVATION_ATTACK_RESULTS.md)
  — sister attack-results note for the action-form question
- [`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md)
  — sister derived-theorem note showing the action-form is closed
  at the continuum level

## Honest scoping summary

`N_F = 1/2` is **not derivable** from Cl(3) algebraic primitives
alone. The seven-attack analysis enumerates the structural barriers:
six of them are definitive (Killing rigidity, Spin(6) inheritance,
anomaly homogeneity, integrality invariance, operational
reconstruction, literature consensus); one is partial (Cl(3)
bivector argument works for SU(2), fails for SU(3)).

The single positive partial result is the **continuum-to-Z_2
reduction**: Cl(3) primitives plus the framework's fixed
Hilbert-space embedding reduce `N_F` from a continuous family to a
discrete two-element set `{1/2, 1}`. The ratio 2 is structurally
fixed (fiber multiplicity); the binary choice between the two
values is genuinely admitted, not derived.

This is a substantive sharpening of the L3 admission from
"continuous scalar" to "binary choice", which is audit-grade
progress. But it does not produce a single-convention-free bridge,
because the binary admission persists.

The result is **bounded type (c)** per the W2 task spec: not a
positive theorem (`N_F = 1/2` not uniquely forced), not a
definitive obstruction (genuine structural progress documented),
but a sharpening of the L3 admission tier from continuous to
discrete. The bridge gap shrinks from "one admitted scalar" to
"one admitted binary choice."
