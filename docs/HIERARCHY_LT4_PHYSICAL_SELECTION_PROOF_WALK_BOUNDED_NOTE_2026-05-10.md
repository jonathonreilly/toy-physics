# Hierarchy L_t = 4 Physical-Selection Proof-Walk Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.
**Source-note proposal disclaimer:** this note is a source-note
proposal; audit verdict and downstream status are set only by the
independent audit lane.
**Primary runner:** [`scripts/frontier_hierarchy_lt4_physical_selection_proof_walk.py`](../scripts/frontier_hierarchy_lt4_physical_selection_proof_walk.py)

## 1. Claim scope

> **Theorem (Conditional `L_t = 4` physical-selection proof-walk).**
> Given (i) the retained algebraic Klein-four orbit theorem on the
> staggered-Dirac APBC temporal circle
> ([`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md),
> retained;
> [`HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md),
> retained;
> [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md),
> retained_bounded), and (ii) three explicitly named admissions
> A-W-A, A-W-B, A-W-C (defined below), the algebraic `L_t = 4`
> selector on the staggered block IS the physical EWSB temporal
> block. The three admissions are necessary: without any one of
> them, the algebraic-to-physical bridge does not close from
> A1 (Cl(3) local algebra) + A2 (Z³ spatial substrate) alone.

This bounded theorem **explicitly does NOT** claim:

- unconditional retirement of any of the three admissions A-W-A,
  A-W-B, A-W-C from A1+A2;
- closure of the framework's electroweak hierarchy formula
  `v = M_Pl × α_LM^16 × (7/8)^(1/4)` (downstream chain);
