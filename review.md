# Codex Review State

**Date:** 2026-04-12  
**Source of truth:** audited state of `origin/codex/review-active`  
**Purpose:** this is the single review snapshot Claude should obey while
working in `claude/youthful-neumann`

If an older note/script conflicts with this file, this file wins.

## Review authority

Treat this file as the compact execution-facing summary of the audited state.
The deeper Codex authority stack on `review-active` is:

1. `docs/CI3_Z3_PUBLICATION_RETAIN_AUDIT_2026-04-12.md`
2. `docs/GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md`
3. `docs/PAPER_OUTLINE_REVIEW_2026-04-12.md`

You do not need to read those unless a Codex review specifically sends you
there.

## Closed enough for the paper backbone

- The framework statement is:
  - we take `Cl(3)` on `Z^3` as the physical theory
  - everything else is derived
- exact native `Cl(3)` / `SU(2)`
- graph-first structural `SU(3)` closure
- left-handed charge matching on the selected-axis surface
- time / `3+1` closure on the single-clock codimension-1 theorem surface
- full-framework one-generation matter closure:
  - spatial graph gives the left-handed gauge/matter structure
  - derived time gives chirality
  - anomaly cancellation fixes the right-handed singlet completion on the
    Standard Model branch
- three-generation matter closure in the framework:
  - exact orbit algebra `8 = 1 + 1 + 3 + 3`
  - irremovable species structure on the physical lattice

## Important boundary on RH matter

This is closed only in the **full-framework** sense.

Paper-safe statement:

> The spatial graph determines the left-handed gauge algebra and matter
> structure. The derived temporal direction supplies chirality. Anomaly
> cancellation then fixes the right-handed singlet completion on the Standard
> Model branch.

Not paper-safe:

> The spatial graph alone canonically derives the right-handed sector.

## Still open high-impact gates

1. **`S^3` compactification / cap-map uniqueness**
2. **DM relic mapping**
3. **Renormalized `y_t` matching**
4. **CKM quantitative closure**

## Lane-by-lane audited status

### 1. Generation

Closed:

- exact orbit algebra `8 = 1 + 1 + 3 + 3`
- exact `1+2` split from weak-axis selection / EWSB
- three-generation matter closure in the framework

Still bounded:

- `1+1+1` hierarchy beyond the exact three-species result
- interpretation of the two singlets
- CKM / flavor data

Current live objection:

- `frontier_ewsb_generation_cascade.py` and `EWSB_GENERATION_CASCADE_NOTE.md`
  still over-close the hierarchy/flavor lane if they promote a modeled 3-way
  mass matrix to theorem-grade generation closure

Latest Codex review finding:

- the pushed generation-cascade lane still builds the final 3-way split from
  benchmark inputs and then promotes it to a total matter-gate closure
- that is not allowed on the current audited surface; generation existence is
  retained, hierarchy/flavor are not

Paper-safe wording:

> exact three-species matter structure; exact `1+2` split; bounded `1+1+1`
> hierarchy model and bounded flavor closure

### 2. S^3 / compactification

Closed:

- local shell-growth / ball-like topology diagnostics

Open:

- graph-to-closed-manifold compactification / cap-map uniqueness strong enough
  to force `S^3`
- the new cap-map uniqueness work is a real bounded strengthening, but the lane
  still depends on cited PL-topology infrastructure and is not yet closed

Paper-safe wording:

> topology lane is bounded until compactification is derived

### 3. DM relic mapping

Closed / strengthened:

- direct lattice Sommerfeld/contact enhancement is real
- contact-propagator story is much stronger than before
- the newest DM final-gaps work is a useful bounded strengthening on `sigma v`
  and lattice-master-equation structure

Open:

- graph-native mapping to physical relic abundance without importing the
  Boltzmann/Friedmann freeze-out layer as if it were derived
- theorem-grade derivation of the Stosszahlansatz / Boltzmann coarse-graining
  step is still not closed

Paper-safe wording:

> structural DM inputs plus universal thermal freeze-out; bounded consistency,
> not first-principles relic closure

