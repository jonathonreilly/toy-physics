# Lane Promotion Proposal — Koide-Brannen Phase `δ = 2/9` (Mixed-Layer)

**Date:** 2026-05-07
**Type:** lane promotion source proposal — mixed verdict (mostly bridge-independent)
**Authority role:** source-note proposal. Audit verdict and lane status are
set only by the independent audit lane.
**Parent unified status:** [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
**Lane register:** [`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`](../../docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)

---

## 0. Executive summary

The Koide-Brannen lane decomposes cleanly into **three semantic layers**, of
which **two are bridge-independent** and **one is bridge-conditional**.
The unified-bridge-status table at
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
listed "Koide-Brannen phase" as one of the four bridge-dependent lanes ready
for bounded-theorem promotion under all three admissions
(`N_F = 1/2`, Convention C-iso, continuum-equivalence parsimony) at ~10%
relative bound. **That blanket characterization is too coarse and slightly
miscredits this lane to the bridge.** Re-examined against the actual
load-bearing chain, only the third layer (physical-bridge CH-descent
support) genuinely consumes any bridge admission.

| Layer | Claim | Bridge dependence | Audit verdict |
|---|---|---|---|
| **L-A: Dimensionless phase formula** | `δ = n_eff/d² = Q/d = 2/9` | **NONE** | bridge-independence note (closed under `Q = 2/3` only) |
| **L-B: CH-three-gap closure (Berry = CH descent)** | Gap 1, Gap 2 (`Ω = 1`), Gap 3 (operator chain) | Gap 2 partially touches the bridge surface | bounded refinement; bridge-bound is structurally negligible at this layer |
| **L-C: Wilson-Dirac finite-lattice support** | Per-fixed-site `η = 2/9` recurrence on `L = 3` cubic carrier | Wilson-action form is the carrier | bounded_theorem promotion under all three admissions; ~10% relative bound |

The headline result of this proposal:

> **The dimensionless Brannen phase formula `δ = 2/9` is bridge-independent.**
> The Brannen-PDG numerical match (`<0.1%`) is a comparison of a derived
> rational against a measured dimensionless quantity; no admitted scalar,
> dictionary convention, or lattice-action choice enters. The lane's open
> bridge is the **radian postulate `P`** (dimensionless `2/9` → `2/9 rad`),
> which is structurally orthogonal to the four `UNIFIED_BRIDGE_STATUS_2026_05_07`
> bridge admissions.

The CH-three-gap closure (per project memory, 2026-04-22) closed the
Berry = CH-descent identification with `Ω = 1` derived by Fubini
integration of `∫F_Y ∧ F_Y / (8π²)` over a minimum-winding 4-tube on
the retained `Z³ × R` lattice. **That integral is invariant under the
bridge admissions** in the sense that re-routing through Wilson vs
heat-kernel vs Manton plaquettes preserves the rational topological
result `Ω = n_⊥ · n_∥ = 1`. The Wilson-Dirac `L = 3` lattice support
(layer L-C) does carry the bridge-admission cost, but it is **support
science**, not load-bearing for the dimensionless `δ = 2/9` claim.

This proposal therefore lands as a **bridge-independence note for the
headline dimensionless claim** plus a **bounded-theorem promotion for
the support layer**, *not* a uniform bounded-theorem promotion of the
whole lane.

---

## 1. Lane summary

### 1.1 What the lane claims

The charged-lepton Koide phase `δ = 2/9` is a dimensionless number that
appears in the Brannen mass relation
([`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)).
The three layers above provide:

- **L-A (representation-theoretic derivation):** `δ` follows uniquely from
  doublet conjugate-pair charge `n_eff = 2` and `|C_3| = d = 3`, giving
  `δ = n_eff/d² = Q/d = 2/9` once `Q = 2/3` is in hand
  ([`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  §1-2).
- **L-B (Berry = CH descent identification):** the selected-line CP¹
  Berry phase equals the descended Callan-Harvey anomaly inflow phase
  on `Z³ × R`, with the descent normalization `Ω = 1` derived by
  Fubini integration of `∫F_Y ∧ F_Y / (8π²)` over the minimum-winding
  4-tube (per [`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md)
  + project memory `Brannen CH three-gap closure`, 2026-04-22, runner
  16/16 PASS).
- **L-C (Wilson-Dirac finite-lattice illustration):** per-fixed-site
  `η = 2/9` recurs at discrete Wilson-parameter plateaus on the
  physical `L = 3` `Z₃`-equivariant Wilson-Dirac carrier
  ([`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
  §3).

### 1.2 What lies upstream (out of scope for this proposal)

`Q = 2/3` (the Koide ratio source-side gap, "I1") is **not** part of this
lane's bridge interaction. Its current state is documented in
[`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`](../../docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)
§0. Closing I1 propagates to L-A automatically via `δ = Q/d`. Whether
the I1 closure path itself touches the four bridge admissions is the
subject of a separate lane proposal (the `Q = 2/3` source-law lane,
not promoted here).

### 1.3 What lies downstream (out of scope for this proposal)

The selected-line ratio `w/v ≈ 4.101` (the lepton mass-ratio numerical
output) is conditional on closing the radian-bridge postulate `P`
(dimensionless `2/9` → `2/9 rad`). That postulate's status is
documented in
[`KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md`](../../docs/KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md)
and the no-go in
[`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](../../docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md).
It is **not** one of the four `UNIFIED_BRIDGE_STATUS_2026_05_07` admissions.

---

## 2. Pre-promotion state (per audit ledger and `UNIFIED_BRIDGE_STATUS_2026_05_07`)

| Component | Pre-promotion ledger / unified-status | Pre-promotion runner |
|---|---|---|
| L-A Phase reduction theorem | `bounded` (conditional on `Q = 2/3` = I1) | [`scripts/frontier_koide_brannen_phase_reduction_theorem.py`](../../scripts/frontier_koide_brannen_phase_reduction_theorem.py) PASS |
| L-A Berry holonomy theorem | `proposed_retained, audited_conditional` | [`scripts/frontier_koide_berry_phase_theorem.py`](../../scripts/frontier_koide_berry_phase_theorem.py) 24/0 PASS |
| L-B CH three-gap closure (memory only) | per memory: closed at runner 16/16; **note `KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md` not in current worktree** (memory may reference state from an earlier branch; verify before citing as load-bearing on this branch) | [`scripts/frontier_koide_brannen_ch_three_gap_closure.py`](../../scripts/frontier_koide_brannen_ch_three_gap_closure.py) (per memory; not verified live this session) |
| L-B CH candidate (without three-gap closure) | bridge-conditioned support candidate | [`scripts/frontier_koide_brannen_callan_harvey_candidate.py`](../../scripts/frontier_koide_brannen_callan_harvey_candidate.py) PASS |
| L-C Wilson-Dirac support | support-grade finite-lattice illustration | [`scripts/frontier_koide_brannen_dirac_support.py`](../../scripts/frontier_koide_brannen_dirac_support.py) PASS |
| Lane status (unified) | listed as bridge-dependent in [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md) §"Lane unlock" table; "all 3 admissions apply; total ~10% relative bound" | — |

The `UNIFIED_BRIDGE_STATUS_2026_05_07` characterization
("Koide-Brannen phase: all 3 admissions apply; total ~10% relative bound")
applies cleanly to **L-C** (Wilson-Dirac support), **partially** to
**L-B** (Gap 2's curvature integral), and **not at all** to **L-A**
(the dimensionless phase formula). The current proposal sharpens the
unified-status row accordingly.

---

## 3. Proposed claim — split by layer

### 3.1 Layer L-A: Bridge-Independence Note for `δ = n_eff/d² = 2/9`

**Claim type:** `bridge_independence` (no promotion needed; the claim
is already a `bounded` representation-theoretic theorem at
[`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
conditional only on `Q = 2/3`).

**Statement:** The dimensionless equality `δ = n_eff/d² = 2/9` is a
representation-theoretic identity derived from
- the C_3 = Z/3Z permutation action on C³ (forced by `Cl(3)`'s C₃
  cyclic generation symmetry retained on the framework's symmetric
  base, [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md));
- the doublet conjugate-pair structure `L_ω̄ = conj(L_ω)`, which forces
  projective doublet phase to advance at rate `n_eff = 2` per unit
  `θ`-rotation (forced, no choice — proved in
  [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  §1.3);
- the Brannen normalization `δ_per_step = |Δ(arg ζ)|/(2π · d) = n_eff/d²`.

**None of the four `UNIFIED_BRIDGE_STATUS_2026_05_07` admissions enters
this chain.** Specifically:
- `N_F = 1/2` (canonical Gell-Mann trace normalization) does not
  appear: the chain uses no `Tr(T_a T_b)` or Casimir value.
- Convention C-iso (Hamilton-Lagrangian dictionary isotropic reduction)
  does not appear: the chain does no Trotterization, no temporal-vs-
  spatial plaquette routing, no `g²/2` ↔ `β` conversion.
- Continuum-equivalence parsimony (Wilson vs heat-kernel vs Manton
  plaquette form) does not appear: the chain does no plaquette
  observable, no curvature integral, no character expansion.

The single open dependency is `Q = 2/3` (I1, separate lane).

**Audit ask (L-A only):** the audit lane should reclassify the
unified-status row's "Koide-Brannen phase" entry from "all 3 admissions
apply" to "bridge-independent at headline dimensionless layer; bridge
admissions enter only at Wilson-Dirac support layer (L-C) and partially
at Gap 2 of the CH-bridge identification (L-B)".

### 3.2 Layer L-B: CH-Three-Gap Closure (bounded refinement)

**Claim type:** `bounded_theorem` candidate (per project memory, 2026-04-22,
runner 16/16 PASS).

**Statement (per memory):** The selected-line CP¹ Berry phase equals
the descended Callan-Harvey anomaly inflow phase on `Z³ × R`, via
- Gap 1 (identification): two evaluations of the same defect zero-mode
  Pancharatnam-Berry holonomy on the CP¹ carrier.
- Gap 2 (descent factor): `Ω = 2 · n_⊥ · n_∥ · (2π)² / (8π²) = n_⊥ ·
  n_∥ = 1` by Fubini integration over the minimum-winding 4-tube on
  retained `Z³ × R`, with `n_⊥ = n_∥ = 1` as the minimum-nonzero
  Dirac-quantized choice.
- Gap 3 (operator map): `J^μ_Y → Q_Σ → CP¹ tautological Berry
  connection` chain, with projective winding rate `d(arg ζ)/dθ =
  -n_eff = -2` verified.

**Bridge dependence:** Gap 2's `∫F_Y ∧ F_Y / (8π²)` curvature integral
formally lives on the Wilson-action surface (the `F` here is the
emergent gauge curvature on the spatial substrate, whose coefficient
in the full action is fixed by L4 of the four-layer stratification at
[`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)).

However, Gap 2's **conclusion** is a rational topological winding
number `n_⊥ · n_∥ = 1`. Re-routing the curvature integrand through
heat-kernel or Manton plaquettes (instead of Wilson) does not change
this rational result — the curvature 2-form `F` and its differential
`d(F ∧ F)` are continuum-level objects whose integral over a closed
4-cycle is preserved across the continuum-equivalence class
([`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md), `Tr(F²)` form
forced at continuum level). The N_F admission likewise does not enter
the rational result — `N_F` rescales `Tr(T_a T_b)` but the topological
winding number is independent of the Killing-form scalar.

**Net bridge-bound at L-B:** structurally negligible (the rational
`Ω = 1` is invariant under all three admissions).

**Caveat about memory currency:** The CH-three-gap-closure runner and
note are referenced in project memory (2026-04-22) but the specific
file `KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md` is not in
the current worktree. The L-B claim above should be treated as
conditional on independent verification of the runner state on this
branch. If the closure has been demoted or unwound on `main` since
the memory date, this proposal's L-B claims need re-statement.

**Audit ask (L-B only):** verify the runner
[`scripts/frontier_koide_brannen_ch_three_gap_closure.py`](../../scripts/frontier_koide_brannen_ch_three_gap_closure.py)
exists and passes at 16/16 on `main`. If yes, retain L-B as a
`bounded_theorem` with structurally-negligible bridge-bound. If no,
treat L-B as the candidate-tier
[`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md)
classifies it (bridge-conditioned support candidate, not closure).

### 3.3 Layer L-C: Wilson-Dirac Finite-Lattice Support (bounded promotion)

**Claim type:** `bounded_theorem` (promoted from prior `support`-grade
finite-lattice illustration).

**Statement:** On the explicit Euclidean Hermitian Z₃-equivariant
Wilson-Dirac operator on the `3 × 3 × 3` cubic lattice, per-fixed-site
`η = 2/9` recurs at discrete Wilson-parameter plateaus, with exact
symbolic ABSS evaluation `η = 2/9`
([`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
§3).

**Bridge dependence (full):** All three `UNIFIED_BRIDGE_STATUS_2026_05_07`
admissions enter:
- The Wilson-Dirac operator's coefficient structure is `Wilson` (not
  heat-kernel or Manton) — this is the continuum-equivalence-class
  parsimony admission.
- The Hamilton-Lagrangian identification of the lattice operator with
  the framework's Hamiltonian Wilson-Dirac uses the isotropic
  reduction at `a_τ = a_s` (Convention C-iso).
- The trace structure `Tr(T_a T_b) = δ_ab/2` underlies the Dirac
  operator's Cl(3)-bilinear normalization (`N_F = 1/2`).

**Quantitative bound:** ~10% relative (per the joint bound at
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
§"Joint bound on framework's Wilson-target prediction").

**However:** this layer is **support-grade illustration**, not
load-bearing for the dimensionless `δ = 2/9` claim (L-A). Even at full
~10% bridge bound, the headline rational `2/9` survives because L-A is
already independent. The promotion of L-C to `bounded_theorem` is
about cleaning up the support-stack ledger, not unlocking the lane.

**Audit ask (L-C only):** promote
[`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
from `support`-grade to `bounded_theorem` with explicit
admitted_context_inputs (below).

---

## 4. `admitted_context_inputs` — applies to L-C only (not L-A or L-B)

```yaml
admitted_context_inputs:
  - id: N_F_canonical_normalization
    statement: "N_F = 1/2 canonical Gell-Mann trace normalization"
    parent: G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md
    applies_to: L-C (Wilson-Dirac finite-lattice support)
    does_not_apply_to: [L-A dimensionless phase formula, L-B CH descent rational]
    reason: |
      L-A uses no Tr(T_a T_b) or Casimir value; the chain is
      pure-representation-theoretic in Cl(3)/C_3. L-B's conclusion
      is a rational topological winding number n_⊥·n_∥ = 1, which
      is independent of the Killing-form scalar.

  - id: Convention_C_iso_dictionary
    statement: "Hamilton-Lagrangian isotropic reduction at a_τ = a_s"
    parent: DICTIONARY_DERIVED_THEOREM.md
    bound: O(g²) ~ 5-15%
    applies_to: L-C (Wilson-Dirac finite-lattice operator identification)
    does_not_apply_to: [L-A dimensionless phase formula, L-B CH descent rational]
    reason: |
      L-A does no Trotterization; L-B's curvature-integral conclusion
      is invariant under continuum-equivalence routing.

  - id: continuum_equivalence_parsimony
    statement: "lattice action selection within continuum-equivalence class"
    parent: A2_5_DERIVED_THEOREM.md
    bound: ~5-10%
    applies_to: L-C (Wilson-Dirac operator form vs heat-kernel/Manton alternatives)
    does_not_apply_to: [L-A dimensionless phase formula, L-B CH descent rational]
    reason: |
      L-A is plaquette-free; L-B's `∫F_Y ∧ F_Y / (8π²)` is invariant
      under continuum-equivalence-class routing (the integrand at
      continuum is uniquely Tr(F²)).
```

**Joint bound (L-C only):** ~10% relative, per
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
§"Joint bound" (action-form parsimony + Convention C-iso, with N_F as
separately-named admitted scalar).

**Joint bound (L-A and L-B):** zero (or structurally negligible). The
headline dimensionless `δ = 2/9` claim is invariant under all three
admissions; the rational `Ω = 1` in CH-Gap-2 is invariant under all
three admissions.

---

## 5. Quantitative uncertainty

### 5.1 Headline dimensionless claim (L-A)

`δ = 2/9 ≈ 0.222` is an exact rational. The Brannen-PDG numerical
match
- Brannen value: `δ = 2/9 = 0.22222...`
- PDG charged-lepton mass-ratio fit: matches `2/9` at `<0.1%` precision
  (per [`KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md`](../../docs/KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md)
  §0).

**Bridge admission contribution to L-A uncertainty: 0.** The match is
between an exact rational and a measured dimensionless ratio. No
admitted scalar enters either side of the comparison.

### 5.2 CH descent factor (L-B)

`Ω = 1` is an exact rational integer. The contribution to `δ` is the
**multiplier** `Ω · (2/9) = 2/9`. **Bridge admission contribution to
L-B uncertainty: 0** (rational topological invariant).

### 5.3 Wilson-Dirac plateau (L-C)

The per-fixed-site `η` plateau on `L = 3` is centered at `2/9` with
plateau width set by the Wilson-Dirac parameter window. **Bridge
admission contribution to L-C uncertainty: ~10% relative** on the
plateau center and ~10% relative on the plateau width. The exact
symbolic ABSS evaluation `η = 2/9` at the plateau center is preserved
under the admissions because the symbolic evaluation does not require
finite-β Wilson vs heat-kernel discrimination.

**Net:** on the headline `δ = 2/9` claim, post-promotion uncertainty
is **0** (exact rational from L-A); the ~10% bridge bound applies only
to L-C's status as a "Wilson-Dirac realization of the same value",
which is illustrative rather than load-bearing.

---

## 6. What this promotion closes — and what it does not

### 6.1 What it closes

- Sharpens the [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
  §"Lane unlock" row for "Koide-Brannen phase" from
  "all 3 admissions apply; total ~10% relative bound" to
  "bridge-independent at headline; admissions apply only to L-C
  finite-lattice support".
- Promotes L-C
  ([`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md))
  from `support`-grade to `bounded_theorem` with named admissions.
- Documents that L-A
  ([`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md))
  is a **bridge-independence note**, not a bridge-conditional bounded
  theorem — the chain is pure representation theory.
- Documents L-B's bridge-bound as structurally negligible (rational
  topological invariant).

### 6.2 What it does NOT close

- The radian-bridge postulate `P` (dimensionless `2/9` → `2/9 rad`)
  remains open; this is **structurally orthogonal** to the four
  `UNIFIED_BRIDGE_STATUS_2026_05_07` bridge admissions and is tracked
  as the named live residual in
  [`KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md`](../../docs/KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md)
  and the no-go in
  [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](../../docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md).
- The Koide ratio `Q = 2/3` (I1) source-side gap remains open. L-A's
  closure of `δ = Q/d` is conditional on closing I1. The four bridge
  admissions are not part of I1's closure path either (separate lane
  proposal).
- The selected-line ratio `w/v ≈ 4.101` (lepton mass-ratio numerical
  prediction) is conditional on closing the radian-bridge postulate
  `P`, not on the four bridge admissions. So no lepton mass numerical
  value is downstream of the bridge admissions in this lane.
- Whether `N_F = 1/2` is uniquely forced by Cl(3) (the L3 admission's
  Nature-grade open question per
  [`G_BARE_AUDIT_RESIDUAL_CLOSURE.md`](G_BARE_AUDIT_RESIDUAL_CLOSURE.md)
  Barrier 1) — this is upstream of L-C and remains open at Nature
  grade.

### 6.3 Why this lane is mostly bridge-independent (key observation)

Of the four `UNIFIED_BRIDGE_STATUS_2026_05_07` lanes (α_s direct
Wilson loop, Higgs mass from axiom, gauge-scalar observable bridge,
Koide-Brannen phase), the Koide-Brannen phase is the one whose
**numerical headline** is a **rational from group representation
theory**, not a measurement-vs-prediction comparison on the lattice.
The other three lanes target **lattice MC observables** at finite β,
where every admission accumulates. This lane targets a dimensionless
group-theoretic identity, which is invariant under all three
admissions by construction. The blanket "all 3 admissions apply"
characterization in the unified-status table came from treating the
lane as homogeneous; the actual structure is layered, and the bridge
attaches only at the support layer (L-C).

This is consistent with the framework's broader pattern: dimensionless
rational predictions from `Cl(3)/Z³` representation theory (Koide phase,
PMNS phase, fermion generation count) are typically bridge-independent;
dimensionful predictions on the lattice (α_s at MZ, Higgs mass in GeV,
Wilson loop expectation values) are typically bridge-conditional.

---

## 7. Cross-references

### Lane notes (this proposal's load-bearing inputs)

- [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  — L-A representation-theoretic derivation of `δ = n_eff/d² = 2/9`.
- [`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md)
  — L-B candidate (per-generation anomaly coefficient `2/9`); pre-three-gap-closure form.
- [`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
  — L-C Wilson-Dirac finite-lattice support.

### Bridge admissions (`UNIFIED_BRIDGE_STATUS_2026_05_07` triple)

- [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
  — overall bridge status, four-lane unlock table.
- [`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md)
  — continuum-level action-form derived; finite-β parsimony admission.
- [`DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md)
  — Theorem T-AT (Anisotropic Trotter Dictionary); Convention C-iso
  isotropic reduction admission.
- [`G_BARE_AUDIT_RESIDUAL_CLOSURE.md`](G_BARE_AUDIT_RESIDUAL_CLOSURE.md)
  — `g_bare = 1` chain; `N_F = 1/2` admitted scalar at L3 of the
  four-layer stratification.

### Lane state register (open imports)

- [`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`](../../docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md)
  — `Q = 2/3` (I1) and `δ = 2/9` physical bridge residuals; selected-line
  witness `w/v ≈ 4.101`.
- [`KOIDE_LANE_AUDIT_BATCH_NOTE_2026-05-02.md`](../../docs/KOIDE_LANE_AUDIT_BATCH_NOTE_2026-05-02.md)
  — May 2 audit batch confirming Berry phase theorem `audited_conditional`
  status; lane has structural pattern similar to lattice→physical
  matching obstruction.
- [`KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md`](../../docs/KOIDE_DELTA_DIMENSIONLESS_CLOSURE_VIA_V8_THEOREM_NOTE_2026-04-29.md)
  — Two-layer (dimensionless / radian) decomposition of `δ`-closure;
  named radian postulate `P`.
- [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](../../docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
  — radian-bridge no-go through canonical R/Z → U(1) qubit lift.

### Project memory (cross-reference)

- `Brannen CH three-gap closure` (memory entry, 2026-04-22): closed
  Gap 1 (Berry = CH descent), Gap 2 (`Ω = 1` from `∫F_Y ∧ F_Y / (8π²)`
  Fubini integration), Gap 3 (operator chain). Runner 16/16 PASS per
  memory. **Note:** the file
  `KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md` is
  referenced in memory but is not present in this worktree; verify
  current `main` state before treating L-B as load-bearing.

---

## 8. Audit ask

The audit lane should:

### 8.1 At the unified-status row level

Reclassify the [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
§"Lane unlock" "Koide-Brannen phase" row from

> "All 3 admissions apply; total ~10% relative bound"

to

> "Bridge-independent at headline dimensionless layer (L-A representation
> theory). Bridge admissions apply only to support layer (L-C
> Wilson-Dirac finite-lattice illustration). CH-three-gap closure
> (L-B) bridge-bound is structurally negligible (rational topological
> invariant). Live residual is the radian-bridge postulate `P`, which
> is structurally orthogonal to the three bridge admissions."

### 8.2 At the layer level

- **L-A:** retain
  [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](../../docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  at its current `bounded` tier (conditional on `Q = 2/3` = I1, no
  bridge admission needed). This proposal is a documentation /
  metadata refinement of L-A's status, not a tier change.

- **L-B:** verify that the CH-three-gap-closure runner state on
  `main` matches the project-memory claim (16/16 PASS at 2026-04-22,
  with companion note
  `KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md`). If yes,
  L-B retains as `bounded_theorem` with structurally-negligible bridge
  bound. If no (file absent or unwound), L-B reverts to its 2026-04-22
  `bridge-conditioned support candidate` form per
  [`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md).

- **L-C:** promote
  [`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](../../docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
  from `support`-grade to `bounded_theorem` with the three named
  admissions per §4 above. Joint bound: ~10% relative on the plateau;
  exact symbolic ABSS evaluation at plateau center preserved.

### 8.3 Explicit non-asks

- This proposal does **not** ask the audit lane to retain or strengthen
  the radian-bridge postulate `P` beyond its current open status.
- This proposal does **not** ask the audit lane to retain `Q = 2/3`
  (I1); that is a separate lane.
- This proposal does **not** propose any new theorem; all three layers
  cite existing notes.

### 8.4 Audit dependency repair links

- [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
  §"Lane unlock" — sharpen the Koide-Brannen row.
- [`KOIDE_LANE_AUDIT_BATCH_NOTE_2026-05-02.md`](../../docs/KOIDE_LANE_AUDIT_BATCH_NOTE_2026-05-02.md)
  — corrects the May 2 audit batch's "fourth instance of the
  lattice→physical matching obstruction" cluster placement, since the
  Koide-Brannen lane's bridge dependence is layered rather than uniform.

---

## 9. Bottom line

The Koide-Brannen lane was listed as a uniformly bridge-dependent lane
in [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md).
That listing is too coarse. Re-examined layer by layer:

- **L-A (the headline `δ = 2/9` formula): bridge-independent.** Pure
  representation theory in `Cl(3)/C_3`.
- **L-B (CH-descent identification, per memory 2026-04-22): bridge bound
  structurally negligible.** Rational topological invariant.
- **L-C (Wilson-Dirac finite-lattice support): fully bridge-conditional.**
  ~10% bound on the plateau width and center; exact symbolic ABSS
  evaluation at plateau center preserved.

**The honest framing of the lane:** the dimensionless Brannen phase
formula `δ = 2/9` is a bridge-independent representation-theoretic
identity. The bridge admissions enter only when this formula is
re-realized as a Wilson-Dirac lattice plateau (L-C support science),
not when the formula itself is derived (L-A) or identified with the
Berry-equals-CH-descent chain (L-B).

The remaining live gap on this lane is the **radian-bridge postulate
`P`** (dimensionless `2/9` → `2/9 rad`), which is structurally
orthogonal to the four `UNIFIED_BRIDGE_STATUS_2026_05_07` bridge
admissions. Closing the bridge admissions does not advance the lane
toward a numerical lepton-mass prediction; the radian bridge is a
separate residual.

This proposal therefore lands as a **bridge-independence note for the
headline layer** plus a **bounded-theorem promotion for the support
layer**, **not** a uniform bounded-theorem promotion of the whole
lane. The framework's audit-honest reading of the Koide-Brannen lane
sharpens accordingly.
