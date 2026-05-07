# Lane Promotion Proposal — α_s Direct Wilson Loop as `bounded_theorem`

**Date:** 2026-05-07
**Type:** `bounded_theorem_promotion_proposal`
**Authority role:** source-note proposal. The proposal does **not** set
or predict an audit verdict; the actual `claim_type` /
`effective_status` transition is set only by the independent audit
lane.
**Subject lane:** [`ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md)
**Honest-status prior repair:** [`ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md)
**Bridge synthesis basis:** [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
**Primary runner (unchanged):** [`scripts/frontier_alpha_s_direct_wilson_loop.py`](../../scripts/frontier_alpha_s_direct_wilson_loop.py)
(verified PASS=18/0 strict mode at the time of the prior repair)

## 1. Lane summary

The α_s direct Wilson-loop lane derives `α_s(M_Z)` on the Cl(3)/Z³
graph-first SU(3) Wilson gauge surface at `g_bare = 1`, β = 6 by the
standard lattice-QCD route: rectangular Wilson-loop expectation values
on three thermalized ensembles, plateau-fit static potential
`V(R) = -lim_{T→∞}(1/T) log W(R,T)`, force-scheme coupling
`α_qq(1/R) = (R²/C_F) dV/dR` with `C_F = 4/3`, Sommer-scale anchoring
`R² dV/dR = 1.65` at `R = r_0`, then 4-loop QCD running to `M_Z`. The
strict runner records `α_s(M_Z) = 0.1180 ± 0.0068`, agreeing with PDG
2025 world average `0.1180 ± 0.0009` within 1σ. The route deliberately
avoids the older `α_LM/u_0` decoration trap; the strict runner forbids
`u_0`, `alpha_lm`, `alpha_bare_over_u0_squared`, and
`plaquette_authority` as derivation inputs.

## 2. Pre-promotion state

The lane currently sits at the surface left by the 2026-05-02 honest
status audit:

- **Parent claim note**
  [`ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md):
  declared `claim_type: bounded_theorem` / `proposed_retained,
  unaudited` in the audit ledger.
- **Honest-status correction**
  [`ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md):
  recommended demotion to `bounded support theorem on retained
  graph-first surface with admitted Sommer-scale and standard
  QCD-running imports`. Effective status: `bounded`. Criteria 1, 2, 3
  failed; Criterion 4 partial. The Sommer-scale `r_0 = 0.5 fm` and the
  4-loop QCD running bridge were named as admitted standard
  corrections.

### Hidden admission load-bearing on the prior surface

The 2026-05-02 honest-status audit named two admitted external
imports (Sommer scale, 4-loop running bridge) but **did not** name the
deeper structural admission that the lane silently inherits from
[`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](../../docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
and the `g_bare = 1` chain: namely, that **the Wilson plaquette
action `S_W = -β Σ_p (1/N_c) Re Tr(U_p)` itself is admitted as
convention**, not derived from A1 + A2. This is the "Wilson is admitted
import not derived from Cl(3)/Z³" bridge gap explicitly identified in
the 2026-05-06 ten-agent attack and recorded in
[`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md).

Concretely, the static-potential extraction depends on:

(a) the lattice action being Wilson (sets `β = 6` ↔ `g_bare = 1`
mapping via small-`a` continuum matching),
(b) the canonical Gell-Mann trace normalization `N_F = 1/2` (sets
`C_F = 4/3` used in the force-scheme coupling formula),
(c) the Hamilton-to-Lagrangian dictionary that translates the
framework's natural `H_KS` into the 4D isotropic Wilson action
consumed by the runner.

Items (a), (b), (c) were carried as silent imports prior to the
2026-05-07 four-agent run. The promotion proposed here makes each
one explicit, audit-defensible, and quantitatively bounded.

## 3. Proposed bounded-theorem claim

**Claim (lane-level).** Under the three audit-defensible admissions
listed in Section 4 below, the framework's α_s direct Wilson-loop
lane derives, from A1 + A2 + retained graph-first SU(3) chain +
retained `g_bare` chain (with single localized convention scalar) +
retained Hamilton-Lagrangian dictionary at the anisotropic-Trotter
level, plus the lane's existing Wilson-loop / static-potential /
Sommer-scale / 4-loop running machinery,

```
α_s(M_Z) = 0.1180 ± 0.0068  (statistical + scale + running),
                         ± ~10% relative bridge-level systematic,
```

agreeing with PDG 2025 world average `0.1180 ± 0.0009` within 1σ on
the statistical/scale/running budget, and within the bridge-level
systematic (Section 6) on the dictionary/parsimony/N_F admissions.

The claim's scope is **finite-β lattice-QCD α_s extraction at canonical
operating point β = 6, ξ = 1**, not exact-tier closure of α_s. The
finite-β residual on action-form ambiguity remains under the existing
no-go
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)),
fragmented into bounded admissions per the 2026-05-07 unified bridge
status.