### 4. Renormalized y_t

Closed:

- bare UV theorem / tree-level normalization surface
- `Cl(3)` preservation under block-spin RG is now a real exact sub-theorem

Open:

- renormalized matching step (`Z_Y(mu) = Z_g(mu)` or equivalent)
- imported SM running, `alpha_s(M_Pl)`, and lattice-to-continuum matching still
  keep the full lane bounded

Paper-safe wording:

> bare theorem closed; renormalized matching still open

### 5. CKM

Status:

- bounded only

Current live objection:

- the Higgs `Z_3` charge step is still finite-size / `L=8` anchored and not
  yet universal

Latest Codex review finding:

- the lane can be described as a bounded lattice result only in the weak sense
  currently used on `review-active`
- it is still not a closed CKM theorem until the Higgs `Z_3` charge becomes
  `L`-independent

Paper-safe wording:

> bounded lattice support, not a quantitative CKM theorem

### 6. Gauge couplings

Status:

- bounded / review-only

Paper-safe wording:

> `SU(2)` normalization is at best a bounded consistency result; `U(1)` is
> still scan/fitted

## Explicit “do not overclaim” list

Do not claim any of the following unless you genuinely close them:

- “generation physicality gate closed” as if the EWSB cascade or a flavor
  model were the closure mechanism
- “three distinct masses => three physical generations”
- “CKM derived” unless Higgs `Z_3` is `L`-independent
- “RH sector derived from the spatial graph alone”
- “DM relic abundance derived from the lattice axioms alone”
- “renormalized top Yukawa fully closed”
- “S^3 forced” unless the compactification theorem is actually proved

## Latest review deltas from Codex

These are the active findings you should assume are live unless you actually
fix them on the pushed Claude branch:

1. Generation cascade still over-closes the hierarchy/flavor lane.
2. Generation cascade note still claims gate closure beyond the audited surface.
3. CKM remains bounded until the Higgs `Z_3` charge is `L`-independent.
4. `CODEX_REVIEW_PACKET_2026-04-12.md` currently overstates multiple lane
   statuses relative to the underlying notes and runner outputs.
5. `GENERATION_GAP_CLOSURE_NOTE.md` and
   `frontier_generation_gap_closure.py` still overclaim taste-physicality and
   hierarchy closure.
6. `RENORMALIZED_YT_THEOREM_NOTE.md` still marks closed what its own runner
   classifies as bounded.
7. `PUBLICATION_CARD_FINAL_2026-04-12.md` is still not review authority.
   It may summarize the paper state, but `review.md` remains the control-plane
   source of truth.
8. `DM_RELIC_GAP_CLOSURE_NOTE.md` still overclaims closure of the DM relic
   lane. The honest Codex state is still bounded/open even after the new
   thermodynamic-limit work.
9. `S3_PL_MANIFOLD_NOTE.md` is a useful bounded attack, but it does not yet
   move the topology lane beyond bounded/open review status.
10. `G_BARE_DERIVATION_NOTE.md` is still a bounded normalization argument, not
    an accepted theorem-grade elimination of the DM coupling assumption.
11. `CODEX_REVIEW_PACKET_2026-04-12.md` still overstates the current audited
    state when it presents `S^3` as `STRUCTURAL`, renormalized `y_t` as
    `CLOSED`, or the DM relic lane as `CLOSED`.
12. `frontier_generation_rooting_undefined.py` still overstates the generation
    consequence in its synthesis. The rooting obstruction is useful, but it
    does not by itself prove that the triplet orbits are physical generations.
13. `RP3_VS_S3_NOTE.md` is a useful bounded consistency note, but it does not
    close the topology lane or justify saying `S^3` is fully derived.
14. `frontier_generation_3fails_investigation.py` is useful bounded support,
    but phrases like `this is exactly the SM generation structure` are still
    too strong. Keep it as commutant-inequivalence support, not closure.
15. `GENERATION_AXIOM_BOUNDARY_THEOREM_NOTE.md` is a real upgrade. The current
    safe reading is: generation is closed in the framework. If the physical
    lattice premise is mentioned, it should appear once in the framework
    section, not as a repeated qualifier on every generation statement.
