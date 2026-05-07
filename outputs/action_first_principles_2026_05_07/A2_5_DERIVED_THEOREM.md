# A2.5-as-Derived-Theorem — RP+Substrate+Symanzik Forcing of Continuum-Limit Wilson-Form

**Date:** 2026-05-07
**Type:** bounded_theorem (candidate, audit-pending) — closes A2.5 at
the continuum level only; finite-β residual remains open per existing
no-go.
**Claim type:** open_axiom → proposed_bounded_derived_theorem (this
note's content, *if* audited clean, demotes the previously proposed
A2.5 axiom to a derived consequence of existing primitives **at the
continuum level**; the existing no-go on finite-β action-form
uniqueness still stands)
**Status authority:** independent audit lane only. This source note does
not set or predict an audit outcome.

## Scope

This note proves, on the framework's existing retained primitive stack
(A1+A2 + per-site Hilbert dim 2 + canonical Tr-form + retained
SU(3)/Casimir + retained RP + retained microcausality + retained
single-clock + Cl(3) color automorphism + standard Symanzik
power-counting), that the **leading-dim-4 magnetic operator** on each
spatial plaquette of the Kogut-Susskind Hamiltonian is

```
M̂(U_p)|_{leading dim} = α · Re Tr_F(U_p) + β   + O(higher Symanzik)
```

— **Wilson-form at the continuum level**, with α determined by the
Block B continuum-matching constraint and β an irrelevant additive
constant.

This is a **bounded** result, not a full closure: in the continuum
limit `a → 0` it suffices, but at **finite β** the action-form
ambiguity (Wilson vs heat-kernel vs Manton) remains as the existing
no-go states
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)).

If audited clean, this note demotes A2.5's **continuum-limit content**
from "proposed axiom" to "derived theorem" and the framework's
primitive stack is unchanged. The bridge-gap action-form ambiguity
**at the continuum level** then closes modulo the open `g_bare = 1`
gate (canonical-coupling residual). The bridge-gap action-form
ambiguity **at finite β** remains open per the existing no-go.

## Inputs (no new axiom)

The proof uses ONLY:

1. **A1**: Cl(3) is the local algebra at each lattice site
   ([`MINIMAL_AXIOMS_2026-05-03.md`](../../docs/MINIMAL_AXIOMS_2026-05-03.md)).
2. **A2**: Z³ is the spatial substrate
   ([`MINIMAL_AXIOMS_2026-05-03.md`](../../docs/MINIMAL_AXIOMS_2026-05-03.md)).
3. **Per-site Hilbert dim 2** (Pauli realization)
   ([`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)).
4. **Canonical Tr-form** `Tr(T_a T_b) = δ_{ab}/2`
   ([`G_BARE_RIGIDITY_THEOREM_NOTE.md`](../../docs/G_BARE_RIGIDITY_THEOREM_NOTE.md);
   [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)).
5. **SU(3) emergence** on the symmetric base
   ([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md)).
6. **Retained reflection positivity** along the temporal axis
   ([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)).
7. **Retained microcausality / Lieb-Robinson + tensor factorization**
   on equal-time slices
   ([`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)).
