# Review: `claude/yt-retention-landing-2026-04-18`

## Current Call

**Approved.**

My current disposition is:

- **Yes** as approved YT science
- **Yes** as material ready to land onto `main`
- **Yes** for repo weaving after landing

This approval is for the science content represented by the two YT
submission commits on the branch (`108c013b`, `946f9139`). The branch
itself is still behind current `origin/main`, so the correct landing
mechanism is a clean main-based landing branch or selective
cherry-pick, not a raw merge of the review branch tip.

## Replay Status

I checked the updated remote tip and replayed the key aggregate
validators:

- `python3 scripts/frontier_yt_retention_manifest.py`
  ends with `Manifest-validator PASSED: 149`, `FAILED: 0`
- `python3 scripts/frontier_yt_retention_landing_readiness.py`
  ends cleanly with `landing readiness runner complete`
- `python3 scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py`
  ends with `PASS=45 FAIL=0` and reports
  `Δ_R = -3.769 % +/- 0.452 %`
- `python3 scripts/frontier_yt_p1_bz_quadrature_2_loop_full_staggered_pt.py`
  keeps the corrected honesty boundary:
  the raw signed MC sum is not physical,
  and the retained through-2-loop central is
  **bound-constrained, not MC-pinned**

The updated bundle now presents one stable story:

- the manifest note and manifest runner agree on slot status
- the top-level notes speak in proposal-review language instead of
  laundering the branch into “already retained”
- the 2-loop BZ note is internally aligned with its own §0 honesty
  correction

## What Changed Since The Prior Review

The earlier blocking findings are resolved:

1. **Proposal-side framing fixed.**
   The readiness report and master manifest now present the branch as a
   submission under review, not as a pre-accepted retained package.

2. **Runner / manifest slot agreement fixed.**
   The manifest validator now reflects the actual on-disk state of the
   Round-2 recreated slots and includes the new `P1.17` slot.

3. **2-loop BZ note scrubbed correctly.**
   The body now matches the corrected interpretation:
   the through-2-loop number is **bound-constrained**, not MC-pinned.

These were the real blockers from the previous round. They are no
longer blocking.

## Non-Blocking Hygiene

I found one small documentation inconsistency that should be cleaned up
during landing, but it is **not** a science blocker:

- `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md` still contains a
  stale Part-2 heading / ASCII summary saying `P1` has `16 slots`,
  while the same note otherwise correctly treats `P1` as `17 slots`
  (`P1.1–P1.17`).

This is a local counting-label cleanup issue, not a contradiction in the
actual runner state or retained slot catalog.

## Landing Guidance

This science is approved, but the review branch itself is now behind
current `origin/main`. So the correct landing path is:

1. start from current `origin/main`
2. cherry-pick the YT science commits
   (`108c013b`, `946f9139`)
3. exclude review-note commits from the landing branch
4. weave the accepted YT science through the repo’s live package
   surfaces on top of current main

## Bottom Line

The YT submission is approved.

The branch has crossed the bar from “large science packet needing
internal honesty cleanup” to “accepted science ready for clean landing.”
What remains is integration work, not another science rejection cycle.
