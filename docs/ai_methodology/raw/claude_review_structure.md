# Claude Review Structure

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`. The review surfaces
captured here include outputs from earlier Claude (Sonnet/Opus 4.x) sessions.

**Machine:** `/Users/jonreilly/Projects/Physics`

**Scope note:** This file captures the raw evidence of how the Claude side of
the workflow performs and consumes branch reviews. Not an analysis of the
review process — direct file paths, counts, and excerpts only.

---

## 1. `review.md` files visible from this worktree

Searched: `/Users/jonreilly/Projects/Physics` and `/private/tmp/`.

```text
/Users/jonreilly/Projects/Physics/.claude/worktrees/blissful-tu-ccc1e8/review.md
/private/tmp/ai-method-review/review.md
/private/tmp/three-sector-review/review.md
/private/tmp/lorentz-boost-covariance-review/review.md
```

The first one (in this worktree) is the **incoming review** of the very
methodology branch this capture is being added to. The other three are live
Codex review packets in `/private/tmp/` worktrees.

## 2. The review of THIS branch (incoming)

Path: `.claude/worktrees/blissful-tu-ccc1e8/review.md` (committed to the
branch as evidence on `2026-04-25`).

Verbatim opening:

```text
# Review: `claude/ai-methodology-capture-2026-04-25`

## Verdict

Useful raw archive, but **not approved verbatim** for `main`.

The branch contains valuable source material for a methodology paper, but the
submitted surface is still a branch-local capture packet rather than a clean
public methodology lane.

I took a **selective landing** instead. The curated subset now on `main`
(`4da26702`) is:

- `docs/AI_METHODOLOGY_NOTE_2026-04-25.md`
- `docs/ai_methodology/README.md`
- `docs/ai_methodology/CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`
- `docs/ai_methodology/AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md`

That is the correct live surface for now.
```

Verbatim verdict tail:

```text
## Bottom Line

This branch was the right raw evidence-gathering step, but not the right final
repo surface. The methodology lane now exists on `main` in a curated form, and
the remaining Codex/review/hygiene capture should build on that live lane
rather than trying to land the entire raw archive unchanged.
```

The follow-up worker tasks listed in this `review.md`:

```text
1. Codex prompt/session capture.
2. `review.md` corpus and branch-review patterns.
3. Selective-landing case studies.
4. Repo-hygiene / claim-surface correction examples.
5. Cross-tool disagreement and reconciliation examples.
6. Sanitized archival index for raw prompt/protocol material, if that archive
   is still wanted on `main`.