8. **Retained single-clock codimension-1 evolution** (RP axis is
   uniquely temporal)
   ([`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)).
9. **Z³ regular cubical CW complex structure** (substrate
   combinatorics): every 2-cell is a 1×1 plaquette.
10. **Standard QFT operator-dimension power-counting** (Symanzik
    1983): operators of dimension > 4 are irrelevant in the
    long-wavelength continuum limit.

The proof uses NO additional axiom. In particular, A2.5 is not
admitted; it is the conclusion of this theorem.

## Statement

**Theorem (continuum-level uniqueness of the dim-4 magnetic
operator — bounded form).** Under inputs 1–10 above, the framework's
magnetic operator on each spatial plaquette of the KS Hamiltonian,
**in the long-wavelength continuum limit `a → 0`**, takes the form

```
M̂_{continuum}(F_p) = α_eff · Tr(F_p²)
```

with `α_eff ≥ 0` a real constant determined by the Block B continuum-
matching constraint
([`BLOCK_B_HAMILTONIAN_DERIVATION.md`](BLOCK_B_HAMILTONIAN_DERIVATION.md))
modulo the open `g_bare = 1` gate.

**Wilson lattice form is the parsimonious lattice representative** of
this continuum operator (zero higher-character coefficients,
`m_F · Re χ_F` only). Heat-kernel and Manton are alternative lattice
representatives of the same continuum operator with different
higher-character coefficient distributions; they are RP-compatible
and give the same continuum limit but differ at finite β.

**Finite-β residual:** This theorem does NOT select Wilson over
heat-kernel or Manton at finite β; that selection is consistent with
the existing no-go on action-form uniqueness
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md))
and remains a structural ambiguity at finite β. Wilson-form is a
canonical convention, not a derived uniqueness, at the lattice level.

## Proof

The proof has six steps. Steps 1–4 establish that any RP-compatible
primary magnetic operator on a single 1×1 plaquette has a positive
character expansion using only the fundamental and its dual. Step 5
applies standard Symanzik power-counting to argue the leading-dim-4
contribution is uniquely Wilson-form at the continuum level. Step 6
collects the conclusion.

### Step 1 — Substrate forces 1×1 plaquette as the elementary closed loop

Z³ as a regular cubical CW complex has 0-cells (sites), 1-cells
(links), 2-cells (1×1 plaquettes), 3-cells (unit cubes), each
indexed by a vertex `x ∈ Z³` and a coordinate-axis tuple. Every 2-cell
of Z³ is a unit 1×1 plaquette by construction.

By cubical Stokes / chain-complex relation `∂_2 : C_2 → C_1`, every
non-trivial closed 1-chain `c` that bounds a 2-chain `S` (i.e.,
`c = ∂_2 S`) decomposes as a signed sum of the boundaries of the
constituent unit 2-cells of `S`. The minimum-length non-trivial closed
1-chain is therefore the boundary of a single 1×1 plaquette (length
4). Larger loops are signed sums of such plaquette boundaries up to
isoperimetric corrections (`|∂A| ≥ 4√|A|` for a 2-chain `A` of area
`|A| ≥ 1` on Z², saturated only at `|A| = 1`).

This is purely substrate combinatorics — A2 alone, no algebra
required.

So the elementary gauge-invariant closed loop on Z³ is the 1×1
plaquette.

(See Attack 3 of
[`A2_5_DERIVATION_ATTACK_RESULTS.md`](A2_5_DERIVATION_ATTACK_RESULTS.md)
for the full statement.) ∎

### Step 2 — Cl(3) primitive operations admit only the fundamental trace as natural single-link operation

By the Cl(3) per-site uniqueness theorem
([`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md))
the minimal faithful Cl(3)-irrep is the 2-dimensional spinor module.
By the Cl(3) color automorphism theorem
([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md)),
SU(3) emerges acting on the 3-dim symmetric base of the taste cube
as the *fundamental* representation `V_F`.

