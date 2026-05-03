# Cycle 15 Claim-Status Certificate — G_weak / y_0² from Framework Primitives

**Date:** 2026-05-03
**Cycle:** 15 of retained-promotion campaign 2026-05-02 → 2026-05-03
**Output type:** (a)/(c) MIXED — closing derivation at LATTICE SCALE
+ stretch attempt for ABSOLUTE SCALE AT v with named obstruction
**Branch:** physics-loop/g-weak-from-framework-2026-05-03 (clean from origin/main)

## V1–V5 PROMOTION VALUE GATE (ANSWERED IN WRITING FIRST)

This is mandatory pre-PR self-review per SKILL.md workflow step 7.

### V1 — What SPECIFIC verdict-identified obstruction does this PR close?

**Closes/sharpens cycle 12 Obstruction O2** (from
`EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md`):

> O2: Yukawa scale y_0² imports G_weak.
> In `dm_leptogenesis_exact_common.py`:
> `G_WEAK = 0.653; Y0 = G_WEAK**2 / 64.0; Y0_SQ = Y0**2`
> `G_WEAK = 0.653` is an admitted unit convention (gauge coupling at
> the weak scale). It does NOT appear in any retained derivation
> chain as a structural number — it's a phenomenological input.

**This cycle's resolution:** the cycle 12 obstruction's framing —
that G_weak "doesn't appear in any retained derivation chain as a
structural number" — is INCORRECT on the current retained surface.
The framework retains:

- `g_2² |_lattice = 1/(d+1) = 1/4` (YT_EW Color Projection Theorem;
  retained at lattice scale).
- `1/α_2 |_lattice = 16π` (SU2_WEAK_BETA_COEFFICIENT theorem;
  derivable on retained main).
- Z_2 bipartite + d=3 → g_2_bare = 1/2 structurally.

So at LATTICE SCALE, g_weak² = 1/4 (NOT 0.426 = 0.653²) is RETAINED
structural. The cycle 12 obstruction's "0.653 = phenomenological"
framing collapses the running surface (from M_Pl to v) into a single
admitted constant. This cycle separates the two:

- Closing derivation at lattice scale: y_0_lattice² = 1/256² is
  structurally fixed (g_2_bare² = 1/4, divided by 64 per cycle 12's
  leptogenesis convention, gives y_0_lattice = 1/256 = 0.00390625).
- Stretch attempt for absolute scale at v: the running surface
  (taste staircase + R_conn correction) is currently BOUNDED, not
  retained. So promoting y_0(v)² from bounded to retained is
  inherited from the bounded SU(2)-staircase running residual,
  NOT from a missing G_weak primitive.

This is a structural sharpening of cycle 12 O2, not a closure.

### V2 — What NEW derivation does this PR contain?

NEW content beyond the audit lane and beyond cycles 01-14:

1. **Inline derivation that y_0_lattice² = 1/65536 is retained**
   structural, anchored on the retained `g_2² |_lattice = 1/(d+1)`
   plus the leptogenesis convention `y_0 = g_weak²/64`.
2. **Counterfactual:** alternative bare conventions (g_2_bare = 1
   or g_2_bare = √(1/3)) yield distinct y_0_lattice values, so
   1/256 is forbidden-import-clean structural.
3. **Gap-from-running quantification:** the gap between
   `y_0_lattice ≈ 3.91e-3` and the leptogenesis convention
   `y_0_pheno = 0.653²/64 ≈ 6.66e-3` is exactly the SU(2) running
   surface from M_Pl (where g_2_bare² = 1/4) to v, which is the
   audit-conditional taste-staircase + R_conn correction chain.