```

This raw-capture pass (the one this very file is part of) is a partial response
to that to-do list — items 1–4 are populated by the new `claude_*` raw
files and the previous `codex_*` raw files.

## 3. Repo-side review packet inventory

`docs/*REVIEW*` matches found in the repo (selected, 2026-04-25):

```text
/Users/jonreilly/Projects/Physics/docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md
/Users/jonreilly/Projects/Physics/docs/KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md
/Users/jonreilly/Projects/Physics/docs/MOONSHOT_HONEST_REVIEW_2026-04-09.md
/Users/jonreilly/Projects/Physics/docs/QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md
/Users/jonreilly/Projects/Physics/docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md
/Users/jonreilly/Projects/Physics/docs/K_DEPENDENCE_REVIEW_SAFE_NOTE.md
/Users/jonreilly/Projects/Physics/docs/SCALAR_SELECTOR_REVIEWER_PACKAGE_2026-04-20.md
/Users/jonreilly/Projects/Physics/docs/KOIDE_REVIEWER_STRESS_TEST_NOTE_2026-04-21.md
/Users/jonreilly/Projects/Physics/docs/NEUTRINO_RETAINED_LANES_REVIEW_PACKET_2026-04-16.md
/Users/jonreilly/Projects/Physics/docs/GRAVITY_REVIEWER_DERIVATION_SUMMARY_2026-04-15.md
/Users/jonreilly/Projects/Physics/docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md
/Users/jonreilly/Projects/Physics/docs/KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md
/Users/jonreilly/Projects/Physics/docs/KOIDE_Q_SECOND_ORDER_REVIEWER_STRESS_TEST_NOTE_2026-04-22.md
/Users/jonreilly/Projects/Physics/docs/KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW_NOTE_2026-04-24.md
/Users/jonreilly/Projects/Physics/docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md
/Users/jonreilly/Projects/Physics/docs/DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md
/Users/jonreilly/Projects/Physics/docs/repo/ACTIVE_REVIEW_QUEUE.md
/Users/jonreilly/Projects/Physics/docs/repo/REVIEW_FEEDBACK_WORKFLOW.md
```

Naming convention observed:
- `*_REVIEW_PACKET_<DATE>.md` — review-ready bundle prepared on a branch
  before submission
- `*_REVIEW_NOTE_<DATE>.md` — written review of an existing claim
- `*_REVIEWER_STRESS_TEST_NOTE_<DATE>.md` — adversarial review pass
- `*_HOSTILE_REVIEW_GUARD_NOTE_<DATE>.md` — defensive note pre-empting hostile review
- `*_NATURE_REVIEW_NOTE_<DATE>.md` — review tuned for top-tier journal standards
- `ACTIVE_REVIEW_QUEUE.md` + `REVIEW_FEEDBACK_WORKFLOW.md` — repo-level
  review-process documentation

This packet structure is what review.md outputs (like §2 above) feed into.

## 4. Branch-summary and session-synthesis surfaces

```text
/Users/jonreilly/Projects/Physics/docs/BRANCH_SUMMARY_DISTRACTED_NAPIER.md
/Users/jonreilly/Projects/Physics/docs/SESSION_SYNTHESIS_2026-04-09.md
/Users/jonreilly/Projects/Physics/docs/SESSION_SYNTHESIS_2026-04-10_FINAL.md
/Users/jonreilly/Projects/Physics/docs/SESSION_SYNTHESIS_2026-04-10_GRAPH_AXIOMS.md
/Users/jonreilly/Projects/Physics/docs/SESSION_SYNTHESIS_2026-04-11.md
```

Each `BRANCH_SUMMARY_<NAME>.md` corresponds to a closed-out worktree branch
(here: `distracted-napier`). The `SESSION_SYNTHESIS_<DATE>.md` files are
end-of-day rollups across multiple worktrees on a single calendar day.
These are AI-authored synthesis documents that compress a session of Claude
work into a citable artifact.

## 5. Project-level slash commands that drive review

Path: `/Users/jonreilly/Projects/Physics/.claude/commands/` (14 files):

```text
analyze.md
autopilot.md
design-experiment.md
first-principles.md
frontier.md
hypothesis.md
investigate-physics.md
progress.md
pstack.md
sanity.md
sweep.md
theory-review.md
validate.md
write-up.md
```

The review-relevant ones for this section are `theory-review.md`,
`sanity.md`, `validate.md`, and `analyze.md`. (Full bodies are captured in
the existing `workflow_tooling.md` raw file in this archive.)

User-global commands (different surface):

```text
/Users/jonreilly/.claude/commands/codemap.md
/Users/jonreilly/.claude/commands/rc.md
/Users/jonreilly/.claude/commands/refactor-clean.md
/Users/jonreilly/.claude/commands/review.md
/Users/jonreilly/.claude/commands/tdd.md
/Users/jonreilly/.claude/commands/verify.md
```

The user-global `review.md` is shared across projects; the project-specific
review surface is the `theory-review` / `sanity` / `validate` / `analyze`
quartet plus the bigger `*_REVIEW_*` packet inventory in §3 above.

## 6. Cross-tool review evidence

The `/private/tmp/*-review/` worktrees observed during this capture are
**Codex** workers attached to specific Claude or shared branches to perform
adversarial review. Listed from `git worktree list`:

```text
/private/tmp/ai-method-review                     91b52c8e [codex/review-ai-methodology-capture-2026-04-25]
/private/tmp/three-sector-review                  527864cb [codex/review-three-sector-dim-color-2026-04-25]
/private/tmp/lorentz-boost-covariance-review      3faae6d6 [lorentz-boost-covariance-review-note]
/private/tmp/great-nobel-review.cpqYSB            a7898f83 (detached HEAD)
/private/tmp/hypercharge2-review                  29a2b8c9 (detached HEAD)
/private/tmp/koide-a1-frac-review                 5e9ce500 (detached HEAD)
/private/tmp/koide-brannen-ch-three-gap-review    f68dc664 [koide-brannen-ch-three-gap-review]
/private/tmp/koide-charged-lepton-axiom-native-review  1055aefc (detached HEAD)
/private/tmp/koide-dimensionless-objection-review      970933e6 (detached HEAD)
/private/tmp/koide-equivariant-berry-aps-selector-review  451f5f9c (detached HEAD)
/private/tmp/koide-equivariant-review              1f2dd411 (detached HEAD)
/private/tmp/lh-anomaly-review                     8b649a42 (detached HEAD)
/private/tmp/morning-4-21-review                   1e675110 (detached HEAD)
```

So the active review surface for this branch is in two places:

- the **branch-local** `review.md` in this worktree (Codex review of the
  Claude-authored capture branch — see §2)
- the **paired Codex review worktree**
  `/private/tmp/ai-method-review` on branch
  `codex/review-ai-methodology-capture-2026-04-25`

Recent commit on the Codex review worktree:

```text
91b52c8e docs: add codex raw capture to methodology archive
c36cbe81 docs: add review for ai methodology capture branch
```

So the Codex side of this same lane has already added its own raw capture
(the `codex_*` files in this archive) and committed the `review.md` that is
visible in this Claude worktree. The two tools' raw files now coexist in the
same `docs/ai_methodology/raw/` directory.

## 7. Cross-tool review interaction observed in commit log

From `git log --since=2026-04-22` filtered for review-related events:

```text
c36cbe81 docs: add review for ai methodology capture branch
2d4618f2 koide: land dimensionless objection review packet
c67de08e Demote review-state language in delicate lane notes
870030c2 land scalar selector review package
c02e1aab framework: land reviewed CL3 support and selector-gap packet
90c78a87 docs: package quark route-2 science review stack
32e2d8bb docs: weave bounded quark review packet through main surfaces
de6a472e Add quark science review stack
4128417d docs: archive operational review backlog surfaces
f124537d cosmology: review pass on graviton-mass identity theorem note
d423f8ad charged-lepton: land koide review support stack
f4e81b2f dm: add reviewed Wilson direct-descendant science stack
c0fd45b0 docs: address first-round reviewer findings on YT retention submission
0c47dc12 docs: retire branch-entanglement GHZ review blocker
6700b7ae docs: retire stale Wilson Newton review blocker
8dcfc86e docs: retire bmv overclaim review item
093a46f2 docs: retire old staggered two-body review item
668c16ce review: demote symmetrized DAG claims
3851f7a5 review: retire resolved self-consistency control finding
2679fe30 review: rerun-correct two-field wave family audit
```

Pattern visible directly in raw commit log:

- `land reviewed <X>` — a packet that has already passed a review pass before
  landing
- `land <X> review packet` — a review-bundle being landed for further scrutiny
- `address ... reviewer findings` — fix-up commits responding to a review
- `retire <X> review blocker` — closing out a previously-flagged objection
- `demote <X> claims` — downgrading an overstated claim after review

## 8. Memory-encoded review feedback

From `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md`:

```text
- Hostile review must challenge semantics —
  Trace-ratio derivations can be arithmetically perfect while comparing against
  convention-defined sources rather than physical couplings; hostile-review
  passes must stress-test the action-level identification of symbols, not just
  algebra
```

This memory entry is itself review-process feedback that has been promoted
from a single-conversation lesson into a persistent cross-conversation rule.
Future Claude sessions on this machine load this rule on every start.
