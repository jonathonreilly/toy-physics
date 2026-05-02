# Claim Status Certificate — EW Color-Projection Cycle Cleanup (Block 2 / follow-up)

**Block:** ew-color-projection-cycle-cleanup-block02-20260501
**Branch:** physics-loop/ew-color-projection-cycle-cleanup-block02-20260501
**Stacked on:** physics-loop/ew-current-fierz-channel-derivation-block01-20260501 (PR #249)
**Files modified:**
- docs/YT_EW_COLOR_PROJECTION_THEOREM.md
- docs/RCONN_DERIVED_NOTE.md
- docs/EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md
**Files added:**
- scripts/frontier_ew_color_projection_cycle_cleanup_integration.py
- .claude/science/physics-loops/ew-color-projection-cycle-cleanup-20260501/CLAIM_STATUS_CERTIFICATE.md
- .claude/science/physics-loops/ew-color-projection-cycle-cleanup-20260501/REVIEW_HISTORY.md

## Status

```yaml
actual_current_surface_status: support / audit-graph integration (cycle cleanup)
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "This block is pure citation-graph integration. It adds the Fierz-channel note (PR #249) as a load-bearing one-hop dep of YT_EW_COLOR_PROJECTION_THEOREM, and adds sibling cross-refs from RCONN_DERIVED_NOTE and EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE to the Fierz note. It does not derive new physics, retire any claim, or propose retention."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Disposition

**Goal:** integrate the new Fierz-channel exact derivation (PR #249) into
the audit-graph chain for the (N_c^2 − 1)/N_c^2 EW coupling coefficient,
so the package-level coefficient is no longer load-bearing on the 1/N_c
expansion alone.

**Edits:**

1. **YT_EW_COLOR_PROJECTION_THEOREM.md**
   - Added the Fierz-channel note as a primary one-hop dep in the header
     "Cited authorities" list, labeled **"primary group-theory derivation
     route"**.
   - Re-labeled RCONN_DERIVED_NOTE as **"complementary"** (1/N_c
     dynamical-correction sibling).
   - Added a "Note on the matching rule (M)" paragraph that names the
     residual structural input.
   - Updated §2.7 from "now DERIVED" to "TWO INDEPENDENT EXACT
     DERIVATIONS" and added Route A (Fierz exact) / Route B (1/N_c
     dynamical-correction) framing.
   - Updated "What prevents THEOREM status" item 2 from "R_conn has
     O(1/N_c⁴) corrections" (which is true only for Route B) to "the
     matching rule (M) is the residual load-bearing input" (the actual
     bottleneck after Route A).

2. **RCONN_DERIVED_NOTE.md**
   - Added a "Sibling exact derivation" cross-ref to the Fierz note.
   - Distinguishes the two routes: this note's 1/N_c expansion is the
     dynamical-correction sibling of the Fierz note's exact group-theory
     ratio.

3. **EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md**
   - Added the same "Sibling exact derivation" cross-ref.
   - Explicitly distinguishes this note's dynamical-suppression role
     (bounding the disconnected piece) from the Fierz note's
     channel-fraction role (specifying the connected weight).

**Did NOT change** any of the load-bearing physics content of the 3 cycle
nodes. The runner's Part 5 verifies the original signature equations
remain present:

- YT_EW: 9/8 = N_c^2/(N_c^2-1) statement; Fierz identity
  `Pi_EW = N_c D - 2N_c sum_A Pi_3^{AA}`.
- RCONN: leading-order `R_conn = (N_c^2 - 1)/N_c^2 + O(1/N_c^4)`.
- OZI: `Pi_EW^{phys} = Pi_EW^{conn} * (1 + O(1/N_c^2))`.

## Allowed PR/Status Wording

- "support / audit-graph integration (cycle cleanup)"
- "stacked on PR #249"
- "no new physics; pure citation integration"
- "preserves load-bearing physics content"
- "matches the Fierz note's primary group-theory route as load-bearing dep of YT_EW"

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "promotes 9/8 to retained"
- "closes the EW coupling correction"
- "retires RCONN_DERIVED_NOTE"

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_ew_color_projection_cycle_cleanup_integration.py
# expected: PASS=17 FAIL=0
```

The integration runner verifies:

1. Fierz note (PR #249 dep) is present in the working tree.
2. YT_EW cites the Fierz note via markdown link as one-hop dep, labeled
   primary group-theory derivation route.
3. RCONN has the sibling cross-ref to the Fierz note.
4. OZI has the sibling cross-ref to the Fierz note.
5. **No load-bearing physics content was removed** from any of the 3
   cycle nodes (signature equations preserved).
6. The cycle-break is now reflected in YT_EW's prose (matching rule (M)
   named as residual load-bearing input).

Additional independent confirmations:

- `frontier_color_projection_mc.py` continues to PASS (existing MC verification
  of R_conn ≈ 8/9; runtime ~3.7 minutes).
- `frontier_ew_current_fierz_channel_decomposition.py` continues to give
  PASS=31 FAIL=0 (PR #249's runner).

## Independent Audit

Audit must verify:

1. The Fierz note (PR #249 dep) lands first in any review-merge ordering;
   this PR's edits assume that file is present at
   `docs/EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`.
2. No load-bearing physics signature was removed from any of the 3
   cycle nodes (run integration runner Part 5).
3. The new YT_EW header section correctly labels the Fierz note as
   primary group-theory route; RCONN as complementary 1/N_c sibling;
   OZI as bounded large-N_c support.
4. The matching rule (M) is named as residual load-bearing input in
   YT_EW's "What prevents THEOREM status" section.
5. After this PR + PR #249 land and the audit pipeline regenerates the
   citation graph and re-evaluates effective_status, the 385 transitive
   descendants of YT_EW_COLOR_PROJECTION_THEOREM should propagate
   downstream cleanly modulo the matching rule (M) honestly named in
   their chains.

## Stacked-PR notes

**Base:** PR #249 branch. The follow-up edits assume the new Fierz note
exists. If PR #249 is rebased or modified, this PR should be rebased
onto the updated branch before merge.

If the audit team prefers to merge to `main` in a single combined PR,
this branch can be squash-merged into PR #249's branch instead of opening
a separate PR. Either resolution preserves the cycle-break.
