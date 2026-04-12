# Nature Backlog Blockers Audit

**Date:** 2026-04-11  
**Branch:** `codex/review-final-20260411`  
**Purpose:** classify the remaining Nature-backlog surface into promotion blockers, fundamental boundaries, and nice-to-have improvements.

This note is scoped to the current retained `main` surface plus the review
inbox / hold ledger. It is not a new physics result. It is a decision map:

- what still blocks promotion to `main`
- what is a fundamental boundary of the current framework
- what is only a nice-to-have hardening step

## Source Of Truth

Use this note together with:

- `docs/REVIEW_WORKTREE_INBOX_2026-04-11.md`
- `docs/REMAINING_NON_MAIN_HOLDS_2026-04-11.md`
- `docs/MAIN_REVISIT_SWEEP_2026-04-11.md`
- `docs/CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md`
- `docs/NATURE_BACKLOG_2026-04-10.md` as a historical framing note only

The current retained `main` floor is already clear on:

- bounded Wilson test-mass / continuum companions
- bounded staggered weak-field companions
- bounded irregular same-surface core-packet sign separator
- bounded `64^3` path-sum continuation
- bounded action-uniqueness family-law note

That means the backlog is no longer asking "does anything work at all?".
It is asking which remaining gaps are still scientifically blocking a Nature
paper, and which gaps are only claim-shaping or hardening work.

## Executive Verdict

No new physics blocker was found beyond the blockers already tracked in the
review hold ledger and main revisit sweep.

The main omission in the backlog framing is not a missing experiment. It is a
missing hierarchy:

- some items are true promotion blockers
- some items are fundamental boundaries of the current framework
- some items are just nice-to-have hardening or portability work

That separation should be explicit everywhere the backlog is summarized.

## Promotable Candidates, Not Blockers

These are not blockers to the backlog itself. They are bounded candidates that
look strong enough to audit for promotion:

1. `EMERGENT_PRODUCT_LAW_NOTE.md`
2. `ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`

Why they are not blockers:

- they already close a real gap in bounded form
- they are specifically framed as companion / portability results
- they do not claim full Newton closure

What still needs audit:

- keep the product-law claim at field-linearity emergence on the audited
  surface
- keep the portability claim at source-mass portability, not architecture-
  independent full Newton closure

## Promotion Blockers

These are the items that still block a Nature-level claim if they remain open.

| Blocker | Why it still blocks | Missing control / redesign |
|---|---|---|
| Wilson mutual-attraction side lane | The mutual channel is real, and the near-inverse-square window is real, but frozen/static and lagged-refresh controls still do not separate dynamic shared backreaction from static or adiabatic explanations. | An intervention-style observable on the same open 3D Wilson surface that cleanly distinguishes shared backreaction from frozen/static or lagged-refresh explanations. |
| Exact two-particle product law toy | The old exact 1D product-law test still bakes the bilinear factor into the ansatz, so it is a control, not an emergence result. | Move the bilinear factor out of the ansatz, add a frozen/static-source control, and replay on the primary staggered/open-cubic surface. |
| Staggered two-body closure family | Partner-force survives, but direct-CoM, mid-plane link-current, and packet-local momentum-flux remain negative on the audited open-cubic surface. | A genuinely different conserved-current observable or a different graph geometry. Centroid variants are exhausted. |
| Irregular transport / portability beyond core-packet | The core-packet same-surface separator is now retained, but portability beyond that surface is still not closed. | A portability-grade transport or invariant observable on the same irregular surface. |
| Full both-masses Newton closure | Source-mass scaling is now strong, but full `M1*M2 / r^2` closure still requires a valid both-masses law on the same audited surface. | A same-surface both-masses law that is not baked into the Hamiltonian and survives the same controls. |
| Continuum closure / h -> 0 finalization | The current continuation is promising, but the running `h = 0.0625` work has not yet been merged into a final audit surface. | Final `h -> 0` confirmation and, if needed, a second boundary/control condition. |

## Fundamental Boundaries

These are not promotion blockers in the same sense. They are the current limit
of what the framework can honestly claim.

| Boundary | What it means |
|---|---|
| Born rule | Already closed as a structural boundary marker. It is not a Nature backlog blocker. The linear propagator keeps `I_3` at machine precision; the remaining work is elsewhere. |
| Action uniqueness | The current note is a bounded family-law statement, not a theorem on arbitrary graphs. Weak-field-linear valleys are Newtonian on the tested family, but architecture-independent uniqueness is not proven. |
| Persistent-pattern inertia | The current code still lacks a localized persistent state whose inertial response can be measured as a closed one-parameter mass. This is a real boundary of the present framework, not just a missing benchmark. |
| Same-surface bounded claims | A strong same-surface or same-family positive does not automatically transfer to portability, universality, or full Newton closure. |
| Architecture portability of full Newton | Mass-law portability is now much better; full `F = GM1M2/r^2` portability is still not established. |

## Nice-To-Have Improvements

These are useful, but they do not by themselves block promotion.

| Improvement | Why it helps |
|---|---|
| More sizes and seeds on already-retained lanes | Hardens bounds, reduces the chance of overreading a narrow window. |
| A second boundary condition for the 64^3 continuation | Would make the distance-law continuation harder to dismiss as a single-surface artifact. |
| Extra family coverage for portability companions | Makes the bounded portability claim more durable, but does not change the claim type. |
| Cleaner language normalization across retained notes | Prevents stale summaries from outrunning the current review ledger. |
| Better runner naming for bounded companions | Reduces future promotion mistakes, especially where a control looks like a theorem. |

## What Is Missing From The Current Backlog Framing

This is the main gap I found in the backlog framing itself.

1. The backlog does not clearly separate **promotion blockers** from
   **fundamental boundaries** and **nice-to-have hardening**. That separation
   is now necessary because the repo has both retained companions and real
   holds.
2. The backlog does not consistently state that **mass-law portability is not
   the same thing as full Newton closure**. Those are different claims and
   they should stay separated.
3. The backlog should call out the **continuum h -> 0** work as a formal
   continuation gate, not just an in-flight refinement.
4. The backlog should treat the new bounded candidates as **candidates**,
   not as blockers:
   - emergent product law
   - architecture portability
5. The older `NATURE_BACKLOG_2026-04-10.md` should be marked as historical
   framing only. It is still useful as a record of how the queue was formed,
   but it is no longer the live blocker map.

## Bottom Line

The existing hold ledger already covers the real blockers.

- No new physics blocker was found that is not already tracked.
- The missing piece is clearer framing: which items are blockers, which are
  boundaries, and which are just hardening work.
- The review branch should now treat the Nature backlog as a tiered map, not a
  single undifferentiated queue.
