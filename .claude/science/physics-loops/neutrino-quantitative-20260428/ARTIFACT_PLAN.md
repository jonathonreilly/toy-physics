# Lane 4 Neutrino — Artifact Plan

**Loop:** `neutrino-quantitative-20260428`

## Cycle 1 — R1 Lane-4 dependency audit + theorem plan (Tier A)

**Artifact:** `docs/NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28.md`

Mirrors Lane-1 Cycle 1 structure: lane-file's "first parallel-worker
target". §0 statement + §1 retained content used + §2 the seven
derivation targets with closure-status tables + §3 cross-lane
dependency map (Lane 5 cosmology bridge for 4F; DM closed package for
4G) + §4 Lane-4-internal route recommendations + §5 phase ordering +
§6 cross-references + §7 boundary.

**Audit-grade.** Counts toward the 2-cycle audit quota.

## Cycle 2 — R2 Dirac vs Majorana global lift (4D, Tier B)

**Artifact:** `docs/NEUTRINO_DIRAC_GLOBAL_LIFT_THEOREM_NOTE_2026-04-28.md`
+ optionally `scripts/frontier_neutrino_dirac_global_lift.py` if
symbolic verification is non-trivial.

Statement to attempt: **Theorem (Global Dirac).** On the retained
`Cl(3)/Z^3` framework with three generations and the retained current-
stack Majorana zero law plus Majorana no-go cluster, neutrinos are
globally Dirac.

Proof template:
- (P1) retained current-stack Majorana zero law (local witness)
- (P2) retained mass-reduction-to-Dirac (carrier identity)
- (P3) Majorana no-go cluster (Native-Gaussian, Finite-Normal-Grammar,
  Lower-Level-Pairing) (closed obstruction list)
- Step 1: enumerate Majorana mass-matrix construction classes on
  `Cl(3)/Z^3`. Show each is closed by (P3) or by (P1).
- Step 2: show the only retained mass-spectrum carrier is Dirac via
  (P2).
- Step 3: globalize (i.e., extend from "current stack" to "all
  retained-equivalent stacks").

If Step 3 fails to globalize cleanly, the cycle output is a
**partial-lift theorem** + named obstruction — valid under Deep Work
Rules' no-churn exception.

**Falsifier:** any positive 0νββ signal up to experimental precision;
predicts no Majorana phases.

**Stretch-eligible.** Counts as substantive cycle (not audit-quota).

## Cycle 3 — R3 Seesaw spectrum partial→retained (4E, Tier B-C)

If Cycle 2 lands the Dirac global lift, seesaw is forced type-I and
the active mass spectrum reduces to (right-handed spectrum + Yukawa
structure). Cycle 3 attempts to retain (M_R1, M_R2, M_R3) from the
existing Phase-4 partial.

If Cycle 2 lands only as partial-lift, Cycle 3 may pivot to:
- the obstruction identified in Cycle 2's globalization step (= deeper
  attack on that obstruction);
- Σm_ν cosmological constraint (R5; Lane 5 bridge work).

## Cycle 4 — stretch attempt or fan-out (per Deep Work Rules)

If Cycles 1-3 included 2 or more audit-grade outputs, Cycle 4 must be
a stretch attempt on a named hard residual (likely `m_lightest`,
`Delta m^2_31`, or whatever obstruction the Cycle 2/3 sequence
isolated). Work it from minimal axioms for at least one `--deep-block`
(90 min).

## Repo-wide weaving (NOT done in workstream — recorded in HANDOFF)

When this branch reaches the post-loop integration step, propose:
- `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`
  §4 scaffolding list update.
- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` row updates
  for retired Majorana-phase inputs (if R2 lands).
- `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md` Lane 4 status line.
- DM closed package cross-reference for δ_CP / θ_23 consistency
  (Cycle 4 if 4G lands).

These weaves are NOT applied on this branch per skill science-only
delivery policy. The post-workstream pipeline will pick them up via
the loop-end review PR.