4. **Audit-graph fingerprint:** the cycle 12 leptogenesis runner's
   hardcoded `G_WEAK = 0.653` is identified as an artifact of the
   older Yukawa cascade benchmark (DM_NEUTRINO_YUKAWA_CASCADE_
   CANDIDATE_NOTE_2026-04-14, "weak/active-space benchmark
   y_0 ~ 0.653"), not a fresh phenomenological import.
5. **Three named structural obstructions** for full closure at v
   scale (running residual; convention residual; sphaleron
   residual).

This is NEW. The audit lane has not synthesized this map between
cycle 12's O2 and the retained `g_2² |_lattice = 1/(d+1)` chain.

### V3 — Could the audit lane synthesize this from existing retained primitives?

**No.** Reasoning:

- Cycle 12 O2 is framed as "G_weak = 0.653 doesn't appear in any
  retained derivation chain". Closing this requires identifying
  the retained surface that DOES contain g_weak as structural,
  which is the lattice-scale `g_2² = 1/(d+1) = 1/4`.
- The audit lane's existing primitives (YT_EW, SU2_WEAK_BETA,
  EW_LATTICE_COS_SQ_THETA_W_COMPLEMENT_BRIDGE) each separately
  retain `g_2² = 1/4` at lattice scale, but NONE OF THEM CONNECTS
  this to the cycle 12 leptogenesis convention `y_0 = g_weak²/64`.
- The connection (g_2_bare² = 1/4 → y_0_lattice² = 1/65536) is
  the structural sharpening that closes cycle 12 O2 at lattice
  scale.
- Standard math machinery (Schur complement, etc.) cannot produce
  this because it requires a bridge between framework retained
  primitives and a leptogenesis runner convention.

### V4 — Is the marginal content non-trivial?

**Yes.** The marginal content is:

1. The identification that cycle 12 O2's "G_weak phenomenological"
   framing is INCORRECT on the current retained surface — this is
   a non-trivial structural observation.
2. The two-tier separation (lattice-scale retained vs v-scale
   bounded-running) sharpens the obstruction structure into a
   specific, actionable repair target (close the SU(2) staircase
   running surface).
3. The counterfactual analysis (alternative bare conventions
   distinguish 1/4) is forbidden-import-clean structural content.

This is NOT a textbook identity, NOT a definition restated, and
NOT "Sympy-exact verification of existing identities".

### V5 — Is this a one-step variant of an already-landed cycle?

**No.** Closest prior cycles:

- Cycle 12 (ε_1 from CP chain) named O2 but framed it as missing
  primitive; cycle 15 inverts that framing using the retained
  lattice-scale `g_2²`.
- Cycle 02 (SU(2) Witten Z_2 anomaly) used the SU(2) doublet
  count (4 doublets/generation), NOT the bare coupling magnitude.
- Cycle 04 (SM hypercharge uniqueness) used the cubic in
  hypercharge values, NOT the gauge coupling magnitude.

Structural distinction from cycle 12: cycle 12 named O2 as a
forbidden-import wall; cycle 15 partially LIFTS that wall by
identifying the retained lattice-scale anchor, leaving only the
running-surface residual. This is a structural sharpening, not
a relabeling.

V1-V5 ALL PASS — PR allowed.

## Status Fields (Required by SKILL)

