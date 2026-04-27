# Hubble H_0 — Handoff

**Branch:** `frontier/hubble-h0-20260426`
**Workstream:** `hubble-h0-20260426`

## Current State

**Cycles 1 and 2 complete.**

**Cycle 1 (R4 — Hubble Tension Structural Lock):**

- `docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`
- `scripts/frontier_hubble_tension_structural_lock.py` — 5/5 PASS
- `logs/2026-04-26-hubble-tension-structural-lock.txt`

**Cycle 2 (R3 — Cosmology Open-Number Reduction):**

- `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`
- `scripts/frontier_cosmology_open_number_reduction.py` — 5/5 PASS
- `logs/2026-04-26-cosmology-open-number-reduction.txt`

Branch-local 6-criterion self-review PASS for both cycles. Cycle 1
required one premise-tightening edit (3 → 2 premises). Cycle 2 required
two corrections: a wrong expected range in the runner (R_Lambda is
~5.4 Gpc, not the Hubble radius) and an inverted formula in the theorem
note table (`1 + z_mLambda = (L/M)^(1/3)`, not the inverse).

`STATE.yaml` is the single-source-of-truth resume surface.

## Claim-state movement achieved

**Lane 5 Phase 1 (5C — Hubble tension explicit stance):** advanced from
"Tier A planning, ~1 week" (lane file framing) to **theorem-note grade
with an explicit operational falsifier** (no late-time `H_0` drift on the
retained surface). Late-time-only resolutions of any genuine Hubble
tension are now structurally forbidden on the retained surface;
resolution must come from pre-recombination physics or measurement
systematics.

**New: Cosmology open-number-count theorem.** The late-time bounded
cosmology surface has exactly 2 open structural numbers: `(H_0, L)`. All
of `{H_inf, R_Lambda, Omega_Lambda, Omega_m, q_0, z_*, z_mLambda, H(a)}`
are exact closed-form functions of the pair. **No fourth class of
derivation** retires the cosmology surface beyond {derive `L`,
derive `H_0`, derive `R_Lambda` + one of `(L, H_0)`}.

Neither cycle retires the `H_0` import (Lane 5 main target). They lock
the structural form and exhaustively classify the closure pathways.

## Next Exact Action (Cycle 3 candidate)

Per `ROUTE_PORTFOLIO.md` scoring, the strongest remaining single-cycle
candidates are:

- **Cycle 3 candidate A — Route R5 (eta retirement audit).** Survey the
  surviving DM leptogenesis branches (`eta/eta_obs = 0.1888` exact
  one-flavor; `1.0` reduced-surface PMNS) and identify the minimal
  selector/normalization closure that retires `eta` from the bounded
  `Omega_b` cascade. Tier B. Cross-lane dependency: requires reading
  DM-leptogenesis lane notes outside this branch's existing context.
- **Cycle 3 candidate B — Route R7 (minimal-axiom cosmology no-go).**
  Prove that on the minimal accepted axiom stack alone, `L` cannot be
  derived without an additional structural premise (e.g., an absolute-
  scale axiom or a separate dimensionless ratio). Program-bounding
  negative — would isolate the gap that Lane 5 needs an additional
  structural premise to close.
- **Recommendation:** both are Tier B and warrant a fresh session for
  clean grounding (Cycle-1/2 context is heavy with cosmology theorem
  detail; switching to DM-lane content for R5, or to careful axiom-stack
  formulation for R7, is best done with a clean reader). Either can be
  started by re-invoking `/frontier-workstream --mode resume --workstream
  hubble-h0-20260426`.

## Repo-Wide Weaving (NOT to apply on this branch)

When this branch reaches the post-workstream review-and-integration step,
propose:

- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §5
  (cosmology-windows row): cite the structural lock theorem alongside the
  matter-bridge identity. Update phrasing to reflect the late-time lock
  ("the FRW kinematic identities are structural support, with late-time
  `H_0(z)` running forbidden on the retained surface").
- `docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md`: revise the
  Hubble-tension framing — the framework's commitment to ΛCDM at late
  times rules out late-time-only tension resolutions; add a paragraph
  citing the new theorem.
- `docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`
  §4 scaffolding list: add the new theorem note. Update §5 Phase 1 (5C)
  status from "Tier A, ~1 week" to "landed on `frontier/hubble-h0-20260426`,
  awaiting integration".
- `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md`: status line on Lane 5 —
  Phase 1 (5C) landed branch-locally; Phase 2 (5A `Omega_m` closure)
  remains open.
- `docs/CANONICAL_HARNESS_INDEX.md` (if relevant): add
  `frontier_hubble_tension_structural_lock.py` to the cosmology runner
  list.
- `docs/publication/ci3_z3/CLAIMS_TABLE.md` (or equivalent): add an entry
  for the structural lock claim — exact, falsifiable, manuscript-grade.

Do **not** apply these weaves on `frontier/hubble-h0-20260426`. Per skill
delivery policy, this branch carries science only; repo-wide weaving is
for post-workstream review.

## Stop Conditions Status

- Runtime budget: 10h declared; significant remaining at Cycle 1 complete.
- Max cycles: not configured.
- Review blocker: none.
- External worktree change: not applicable.
- Target status achieved: no — Lane 5 Phase 1 (5C) advanced; Phase 2 (5A,
  5B) and core target (`H_0` retirement) remain open.
- Required network/literature/tool access unavailable: no.

May continue to Cycle 2 in this session, or wait for explicit user
direction. Next session can resume cleanly via `--mode resume` against
`STATE.yaml`.

## Notes for resume

If a future session picks this up via `--mode resume`:

1. Read `STATE.yaml` first.
2. Verify `branch` matches current checkout and `base` is still
   `origin/main` (re-fetch if needed).
3. Confirm `lock_status: unavailable` is still the case
   (`scripts/automation_lock.py` path still hardcoded to `/Users/jonreilly`);
   skip cooperative lock per skill.
4. Resume from the Cycle 2 candidate listed in **Next Exact Action**
   above, or re-evaluate the route portfolio if upstream conditions have
   changed.
5. Do not re-do the grounding or pack-build steps. Cycle 1 is complete.