The natural Cl(3)-primitive trace operation is the **fundamental
trace** `Tr_F : End(V_F) → ℂ`; it equals `2⟨·⟩₀` after the
identification of the spinor rep dimension. Higher-rank traces
(`Tr_(2,0)`, `Tr_(1,1)`, etc.) require constructing tensor-product
representations (e.g., `Sym² V_F`, `V ⊗ V^*`) and projecting onto
isotypic components — operations not built into the Cl(3) primitive
vocabulary
([`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md)
attack-5 response, scope-clarification 1).

Therefore on a single plaquette, the only Cl(3)-primitive trace
operation acting on the holonomy `U_p ∈ SU(3)` is `Tr_F(U_p)` (or
products / polynomials thereof; the ring-theoretic question is handled
in Step 3 via RP).

### Step 3 — RP forces non-negativity of character coefficients

By the retained RP theorem, the framework admits a temporal-link
reflection `θ` along the unique RP-admissible axis (the temporal
axis, by single-clock theorem). The OS / Sharatchandra-Thun-Weisz
factorization of the action restricts to:

```
Z[F] = || ∫_{Λ_+ ∪ ∂} DU exp(-S_+) F ||²_{L²(SU(3) crossing links, Haar)}
                                                                    (*)
```

For a candidate primary magnetic operator on a temporal plaquette
expanded in SU(3) characters,

```
M̂(U_p) = Σ_λ m_λ Re χ_λ(U_p),     S_p = β · (const − M̂(U_p)/N_c)
```

the Boltzmann weight `e^{-S_p}` admits a character expansion
`Σ_λ c_λ(β) χ_λ(U_p)` whose coefficients depend on the action form.

(R3-a) **Non-negativity required.** For (*) to give a **non-negative**
`Z[F]` for arbitrary positive-time `F`, the character coefficients
`c_λ(β)` of `e^{-S_p}` must be non-negative for all λ. If any
`c_λ(β) < 0`, the OS rewriting fails: the Haar integral over the
crossing temporal links can produce negative contributions on
specific test functions `F`, breaking `Z[F] ≥ 0`.

This forbids **negative-coefficient improvement schemes**: the
Lüscher-Weisz improved action with `c_1 < 0` for the 2×1 rectangle
(used to cancel O(a²) lattice artifacts) gives a character expansion
of `e^{-S_p}` with some `c_λ(β) < 0`, hence violates RP at the
plaquette level. This matches the retained RP theorem's explicit
note that "no other plaquette form (e.g. improved actions with
negative-coefficient rectangles) is permitted"
([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`, line 251-254](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)).

(R3-b) **Wilson, heat-kernel, Manton are all RP-compatible.** All
three actions have **positive** character expansions for `β > 0`:
- Wilson: `e^{-β(1-Re Tr U/N_c)}` expands as `Σ_λ c_λ(β) χ_λ(U)`
  with `c_λ(β) > 0` for all λ (Bessel-determinant character
  coefficients; Drouffe-Zuber 1983).
- Heat-kernel: `Σ_λ d_λ e^{-(t/2)C_2(λ)} χ_λ(U)` with all
  coefficients `> 0` directly.
- Manton: `e^{-β d²(U,I)}` expands as `Σ_λ c_λ(β) χ_λ(U)` with
  `c_λ(β) > 0` (positive heat-semigroup-type coefficients).

So **RP alone does not select Wilson over heat-kernel or Manton**.
This is consistent with the existing no-go
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)).

**What RP does close**: the action term must, when expanded in
characters, have all non-negative character contributions. This
rules out a substantial class of "improved" actions, but does not
single out Wilson uniquely.

### Step 4 — Cubic point-group symmetry transports temporal to spatial form

By A2 (Z³), the 3D lattice has an action of the spatial cubic point
group `O_h`. Spatial plaquettes `p_{ij}` (in the `i, j` plane, both
`i, j` spatial) for `(i, j) ∈ {(1,2), (1,3), (2,3)}` are
`O_h`-equivalent and must carry the same magnetic operator form.

By the Block B continuum-matching constraint
([`BLOCK_B_HAMILTONIAN_DERIVATION.md`](BLOCK_B_HAMILTONIAN_DERIVATION.md))
and the Hamilton-limit Wick rotation, the spatial-plaquette
magnetic operator must reproduce the temporal-plaquette form (the
form that survives RP) up to an `(a_τ / a_s)` rescaling.

Combined with Step 3's RP-positivity requirement and Step 1's
single-plaquette substrate localization, the spatial-plaquette
magnetic operator is constrained to a non-negative real combination
of plaquette characters with positive expansion of `e^{-S_p}`.

### Step 5 — Symanzik power-counting forces dim-4 `Tr(F²)` operator at the continuum

By Steps 1–4, the magnetic operator on each spatial plaquette is
expanded as