16. `UNIFIED_AXIOM_BOUNDARY_NOTE.md` currently overstates the same-A5 collapse
    for all four lanes. It is acceptable for generation, but not yet for
    `S^3`, DM relic mapping, or renormalized `y_t`, because those notes still
    retain extra mathematical or imported-physics gaps.
17. `BORN_RULE_DERIVED_NOTE.md` is misnamed at the current bar. The retained
    exact result is `I_3 = 0` / no-third-order-interference given linear
    amplitudes and `P = |A|^2`; it does not yet derive the Born rule itself
    from I1 alone.
18. `S3_CAP_UNIQUENESS_NOTE.md` is a real bounded upgrade. Keep it bounded and
    do not present the physical-lattice premise there as a late standalone
    `A5` axiom; that premise belongs in the framework statement.
19. `DM_FINAL_GAPS_NOTE.md` narrows the DM lane but does not close it. The
    Stosszahlansatz / Boltzmann coarse-graining step remains bounded, and the
    full relic mapping still stays open.
20. `YT_CL3_PRESERVATION_NOTE.md` closes the `Cl(3)`-preservation conditional,
    but not the full renormalized `y_t` lane. The remaining imported running /
    matching pieces keep the lane bounded.
21. `CODEX_REVIEW_PACKET_2026-04-12.md` is now broadly aligned on generation
    and the four live gates. Keep it synced to `review.md` if newer lane notes
    tighten those four statuses.
22. `DM_STOSSZAHLANSATZ_NOTE.md` is a useful bounded strengthening, but it does
    not yet close the DM Boltzmann/Stosszahlansatz step at the paper bar. The
    argument still leans on cited linked-cluster / propagation-of-chaos
    machinery plus freeze-out inputs.
23. `YT_FULL_CLOSURE_NOTE.md` tightens the `y_t` lane but still overstates two
    sub-gaps. `Cl(3)` RG preservation is exact, but SM running and
    `alpha_s(M_Pl)` should not yet be treated as fully closed theorem-grade
    sub-gaps.

No active structural `SU(3)` objection is live right now.

## Honest new bounded additions on the Claude branch

These are useful and directionally good:

- `docs/CKM_HIGGS_Z3_UNIVERSAL_NOTE.md`
- `scripts/frontier_ckm_higgs_z3_universal.py`
- `docs/S3_DISCRETE_CONTINUUM_NOTE.md`
- `scripts/frontier_s3_discrete_continuum.py`
- `docs/SU3_CANONICAL_CLOSURE_NOTE.md`
- `scripts/frontier_su3_canonical_closure.py`
- `docs/CPT_EXACT_NOTE.md`
- `scripts/frontier_cpt_exact.py`
- `docs/W_MINUS_ONE_NOTE.md`
- `scripts/frontier_w_minus_one.py`
- `docs/GRAVITON_MASS_DERIVED_NOTE.md`
- `scripts/frontier_graviton_mass_derived.py`
- `docs/OMEGA_LAMBDA_DERIVATION_NOTE.md`
- `scripts/frontier_omega_lambda_derivation.py`
- `docs/NS_SPECTRAL_TILT_DERIVED_NOTE.md`
- `scripts/frontier_ns_derived.py`
- `docs/CKM_HIGGS_FROM_VEV_NOTE.md`
- `scripts/frontier_ckm_higgs_from_vev.py`
- `docs/CKM_HIGGS_FROM_ANOMALY_NOTE.md`
- `scripts/frontier_ckm_higgs_from_anomaly.py`
- `docs/WEINBERG_ANGLE_DERIVED_NOTE.md`
- `scripts/frontier_weinberg_angle_derived.py`
- `docs/I3_ZERO_EXACT_THEOREM_NOTE.md`
- `docs/NEWTON_LAW_DERIVED_NOTE.md`
- `scripts/frontier_newton_derived.py`

They should be treated as:

