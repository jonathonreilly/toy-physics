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
> Given (i) the retained algebraic inputs and the runner-rederived
> Klein-four orbit calculation on the staggered-Dirac APBC temporal circle
> ([`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md),
> retained;
> [`HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md),
> retained;
> [`HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`](HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md),
> retained_bounded), and (ii) three explicitly named admissions
> (the staggered-Dirac realization gate, scalar-additivity admission,
> and CPT phase-blindness admission), the algebraic `L_t = 4`
> selector on the staggered block IS the physical EWSB temporal
> block. The three admissions are necessary: without any one of
> them, the algebraic-to-physical bridge does not close from
> the physical Cl(3) local algebra plus Z^3 spatial substrate alone.

This bounded theorem **explicitly does NOT** claim:

- unconditional retirement of any of the three admissions from the
  physical Cl(3) local algebra plus Z^3 spatial substrate;
- closure of the framework's electroweak hierarchy formula
  `v = M_Pl × α_LM^16 × (7/8)^(1/4)` (downstream chain);
- closure of `M_Pl` or `α_LM^16` (separate authority chains);
- retirement of the open staggered-Dirac realization gate
  ([`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md));
- a positive-theorem promotion of any cited authority. The
  conditional shape — closure given the three named admissions —
  is the load-bearing content.

This note walks the existing chain step-by-step and isolates the
named admissions, without adding new content beyond making the
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
   the unique minimal **resolved** orbit of size 4; the runner
   checks the next even cases `L_t = 6, 8` as split into multiple
   orbit sectors.

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
is the four-step chain (a)-(d) below. Each step's inputs are
catalogued, and the three named admissions are isolated.

### Step (a). Klein-four orbit on the staggered block at `L_t = 4`

**Statement:** the Klein-four action `z → z, −z, z*, −z*` on the
APBC temporal phases `z_n = exp(i(2n+1)π/L_t)` has a unique minimal
**resolved** orbit at `L_t = 4`.

**Source:** items 2 + 3 of §2 above, with the finite orbit calculation
rerun by the paired verifier. This step is algebraic and closed on the
staggered-Dirac block at the checked sizes.

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
That identification is the scalar-additivity admission below.

**Admission wall invoked:**

- **Scalar-additivity / observable-class admission.**
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

- **CPT-even phase-blindness admission.** The CPT primitive
  is supplied by [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), which
  carries `effective_status = unaudited` in the live audit ledger.
  The 2026-05-10 narrow specialization
  [`CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`](CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md)
  also carries `effective_status = unaudited`, and the older
  `AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
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

- **Staggered-Dirac realization admission.** The framework baseline is
  **the physical Cl(3) local algebra plus Z^3 spatial substrate**. The
  staggered-Dirac realization on `Z³` (with APBC temporal extent
  and 8-corner doubler structure) is recorded as an **open gate**
  in
  [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  with `effective_status = open_gate`. Without closure of that
  gate, "the staggered block IS the physical EW substrate" is an
  admission, not a derivation. The Klein-four argument lives on
  the staggered block; it inherits the gate.

## 4. Conditional load-bearing statement

> Conditional on (i) the staggered-Dirac realization gate closing
> from the physical Cl(3) local algebra plus Z^3 spatial substrate,
> (ii) scalar-additivity P1 on independent subsystems forcing
> `log|det|` as the physical scalar generator, and (iii) CPT-even
> phase blindness on the staggered block being retained from a CPT
> primitive, the chain (a) → (b) → (c) → (d) in §3 closes and the
> physical EWSB temporal block is `L_t = 4`.

This is the bounded conditional shape this note targets.
**Unconditional retirement of the three admissions from the physical
Cl(3) local algebra plus Z^3 spatial substrate is not closed by this
note.** Each admission is recorded with its
existing open-gate / audited-conditional / unaudited authority
row in the live ledger.

## 5. Proof-Walk catalogue

The chain has four steps and three admissions. The proof-walk
catalogue is:

| Step | Statement | Algebra source | Admission wall? |
|---|---|---|---|
| (a) | Klein-four orbit on APBC phases, unique resolved at L_t=4 | retained Matsubara + retained 7/8 + retained_bounded spatial BC | none (algebraic) |
| (b) | EWSB order param = local bosonic CPT-even bilinear = `log\|det\|` curvature | bosonic-bilinear selector + observable principle | scalar-additivity admission |
| (c) | Physical EWSB curvature is Klein-four invariant | CPT-even phase blindness on staggered D | CPT phase-blindness admission |
| (d) | Therefore physical EWSB temporal block = L_t = 4 | (a) ∧ (b) ∧ (c); staggered block IS physical substrate | staggered-Dirac realization gate |

The checked proof-walk **does not** add any new axiom, any new
repo-wide theory class, or any retained status claim. It does
not retire any of the three admission walls.

## 6. Forbidden imports check

- **NO** new framework axioms beyond the physical Cl(3) local algebra
  plus Z^3 spatial substrate baseline.
- **NO** PDG observed values consumed as derivation inputs.
- **NO** fitted matching coefficients.
- **NO** new repo vocabulary. Terms used (`Klein-four`,
  `APBC temporal circle`, `staggered Dirac`, `bilinear`,
  `EWSB`, `effective potential`, `CPT-even`,
  `scalar additivity`) are all standard physics / repo-canonical
  vocabulary.
- **NO** new repo-wide tags. The note is positioned as a `bounded_theorem`
  proof-walk in the existing proof-walk-bounded-note family.

## 7. Load-bearing boundary

The load-bearing result is a bounded reframing: it recasts the
algebraic Klein-four orbit result into the conditional
physical-selection statement by walking the four bridge steps and
isolating the three admissions. The algebraic content is supported
by retained / retained-bounded upstream rows plus the paired finite
verifier; the bridge to "physical" remains conditional on the three
named admissions.

## 8. What this bounded theorem supports

- An **explicit catalogue** of the three admission walls between
  the retained algebraic L_t = 4 result and the physical EWSB
  temporal-block claim used by the v formula
  `v = M_Pl × α_LM^16 × (7/8)^(1/4)`.
- A **conditional load-bearing statement** that downstream rows
  citing the L_t = 4 selection can use to inherit the three
  admission walls explicitly rather than implicitly.
- **Audit-tractable narrowing**: the electroweak hierarchy
  baseline admission used by the v formula is now decomposed into
  three existing authority rows: the staggered-Dirac realization
  gate, scalar-additivity P1, and CPT-even phase blindness.

## 9. What this theorem does NOT close

- **Unconditional retirement of the staggered-Dirac realization gate.** Closure of the
  staggered-Dirac realization gate from the physical Cl(3) local algebra plus Z^3 spatial substrate is the explicit
  open-gate identity carried by
  [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md);
  it is not retired here.
- **Unconditional retirement of scalar-additivity P1.** Derivation of scalar
  additivity P1 on independent subsystems from the physical Cl(3) local algebra plus Z^3 spatial substrate is the
  audit-named repair target for
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md);
  it is not retired here.
- **Unconditional retirement of CPT-even phase blindness.** Retention of CPT-even
  phase blindness from a CPT primitive is downstream of
  [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) (unaudited) and
  [`CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`](CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md)
  (unaudited); it is not retired here.
- **The v formula closure.** The full chain
  `v = M_Pl × α_LM^16 × (7/8)^(1/4)` includes `M_Pl` closure,
  `α_LM^16` closure, and the `(1/4)` outer-exponent closure
  (downstream of `HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md`);
  none of those is in scope here.

## 10. Verification (runner)

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_lt4_physical_selection_proof_walk.py
```

The runner verifies the finite algebraic content:

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
   three admission walls, each tied to a
   specific upstream authority row with the named effective
   status. The runner reads the live ledger
   (`docs/audit/data/audit_ledger.json`) and reports each row's
   current `effective_status` so the conditional shape is
   ledger-checked at runtime.
7. **T7.** Forbidden-imports check: the runner re-derives T1-T5
   from `cmath` / `math` only, with **no** import of PDG values,
   `M_Pl`, `α_LM`, `u_0`, or any framework numerical constant.

Target PASS = 7, FAIL = 0.

## 11. Cross-references

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

### Algebraic upstream and bridge context
- [`HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md`](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
  — unaudited (bounded_theorem); algebraic Klein-four orbit
  decomposition statement. The present proof-walk recomputes its
  algebraic content T1-T5 from primitives, while its EWSB-bilinear
  identification remains part of the disclosed bridge context.

### Admission-wall authorities
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  — open_gate; staggered-Dirac realization gate authority.
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — audited_conditional; scalar-additivity P1 authority (P1 scalar
  additivity admission named in audit verdict).
- `OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md`
  — meta; records the audit verdict naming P1.
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
  — unaudited; CPT-even phase-blindness authority.
- [`CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`](CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md)
  — unaudited; CPT-even phase-blindness narrow specialization.
- `AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
  — audited_conditional; CPT-even phase-blindness older route.

### Framework axiom set
- `MINIMAL_AXIOMS_2026-05-03.md`
  — meta; records the physical Cl(3) local algebra plus Z^3 spatial
  substrate baseline.

### Downstream chain (relational, not load-bearing here)
- `HIERARCHY_HEAT_KERNEL_D4_COMPRESSION_BOUNDED_THEOREM_NOTE_2026-05-10.md`
  — unaudited (bounded_theorem); handles the `(1/4)` outer
  exponent question; not consumed here.
- `COMPLETE_PREDICTION_CHAIN_2026_04_15.md`
  — full `v = M_Pl × α_LM^16 × (7/8)^(1/4)` chain; not closed by
  this note.

## 12. Audit boundary

This note is a conditional proof-walk. It walks the existing four-
step bridge chain from the retained algebraic L_t = 4 result on the
staggered block to the physical EWSB temporal block, isolates the
three disclosed admissions, and states the
conditional closure. It does not retire any of the three walls. It
does not promote any cited authority. The audit lane is the
authority on effective status; this proposal merely contributes a
bounded conditional row whose load-bearing chain is the
admission catalogue plus the conditional closure statement.