## 4. `admitted_context_inputs` (audit-defensible, explicitly named)

```yaml
admitted_context_inputs:
  - id: N_F_canonical_normalization
    statement: "N_F = 1/2 canonical Gell-Mann trace normalization in
                Tr(T_a T_b) = N_F · δ_ab"
    parent: G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md
    layer: L3 in four-layer stratification
    bound: not numerical (single admitted scalar)
  - id: Convention_C_iso_dictionary
    statement: "Hamilton-Lagrangian isotropic reduction at a_τ = a_s
                with Wilson-replacement of heat-kernel temporal plaquette"
    parent: DICTIONARY_DERIVED_THEOREM.md
    bound: O(g²) ~ 5-15% at canonical operating point (s_t = 0.5, ξ = 1)
  - id: continuum_equivalence_parsimony
    statement: "lattice action selection within continuum-equivalence
                class {Wilson, heat-kernel, Manton} at finite β"
    parent: A2_5_DERIVED_THEOREM.md
    bound: ~5-10% across the equivalence class at β = 6
```

### How each admission relates to the prior surface

- **`N_F_canonical_normalization`** is the *one* convention scalar
  identified by the four-layer stratification of the `g_bare` chain
  ([`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md))
  at L3. It is consumed by the lane's `C_F = (8/3) N_F = 4/3` factor
  and indirectly via β = 2 N_c = 6 at L4b. It replaces what the
  2026-05-02 audit called the "minimal_axioms_2026-04-11" partial
  dependency; under the 2026-05-07 strengthening, the convention is
  precisely localized at this single scalar.
- **`Convention_C_iso_dictionary`** is the explicit admission, with
  numerical bound, identified by the Anisotropic Trotter Dictionary
  Theorem T-AT
  ([`DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md))
  Corollary T-AT.3 / T-AT.4. It covers (i) `a_τ = a_s` time-discretization
  (Convention C-iso) and (ii) Wilson-replacement of the heat-kernel
  temporal plaquette. Numerically verified at `O(g²) ≈ 7-9%` at
  `g² = 1, ξ = 1`. This admission unwinds the implicit assumption that
  the framework's natural `H_KS` Trotterizes to standard 4D isotropic
  Wilson at `β = 6`.
