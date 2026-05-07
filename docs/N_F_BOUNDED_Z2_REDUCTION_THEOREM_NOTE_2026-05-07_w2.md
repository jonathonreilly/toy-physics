# N_F Bounded Z_2 Reduction Theorem — Continuous Admission Becomes Discrete

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide whether the candidate is retained.
**Primary runner:** [`outputs/action_first_principles_2026_05_07/w2_n_f_derivation/cl3_n_f_derivation_2026_05_07_w2_check.py`](../outputs/action_first_principles_2026_05_07/w2_n_f_derivation/cl3_n_f_derivation_2026_05_07_w2_check.py)
**Source-note proposal:** audit verdict and downstream status set only
by the independent audit lane.

## 0. Audit context

The four-layer stratification
([`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md))
identifies a single admission at L3: the overall scalar `N_F` of the
Hilbert–Schmidt form. That note documents `N_F` as "any positive
scalar"; the framework adopts `N_F = 1/2` (canonical Gell-Mann).

The W2 follow-up question (per
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](../outputs/action_first_principles_2026_05_07/UNIFIED_BRIDGE_STATUS_2026_05_07.md)
"Genuine remaining work" Section W2) is whether `N_F = 1/2` itself
is uniquely forced by Cl(3) algebraic structure alone. The present
note answers this **partially**:

> Cl(3) primitives plus the framework's fixed Hilbert-space embedding
> reduce `N_F` from a continuous family to a discrete two-element
> set `{1/2, 1}`. The Z_2 → 1 reduction (selecting which of the two)
> is not closed; it requires an additional binary admission.

The result is a **bounded sharpening** of the L3 admission, replacing
"continuous family" with "binary choice." This is structurally
substantive but does not close the deeper question.

## 1. Claim scope

> **Theorem (N_F continuum-to-Z_2 reduction).**
>
> Let `V = C^8` be the framework's full Hilbert space (per
> [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
> and the taste-cube Z³-substrate structure). Let
> `g_conc = su(3) ⊂ End(V)` be the derived gauge subalgebra in the
> canonical triplet block per
> [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
> Claim 1, with `V_3 ⊂ V` the 3D irreducible carrier per
> [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md).
>
> Then under the framework's fixed Hilbert-space inner product on V:
>
> **(Z1) Continuum-to-Z_2 reduction.** The continuous family of
> Ad-invariant inner products on `g_conc` (1-parameter family by
> Killing rigidity) reduces to exactly **two** structurally-
> distinguished representatives:
>
> | Representative | Definition | `N_F` value |
> |---|---|---|
> | `B^{(3)}` | `Tr_{V_3}(X · Y)` (trace on V_3) | `1/2` |
> | `B^{(V)}` | `Tr_V(X · Y)` (trace on V = C^8) | `1` |
>
> with the ratio
>
> ```
> B^{(V)} / B^{(3)} = 2 = dim(I_2)                                  (R)
> ```
>
> structurally fixed by the Cl(3)⊗Z³ substrate's tensor-product
> decomposition `V = (V_3 ⊕ V_singlet) ⊗ V_fiber`, where
> `V_fiber = C²` and `dim(V_fiber) = 2` is the fiber multiplicity.
>
> **(Z2) Joint Ad-invariance.** Both `B^{(3)}` and `B^{(V)}` are
> Ad-invariant on `g_conc`. They differ by the structural factor `2`,
> which is *not* a free convention but a fiber-multiplicity factor.
>
> **(Z3) Z_2 → 1 binary admission.** The choice between
> `B^{(3)}` (yielding `N_F = 1/2`) and `B^{(V)}` (yielding
> `N_F = 1`) is binary admitted: it requires the additional
> structural input "trace on the irreducible carrier" vs "trace on
> the full Hilbert space." Cl(3) primitives provide both options;
> they do not select between them.
>
> **(Z4) Sharpened L3 admission.** The four-layer stratification's
> L3 admission is sharpened from "continuous family `N_F ∈ ℝ_+`"
> to "discrete binary choice `N_F ∈ {1/2, 1}`."
>
> The theorem **does not** claim:
>
> - that the binary choice between `B^{(3)}` and `B^{(V)}` is
>   derivable from Cl(3) primitives — it is genuinely admitted;
> - that `N_F = 1/2` is uniquely forced by `A1` (Cl(3)) and `A2`
>   (Z³) alone — the binary choice remains;
> - closure of the deeper "absolute derivation of `g_bare = 1` from
>   A1+A2" Nature-grade target.

## 2. Structural derivation of (R)

The Cl(3)⊗Z³ substrate's taste cube has the natural decomposition
[`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
Step B):

```
V = C^8 = (b₁,b₂)-base ⊗ (b₃)-fiber = C^4 ⊗ C^2
       = (C^3_sym ⊕ C^1_antisym) ⊗ C^2
       = (V_3       ⊕ V_singlet)  ⊗ V_fiber
```

where:
- `V_3 = C^3_sym`: the 3D symmetric subspace under b₁↔b₂ exchange
  (color triplet carrier);
- `V_singlet = C^1_antisym`: the 1D antisymmetric subspace
  (lepton singlet);
- `V_fiber = C^2`: the b₃ axis (weak-doublet fiber).

The SU(3) generators are embedded as `T_a^V = T_a^{(3)} ⊗ I_{V_fiber}`
on V_3 ⊗ V_fiber, with zero on V_singlet ⊗ V_fiber. Equivalently:

```
T_a^V = (M_3 ⊗ I_2) ⊕ 0_(2x2 lepton) on the full 8D space
```

For any two SU(3) generators `T_a^V`, `T_b^V`:

```
Tr_V(T_a^V · T_b^V) = Tr_(V_3 ⊗ V_fiber) [(T_a^{(3)} T_b^{(3)}) ⊗ I_2]
                    + Tr_(V_singlet ⊗ V_fiber) [0]
                    = Tr_{V_3}(T_a^{(3)} T_b^{(3)}) · Tr_{V_fiber}(I_2)
                    = (1/2) δ_{ab} · 2
                    = δ_{ab}                                     (V-trace)
```

So `Tr_V(T_a^V T_b^V) = 1 · δ_{ab}` exactly, i.e. `N_F^{(V)} = 1`.

The factor 2 in the third line above is `dim(V_fiber) = 2`, the
fiber multiplicity. This is the structural ratio (R).

The factor 1/2 in the third line is the canonical Gell-Mann
convention on V_3, i.e. `N_F^{(3)} = 1/2`.

These two values are the only natural choices — any other Ad-invariant
representative would differ from these by an additional positive
scalar admission (which Killing rigidity says is allowed but Cl(3)
substrate primitives do not provide).

## 3. Why the binary choice (V_3 vs V) is genuinely admitted

The two trace functors `Tr_{V_3}` and `Tr_V` are both **categorically
natural** within the framework's representation-theoretic structure:

- `Tr_{V_3}` is the **canonical trace on the irreducible carrier** of
  the SU(3) fundamental rep. This is the choice used by standard
  rep theory (Slansky, Howe-Tan, Cvitanović, all of representation
  theory of compact Lie groups). The "natural" mathematical choice.

- `Tr_V` is the **canonical trace on the framework Hilbert space**
  V = C^8 in which the entire framework operator algebra lives. This
  is the choice used by the framework's Hamiltonian formulation
  ([`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md))
  and by lattice gauge theory (where the Hilbert space includes all
  taste/color/flavor degrees of freedom together). The "natural"
  physical choice.

The conflict between these two reflects a fundamental tension between:
- **rep-theoretic naturality** (trace on irreducible carrier is
  canonical from a category-of-finite-dim-G-modules perspective)
- **physical-Hilbert-space naturality** (trace on the full state
  space is canonical from a quantum-mechanics perspective)

Both are valid "natural" structures from different perspectives.
Cl(3) primitives — taking the algebra product, Clifford conjugation,
grade-0 projection, and Hilbert-Schmidt trace — admit **both** trace
functors as well-defined operations on `g_conc`. The framework's
existing notes uniformly adopt convention (a) (canonical Gell-Mann
`N_F = 1/2`); convention (b) is equally valid and would simply
re-parametrize all `g_bare` predictions.

## 4. Why no further reduction is possible from Cl(3) primitives alone

The seven-attack analysis (full report in
[`outputs/action_first_principles_2026_05_07/w2_n_f_derivation/ATTACK_RESULTS.md`](../outputs/action_first_principles_2026_05_07/w2_n_f_derivation/ATTACK_RESULTS.md))
systematically probes whether further structural arguments select
between `B^{(3)}` and `B^{(V)}`. Key findings:

| Attack | Verdict |
|---|---|
| Hilbert-Schmidt / Killing rigidity | "Up to scalar" by classical theorem; silent on overall scale |
| Cl(3)⊗Cl(3) ≅ Cl(6) / Spin(6) embedding | Routes admission upstream (SU(4) inherits the same convention) |
| Anomaly cancellation | Homogeneous in gauge-field power; invariant under N_F rescaling |
| Quantization / representation-integrality | Invariant under integer rescaling; multiple integrality conventions |
| Hardy operational reconstruction | Dimension-counting axioms scale-blind |
| Standard QFT literature consensus | Uniformly admits N_F = 1/2 as convention |
| Direct Cl(3) bivector trace | Works for SU(2); fails to extend to SU(3) |

The combined analysis: six structural obstructions are **definitive**
or **specific** (each names a structural barrier preventing the
corresponding closure path). One attack (Cl(3) bivector trace)
**partially** closes the SU(2) case via the Spin(3) → SO(3) double
cover, but does NOT extend to SU(3) because SU(3) generators are
not Cl(3) bivectors.

The single open route identified is:

**Categorical universality argument.** If one can show via
universal-property reasoning that the trace on the irreducible
carrier is uniquely "natural" in a category-theoretic sense, then
`B^{(3)}` would be uniquely selected. This is not closed here and
is documented in
[`outputs/action_first_principles_2026_05_07/w2_n_f_derivation/THEOREM_NOTE.md`](../outputs/action_first_principles_2026_05_07/w2_n_f_derivation/THEOREM_NOTE.md)
Section "Could a categorical / universal-property argument close
this?" as a future research target.

The most likely answer (per standard rep theory): trace on each
isotypic component is canonical, but there is no "preferred"
combination of components — so the V_3 vs V choice remains binary
admitted.

## 5. Strict tier comparison: pre-2026-05-07-W2 vs post

### Pre (four-layer stratification, L3 admission)

```yaml
L3_admission:
  type: continuous
  family: N_F ∈ ℝ_+ (any positive scalar)
  framework_choice: N_F = 1/2 (canonical Gell-Mann; one of infinitely many valid options)
  audit_implication: continuous-scalar admission per L3
```

### Post (this note's strict tightening)

```yaml
L3_admission:
  type: discrete
  family: N_F ∈ {1/2, 1}
  framework_choice: N_F = 1/2 (one of TWO structurally-natural options)
  structural_basis:
    - 1/2: canonical Gell-Mann (trace on V_3, irreducible carrier)
    - 1: full Hilbert-Schmidt (trace on V = C^8, full framework space)
    - ratio: exactly 2 = dim(V_fiber), fiber multiplicity (structural)
  audit_implication: binary admission per L3b (V_3 vs V)
```

The tightening is **strict** in the sense:
- continuous → discrete (one substrate-fixed parameter eliminated)
- the two values `{1/2, 1}` are **not** independent free parameters;
  they are exactly the natural HS representatives within Cl(3)+Z³
- the binary admission is **categorical** (V_3 vs V), not numerical

### Audit-grade implication for the parent

The parent
[`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
should be updated (after this note retains) to cite the **binary
admission at L3b** rather than the **continuous admission at L3**.
The four-layer stratification becomes a five-layer stratification as
shown in
[`outputs/action_first_principles_2026_05_07/w2_n_f_derivation/THEOREM_NOTE.md`](../outputs/action_first_principles_2026_05_07/w2_n_f_derivation/THEOREM_NOTE.md)
Table.

## 6. Declared audit dependencies (one hop)

| Authority | Audit-lane status | Role |
|---|---|---|
| [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) | unaudited candidate (positive_theorem proposed) | Killing rigidity (R1) — "up to scalar" structural result |
| [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md) | unaudited candidate (positive_theorem proposed) | Four-layer stratification (parent of the L3 sharpening this note delivers) |
| [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) | proposed_retained Claims 1, 2 | Cl(3) → End(V) embedding canonicity (Claim 1) |
| [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md) | bounded_theorem | SU(3) on V_3 (3D symmetric base) embedding |
| [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) | positive_theorem (proposed) | Per-site Hilbert dim = 2 (Pauli on C²) |

## 7. Load-bearing step (class A)

```text
Inputs:
  V = C^8 with fixed Hilbert-space inner product (axiom-level)
  V_3 ⊂ V: 3D symmetric base subspace (structural normalization Cl. 1)
  V_singlet ⊂ V: 1D antisymmetric base subspace
  V_fiber = C^2: b₃-fiber (per cl3_color_automorphism_theorem)
  V = (V_3 ⊕ V_singlet) ⊗ V_fiber                              (decomposition)

Step 1 (Killing rigidity, dep: HS rigidity theorem R1).
  B_HS on g_conc = su(3) is Ad-invariant; unique up to overall
  positive scalar k > 0 by classical Killing rigidity for simple
  Lie algebras.

Step 2 (Two natural representatives from substrate decomposition).
  The decomposition V = (V_3 ⊕ V_singlet) ⊗ V_fiber gives two
  natural Ad-invariant traces:
    B^{(3)}(X, Y) = Tr_{V_3}(X · Y)
    B^{(V)}(X, Y) = Tr_V(X · Y) = Tr_{V_3 ⊗ V_fiber}(...) + 0_singlet
                  = Tr_{V_3}(...) · Tr_{V_fiber}(I) + 0
                  = Tr_{V_3}(...) · dim(V_fiber)

Step 3 (Ratio = fiber multiplicity).
  B^{(V)} / B^{(3)} = dim(V_fiber) = 2
  This factor 2 is structurally fixed by the substrate decomposition;
  it is NOT a free convention.

Step 4 (Continuum-to-Z_2 reduction).
  Killing rigidity admits a 1-parameter family of forms (any positive
  k > 0). Cl(3)+Z³ substrate primitives admit exactly two natural
  representatives within this family: B^{(3)} and B^{(V)}.
  N_F^{(3)} = 1/2; N_F^{(V)} = 1.
  Reduction: continuous family → discrete 2-element set.

Step 5 (Z_2 → 1 admission).
  No Cl(3) primitive selects between B^{(3)} and B^{(V)}. Both are
  Ad-invariant; both correspond to natural decompositions; the ratio
  is structurally fixed but the choice is not.
  This is a binary admission: trace on irreducible carrier (selects
  N_F = 1/2) vs trace on full Hilbert space (selects N_F = 1).

Conclusion (class A):
  Cl(3) + Z³ + fixed Hilbert space embedding reduce N_F admission
  from continuous (any positive scalar) to discrete (one of two
  structurally-natural choices). The discrete choice is admitted.
```

The load-bearing step is class (A) — algebraic identities throughout,
with the substrate decomposition (`V = (V_3 ⊕ V_singlet) ⊗ V_fiber`)
as the structural input that fixes the ratio.

## 8. Verification

```bash
python3 outputs/action_first_principles_2026_05_07/w2_n_f_derivation/cl3_n_f_derivation_2026_05_07_w2_check.py
```

Verifies (live result: 22/0 EXACT pass, 0/0 BOUNDED):

1. Canonical Gell-Mann normalization on V_3: `Tr_3(T_a T_b) = (1/2) δ_{ab}`
2. Full taste-space trace on V: `Tr_V(T_a^V T_b^V) = 1 · δ_{ab}`
3. Ratio `Tr_V/Tr_3 = 2 = dim(V_fiber)` exactly
4. Casimir on V_3: `Σ_a T_a T_a = (4/3) I_3`
5. Killing-form Ad-invariance under random SU(3) action (3 trials)
6. Spin(6)/SU(4) trace inheritance: SU(3) ⊂ SU(4) gives `N_F = 1/2`
   via canonical SU(4) convention (illustrating the inheritance,
   not a derivation)
7. d-symbol values at canonical: `d_{118} = 1/√3`
8. SU(2) bivector argument: `Tr_2(σ_a/2 · σ_b/2) = (1/2) δ_{ab}`
9. SU(3) generators are NOT Cl(3) bivectors (does not extend to SU(3))
10. Discrete admission `N_F ∈ {1/2, 1}` numerically witnessed

## 9. Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Cl(3) primitives plus the framework's fixed Hilbert-space embedding
  V = C^8 reduce the L3 admission of the four-layer stratification
  from a continuous family N_F ∈ ℝ_+ to a discrete 2-element set
  N_F ∈ {1/2, 1}. The ratio 2 = dim(I_2) is structurally fixed by
  the Cl(3)⊗Z³ substrate's tensor-product decomposition.
proposed_load_bearing_step_class: A
declared_one_hop_deps:
  - g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07
  - g_bare_constraint_vs_convention_restatement_note_2026-05-07
  - g_bare_structural_normalization_theorem_note_2026-04-18
  - cl3_color_automorphism_theorem
  - cl3_per_site_hilbert_dim_two_theorem_note_2026-05-02
audit_required_before_effective_retained: true
parent_update_allowed_only_after_retained: true
admitted_context_inputs:
  - L3b binary admission: "trace space = V_3 (selects N_F = 1/2)"
    vs "trace space = V (selects N_F = 1)". This is the single
    remaining admission in the g_bare chain after the present
    sharpening.
distinguishing_content_from_2026-05-07_four_layer:
  the four-layer stratification's L3 is "any positive scalar N_F
  ∈ ℝ_+". The present note sharpens this to "discrete N_F ∈ {1/2, 1}",
  with the binary choice corresponding to V_3 vs V trace. This is a
  substantive sharpening of the L3 admission tier (continuous to
  discrete) supported by structural identification of the two
  natural HS representatives via the fiber-multiplicity factor 2.
```

## 10. What this candidate can support after retention

- **Sharpening of the four-layer stratification.** The L3 admission
  is reduced from continuous to binary. After retention, the parent
  restatement note should be cross-linked to cite this Z_2 reduction
  explicitly.

- **Strengthened bridge-gap closure.** The framework's `g_bare = 1`
  chain has an even tighter named admission (binary choice), making
  the bridge audit-defensibility one tier sharper than the
  continuous-scalar admission.

- **Foreclosure of the Nature-grade target.** The seven attack
  vectors define what's foreclosed. Future attempts to derive
  `N_F = 1/2` should NOT retry these seven routes; they should
  pursue only the open route (categorical universality) or admit
  the Z_2 binary as definitive.

## 11. What this theorem does NOT close

- **The Z_2 → 1 reduction.** The choice between `N_F = 1/2` (V_3
  trace) and `N_F = 1` (V trace) is not closed. Both are
  structurally admissible.

- **The deeper "absolute derivation of `g_bare = 1` from A1+A2"
  Nature-grade target.** The Z_2 reduction is a sharpening, not a
  closure.

- **The action-form question** (Wilson plaquette form). Separate
  retention target via A2.5; not addressed here.

- **The Hamiltonian-Lagrangian dictionary** (Convention C-iso).
  Separate; not addressed here.

## 12. Cross-references

- [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) — parent
  note that may cite this candidate after retention as the
  strengthened L3-admission sharpening.
- [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  — declared one-hop dep providing the four-layer stratification
  parent that this note sharpens at L3.
- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  — declared one-hop dep providing the Killing rigidity (R1) "up to
  scalar" result.
- [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md)
  — sister Hamiltonian-level rigidity argument (uses V trace
  explicitly; complementary to the present V_3 vs V binary choice
  framing).
- [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  — declared one-hop dep providing the Cl(3) → End(V) → su(3) chain
  (Claim 1) and the Ad-invariant form identification (Claim 2).
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  — declared one-hop dep providing SU(3) on V_3 with the substrate
  decomposition `V = (V_3 ⊕ V_singlet) ⊗ V_fiber`.
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
  — provides `C_F = 4/3` at canonical `N_F = 1/2`.
- [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)
  — declared one-hop dep providing per-site dim = 2 (Pauli rep).
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  — current framework axiom set (A1, A2). The present theorem is
  consistent with the open-gate treatment in the minimal axioms note.
- [`outputs/action_first_principles_2026_05_07/w2_n_f_derivation/THEOREM_NOTE.md`](../outputs/action_first_principles_2026_05_07/w2_n_f_derivation/THEOREM_NOTE.md)
  — main W2 theorem note documenting the full derivation context
  and seven-attack analysis.
- [`outputs/action_first_principles_2026_05_07/w2_n_f_derivation/ATTACK_RESULTS.md`](../outputs/action_first_principles_2026_05_07/w2_n_f_derivation/ATTACK_RESULTS.md)
  — full seven-attack attack-results note enumerating the structural
  barriers.

## 13. Honest scoping summary

The continuum-to-Z_2 reduction is the **one positive partial result**
of the W2 N_F derivation attack. Cl(3) primitives plus the framework's
fixed Hilbert-space embedding reduce `N_F` admission from a continuous
family to a discrete 2-element set `{1/2, 1}`. The ratio between
these two values (factor 2 = fiber multiplicity) is structurally
fixed by the Cl(3)⊗Z³ substrate.

The Z_2 → 1 reduction is genuinely admitted, not derived. The seven
attack vectors enumerate the structural barriers preventing the
deeper closure. Six of these are definitive (rigidity, embedding
inheritance, anomaly homogeneity, integrality invariance,
operational reconstruction, literature consensus); one (Cl(3)
bivector trace) is partial — it closes SU(2)'s `N_F = 1/2` but
fails to extend to SU(3).

The single open route (not pursued here) is categorical universality:
whether the trace on the irreducible carrier is uniquely "natural" in
a category-of-G-modules sense. This is a separate Nature-grade
research target.

The bottom line: the framework's bridge gap shrinks from "one
admitted continuous scalar" to "one admitted binary choice." This
is a substantive sharpening of the L3 admission tier — not a
closure of the deeper question of whether `N_F = 1/2` itself is
uniquely forced.