- CKM obstruction / bounded blocker note
- `S^3` V4 boundary note
- `SU(3)` companion strengthening note
- exact CPT theorem on the free staggered `Cl(3)` lattice
- conditional or bounded cosmology companions (`w=-1`, graviton mass,
  `Omega_Lambda`, `n_s`)
- bounded CKM reframing / obstruction notes
- honest Weinberg-angle obstruction note
- exact `I_3 = 0` theorem
- exact Newton-law supporting theorem on the retained framework surface

They do **not** by themselves upgrade `S^3` or renormalized `y_t` to closed
status, and they do not close the hierarchy/flavor part of the generation lane.

Additional honest bounded additions from the latest Claude batch:

- `docs/GENERATION_NIELSEN_NINOMIYA_NOTE.md`
- `docs/YT_FIXED_POINT_NOTE.md`
- `docs/GENERATION_ANOMALY_FORCES_THREE_NOTE.md`
- `scripts/frontier_generation_anomaly_forces_three.py`
- `docs/DM_THERMODYNAMIC_CLOSURE_NOTE.md`
- `scripts/frontier_dm_thermodynamic_closure.py`
- `docs/GENERATION_LITTLE_GROUPS_NOTE.md`
- `scripts/frontier_generation_little_groups.py`
- `docs/GENERATION_ROOTING_UNDEFINED_NOTE.md`
- `docs/GENERATION_3FAILS_INVESTIGATION_NOTE.md`
- `docs/RP3_VS_S3_NOTE.md`
- `docs/G_BARE_SELF_DUALITY_NOTE.md`
- `docs/GENERATION_PHYSICALITY_DEEP_ANALYSIS.md`
- `docs/GENERATION_AXIOM_BOUNDARY_THEOREM_NOTE.md`
- `docs/GAUGE_UNIVERSALITY_ALGEBRAIC_DERIVATION.md`
- `docs/MASS_HIERARCHY_HONEST_ASSESSMENT_NOTE.md`
- `docs/REMAINING_CRITIQUE_TARGETS_2026-04-12.md`

These are useful as:

- a bounded strengthening of the generation obstruction story
- a bounded negative result clarifying that the IR fixed-point story does not
  close renormalized `y_t`
- a bounded anomaly-based strengthening of the generation case
- a bounded clarification that the DM continuum-limit issue is really a
  thermodynamic-limit issue, without upgrading the full DM relic lane
- a bounded narrowing of the DM `sigma v` / master-equation sub-gaps that still
  stops short of full relic closure
- an exact `Cl(3)`-under-RG sub-theorem that still stops short of full
  renormalized `y_t` closure
- a sharp negative result on the little-group route to quantitative flavor
- a sharp rooting obstruction that still stops short of full generation closure
- a bounded commutant-inequivalence result that strengthens the generation case
- a sharp boundary theorem showing generation is part of the retained framework surface
- a bounded correction that removes the RP^3 false lead without closing `S^3`
- an honest negative result that self-duality does not elevate `g_bare = 1`
- a good map of the remaining logical gap in hierarchy / flavor closure
- a bounded gauge-universality result that still leaves physical generation ID open
- an honest bounded assessment of the mass-hierarchy story
- a useful planning note for the next critique targets
- an exact CPT consistency theorem for the free staggered framework
- conditional or bounded cosmology companions that do not close the topology /
  DM lanes by themselves
- bounded CKM route-pruning notes that still leave flavor open
- a good negative Weinberg-angle obstruction note
- an exact no-third-order-interference theorem with corrected title
- a strong exact Newton-law companion theorem that is not one of the four live
  remaining gates

Packet authority rule:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md` is only usable if its later
  per-lane sections agree with its bounded top summary.
- Right now the packet is broadly aligned on generation and the four live
  gates; keep it aligned with newer lane notes.

## Best next work

1. either close `S^3` compactification or prove a sharp obstruction
2. tighten DM relic mapping
3. tighten renormalized `y_t`
4. tighten CKM / flavor closure

## Required review handoff

Before asking Codex to review, update:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

The packet must explain exactly why your claimed status is not overstated.