- **`continuum_equivalence_parsimony`** is the finite-β residual of
  the A2.5 derivation theorem
  ([`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md)) Step 5: the
  continuum-level magnetic operator `α_eff · Tr(F²)` is uniquely
  derived, but Wilson, heat-kernel, and Manton are all RP-positive
  lattice representatives of that same continuum operator with
  ~5-10% finite-β observable spread. Selecting Wilson-form at finite
  β is a **parsimony convention** within this continuum-equivalence
  class — distinct from C-iso, distinct from N_F.

These three admissions together replace what was previously the
single load-bearing "Wilson is admitted import" hidden admission with
**three named, bounded, audit-defensible admissions**, mirroring the
fragmentation reported in
[`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
§"Bridge gap fragmentation: pre vs post".

### Independent admitted external imports (unchanged from prior surface)

The lane also depends on the original two external imports flagged by
the honest-status audit. These are **not** new and are listed for
completeness:

- Sommer-scale calibration `r_0 = 0.5 fm` — admitted as standard
  literature anchor (Sommer 1993; FLAG).
- 4-loop QCD running β-function and threshold matching — admitted as
  standard PDG-style machinery (PDG 2025 §9.4).

These remain admitted standard corrections; the present promotion
proposal does **not** retire them. They feed the `0.0068`
statistical/scale/running uncertainty already reported in the lane's
budget.

## 5. Quantitative uncertainty

The three new bridge-level admissions produce structurally separable
contributions which are conservatively combined as a single relative
bound on the lane's prediction:

| Admission | Bound at canonical operating point |
|---|---|
| `N_F_canonical_normalization` | exact under L3 admission (no numerical band) |
| `Convention_C_iso_dictionary` | `O(g²) ≈ 7-9%` at `g² = 1, ξ = 1` |
| `continuum_equivalence_parsimony` | `~5-10%` across {Wilson, HK, Manton} at β = 6 |
| **Combined bridge-level relative bound** | **~10% relative** (mirroring [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md) §"Joint bound") |

This `~10%` relative bridge-level systematic is **distinct from and
in addition to** the lane's existing statistical / finite-volume /
finite-spacing / scale-setting / running-bridge budget of `±0.0068`.
It enters the lane's claim only on the dictionary / parsimony / N_F
admissions, not on the lattice MC machinery itself.

The lane's PDG-comparator posture is unchanged: the lattice MC central
value `0.1180` already sits inside the PDG 1σ window
`0.1180 ± 0.0009`, and the bridge-level systematic does not displace
this. The bridge-level bound documents the *honesty* of the bounded
claim, not a redirection of the central value.

## 6. What this promotion DOES vs DOES NOT close

### DOES close

- **Promotes the lane from `bounded support theorem with hidden
  Wilson-admission` to `bounded_theorem` with EXPLICITLY NAMED
  admissions.** Each of the three load-bearing bridge-level
  admissions is now (a) named, (b) parented to a 2026-05-07 source
  note, (c) numerically bounded, (d) audit-defensible.
- **Resolves the 2026-05-02 honest-status repair point.** Criterion 3
  (no admitted unit conventions or literature values as load-bearing
  proof inputs) is reframed: the admitted external imports
  (Sommer-scale, running bridge) remain outside the bounded claim's
  load-bearing scope, and the bridge-level structural admissions are
  now explicit `admitted_context_inputs` per repository convention,
  consistent with how
  [`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md) and
  [`DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md)
  themselves carry admitted context.
- **Aligns the lane with the 2026-05-07 bridge-fragmentation
  framework** so that downstream consumers cite a single audit
  surface for the lane's status.

### DOES NOT close

- **Does NOT promote to exact-tier `ε_witness` retention.** Exact-tier
  closure requires:
  - **W1**: full multi-plaquette numerics with proper SU(3)
    spin-network ED (vertex intertwiners, full Clebsch-Gordan for
    overlapping plaquettes). The current 2×2 torus result
    (`⟨P⟩ = 0.0434 ± 0.0006`) is in strong-coupling LO regime;
    matching KS literature `~0.55-0.60` at `g² = 1` is engineering,
    not new physics, but is not yet implemented. See
    [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
    §"Genuine remaining work" item W1.
  - **W2**: derivation of `N_F = 1/2` from Cl(3) Hilbert-Schmidt
    structure alone. Currently L3 admitted scalar; lifting it to L4
    derived would close the one remaining convention layer. Per
    [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
    this is a separate Nature-grade target.
  - **W3**: independent audit-lane retention of the new 2026-05-07
    candidate notes
    ([`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md),
    [`DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md),
    [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md),
    [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)).
- **Does NOT retire the Sommer-scale or 4-loop running-bridge
  external imports.** Those remain admitted standard corrections per
  the 2026-05-02 honest-status audit, and feed the lane's existing
  `±0.0068` budget. Retiring them is independently hard (would need
  framework-native scale-anchor and running theorems), and is not
  addressed by this promotion.
- **Does NOT bypass the existing finite-β no-go.** The
  continuum-equivalence parsimony admission is precisely the
  audit-defensible re-encoding of that no-go's residual content, not
  a circumvention of it.

## 7. Cross-references

### Direct parents of the three admissions

- [`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md) — A2.5
  bounded-theorem derivation; parent of `continuum_equivalence_parsimony`.
- [`DICTIONARY_DERIVED_THEOREM.md`](DICTIONARY_DERIVED_THEOREM.md) —
  Anisotropic Trotter Dictionary Theorem T-AT; parent of
  `Convention_C_iso_dictionary`.
- [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  — four-layer stratification; parent of `N_F_canonical_normalization`.

### Indirect dependencies (retained chain)

- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  — joint trace-AND-Casimir rigidity; supports L2 form rigidity in
  the `N_F` admission's parent stratification.
- [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](../../docs/G_BARE_RIGIDITY_THEOREM_NOTE.md)
  — Hamiltonian-level `g_bare` rigidity; sister argument at L2/L4.
- [`G_BARE_AUDIT_RESIDUAL_CLOSURE.md`](G_BARE_AUDIT_RESIDUAL_CLOSURE.md)
  — master synthesis of the `g_bare` audit-residual closure.
- [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
  — bridge-level synthesis identifying this lane as one of four
  ready-to-promote bridge-dependent lanes.
- [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)
  — finite-β no-go that motivates the parsimony admission.
- [`MINIMAL_AXIOMS_2026-05-03.md`](../../docs/MINIMAL_AXIOMS_2026-05-03.md)
  — A1 + A2 minimal axiom surface.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](../../docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  — retained Wilson SU(3) gauge surface used by the lane's runner.

### Lane source notes (subjects of this promotion)

- [`ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md)
  — original lane note proposing the bounded theorem.
- [`ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md)
  — prior repair point; honest-status audit recommending demotion to
  `bounded support theorem`.

### Runner artifacts (unchanged by this proposal)

- [`scripts/frontier_alpha_s_direct_wilson_loop.py`](../../scripts/frontier_alpha_s_direct_wilson_loop.py)
  — strict runner; PASS=18/0 verified at the 2026-05-02 repair point.
- `outputs/alpha_s_direct_wilson_loop_certificate_2026-04-30.json` —
  the production certificate consumed by the strict runner.

## 8. Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  On the Cl(3)/Z³ graph-first SU(3) Wilson gauge surface at g_bare = 1,
  β = 6, the renormalized strong coupling extracted from rectangular
  Wilson-loop expectation values via static-potential plateau fits,
  Sommer-scale anchoring r_0 = 0.5 fm, and 4-loop QCD running to M_Z
  satisfies α_s(M_Z) = 0.1180 ± 0.0068 (statistical + scale + running),
  with an additional ~10% relative bridge-level systematic from the
  three named admissions: N_F = 1/2 canonical Gell-Mann normalization
  (L3 of g_bare four-layer stratification); Convention C-iso for the
  Hamilton-Lagrangian isotropic reduction with Wilson-replacement of
  the temporal heat-kernel plaquette (O(g²) ~ 7-9%); and parsimony
  selection within the continuum-equivalence class {Wilson, heat-kernel,
  Manton} at finite β (~5-10%). The claim is finite-β lattice-QCD
  α_s extraction at canonical operating point, not exact-tier closure.
proposed_load_bearing_step_class: B (bounded derived theorem on the
  retained graph-first surface plus retained g_bare chain plus
  retained Hamilton-Lagrangian dictionary, with three explicitly named
  bridge-level admissions and two unchanged external standard imports).
admitted_context_inputs:
  - N_F_canonical_normalization
    (parent: G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  - Convention_C_iso_dictionary
    (parent: DICTIONARY_DERIVED_THEOREM.md)
  - continuum_equivalence_parsimony
    (parent: A2_5_DERIVED_THEOREM.md)
external_admitted_imports:
  - Sommer-scale calibration r_0 = 0.5 fm (Sommer 1993; FLAG)
  - 4-loop QCD running β-function + threshold matching (PDG 2025 §9.4)
declared_one_hop_deps:
  - alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30
  - alpha_s_direct_wilson_loop_honest_status_audit_note_2026-05-02
  - a2_5_derived_theorem_2026-05-07
  - dictionary_derived_theorem_2026-05-07
  - g_bare_constraint_vs_convention_restatement_note_2026-05-07
  - graph_first_su3_integration_note
audit_required_before_effective_retained: true
parent_update_allowed_only_after_retained: true
proposal_allowed: true
proposal_allowed_reason: |
  All three new bridge-level admissions are parented to 2026-05-07
  candidate notes that are themselves audit-pending under the same
  4-agent run; the lane's runner artifact is unchanged and continues
  to PASS=18/0 strict mode; no new fitted parameter or observed value
  is introduced; the two external imports (Sommer scale, running
  bridge) remain admitted standard corrections per the prior
  honest-status audit and feed only the lane's existing ±0.0068
  budget, not the new bridge-level systematic. The bounded scope is
  honest: lane closure is at finite-β bounded_theorem, not exact-tier
  ε_witness.
```

### Disposition request

This proposal asks the audit lane to:

1. **Retain the three 2026-05-07 parent candidate notes** (see §7
   "Direct parents") on the audit surface they declare. The lane
   promotion is conditional on each parent's retention.
2. **Submit the parent lane note**
   [`ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`](../../docs/ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md)
   for re-classification on the strengthened dependency surface, with
   the explicit `admitted_context_inputs` block in §4 above replacing
   the implicit "Wilson is admitted" hidden admission previously
   load-bearing on the lane.
3. **If all three parents retain, classify the lane as
   `audited_clean` / `retained_bounded` at `claim_type:
   bounded_theorem`** with `effective_status: bounded` and the
   ~10% relative bridge-level systematic recorded against the
   three named admissions.
4. **If one or more parents do not retain, hold the lane at
   `audited_conditional` with strengthened substance** (the runner
   continues to PASS=18/0; the three admissions are explicitly named
   even if one or more parents do not yet retain), pending closure of
   the parent or substitution of an alternative audit-defensible
   admission.

### What retention would unlock downstream

Per [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
§"Lane unlock", retention of this lane at `bounded_theorem` /
`retained_bounded` with the three explicit admissions would make the
lane's `α_s(M_Z) = 0.1180 ± 0.0068 ± ~10% bridge-systematic`
available to its 259 transitive descendants as a **bounded-theorem
input with explicit, named, parented bridge-level admissions** —
materially stronger than the prior surface (where the descendants
inherited the lane's hidden Wilson-admission tacitly). Descendant
rows that previously rested on the lane's `proposed_retained` claim
without naming the bridge admissions would be brought into
audit-coherent status by this promotion.

Exact-tier closure of the lane (`claim_type: ε_witness`) remains
gated on W1 + W2 + W3 per §6 above and is not addressed by this
proposal.
