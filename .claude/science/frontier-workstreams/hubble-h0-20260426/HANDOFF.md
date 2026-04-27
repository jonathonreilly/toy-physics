# Hubble H_0 — Handoff

**Branch:** `frontier/hubble-h0-20260426`
**Workstream:** `hubble-h0-20260426`

## Current State

**Cycle 1 complete.** Hubble Tension Structural Lock theorem (route R4)
landed on the science branch:

- `docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`
- `scripts/frontier_hubble_tension_structural_lock.py` — 5/5 checks PASS
- `logs/2026-04-26-hubble-tension-structural-lock.txt` — paired log

Branch-local self-review (6 reviewer criteria) PASS after one tightening
edit (premise count reduced from 3 to 2 in theorem §0). Findings recorded
in `REVIEW_HISTORY.md`.

`STATE.yaml` is the single-source-of-truth resume surface. Pack files
unchanged from scaffold except `REVIEW_HISTORY.md`, `STATE.yaml`, and this
file.

## Claim-state movement achieved

**Lane 5 Phase 1 (5C — Hubble tension explicit stance)**: advanced from
"Tier A planning, ~1 week" (lane file framing) to **theorem-note grade with
an explicit operational falsifier** (no late-time `H_0` drift on the
retained surface). Late-time-only resolutions of any genuine Hubble tension
are now structurally forbidden on the retained surface; resolution must
come from pre-recombination physics or measurement systematics.

This does NOT retire the `H_0` import. It locks the structural form of
late-time `H_0` measurements.

## Next Exact Action (Cycle 2 candidate)

Per `ROUTE_PORTFOLIO.md` scoring:

- **Cycle 2 candidate A — Route R3 (Open-Number Reduction theorem).**
  Formalize the parameter-count statement: every late-time bounded
  cosmology row is an exact function of `(H_0, L)` where
  `L = Omega_Lambda = (H_inf/H_0)^2`. This packages the matter-bridge
  theorem + inverse reconstruction theorem + structural lock theorem into
  one open-number-count statement. Tier A. No blockers.
- **Cycle 2 candidate B — Route R5 (eta retirement audit).** Survey the
  surviving DM leptogenesis branches (`eta/eta_obs = 0.1888` exact
  one-flavor; `1.0` reduced-surface PMNS) and identify the minimal
  selector/normalization closure that retires `eta` from the bounded
  `Omega_b` cascade. Tier B. Cross-lane dependency.
- **Recommendation:** R3 first (Tier A, single-cycle achievable, no
  blockers, completes the cosmology open-number-count story). R5 is the
  better second step toward `Omega_m` closure but warrants a separate
  session.

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
