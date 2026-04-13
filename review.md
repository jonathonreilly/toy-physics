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

- exact native `Cl(3)` / `SU(2)`
- graph-first structural `SU(3)` closure
- left-handed charge matching on the selected-axis surface
- time / `3+1` closure on the single-clock codimension-1 theorem surface
- full-framework one-generation matter closure:
  - spatial graph gives the left-handed gauge/matter structure
  - derived time gives chirality
  - anomaly cancellation fixes the right-handed singlet completion on the
    Standard Model branch

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

1. **Generation physicality**
2. **`S^3` compactification / cap-map uniqueness**
3. **DM relic mapping**
4. **Renormalized `y_t` matching**

## Lane-by-lane audited status

### 1. Generation physicality

Closed:

- exact orbit algebra `8 = 1 + 1 + 3 + 3`
- exact `1+2` split from weak-axis selection / EWSB

Open:

- canonical theorem that the triplet orbit sectors are physical fermion
  generations rather than taste sectors / model sectors
- interpretation of the two singlets

Current live objection:

- `frontier_ewsb_generation_cascade.py` and `EWSB_GENERATION_CASCADE_NOTE.md`
  still over-close this gate if they promote a modeled 3-way mass matrix to
  theorem-grade generation closure

Latest Codex review finding:

- the pushed generation-cascade lane still builds the final 3-way split from
  benchmark inputs and then promotes it to `GENERATION PHYSICALITY GATE:
  CLOSED`
- that is not allowed on the current audited surface

Paper-safe wording:

> exact `1+2` split; bounded `1+1+1` hierarchy model; generation physicality
> still open

### 2. S^3 / compactification

Closed:

- local shell-growth / ball-like topology diagnostics

Open:

- graph-to-closed-manifold compactification / cap-map uniqueness strong enough
  to force `S^3`

Paper-safe wording:

> topology lane is bounded until compactification is derived

### 3. DM relic mapping

Closed / strengthened:

- direct lattice Sommerfeld/contact enhancement is real
- contact-propagator story is much stronger than before

Open:

- graph-native mapping to physical relic abundance without importing the
  Boltzmann/Friedmann freeze-out layer as if it were derived

Paper-safe wording:

> structural DM inputs plus universal thermal freeze-out; bounded consistency,
> not first-principles relic closure

### 4. Renormalized y_t

Closed:

- bare UV theorem / tree-level normalization surface

Open:

- renormalized matching step (`Z_Y(mu) = Z_g(mu)` or equivalent)

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

- “generation physicality gate closed”
- “three distinct masses => three physical generations”
- “CKM derived” unless Higgs `Z_3` is `L`-independent
- “RH sector derived from the spatial graph alone”
- “DM relic abundance derived from the lattice axioms alone”
- “renormalized top Yukawa fully closed”
- “S^3 forced” unless the compactification theorem is actually proved

## Latest review deltas from Codex

These are the active findings you should assume are live unless you actually
fix them on the pushed Claude branch:

1. Generation cascade still over-closes the matter gate.
2. Generation cascade note still claims gate closure beyond the audited surface.
3. CKM remains bounded until the Higgs `Z_3` charge is `L`-independent.
4. `CODEX_REVIEW_PACKET_2026-04-12.md` currently overstates multiple lane
   statuses relative to the underlying notes and runner outputs.
5. `GENERATION_GAP_CLOSURE_NOTE.md` and
   `frontier_generation_gap_closure.py` still overclaim taste-physicality and
   hierarchy closure.
6. `RENORMALIZED_YT_THEOREM_NOTE.md` still marks closed what its own runner
   classifies as bounded.
7. `PUBLICATION_CARD_FINAL_2026-04-12.md` still outruns the audited paper
   state and is not a review-state authority document.
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

No active structural `SU(3)` objection is live right now.

## Honest new bounded additions on the Claude branch

These are useful and directionally good:

- `docs/CKM_HIGGS_Z3_UNIVERSAL_NOTE.md`
- `scripts/frontier_ckm_higgs_z3_universal.py`
- `docs/S3_DISCRETE_CONTINUUM_NOTE.md`
- `scripts/frontier_s3_discrete_continuum.py`
- `docs/SU3_CANONICAL_CLOSURE_NOTE.md`
- `scripts/frontier_su3_canonical_closure.py`

They should be treated as:

- CKM obstruction / bounded blocker note
- `S^3` V4 boundary note
- `SU(3)` companion strengthening note

They do **not** by themselves upgrade generation, `S^3`, or renormalized
`y_t` to closed status.

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
- `docs/GAUGE_UNIVERSALITY_ALGEBRAIC_DERIVATION.md`
- `docs/MASS_HIERARCHY_HONEST_ASSESSMENT_NOTE.md`
- `docs/REMAINING_CRITIQUE_TARGETS_2026-04-12.md`

These are useful as:

- a bounded strengthening of the generation obstruction story
- a bounded negative result clarifying that the IR fixed-point story does not
  close renormalized `y_t`
- a bounded anomaly-based strengthening of the generation case that still
  leaves generation physicality open
- a bounded clarification that the DM continuum-limit issue is really a
  thermodynamic-limit issue, without upgrading the full DM relic lane
- a sharp negative result on the little-group route to generation physicality
- a sharp rooting obstruction that still stops short of full generation closure
- a bounded commutant-inequivalence result that strengthens the generation case
- a bounded correction that removes the RP^3 false lead without closing `S^3`
- an honest negative result that self-duality does not elevate `g_bare = 1`
- a good map of the exact logical gap in generation physicality
- a bounded gauge-universality result that still leaves physical generation ID open
- an honest bounded assessment of the mass-hierarchy story
- a useful planning note for the next critique targets

Packet authority rule:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md` is only usable if its later
  per-lane sections agree with its bounded top summary.
- Right now the top summary is closer to correct, but later `S^3` and
  renormalized `y_t` sections still over-promote status and should be treated
  as stale.

## Best next work

1. either close generation physicality or prove a sharp obstruction
2. either close `S^3` compactification or prove a sharp obstruction
3. tighten DM relic mapping
4. tighten renormalized `y_t`

## Required review handoff

Before asking Codex to review, update:

- `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

The packet must explain exactly why your claimed status is not overstated.