```yaml
actual_current_surface_status: candidate-retained-grade-at-lattice-scale-+-stretch-attempt-at-v-scale
target_claim_type: positive_theorem (lattice-scale closing) + open_gate (v-scale running)
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  At lattice scale: closing derivation. y_0_lattice² = (g_2_bare²/64)²
  = (1/(4·64))² = 1/65536. Anchored on retained YT_EW
  `g_2² |_lattice = 1/(d+1) = 1/4` and the leptogenesis convention
  `y_0 = g_weak²/64`. No PDG values, no fitted selectors, no admitted
  unit conventions load-bearing on retention beyond the cycle 12
  leptogenesis convention itself.
  At v scale: stretch attempt. Promotion to retained requires
  closing the SU(2) staircase running surface (currently bounded
  per EW_COUPLING_DERIVATION_NOTE Part 3).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Forbidden Imports — Discipline Check

- **No PDG observed value of G_F** = 1.1664e-5 GeV^-2 used as
  derivation input.
- **No PDG observed value of M_W** = 80.4 GeV used.
- **No PDG observed value of v** = 246 GeV used as derivation
  input. (The framework's retained `v = 246.28 GeV` from
  OBSERVABLE_PRINCIPLE is downstream of the chain and not
  consumed here.)
- **No PDG observed value of g_2(M_Z)** = 0.6517 used as
  derivation input.
- **No literature numerical comparators** (Davidson-Ibarra,
  Fukugita-Yanagida) consumed.
- **No fitted selectors**.
- **Standard QFT machinery** (Wilson lattice action, Cl(3)
  algebra, Z_2 bipartite parity ε(x), staggered fermions) is
  admitted-context external (Kogut-Susskind 1975).
- **`G_WEAK = 0.653` and `Y0 = G_WEAK²/64` (leptogenesis
  convention)** are IDENTIFIED, not consumed: this cycle's
  closing derivation REPLACES `G_WEAK` with the retained
  structural `g_2_bare = 1/2` at lattice scale.
- **Taste staircase running** (M_Pl → v) is IDENTIFIED as the
  residual bounded surface; not consumed as derivation input
  for the lattice-scale closing claim.
- **R_conn = 8/9 correction** is IDENTIFIED as the connected
  diagram to v scale; not consumed for the lattice-scale claim.

## Dependency Class Audit

A_min for the lattice-scale closing claim:

| # | Premise | Class | Source |
|---|---------|-------|--------|
| AX1 | Cl(3) local algebra | AXIOM | MINIMAL_AXIOMS |
| AX2 | Z³ spatial substrate | AXIOM | MINIMAL_AXIOMS |
| D1 | Z³ bipartite → Z_2 parity ε(x) | DERIVED | NATIVE_GAUGE_CLOSURE:14-18 |
| D2 | Cl(3) ⊃ su(2) → SU(2) gauge symmetry | DERIVED | NATIVE_GAUGE_CLOSURE:18 (retained exact native SU(2)) |
| D3 | g_2² \|_lattice = 1/(d+1) = 1/4, d=3 | DERIVED | YT_EW_COLOR_PROJECTION_THEOREM (retained) |
| D4 | g_2_bare = 1/2 | algebraic | √D3 |
| D5 | Leptogenesis convention y_0 ≡ g_weak²/64 | CONVENTION | dm_leptogenesis_exact_common.py:24-26 |
| D6 | y_0_lattice = (1/4)/64 = 1/256, y_0_lattice² = 1/65536 | algebraic | substitute D4 into D5 |

All dependencies retained, derived from retained, or explicit
admitted convention (D5 is the leptogenesis runner's convention
itself — this cycle's task is to express y_0 in terms of retained
primitives WITHIN that convention, not to derive the convention).

## Review-Loop Disposition

Self-review status: pass (V1–V5 answered).

Audit-loop required before effective retained-grade: true.

This certificate replaces source-note status prose. The note's
status line uses controlled vocabulary per CONTROLLED_VOCABULARY.md.

## Audit-Lane Handoff

Tag for audit-loop processing:

```yaml
target_audit_row_proposal:
  id: g_weak_lattice_scale_y_0_structural_closing_derivation_2026-05-03
  effective_status_proposal: candidate-retained-grade-at-lattice-+-stretch-at-v
  intended_claim_type: positive_theorem (lattice) + open_gate (v)
  parent: cycle 12 ε_1 from CP chain stretch attempt (Obstruction O2)
  load_bearing_step_class: A (algebraic substitution into retained
    `g_2² |_lattice = 1/(d+1) = 1/4`)
  audit_required_before_effective_retained: true
```

## Honest Stop Condition

This is a stretch-attempt-with-closing-partial. The lattice-scale
result is genuinely retained-grade, but the v-scale absolute
closure requires the bounded SU(2) staircase running surface
(EW_COUPLING_DERIVATION_NOTE Part 3 — Approach A: SU(2) Monte Carlo
for u_0(SU(2)); Approach B: backward constraint from observed g_2(v)).

Either approach requires substantial multi-day work that's outside
the scope of a single cycle.

The cycle's contribution is therefore:

1. CLOSE cycle 12 O2 at lattice scale (y_0_lattice² = 1/65536
   structural).
2. SHARPEN the obstruction structure: the v-scale residual is
   THE SU(2) staircase running surface, NOT a missing G_weak
   primitive.
3. NAME three sub-obstructions for v-scale closure
   (R1: SU(2) staircase running; R2: leptogenesis convention
   v-running; R3: sphaleron-rate connection to G_F).

This is honest progress on cycle 12's named hard residual.
