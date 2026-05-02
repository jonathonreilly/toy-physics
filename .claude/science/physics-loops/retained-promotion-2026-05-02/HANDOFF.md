# Retained-Promotion Campaign 2026-05-02 — HANDOFF

## What ran

Three closing-derivation cycles, each addressing a verdict-identified
obstruction on a distinct parent row:

| cycle | branch / PR | parent row | parent td | block type |
|------|-------------|------------|-----------|------------|
| 01 | physics-loop/su3-cubic-anomaly-3bar-completion-2026-05-02 → [PR #382](https://github.com/jonathonreilly/cl3-lattice-framework/pull/382) | `one_generation_matter_closure_note` (RH-quark-completion gap) | implicit via su3 anomaly chain | (a) closing derivation |
| 02 | physics-loop/su2-witten-doublet-count-derivation-2026-05-02 → [PR #383](https://github.com/jonathonreilly/cl3-lattice-framework/pull/383) | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | 134 (lbs=B) | (a) closing derivation |
| 03 | physics-loop/scalar-additivity-cpt-even-derivation-2026-05-02 → [PR #386](https://github.com/jonathonreilly/cl3-lattice-framework/pull/386) | `observable_principle_from_axiom_note` | 199 (lbs=B) | (a) closing derivation |

All three PRs were opened with V1–V5 promotion value gate answered in
writing in the cert **before** the derivation was written.

## Why the campaign stops here (3 PRs, not 5)

Honest application of the campaign's stop rule: **value-gate
exhaustion**. The remaining candidate landscape:

- Highest-leverage untouched audited_conditional row
  (`gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note`,
  td=248, lbs=A): repair target is "construct the actual slice transfer
  operator for the unmarked spatial environment, prove the exact
  contractions are positive and well-defined, and verify the boundary
  amplitude formula without replacing it by a toy truncated word." This
  is multi-day infrastructure work, not a single-cycle closing
  derivation.
- Most remaining audited_conditional rows have repair targets of the
  form "add retained one-hop dependencies OR derive from primitives".
  The "add deps" branch is Pattern A (forbidden under new rules); the
  "derive from primitives" branch is genuinely the same shape as
  cycles 01 and 02 (anomaly cluster) — V5 (not a one-step variant)
  fails.
- Specific other candidates considered and rejected:
  - `hierarchy_matsubara_decomposition_note` (td=154, lbs=A): repair
    requires deriving physical EWSB order parameter — Nature-grade
    open problem, would need a 90-min stretch-attempt block
    (output type c), not a clean closing derivation.
  - `g_bare_derivation_note` (td=112, lbs=E): class E means it does
    not load-bear on retention; closing has no audit-graph effect.
  - `yt_explicit_systematic_budget_note` (td=174, lbs=B): repair is
    "register dependencies and ratify upstream" — Pattern A activity.
  - `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` (td=117,
    lbs=B): repair is "ratify or repair listed upstream rows" — Pattern
    A activity.
  - Koide cluster (td≤76): repair targets are well-known honest gaps
    that prior session work has already attempted (δ=2/9 derivation,
    Callan-Harvey normalization=1) — high risk of producing
    weak/duplicative content.

The **honest reading** of the campaign directive ("carrying value,
keep going") is: stop when value runs out. Producing cycles 04/05 by
forcing weaker derivations would violate the user's earlier
course-correction ("build REAL value PRs"), even though the volume cap
is 5 and the cluster caps are not yet hit on a hypothetical new
cluster.

## What the 3 PRs collectively contribute

A coherent triple of "premise → derived consequence" closing
derivations across three distinct mathematical domains:

1. **Diophantine enumeration** (cycle 01) — forced 3̄ completion of
   RH quark sector from SU(3)^3 cubic anomaly cancellation +
   retained Q_L:(3,2).
2. **Parity counting** (cycle 02) — forced even doublet count from
   Witten Z_2 topology + retained Q_L:(2,3) + L_L:(2,1) +
   chirality of SU(2)_L.
3. **Functional-equation reduction** (cycle 03) — two parent
   premises (scalar additivity + CPT-even phase-blindness)
   collapse to one (real continuous strict additivity under
   Grassmann factorization), with CPT-evenness as a derived
   consequence via Cauchy 1821 + lattice CPT structure.

Each cycle produced:
- A new theorem note in `docs/`.
- A new runner in `scripts/` with PASS/FAIL counts.
- A V1–V5 cert in
  `.claude/science/physics-loops/retained-promotion-2026-05-02/`.

PASS totals across all three runners: cycle 01 (15), cycle 02 (14),
cycle 03 (17) — **46 PASS / 0 FAIL**.

## What's queued for future campaigns

| target | td | lbs | repair target | best-fit output |
|---|---|---|---|---|
| `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | 248 | A | construct actual transfer operator | (multi-day infrastructure) |
| `hierarchy_matsubara_decomposition_note` | 154 | A | derive physical EWSB order parameter | (c) stretch-attempt failure with named obstruction |
| `neutrino_majorana_operator_axiom_first_note` | 185 | B | derive full SM-like representation from retained primitives | extension of cycles 01/02 — needs hypercharge derivation first |
| `kubo_fam2_refinement_note` | 2 | — | (currently unaudited proposed_retained) | low leverage |

## Forbidden-import discipline

All three cycles' artifacts checked clean under the campaign's
forbidden-import policy:
- No PDG observed values consumed.
- No literature numerical comparators consumed (Witten 1982 / Cauchy
  1821 are admitted-context external mathematical authorities, not
  data comparators).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-lane handoff

All 3 PRs are tagged for review-loop processing. No files in
`docs/audit/data/audit_ledger.json` were modified; no
audit-acceleration runners were added. The retained-promotion campaign
delivered new derivations only, leaving audit-ledger machinery
untouched for the audit lane to ratify or demote on its own
authority.

The reviewer should evaluate each PR on:
- Does the V1–V5 cert hold up under cross-check?
- Does the derivation actually replace the parent's admitted premises
  with a structural premise + retained machinery + admitted-context
  math?
- Are the counterfactuals (where present) actually demonstrating
  non-triviality of the derivation?
- Does the runner actually verify what it claims to verify?

If any cycle fails review, demote/archive that block individually;
the other cycles are independent.