- closure of `M_Pl` or `α_LM^16` (separate authority chains);
- retirement of the open staggered-Dirac realization gate
  ([`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md));
- a positive-theorem promotion of any cited authority. The
  conditional shape — closure given the three named admissions —
  is the load-bearing content.

This note is a proof-walk in the sense of
[`HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md`](HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md)
and
[`LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md):
it walks the existing chain step-by-step and isolates the named
admissions, without adding new content beyond making the
conditional shape explicit.

## 2. Background — what the retained authorities already establish

The hierarchy authorities cited above collectively establish the
following four algebraic facts on the exact minimal hierarchy
block (`L_s = 2`, staggered Dirac on APBC temporal circle):

1. **Exact Matsubara closed form** ([`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md),
   retained):

   ```text
   |det(D + m)|  =  Π_ω  [m² + u_0² (3 + sin²ω)]⁴,
   ω_n = (2n + 1)π / L_t.
   ```

2. **Klein-four orbit decomposition on APBC phases**
   ([`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md),
   currently `unaudited` per ledger): the APBC temporal phase
   set decomposes into sign-and-conjugation closed orbits under
   the Klein-four action `z → z, −z, z*, −z*`. `L_t = 2` carries
   only the unresolved sign pair `{+i, −i}`; `L_t = 4` carries
   the unique minimal **resolved** orbit of size 4; `L_t > 4`
   immediately splits into multiple orbit sectors.

3. **Uniform temporal weight at the selected orbit**
   ([`HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md),
   retained): at `L_t = 4`, `sin²((2n+1)π/4) = 1/2` for all
   `n ∈ {0, 1, 2, 3}` — the orbit is uniformly weighted. At
   `L_t ∈ {6, 8}`, `sin²` is not uniform on the orbit set
   (explicit values in the cited note).

4. **Spatial-BC and `u_0`-scaling closure**
   ([`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md),
   retained_bounded): on the minimal `L_s = 2` block, spatial APBC
   is selected by the existence of a finite intensive 3+1 order-
   parameter limit, and the linear `1/u_0` tadpole scaling is the
   exact local statement.

Together these establish: **the algebraic L_t = 4 result on the
staggered-Dirac block is settled.** What is not settled is the
bridge from "algebraic L_t = 4 on the staggered block" to "physical
EWSB temporal block."

## 3. The bridge chain — four steps + three admission walls

The bridge from algebraic `L_t = 4` to physical EWSB temporal block
is the four-step chain (a)-(d) of the campaign brief, walked
explicitly. Each step's inputs are catalogued, and the three named
admission walls are isolated.

### Step (a). Klein-four orbit on the staggered block at `L_t = 4`

**Statement:** the Klein-four action `z → z, −z, z*, −z*` on the
APBC temporal phases `z_n = exp(i(2n+1)π/L_t)` has a unique minimal
**resolved** orbit at `L_t = 4`.

**Source:** items 2 + 3 of §2 above (retained / retained-bounded
authorities). This step is algebraic and fully closed on the
staggered-Dirac block.

**Inputs needed:** APBC phase set on the temporal circle;
Klein-four group action.

**Admission walls invoked:** none at this algebraic step.

### Step (b). The EWSB order parameter is a local bosonic CPT-even bilinear

**Statement:** the physical EWSB order parameter, identified with
the local curvature of the effective action
`∂²_φ ΔV_eff |_{φ = 0}`, is:

- bosonic (Z₂ fermion-sign blind);
- quadratic / bilinear in fermions;
- CPT-even (invariant under complex conjugation / time reversal);
- local.

**Source:** [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
asserts this identification. The asserted identification names the
order parameter via a continuum effective-action object
(`ΔV_eff`), which is then matched to the lattice scalar generator
via [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).

**Inputs needed:** an identification of the physical EWSB order
parameter with the lattice scalar generator `W[J] = log|det(D + J)|`.
That identification is the admission wall A-W-B below.

**Admission wall invoked:**

- **A-W-B (scalar-additivity / observable-class admission).**
  The audit-named open admission of
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):
  *"the load-bearing claim is that the unique additive CPT-even
  scalar generator is `W = log|det(D + J)|`; the load-bearing
  step admits scalar additivity on independent subsystems
  (P1) as a physical-principle premise. The runner verifies the
  algebra after that premise is chosen; it does not derive why
  physical scalar observables must select that generator from the
  axiom alone."*
  (Source: audit verdict on `observable_principle_from_axiom_note`
  in the audit ledger.) The 2026-05-09 update to that note
  retired P2/P3/P4 to runner-local consequences but explicitly
  left P1 admitted.

### Step (c). Klein-four invariance of the EWSB sector

**Statement:** the physical EWSB scalar curvature must be
invariant under the Klein-four action on the APBC temporal
phases.

**Source:** items 2 of §2 (algebraic Klein-four invariance) combined
with item (b) (the EWSB order parameter is the local bosonic
CPT-even bilinear). On the staggered block, the Klein-four
invariance of the bilinear is a structural consequence of CPT-even
phase blindness applied to the source-deformed Dirac determinant.

**Inputs needed:** CPT-even phase blindness on the staggered block.

**Admission wall invoked:**

- **A-W-C (CPT-even phase-blindness admission).** The CPT primitive
  is supplied by [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), which
  carries `effective_status = unaudited` in the live audit ledger.
  The 2026-05-10 narrow specialization
  [`CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`](CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md)
  also carries `effective_status = unaudited`, and the older
  [`AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`](AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md)
  carries `effective_status = audited_conditional`. None of the
  CPT primitives is currently retained; CPT-even phase blindness
  is therefore an admission at the bridge from algebra to physical
  bilinear class.

### Step (d). The physical EWSB temporal block IS L_t = 4

**Statement:** combining (a) + (b) + (c), the physical EWSB scalar
curvature on the staggered block is Klein-four invariant, hence its
temporal support lies in a Klein-four-closed orbit. The unique
minimal resolved Klein-four orbit on the APBC temporal circle is
`L_t = 4`. Therefore the physical EWSB temporal block IS `L_t = 4`.

**Source:** algebraic combination of (a) + (b) + (c).

**Inputs needed:** the staggered-Dirac block on which the curvature
lives must itself be the physical EW substrate.

**Admission wall invoked:**

- **A-W-A (staggered-Dirac realization admission).** The framework's
  current minimal axiom set
  ([`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md))
  is **A1 (Cl(3) local algebra) + A2 (Z³ spatial substrate)**. The
  staggered-Dirac realization on `Z³` (with APBC temporal extent
  and 8-corner doubler structure) is recorded as an **open gate**
  in
  [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  with `effective_status = open_gate`. Without closure of that
  gate, "the staggered block IS the physical EW substrate" is an
  admission, not a derivation. The Klein-four argument lives on
  the staggered block; it inherits the gate.

## 4. Conditional load-bearing statement

> Conditional on A-W-A (staggered-Dirac realization gate closes
> from A1+A2), A-W-B (scalar-additivity P1 on independent
> subsystems forces `log|det|` as the physical scalar generator),
> and A-W-C (CPT-even phase blindness on the staggered block is
> retained from a CPT primitive), the chain (a) → (b) → (c) → (d)
> in §3 closes and the physical EWSB temporal block is `L_t = 4`.

This is the bounded conditional shape this note targets.
**Unconditional retirement of A-W-A, A-W-B, A-W-C from A1+A2 is
not closed by this note.** Each admission is recorded with its
existing open-gate / audited-conditional / unaudited authority
row in the live ledger.

## 5. Proof-Walk catalogue

The chain has four steps and three admissions. The proof-walk
catalogue:

| Step | Statement | Algebra source | Admission wall? |
|---|---|---|---|
| (a) | Klein-four orbit on APBC phases, unique resolved at L_t=4 | retained Matsubara + retained 7/8 + retained_bounded spatial BC | none (algebraic) |
| (b) | EWSB order param = local bosonic CPT-even bilinear = `log\|det\|` curvature | bosonic-bilinear selector + observable principle | A-W-B (P1 scalar additivity admission) |
| (c) | Physical EWSB curvature is Klein-four invariant | CPT-even phase blindness on staggered D | A-W-C (CPT-even phase blindness admission) |
| (d) | Therefore physical EWSB temporal block = L_t = 4 | (a) ∧ (b) ∧ (c); staggered block IS physical substrate | A-W-A (staggered-Dirac realization gate) |

The checked proof-walk **does not** add any new axiom, any new
repo-wide theory class, or any retained status claim. It does
not retire any of the three admission walls.

## 6. Forbidden imports check

- **NO** new framework axioms (A1, A2 only).
- **NO** PDG observed values consumed as derivation inputs.
- **NO** fitted matching coefficients.
- **NO** new repo vocabulary. Terms used (`Klein-four`,
  `APBC temporal circle`, `staggered Dirac`, `bilinear`,
  `EWSB`, `effective potential`, `CPT-even`,
  `scalar additivity`) are all standard physics / repo-canonical
  vocabulary.
- **NO** new tags. The note is positioned as a `bounded_theorem`
  proof-walk in the proof-walk-bounded-note family that has
  already landed (hypercharge, SU(5), LH-doublet eigenvalue
  ratio, anomaly cancellation, hypercharge etc.).

## 7. Load-bearing step class

The load-bearing step is **class B (bounded reframing)**: it
recasts the algebraic Klein-four orbit result (retained) into the
conditional physical-selection statement by walking the four
bridge steps and isolating the three admission walls. The
algebraic content is class A (already retained / retained-bounded
upstream); the bridge to "physical" is class B with the three
named admissions.

## 8. What this bounded theorem supports

- An **explicit catalogue** of the three admission walls between
  the retained algebraic L_t = 4 result and the physical EWSB
  temporal-block claim used by the v formula
  `v = M_Pl × α_LM^16 × (7/8)^(1/4)`.
- A **conditional load-bearing statement** that downstream rows
  citing the L_t = 4 selection can use to inherit the three
  admission walls explicitly rather than implicitly.
- **Audit-tractable narrowing**: the (BA-5) electroweak hierarchy
  baseline admission used by the v formula is now decomposed into
  three named open authorities (A-W-A staggered gate, A-W-B
  scalar-additivity P1, A-W-C CPT-even phase-blindness), each of
  which has an existing audit row.

## 9. What this theorem does NOT close

- **Unconditional retirement of A-W-A.** Closure of the
  staggered-Dirac realization gate from A1+A2 is the explicit
  open-gate identity carried by
  [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md);
  it is not retired here.
- **Unconditional retirement of A-W-B.** Derivation of scalar
  additivity P1 on independent subsystems from A1+A2 is the
  audit-named repair target for
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md);
  it is not retired here.
- **Unconditional retirement of A-W-C.** Retention of CPT-even
  phase blindness from a CPT primitive is downstream of
  [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) (unaudited) and
  [`CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`](CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md)
  (unaudited); it is not retired here.
- **The v formula closure.** The full chain
  `v = M_Pl × α_LM^16 × (7/8)^(1/4)` includes `M_Pl` closure,
  `α_LM^16` closure, and the `(1/4)` outer-exponent closure
  (downstream of [`HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md));
  none of those is in scope here.

## 10. Verification (runner)

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_lt4_physical_selection_proof_walk.py
```

The runner verifies (class A / pure algebra):

1. **T1.** On `L_t = 4`, the APBC phase set under the Klein-four
   action `z → z, −z, z*, −z*` is one orbit of size 4
   (recomputed via `cmath` on the explicit phase list, independent
   of the cited authority).
2. **T2.** On `L_t = 2`, the APBC phase set is one orbit of size 2
   (the unresolved `{+i, −i}` sign pair, no resolved orbit).
3. **T3.** On `L_t ∈ {6, 8}`, the APBC phase set splits into
   multiple Klein-four orbit sectors.
4. **T4.** `sin²((2n + 1)π/4) = 1/2` for all `n ∈ {0, 1, 2, 3}`
   (uniform temporal weight at `L_t = 4`).
5. **T5.** `sin²((2n + 1)π/6)` takes values `{1/4, 1, 1/4, 1/4, 1, 1/4}`
   (non-uniform at `L_t = 6`).
6. **T6.** Admission-wall catalogue: the proof-walk has exactly
   three admission walls A-W-A, A-W-B, A-W-C, each tied to a
   specific upstream authority row with the named effective
   status. The runner reads the live ledger
   (`docs/audit/data/audit_ledger.json`) and reports each row's
   current `effective_status` so the conditional shape is
   ledger-checked at runtime.
7. **T7.** Forbidden-imports check: the runner re-derives T1-T5
   from `cmath` / `math` only, with **no** import of PDG values,
   `M_Pl`, `α_LM`, `u_0`, or any framework numerical constant.

Target PASS = 7, FAIL = 0.

## 11. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Conditional proof-walk of the L_t = 4 physical-selection step
  on the staggered-Dirac APBC temporal circle. Bridges the
  retained algebraic Klein-four orbit theorem at L_t = 4 to the
  physical EWSB temporal block via the four-step chain
  (a) Klein-four orbit (algebraic) -> (b) EWSB order param =
  log|det| curvature (admission A-W-B) -> (c) Klein-four
  invariance of EWSB sector (admission A-W-C) -> (d) physical
  EWSB temporal block = L_t = 4 (admission A-W-A). The three
  admissions are A-W-A (staggered-Dirac realization gate,
  open_gate; staggered_dirac_realization_gate_note_2026-05-03),
  A-W-B (scalar-additivity P1 on independent subsystems,
  audited_conditional; observable_principle_from_axiom_note),
  and A-W-C (CPT-even phase blindness, unaudited;
  cpt_exact_note / cpt_exact_real_anti_hermitian_d_narrow_theorem_note_2026-05-10).
  The unconditional retirement of any of A-W-A, A-W-B, A-W-C
  from A1 (Cl(3) local algebra) + A2 (Z^3 spatial substrate) is
  not closed by this note. The bounded conditional shape is the
  load-bearing claim.
proposed_load_bearing_step_class: B
status_authority: independent audit lane only

declared_one_hop_deps:
  - hierarchy_matsubara_decomposition_note
  - hierarchy_seven_eighths_riemann_dirichlet_dimensional_anchor_narrow_theorem_note_2026-05-10
  - hierarchy_spatial_bc_and_u0_scaling_note
  - hierarchy_bosonic_bilinear_selector_note
  - observable_principle_from_axiom_note
  - cpt_exact_note
  - cpt_exact_real_anti_hermitian_d_narrow_theorem_note_2026-05-10
  - staggered_dirac_realization_gate_note_2026-05-03
  - minimal_axioms_2026-05-03

admitted_context_inputs:
  - A-W-A staggered-Dirac realization gate (open_gate; canonical
    parent: staggered_dirac_realization_gate_note_2026-05-03)
  - A-W-B scalar-additivity P1 on independent subsystems
    (audited_conditional; canonical parent:
    observable_principle_from_axiom_note)
  - A-W-C CPT-even phase blindness (unaudited; canonical parent:
    cpt_exact_note / cpt_exact_real_anti_hermitian_d_narrow_theorem_note_2026-05-10)

forbidden_imports_used: false
proposal_allowed: true
audit_required_before_effective_status_change: true
```

## 12. Cross-references

### Algebraic upstream (retained / retained-bounded)
- [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md)
  — retained (positive_theorem); exact Matsubara determinant
  closed form on `L_s = 2`.
- [`HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md)
  — retained (positive_theorem); triple coincidence at `d = 4`
  yielding `7/8` and `sin² = 1/2` uniformity at `L_t = 4`.
- [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)
  — retained_bounded; finite intensive 3+1 limit forces spatial
  APBC at `L_s = 2`.

### Algebraic upstream (currently unaudited; not load-bearing here)
- [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
  — unaudited (bounded_theorem); algebraic Klein-four orbit
  decomposition statement. The present proof-walk recomputes its
  algebraic content T1-T5 from primitives, so its retained status
  is not load-bearing.

### Admission-wall authorities
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — open_gate; A-W-A canonical parent.
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — audited_conditional; A-W-B canonical parent (P1 scalar
  additivity admission named in audit verdict).
- [`OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md`](OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md)
  — meta; records the audit verdict naming P1.
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
  — unaudited; A-W-C canonical parent.
- [`CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`](CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md)
  — unaudited; A-W-C narrow specialization.
- [`AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`](AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md)
  — audited_conditional; A-W-C older route.

### Framework axiom set
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  — meta; current A1 + A2 axiom set.

### Downstream chain (relational, not load-bearing here)
- [`HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md)
  — unaudited (bounded_theorem); handles the `(1/4)` outer
  exponent question; not consumed here.
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
  — full `v = M_Pl × α_LM^16 × (7/8)^(1/4)` chain; not closed by
  this note.

## 13. Sister proof-walk-bounded-note templates

Mirroring the layout of:

- [`HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md`](HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md)
- [`LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md`](LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md)
- [`SU3_CASIMIR_FUNDAMENTAL_ALGEBRAIC_K1_K3_NARROW_PROOF_WALK_BOUNDED_NOTE_2026-05-10.md`](SU3_CASIMIR_FUNDAMENTAL_ALGEBRAIC_K1_K3_NARROW_PROOF_WALK_BOUNDED_NOTE_2026-05-10.md)
- [`GBARE_WILSON_ACTION_INTERNAL_PROOF_WALK_BOUNDED_NOTE_2026-05-08.md`](GBARE_WILSON_ACTION_INTERNAL_PROOF_WALK_BOUNDED_NOTE_2026-05-08.md)

This note differs from those in that it isolates **three named
admission walls** rather than testifying lattice-independence:
the conditional shape is the load-bearing content. The proof-walk
catalogue in §5 is in the same style as the proof-walk catalogue
in the LH-doublet ratio note's §"Proof-Walk".

## 14. Counterfactual Pass record (audit transparency)

Per `feedback_run_counterfactual_before_compute`, the assumptions
were exercised before authoring:

1. **"The algebraic L_t = 4 result already closes the physical
   selection."** — negated: the algebraic content lives on the
   staggered-Dirac block, which is an open gate
   (staggered_dirac_realization_gate_note_2026-05-03). Without
   that gate closing, "the staggered block IS the physical EW
   substrate" is an admission (A-W-A), not a derivation.
2. **"The bosonic-bilinear selector note itself closes T1."** —
   negated: the selector note (currently `unaudited`) admits a
   continuum effective-action identification of the EWSB order
   parameter. The bridge to `log|det|` curvature passes through
   `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE`, which is
   `audited_conditional` on P1 (A-W-B).
3. **"CPT-even phase blindness is automatic from `CPT_EXACT_NOTE`."**
   — negated: `CPT_EXACT_NOTE` is `unaudited`; the
   `CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10`
   specialization is `unaudited`; the
   `AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29` route is
   `audited_conditional`. CPT-even phase blindness on the
   staggered block therefore remains an admission (A-W-C).
4. **"A new physical-selection axiom is required."** — negated:
   the present note does NOT add a new axiom. Instead, it
   isolates the three existing admissions (A-W-A, A-W-B, A-W-C)
   already named in the audit ledger and walks the four-step
   bridge chain conditionally. The conditional load-bearing
   statement is `bounded_theorem`-class.
5. **"The proof-walk introduces new repo vocabulary."** — negated:
   the walls are named A-W-A / A-W-B / A-W-C and tied to the
   existing audit-row identifiers (`staggered_dirac_realization_gate_note_2026-05-03`,
   `observable_principle_from_axiom_note`, `cpt_exact_note`). No
   new tags or class labels introduced. The pattern mirrors the
   existing proof-walk-bounded-note family.

The counterfactual exercise confirmed the result as a class (B)
bounded conditional proof-walk with three named admission walls,
none of which is retired here.

## 15. Author tone and audit boundary

This note is a conditional proof-walk. It walks the existing four-
step bridge chain from the retained algebraic L_t = 4 result on the
staggered block to the physical EWSB temporal block, isolates the
three admission walls A-W-A / A-W-B / A-W-C, and states the
conditional closure. It does not retire any of the three walls. It
does not promote any cited authority. The audit lane is the
authority on effective status; this proposal merely contributes a
class-B bounded conditional row whose load-bearing chain is the
admission-wall catalogue plus the conditional closure statement.
