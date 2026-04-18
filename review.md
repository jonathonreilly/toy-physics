# Review: `claude/yt-retention-landing-2026-04-18`

## Current Call

**Do not land this branch.**

My current disposition is:

- **No** as approved retained science
- **No** as a `main` landing branch
- **Yes** as a large science submission branch that still needs another
  internal cleanup pass before it is ready for a real acceptance decision

The branch is clean in the narrow hygiene sense:

- `1` ahead / `0` behind `origin/main` before this review note
- no publication-surface rewiring
- aggregate runners replay without syntax/runtime failure

But the science-review surface is **not** clean enough to approve, because the
branch’s own top-level authority/validator layer still tells several different
stories about what is actually retained, what is embedded-only, and what is
only bound-constrained.

## Replay Status

I checked the actual remote tip and replayed the aggregate reviewers:

- `python3 scripts/frontier_yt_retention_manifest.py`
  ends with `Manifest-validator PASSED: 118`, `FAILED: 0`
- `python3 scripts/frontier_yt_retention_landing_readiness.py`
  ends with `landing readiness runner complete`
- `python3 scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py`
  ends with `PASS=45 FAIL=0` and reports
  `Δ_R = -3.769 % +/- 0.452 %`
- `python3 scripts/frontier_yt_p1_bz_quadrature_2_loop_full_staggered_pt.py`
  explicitly says the raw 8D-MC signed sum is **not** physical and that the
  retained 2-loop value is the loop-geometric bound with same-sign saturation,
  i.e. **bound-constrained, not MC-pinned**

So the problem is **not** “the scripts crash.” The problem is that the
branch’s own science-summary layer overstates and inconsistently summarizes
what the branch actually closes.

## Main Findings

### 1. The readiness / manifest layer assumes the review conclusion it is supposed to support

The top-level reviewer-facing notes say things like:

- “already-retained YT-lane artifacts”
- “clear for reviewer integration”
- “this note contains no new physics / no new numerical result”

But these notes, runners, and logs are **introduced by this branch**. They are
not already-retained package artifacts on `main`; they are the material under
review. So the branch’s own top-level authority layer is laundering branch-new
science into “already retained” status before review has accepted it.

That is not a small wording issue. It affects the whole reading stance of the
submission, because the reader is repeatedly told to treat the bundle as a
completed retained suite rather than as a proposed retained suite under audit.

Concrete locations:

- `docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md:4-8`
- `docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md:18-34`
- `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md:20-25`

### 2. The manifest note and manifest runner disagree about which slots are on-disk retained vs embedded-only

The manifest note says Round-2 recreated several slots as standalone “ON DISK,”
including:

- `P1.1`
- `P1.2`
- `P3.1`
- `P3.2`
- `M.1`

But the manifest runner still hard-codes those same slots as `embedded`,
with `note=None`, `runner=None`, and `log=None`, and the replay prints them as
`[EMBEDDED]`.

So the branch’s own validator contradicts the manifest’s own summary of what
exists on disk. That means the branch’s headline counts and reviewer roadmap
are not yet trustworthy enough to support approval.

Concrete locations:

- note claiming standalone/on-disk promotion:
  - `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md:88-96`
  - `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md:136-154`
  - `docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md:36-49`
- runner hard-coding them as embedded:
  - `scripts/frontier_yt_retention_manifest.py:120-145`
  - `scripts/frontier_yt_retention_manifest.py:313-328`
  - `scripts/frontier_yt_retention_manifest.py:371`

This is a review-surface blocker. Before approval, the note, the validator, and
the printed replay all need to tell one consistent story about slot status.

### 3. The corrected 2-loop BZ note still contains stale “MC retained / MC pinned” language after its own honesty correction

The amended §0 of the 2-loop BZ note is clear:

- the raw 8D-MC signed sum has the wrong sign and overshoots the bound by ~8x
- the retained 2-loop value is **not** MC-pinned
- the through-2-loop number is **bound-constrained**

That honesty fix is the right move.

But the preserved body still contains lines such as:

- “Refined P1 band (through-2-loop MC-pinned)”
- “MC retained (this note)”

So the same authority note still contains both:

- “not MC-pinned”
- “MC retained / MC-pinned”

That internal contradiction is not a cosmetic issue. The readiness note then
uses this slot in the top-level “clear for integration” story. Until the note
itself tells one stable story, the branch is not ready for approval.

Concrete locations:

- corrected interpretation:
  - `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md:1-25`
  - `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md:104-144`
- stale contradictory language still present:
  - `docs/YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md:358-365`

### 4. The top-level readiness note treats the submission as cleared except for two open items, but the three issues above are themselves additional gating problems

`YT_RETENTION_LANDING_READINESS_2026-04-18.md` says the only known open items
are:

- framework-native 2-loop `Δ_R` closure
- P1.4 standalone note promotion

That is too optimistic relative to the actual branch state.

Even if those two were the only scientific gaps, the branch would still need:

- top-level status language that does not assume “already retained”
- manifest / validator agreement on slot status
- one stable story in the 2-loop bound-constrained note

So the branch is not yet in the “reviewer can now just inspect the science”
state its own readiness note claims.

## Best Outcome From Here

The right next move is **not** to weave this into the repo. The right next move
is to make the submission internally honest and self-consistent.

Minimum fixes before I would consider approving it:

1. Rewrite the readiness and manifest notes so they speak in proposal-review
   language, not “already-retained / clear for integration” language.
2. Make the manifest note and manifest runner agree on which slots are
   standalone and which are embedded-only.
3. Fully scrub the 2-loop BZ note so every occurrence matches the corrected
   status: **bound-constrained, not MC-pinned**.
4. Then rerun the manifest and readiness runners and confirm their summaries
   still match the notes.

Only after that cleanup would it make sense to do a second-pass science review
on whether the retained claims themselves should be accepted.

## Bottom Line

This branch is not approved.

It is a large YT science submission with real work in it, but right now its
own review layer still overstates status and contains internal consistency
problems. That keeps it below approval bar even before any deeper theorem-level
accept/reject call on the new YT science itself.