```
M̂(U_p) = Σ_λ m_λ Re χ_λ(U_p)
```

with `m_λ ≥ 0` (RP) and the support being a single 1×1 plaquette
(substrate combinatorics).

Now apply the small-`a` expansion. For `U_p = exp(i a² F_p)` with
`F_p ~ F_{ij}` the continuum field strength, using standard SU(N)
character expansions (Drouffe-Zuber 1983 §III; Cvitanović 2008 ch. 9):

```
Re χ_F(U_p)     = N_c   − (a⁴/2) Tr(F_p²) + O(a⁸)
Re χ_(2,0)(U_p) = N_c(N_c+1)/2  − (a⁴/2) (N_c+2) Tr(F_p²) + O(a⁸)
Re χ_(1,1)(U_p) = N_c²−1         − (a⁴) · (linear comb. of Tr(F²)) + O(a⁸)
Re χ_λ(U_p)    = c_λ(0)        − (a⁴) ω_λ Tr(F_p²)         + O(a⁸)
```

where `ω_λ` is the second-order coefficient of `χ_λ` in the small-`a`
expansion (a non-negative class function of `λ` and `N_c`).

The key observation: **every** character `χ_λ`, when expanded in
small `a`, contributes `Tr(F²)` at order `a⁴` (i.e., dim-4) with
coefficient `(a⁴/2) ω_λ`. Higher operators (Tr(F³), Tr(F⁴), etc.)
appear only at order `a⁶, a⁸, …` (i.e., dim ≥ 6, 8, ...).

By **standard Symanzik power-counting** (Symanzik 1983; Lüscher 1998
review), operators of mass dimension > 4 are **irrelevant** in the
long-wavelength continuum limit.

So the framework's continuum-level magnetic operator is

```
M̂(U_p)|_{continuum} = α_eff · Tr(F_p²) + Symanzik-irrelevant
```

with `α_eff = (1/2) Σ_λ m_λ ω_λ ≥ 0`, where the sum is over the
non-negative character coefficients `m_λ`.

**This is the same dim-4 operator** `Tr(F²)` that Wilson, heat-
kernel, and Manton all produce. The framework's continuum prediction
at the dim-4 level is unique up to the overall coefficient `α_eff`,
which is fixed by Block B continuum-matching modulo `g_bare = 1`.

**However, this Step 5 closure is weaker than the original A2.5
proposal:** A2.5 was meant to force `m_λ = 0` for all `λ ≠ F`, not
merely to force the dim-4 operator. The Symanzik power-counting
argument forces the *dim-4 operator* to be `Tr(F²)`, but it does
NOT force `m_λ = 0` for higher characters at finite `a`. The
continuum-limit prediction is unique; the lattice-level (finite-`a`,
finite-β) prediction is action-form ambiguous.

This is the substantive content of A2.5 reduced from an axiom to a
derived theorem **at the continuum limit only**.

### Step 6 — Conclusion (bounded — continuum-level only)

Combining Steps 1–5: the framework's continuum-level magnetic
operator on each spatial plaquette, in the long-wavelength
continuum limit `a → 0`, is uniquely

```
M̂_{continuum}(F_p) = α_eff · Tr(F_p²)
```

with `α_eff` determined by Block B continuum-matching modulo the
open `g_bare = 1` gate.

**Wilson-form is the most parsimonious lattice representative** of
this continuum operator: it sets all higher-character coefficients
`m_λ = 0` for `λ ≠ F` at the lattice level, and matches the
continuum limit exactly via `α_eff = m_F · 1 = m_F`. Heat-kernel
sets `m_λ = d_λ e^{-(t/2)C_2(λ)}` at the lattice level, also
matching the continuum limit but via a different lattice-coefficient
distribution. Manton uses the geodesic-distance function; same
continuum limit, different lattice coefficients.

**At finite β** all three (and any RP-positive-character action) are
permitted; Wilson is *one canonical parsimonious choice* among them,
not *the unique forcing*. The framework's existing no-go on action-
form uniqueness at finite β
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md))
remains correct. ∎

