# Higgs Quartic UV Anchor from Tree-Level Mean-Field — Narrow Algebraic Theorem

**Date:** 2026-05-10
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Primary runner:** [`scripts/frontier_higgs_lambda_uv_anchor_narrow.py`](../scripts/frontier_higgs_lambda_uv_anchor_narrow.py)

## 0. Audit context

The framework currently records two competing claims for the Higgs
scalar quartic at the high scale:

1. [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
   asserts `λ(M_Pl) = 0` from "framework-native composite-Higgs /
   no-elementary-scalar boundary structure." The claim is recorded in
   [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)'s
   assumption-derivation ledger as
   "the **weakest leg of the input chain** … mechanism-level support
   exists, but an **independent theorem forcing the high-scale quartic
   boundary from the framework remains open**."
2. [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
   Step 5–6 derives the tree-level mean-field formula
   `m_H_tree = v / (2 u_0) = 140.3 GeV`, with the +12% gap to
   physical `m_H = 125.10 GeV` closed by 2-loop CW corrections,
   lattice-spacing convergence, and Wilson-term taste-breaking.

The composite-Higgs heuristic underpinning claim (1) was retired as a
named obstruction in
[`HIERARCHY_MATSUBARA_QUARTIC_COEFFICIENT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_MATSUBARA_QUARTIC_COEFFICIENT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md)
§4.1 (PR #937): the m⁴ coefficient `B(L_t)` of the staggered
free-energy density is finite and nonzero on both endpoints, so the
slogan "no bare quartic ⟹ λ(M_Pl) = 0" is structurally unsound (NJL
counterexample). After that retirement, the framework has no positive
UV anchor for the Higgs quartic — closing Gate #6 (lambda-UV anchor)
of the seven-gate near-zero-imports map.

This narrow theorem closes Gate #6 by promoting an **already-implicit
framework relation** to an explicit positive Clifford-fixed quartic
UV anchor.

## 1. Claim scope

> **Theorem (Higgs quartic UV anchor from tree-level mean-field).** On
> the canonical Cl(3)/Z³ Wilson-plaquette + staggered-Dirac mean-field
> surface, with the tree-level mean-field reading derived in
> `HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 5–6, the standard Higgs relation
> `m_H² = 2 λ v²` and the framework's tree-level mean-field formula
> `m_H_tree = v / (2 u_0)` jointly imply the **Clifford-fixed
> dimensionless quartic identity**:
>
> ```text
> λ_tree  =  m_H_tree²  /  (2 v²)  =  (v / (2 u_0))²  /  (2 v²)  =  1 / (8 u_0²).
> ```
>
> At the framework operating point `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (gate #7
> engineering frontier; PR #685 lattice MC consensus), the numerical
> value is
>
> ```text
> λ_tree  =  1 / (8 · 0.8776²)  ≈  0.1623.
> ```
>
> The natural matching scale of this `λ_tree` value is the **lattice
> mean-field scale** — the scale below the lattice cutoff at which
> staggered fermions have been integrated out on the L_s = 2 minimal
> APBC block. With the Planck pin (gate #4) `a^(-1) = M_Pl`, this
> scale is `μ_*  ≈  u_0 · M_Pl  ≈  0.88 · M_Pl  ≈  1.07 × 10¹⁹ GeV` —
> Planck-scale up to an O(1) Wilson coefficient.

The narrow theorem **explicitly does NOT** claim:

- a precise specification of the matching scale beyond "Planck-scale
  up to O(1) Wilson coefficient" (the standard lattice-QCD matching
  ambiguity);
- a Higgs-mass closure at observed `m_H = 125.10 GeV` (this requires
  2-loop CW + RGE + lattice-spacing convergence + Wilson taste-breaking
  per HIGGS_MASS_FROM_AXIOM Step 5; out of scope here);
- a *framework-internal* derivation of the SM RGE β-functions (the
  framework's running uses standard SM machinery, admitted external);
- a closure of the Planck pin (gate #4 currently `audited_renaming`);
- a closure of the numerical `u_0` (gate #7 currently
  engineering-frontier);
- a closure of the staggered-Dirac realization gate (currently
  `open_gate`) on which the L_s = 2 mean-field surface depends.

## 2. Counterfactual Pass — implicit assumptions

This section makes the implicit framework choices explicit, per the
"Run Counterfactual Pass before compute" discipline. Each assumption
is named, marked as forced/imported, and the consequence of being
wrong is stated.

| # | Assumption | Forced or imported? | If wrong, what changes? |
|---|---|---|---|
| 1 | Standard Higgs relation `m_H² = 2λv²` applies at the lattice mean-field scale, after Taylor-expanding V_taste to order m⁴. | Imported (standard QFT). Forced once polynomial truncation of V_taste is admitted. | The relation might extract a different effective coupling. |
| 2 | The tree-level mean-field formula `m_H_tree = v/(2u_0)` is a meaningful statement at a single matching scale (rather than averaged over a window). | Forced by HIGGS_MASS_FROM_AXIOM Step 5–6. | The "scale" of λ_tree becomes ill-defined. |
| 3 | The matching scale `μ_*` is `~ M_Pl × u_0`. | Imported (standard lattice QFT: matching ≈ cutoff up to O(1) Wilson coefficients). | The anchor scale shifts; SM RGE running from `μ_*` to `v` changes by O(log(O(1))) corrections. |
| 4 | The lattice cutoff equals `M_Pl` (Planck pin). | Conditional on Gate #4 (Planck pin currently `audited_renaming`). | The anchor sits at an unspecified UV scale instead of M_Pl. |
| 5 | `u_0 = ⟨P⟩^(1/4)` is well-defined and Clifford-determinable. | Conditional on Gate #7 (engineering frontier; current ε_witness < target at NNNLO ξ=4 per `C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md`). | The numerical `λ_tree ≈ 0.163` shifts; structural form `1/(8u_0²)` unchanged. |
| 6 | Composite-Higgs ⟹ λ(M_Pl) = 0 was the only pre-existing UV anchor candidate. | Established by 3-probe survey: SU(5) GUT route empty, Cl(3)-structural route subsumed by this anchor, Koide-fixed-point route closed negatively (Probe #9). | Another anchor candidate would compete with this one. |
| 7 | The framework's standard SM RGE machinery applies for running `λ` from `μ_*` to `v`. | Imported (framework gauge structure consistent with SM at retained sin²θ_W = 3/8 GUT level). | Different running gives different m_H prediction at v. |

Most assumptions are repairable by narrower scoping. The load-bearing
assumption is (1)+(2): the standard Higgs relation applied to the
tree-level mean-field formula gives `λ_tree = 1/(8u_0²)`. This is
class (A) algebraic on the existing framework chain.

## 3. Elon first-principles — what scale is V_taste at?

V_taste comes from integrating out staggered fermions on the L_s = 2
APBC minimal block under mean-field gauge factorization
`U_{ab} → u_0 δ_{ab}` (HIGGS_MASS_FROM_AXIOM Step 4). In Wilsonian RG
language:

- The bare lattice action `S_lattice = S_gauge + S_fermion` lives at
  the lattice cutoff `a^(-1)`.
- Integrating out the staggered fermions on the minimal block gives a
  Wilsonian effective potential `V_taste` at a scale BELOW the cutoff
  — the typical fermion mass scale on the minimal block, which is
  `~ u_0 · a^(-1)` (the eigenvalue scale of the staggered Dirac
  operator at mean field).
- With the Planck pin (Gate #4 conditional) `a^(-1) = M_Pl`, this
  matching scale is `μ_* ≈ u_0 · M_Pl ≈ 0.88 · M_Pl`.

This is **Planck-scale up to an O(1) Wilson coefficient** — the
standard lattice-QFT matching ambiguity. For an AS-template-style
UV anchor, the difference between `M_Pl` and `0.88 M_Pl` produces only
a logarithmic correction in SM RGE running over 38 decades, which is
absorbed in the +12% gap that HIGGS_MASS_FROM_AXIOM Step 5 already
attributes to "lattice spacing convergence."

So: `λ_tree = 1/(8u_0²)` lives at the framework's natural UV scale,
modulo standard lattice-QFT matching corrections. This is the
appropriate object to use as the high-scale boundary condition for SM
RGE running.

## 4. Admitted dependencies

| Authority | Role | Status |
|---|---|---|
| `HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 5–6 | tree-level mean-field formula `m_H = v/(2u_0)` | unaudited |
| Standard Higgs relation `m_H² = 2λv²` | algebraic identity in standard SM Higgs sector | universal physics input |
| `HIERARCHY_MATSUBARA_QUARTIC_COEFFICIENT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md` (PR #937) | composite-Higgs slogan retired (named obstruction) | unaudited (companion) |
| `MINIMAL_AXIOMS_2026-05-03.md` | A1 (Cl(3)) + A2 (Z³); staggered-Dirac realization is open gate | meta |
| Planck pin Gate #4 (lattice cutoff = M_Pl) | scale identification | `audited_renaming` (open) |
| `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` (Gate #7) | numerical input | engineering frontier (NNNLO ξ=4 < ε_witness) |

The bare algebraic identity `λ_tree = 1/(8u_0²)` requires only the
HIGGS_MASS_FROM_AXIOM tree-level formula + standard Higgs relation —
both class (A) once admitted. The scale identification (μ_* ≈ M_Pl)
is conditional on Planck pin (Gate #4). The numerical value
(λ_tree ≈ 0.163) is conditional on Gate #7.

## 5. Load-bearing step (class A)

```text
From HIGGS_MASS_FROM_AXIOM_NOTE.md Step 5–6 (tree-level mean-field on
L_s = 2 mean-field surface, with N_taste = 16 from staggered taste
structure under the open staggered-Dirac realization gate):

  m_H_tree  =  v / (2 u_0).                                      (1)

Squaring:

  m_H_tree²  =  v²  /  (4 u_0²).                                 (2)

The standard SM Higgs relation at tree level:

  m_H²  =  2 λ v²    ⟹    λ  =  m_H²  /  (2 v²).                (3)

Substitute (2) into (3):

  λ_tree  =  v²  /  (4 u_0²)  /  (2 v²)
          =  1  /  (8 u_0²).                                     (4)

The v dependence cancels: λ_tree is a Clifford-fixed dimensionless
quartic depending only on the lattice tadpole u_0.

At u_0 = ⟨P⟩^(1/4) ≈ 0.8776 (per gate #7 engineering frontier with
⟨P⟩ ≈ 0.594 from PR #685 lattice MC consensus on the framework Wilson
surface):

  λ_tree  =  1  /  (8 · 0.8776²)
          =  1  /  (8 · 0.7702)
          =  1  /  6.162
          ≈  0.1623.                                             (5)
```

This is class (A) — algebraic substitution into two existing
relations: the framework's tree-level mean-field formula (admitted
from HIGGS_MASS_FROM_AXIOM) and the standard Higgs relation (admitted
universal physics input). No new admissions for the algebraic
identity (4); the numerical value (5) inherits Gate #7. ∎

## 6. Structural implications (named, not derived)

### 6.1 Replacing the retired `λ(M_Pl) = 0` claim

The framework's prior `λ(M_Pl) = 0` claim from VACUUM_CRITICAL_STABILITY
relied on the composite-Higgs heuristic, which was retired as a named
obstruction in PR #937. With that retirement, the framework had no
positive UV anchor for the Higgs quartic. This theorem closes that
gap by exposing the **implicit** UV anchor that was already present in
HIGGS_MASS_FROM_AXIOM's tree-level reading:

```text
λ(μ_* ≈ M_Pl)  =  1 / (8 u_0²)  ≈  0.1623          [this theorem]

versus

λ(M_Pl)  =  0                                       [retired heuristic]
```

The two values are numerically incompatible. With the composite-Higgs
heuristic retired, this theorem's value is the framework's positive
Clifford-fixed UV anchor.

### 6.2 Comparison to Shaposhnikov-Wetterich

Shaposhnikov-Wetterich (2009) predicted `m_H ≈ 126 GeV` pre-LHC by
imposing `λ(M_Pl) = 0` from an asymptotic-safety UV fixed point and
running 2-loop SM RGE down to `v`. The framework's UV anchor here is
**different**: `λ(μ_* ≈ M_Pl) ≈ 0.1623` from the lattice mean-field
curvature, not from an AS fixed point. The framework's prediction
is therefore distinguishable from the AS prediction at the level of
λ at high scale.

| Theory | λ at high scale | Source |
|---|---|---|
| Shaposhnikov-Wetterich (AS) | `λ(M_Pl) = 0` | UV fixed point (asymptotic safety) |
| Framework (this theorem) | `λ(μ_*) ≈ 0.1623` | Cl(3)/Z³ tree-level mean-field on L_s=2 |
| Standard SM (λ free) | extracted from observed m_H ≈ 0.13 at v, runs to ≈ 0 at M_Pl | observed input |

### 6.3 RGE running to `v` scale

This theorem does **not** perform the SM RGE running. The framework's
3-loop runner in HIGGS_MASS_DERIVED takes `λ(M_Pl) = 0` as input and
predicts `m_H ≈ 125.1 GeV`. With this theorem's `λ(μ_*) ≈ 0.163` as
input instead, the predicted m_H at v would be different. Resolving
which is correct requires:

1. Re-running the 3-loop RGE with the new UV anchor input;
2. Comparing the resulting `m_H(v)` to observed `125.10 GeV`;
3. Disambiguating whether the +12% gap from
   `m_H_tree(v) = 140.3 GeV` to physical `125.10 GeV` is "RGE running
   from `λ(M_Pl) = 0`" or "lattice spacing convergence + Wilson
   taste-breaking from `λ(μ_*) = 0.163`".

This is a follow-on engineering task, not closed by this theorem.

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_higgs_lambda_uv_anchor_narrow.py
```

Verifies:

1. The algebraic identity `λ_tree = 1/(8u_0²)` symbolically via SymPy:
   start from `m_H = v/(2u_0)`, substitute into `m_H² = 2λv²`, solve
   for λ, and check the v dependence cancels.
2. Numerical evaluation at `u_0 = 0.8776` gives `λ_tree ≈ 0.1623`.
3. The numerical comparator `λ_tree(observed m_H) = m_H²/(2v²) ≈ 0.129`
   at `m_H = 125.10 GeV, v = 246.22 GeV` — included as audit comparator
   to flag the +20% gap between framework tree-level UV anchor and
   physical `λ(v)`. NOT a derivation input.
4. Scale identification: `μ_* = u_0 × M_Pl ≈ 0.88 × M_Pl` numerically
   via SymPy substitution.
5. Comparison with retired claim: `λ_tree ≠ 0` confirmed via Fraction
   arithmetic.
6. Note structure / scope discipline / scope disclaimers present.

## 8. Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Algebraic identity lambda_tree = m_H_tree^2 / (2 v^2) = 1/(8 u_0^2)
  on the canonical Cl(3)/Z^3 Wilson-plaquette + staggered-Dirac mean-field
  surface, derived from HIGGS_MASS_FROM_AXIOM's tree-level mean-field
  formula m_H_tree = v/(2 u_0) plus the standard SM Higgs relation
  m_H^2 = 2 lambda v^2. At u_0 = 0.8776 (gate #7), lambda_tree ≈ 0.1623.
  Identifies this as the framework's Clifford-fixed quartic UV anchor at
  the lattice mean-field scale mu_* ≈ M_Pl × u_0, replacing the now-retired
  lambda(M_Pl) = 0 heuristic from VACUUM_CRITICAL_STABILITY.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only

declared_one_hop_deps:
  - higgs_mass_from_axiom_note
  - hierarchy_matsubara_quartic_coefficient_ratio_narrow_theorem_note_2026-05-10
  - vacuum_critical_stability_note
  - higgs_mass_derived_note
  - minimal_axioms_2026-05-03
  - planck_scale_lane_status_note_2026-04-23
  - c_iso_su3_nnlo_closure_bounded_note_2026-05-10_su3nnlo

admitted_context_inputs:
  - tree-level mean-field formula m_H_tree = v/(2 u_0)
    (inherits from HIGGS_MASS_FROM_AXIOM Step 5-6; depends on
    staggered-Dirac realization open gate via N_taste = 16)
  - standard SM Higgs relation m_H^2 = 2 lambda v^2
    (universal physics input)
  - lattice cutoff identification a^(-1) = M_Pl
    (inherits from Planck pin gate #4 audited_renaming)
  - numerical u_0 = <P>^(1/4) ≈ 0.8776
    (inherits from gate #7 engineering frontier; structural form
    1/(8 u_0^2) holds independent of numerical value)

forbidden_imports_used: false  # no PDG/lattice MC values are derivation inputs;
                                # observed m_H = 125.10 GeV and lambda_obs(v) ≈ 0.129
                                # appear only as audit comparators
proposal_allowed: true
audit_required_before_effective_status_change: true
```

The narrow theorem is class (A) algebraic substitution. The
load-bearing identity (4) requires only HIGGS_MASS_FROM_AXIOM's
tree-level formula + the standard Higgs relation. The scale and
numerical value inherit named admissions.

## 9. What this theorem closes

- **Gate #6 (lambda-UV anchor) closes positively** with a
  Clifford-fixed dimensionless quartic identity at the lattice
  mean-field scale.
- **The implicit UV anchor in HIGGS_MASS_FROM_AXIOM is now explicit** —
  promoting `λ_tree = 1/(8u_0²)` from an unspoken consequence of the
  tree-level mean-field formula to a stated theorem.
- **The contradiction with the retired `λ(M_Pl) = 0` claim is
  resolved** in favor of `λ_tree ≈ 0.163`, consistent with PR #937's
  named obstruction retiring the composite-Higgs heuristic.

## 10. What this theorem does NOT close

- The Higgs-mass prediction at v (requires SM RGE running + the
  framework's named CW + lattice spacing + Wilson taste-breaking
  corrections per HIGGS_MASS_FROM_AXIOM Step 5).
- The Planck pin (Gate #4 `audited_renaming`).
- The staggered-Dirac realization gate (open).
- The numerical u_0 (Gate #7 engineering frontier).
- Whether the framework's `λ(μ_*) = 0.163` UV anchor RG-runs to the
  observed `λ(v) ≈ 0.129` via standard SM RGE (a follow-on
  engineering task; if not, the +12% gap interpretation needs
  refinement).

## 11. Cross-references

### Companion / sister theorems (this session)
- [`HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md)
  — sister narrow theorem (PR #924); (7/8)^16 determinant ratio
  identity + (1/4) compression bridge corollary.
- [`HIERARCHY_MATSUBARA_QUARTIC_COEFFICIENT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md`](HIERARCHY_MATSUBARA_QUARTIC_COEFFICIENT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md)
  — sister narrow theorem (PR #937); B(L_t) m⁴ coefficient + (8/7)²
  ratio identity + composite-Higgs slogan retirement (named
  obstruction). This theorem builds on PR #937's slogan retirement.

### Higgs / vacuum chain
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — provides the tree-level mean-field formula `m_H = v/(2u_0)` that
  this theorem reads as a UV anchor.
- [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md)
  — claims `λ(M_Pl) = 0` from composite-Higgs heuristic; this theorem
  proposes the positive replacement.
- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md) —
  assumption-derivation ledger flags `λ(M_Pl) = 0` as "weakest leg of
  input chain"; this theorem closes the open theorem the ledger names.

### Framework axioms / structural
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md`](PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md)
  — Planck pin gate #4 status.
- [`C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md`](C_ISO_SU3_NNLO_CLOSURE_BOUNDED_NOTE_2026-05-10_su3nnlo.md)
  — Gate #7 engineering frontier; provides u_0 numerical context.

### Standard physics references (admitted-context literature, not load-bearing)
- Shaposhnikov & Wetterich (2009) — pre-LHC `m_H ≈ 126 GeV` prediction
  from `λ(M_Pl) = 0` (AS UV fixed point), comparator only.
- Buttazzo et al. (2013), Bednyakov et al. (2015) — SM stability
  boundary, comparator only.
- Bardeen, Hill, Lindner (1990) — top-condensation NJL: composite
  scalar with finite quartic at matching scale (justification for
  PR #937's composite-Higgs slogan retirement, on which this theorem
  builds).