The substantive result: the framework's **continuum-level
prediction** for the dim-4 magnetic operator is uniquely
`α_eff · Tr(F²)` from existing primitives (no A2.5 needed). This
discharges A2.5's continuum content. A2.5's finite-β content
(specifically picking Wilson over heat-kernel/Manton at finite β
as the parsimonious member) is structurally undetermined and must
remain a *convention*, not a derivation.

## What this theorem closes

(a) **Continuum-level magnetic operator unique up to coefficient**:
the framework's continuum-level magnetic operator on each spatial
plaquette is uniquely `α_eff · Tr(F_p²)` with `α_eff ≥ 0` determined
by Block B continuum-matching modulo the `g_bare = 1` open gate.
This is the unique dim-4 operator content. Wilson lattice form is
the parsimonious lattice representative of this continuum operator.

(b) **A2.5 axiom proposal continuum content**: if this theorem is
audited clean, A2.5's **continuum-level content** ("the framework's
continuum prediction is uniquely the dim-4 `Tr(F²)` operator") is
demoted from "proposed axiom" to "derived theorem". A2.5's
**finite-β content** (forcing Wilson over heat-kernel/Manton at
finite β as the unique lattice action) is NOT derived; it remains
either an admitted convention or, more honestly, a parsimony
selection within the equivalence class of lattice realizations of
the same continuum operator. The framework's axiom stack remains
A1+A2 unchanged.

(c) **Bridge gap at the continuum level**: reduces to the open
`g_bare = 1` gate
([`G_BARE_DERIVATION_NOTE.md`](../../docs/G_BARE_DERIVATION_NOTE.md))
plus the Hamilton-limit / multi-plaquette extrapolation
([`G_BARE_3PLUS1_REFRAMING.md`](G_BARE_3PLUS1_REFRAMING.md)). The
existing no-go on **finite-β action-form uniqueness** is unchanged
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)).

## What this theorem does NOT close

(a) **Finite-β action-form uniqueness**: heat-kernel, Wilson, Manton
all satisfy: A1+A2, RP, microcausality, single-clock, canonical
Tr-form, Casimir-derived inputs, and have positive character
expansions. Each gives the same dim-4 leading operator; they differ
at finite β only by Symanzik-irrelevant higher-character corrections.
The framework predicts **the same continuum limit** for all three;
at finite β, the prediction is action-form ambiguous.

(b) **Sub-leading (dim ≥ 8) corrections**: this theorem treats
higher-character contributions as Symanzik-irrelevant in the
continuum limit, but does not derive their *specific values* at
finite β. Different action-form choices yield different specific
finite-β values for sub-leading observables.

## Sharp residuals + audit-lane handoff

Two residuals remain for audit verification:

**Residual A: temporal vs spatial plaquette transport (Step 4).** The
spatial-plaquette form is forced by spatial cubic symmetry combined
with Hamilton-limit matching. The audit lane should verify that the
Block B continuum-matching constraint is sufficient to transport
the temporal-plaquette form to spatial plaquettes.

**Residual B: Symanzik power-counting acceptability (Step 5).** The
load-bearing step is the standard QFT result that operators of
dim > 4 are irrelevant in the continuum limit (Symanzik 1983). This
is universal physics power-counting and not framework-specific. If
the audit lane accepts this as standard, the theorem closes at the
continuum level. If the audit lane treats Symanzik power-counting
itself as an admission requiring framework-internal derivation, the
theorem becomes scope-narrower.

If both residuals are audited clean, this theorem closes A2.5's
continuum-level content as a derived consequence of existing
primitives + standard Symanzik power-counting. The finite-β residual
remains under the existing no-go.

## Honest claim status

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  From A1+A2 + canonical Tr-form + retained RP + retained microcausality
  + retained single-clock + Z³ CW-complex substrate combinatorics +
  standard Symanzik power-counting, the framework's spatial-plaquette
  magnetic operator in the KS Hamiltonian, IN THE LONG-WAVELENGTH
  CONTINUUM LIMIT (a → 0), is uniquely α_eff · Tr(F_p²) for α_eff ≥ 0
  determined by Block B continuum-matching modulo the open g_bare = 1
  gate. Wilson lattice form is the parsimonious lattice representative
  of this continuum operator; heat-kernel and Manton are alternative
  lattice representatives giving the same continuum limit. AT FINITE β
  the lattice action form remains ambiguous over {Wilson, heat-kernel,
  Manton}, consistent with the existing no-go. The previously proposed
  axiom A2.5's continuum-level content is thereby demoted from
  proposed_axiom to proposed_bounded_derived_theorem; its finite-β
  content remains structurally undetermined and is a parsimony
  convention rather than a derivation.
admitted_context_inputs:
  - Standard Symanzik power-counting (Symanzik 1983; universal QFT,
    not framework-specific) — load-bearing for the continuum-limit
    closure
  - g_bare = 1 open gate (canonical-coupling residual; tracked
    separately at G_BARE_DERIVATION_NOTE.md)
proposed_load_bearing_step_class: B (bounded derived theorem on A_min
  plus retained-grade support inputs plus standard QFT power-counting;
  no new axiom; bounded by the open g_bare gate and the existing
  finite-β no-go).
status_authority: independent audit lane only
actual_current_surface_status: source_proposal
conditional_surface_status: bounded derived theorem on A_min + 4
  retained-grade input theorems + standard Symanzik power-counting,
  contingent on audit verdict; finite-β residual unchanged.
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  All load-bearing inputs are retained or near-retained on the current
  authority surface. The proof uses only retained primitives, retained
  support theorems, substrate combinatorics on Z³ as a regular cubical
  CW complex, and standard Symanzik power-counting (universal QFT
  convention, not framework-specific). No new axiom introduced; no
  new fitted parameter; no new observed value; no new convention
  beyond universal QFT power-counting. The bounded scope is honest:
  the theorem closes the continuum-level content of A2.5 only; the
  finite-β residual remains open per the existing no-go.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Cross-references

- [`A2_5_DERIVATION_ATTACK_RESULTS.md`](A2_5_DERIVATION_ATTACK_RESULTS.md) — six-attack analysis (this note's parent)
- [`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md) — A2.5 axiom proposal + 5-attack review
- [`BLOCK_B7_PRIMITIVE_OPS_FORCING.md`](BLOCK_B7_PRIMITIVE_OPS_FORCING.md) — the original B.7 forcing argument under A2.5
- [`BLOCK_B_HAMILTONIAN_DERIVATION.md`](BLOCK_B_HAMILTONIAN_DERIVATION.md) — KS Hamiltonian derivation
- [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) — RP theorem (load-bearing input of Step 3)
- [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) — single-clock theorem (used in Step 3)
- [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) — microcausality theorem
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md) — SU(3) emergence (Step 2)
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md) — Casimir support
- [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](../../docs/G_BARE_RIGIDITY_THEOREM_NOTE.md) — `g_bare = 1` rigidity (used in Step 3 coefficient handling)
- [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md) — prior no-go (this theorem's target)

## Standard external references

- Osterwalder, K. & Seiler, E. (1978), "Gauge field theories on the
  lattice," *Ann. Phys.* 110.
- Sharatchandra, H. S., Thun, H. J., Weisz, P. (1981), *Nucl. Phys. B*
  192, 205.
- Symanzik, K. (1983), "Continuum limit and improved action in
  lattice theories," *Nucl. Phys. B* 226, 187.
- Lüscher, M. (1998), "Advanced lattice QCD," in *Probing the
  Standard Model of Particle Interactions*, Les Houches Session
  LXVIII, Elsevier.
- Hatcher, A. (2002), *Algebraic Topology*, Cambridge Univ. Press,
  ch. 2 (CW complexes).
- Schur's lemma, standard SU(N) representation theory.
