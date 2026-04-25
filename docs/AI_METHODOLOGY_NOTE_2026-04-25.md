# AI Methodology Note — Cl(3)/Z^3 Framework

**Date:** 2026-04-25  
**Status:** active methodology-capture lane on `main`; curated front-door note,
not the final methodology paper  
**Scope:** how AI systems were used to generate, audit, demote, reject, and
land the framework's science

This note does not add or promote any physics claim. Its job is to document the
method by which claims were produced and controlled.

## 1. Reading Rule

This lane is separate from the physics claim surface.

- For the current scientific package, use the publication surfaces in
  [`docs/publication/ci3_z3/`](./publication/ci3_z3/README.md).
- For the AI/process methodology, use this note and the methodology index in
  [`docs/ai_methodology/README.md`](./ai_methodology/README.md).

The methodology lane is about:

- how candidate theorems were generated;
- how executable runner harnesses were used to separate algebra from rhetoric;
- how bounded/retained/open status was kept explicit;
- how Claude and Codex were used in partially adversarial roles;
- how branch review, selective landing, and repo hygiene were enforced.

It is not itself a theorem note.

## 2. Snapshot Of The Project Surface

As of the 2026-04-25 capture on current `main`:

- `origin/main` commits: `2666`
- initial commit: `2026-03-13` (`7a5f1dca`)
- current `origin/main` tip at capture: `0a116fa1`
- markdown documents under `docs/`: `1467`
- Python scripts under `scripts/`: `2087`
- `frontier_*.py` runners: `1030`
- visible remote `claude/*` and `codex/*` branches: `89`

These numbers matter because the methodological claim is not "AI helped write
some text." The methodological claim is that a very large theorem/search/review
surface was managed through explicit executable and editorial controls.

## 3. Division Of Labor

### 3.1 Human role

The human author retained responsibility for:

- the founding choice of `Cl(3)` on `Z^3` as the framework surface;
- the physics targets worth pursuing;
- the decision to promote, demote, or reject a claim;
- the final claim boundary on `main`;
- the interpretation of results and the manuscript posture.

### 3.2 Claude role

Claude was used heavily on the forward-production side:

- theorem-note drafting;
- derivation search;
- obstruction and no-go production;
- runner generation;
- branch-local science packaging;
- high-volume exploratory work across parallel worktrees.

### 3.3 Codex role

Codex was used heavily on the adversarial and integration side:

- branch review;
- overclaim detection;
- theorem-premise audits;
- selective subset landing onto `main`;
- claim-surface weaving;
- repo-hygiene and review-note enforcement.

The two tools were not treated as interchangeable. In practice they formed a
partially adversarial pair: one often proposed or extended science, while the
other pressured the claim boundary and forced narrower honest landings.

## 4. Core Method

The working method that emerged in this repository has six recurring parts.

### 4.1 Candidate work happens off `main`

New science is usually developed on a dedicated branch/worktree first. That
keeps exploratory work, failed routes, and overclaimed drafts off the live
package surface.

Relevant repo-side examples:

- [`docs/CLAUDE_BRANCH_RETAINABILITY_NOTE.md`](./CLAUDE_BRANCH_RETAINABILITY_NOTE.md)
- [`docs/UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md`](./UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md)

### 4.2 Notes and runners are paired

A claim is not just prose. The normal unit of work is:

- theorem/support/no-go note;
- paired `frontier_*.py` runner;
- replayable PASS/FAIL output;
- sometimes a retained log.

This pairing is the primary defense against AI-generated rhetorical drift.

### 4.3 Claim status is explicit

The repo uses explicit status distinctions instead of a single bucket called
"proved":

- `retained`
- `bounded`
- `support`
- `conditional`
- `open`
- `no-go`
- `reject`

This is one of the main mechanisms used to stop AI systems from silently
upgrading a suggestive route into a theorem.

The package-wide negative boundary is maintained explicitly in:

- [`docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md`](./publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md)

### 4.4 No-go production is first-class

The methodology does not only reward positive closes. It also keeps and cites:

- route obstructions;
- failed closure attempts;
- support-only demotions;
- theorem-level no-go notes;
- review notes that explain why a branch is not yet landable.

This matters because AI systems are very good at producing plausible positive
stories. The repo's no-go surface is one of the main controls against that bias.

### 4.5 Review is not cosmetic

The repo has an explicit review workflow for deciding what becomes live truth on
`main`:

- [`docs/repo/REVIEW_FEEDBACK_WORKFLOW.md`](./repo/REVIEW_FEEDBACK_WORKFLOW.md)

The narrowest honest fix is the rule:

- wording and packaging problems get fixed on `main`;
- real missing theorem steps do not get patched with rhetoric;
- unsupported science stays off `main` or gets demoted.

### 4.6 Selective landing is normal

A branch is not all-or-nothing. Many branches are valuable but only in part.
The standard `main` move is often:

1. reject the branch as submitted;
2. salvage the honest subset;
3. land that subset at the correct status;
4. keep the rest off `main`.

This selective-landing discipline is central to how AI-produced material was
made usable without allowing every high-volume branch to rewrite the live claim
surface.

## 5. Repo Hygiene As Methodology

Repo hygiene is not auxiliary here. It is part of the method.

Important surfaces include:

- [`docs/CANONICAL_HARNESS_INDEX.md`](./CANONICAL_HARNESS_INDEX.md)
- [`docs/repo/ACTIVE_REVIEW_QUEUE.md`](./repo/ACTIVE_REVIEW_QUEUE.md)
- [`AUTOPILOT_PROTOCOL.md`](../AUTOPILOT_PROTOCOL.md)
- [`AUTOPILOT_JANITOR_PROTOCOL.md`](../AUTOPILOT_JANITOR_PROTOCOL.md)
- [`AUTOPILOT_SUMMARY_PROTOCOL.md`](../AUTOPILOT_SUMMARY_PROTOCOL.md)

These files encode a reproducibility discipline:

- branch work is isolated;
- locks prevent concurrent corruption;
- handoff state is explicit;
- review queues are canonicalized;
- stale or superseded material is pushed into `docs/work_history/` instead of
  polluting the front door.

In other words, repo hygiene is part of the epistemic control surface, not just
an engineering nicety.

## 6. Current Evidence Surface

The curated methodology lane on `main` now consists of:

- this front-door note;
- a methodology index:
  [`docs/ai_methodology/README.md`](./ai_methodology/README.md);
- a canonical per-paper disclosure paragraph:
  [`docs/ai_methodology/CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`](./ai_methodology/CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md);
- a package-level accountability note:
  [`docs/ai_methodology/AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md`](./ai_methodology/AI_ACCOUNTABILITY_AND_DISCLOSURE_NOTE_2026-04-25.md).

These are the publishable part of the methodology lane.

They are intentionally smaller than the raw archive branch material. The point
on `main` is to keep the lane readable, citable, and honest.

## 7. What Is Not On `main` In This Pass

The branch that motivated this landing carried a much larger raw-capture
archive, including:

- prompt/session dumps;
- full protocol captures;
- machine-local path inventories;
- partial Claude-only capture without the Codex side completed.

That material is useful, but it is not the right `main` surface yet.

In particular, the following still need a dedicated capture/sanitization pass
before they should be promoted:

- Codex prompt/session history;
- `review.md` corpus and selective-landing history;
- branch-review and repo-hygiene examples across the `codex/*` work;
- normalized raw transcript archives that do not depend on one machine-local
  path layout.

## 8. Next Capture Targets

The next methodology pass should add the Codex side explicitly:

1. Codex prompt/session capture.
2. Review-note corpus capture (`review.md` on science branches).
3. Selective-landing case studies.
4. Repo-hygiene and claim-surface correction examples.
5. Cross-tool disagreement/reconciliation events where one system caught an
   overclaim or premise gap introduced by the other.

That second pass is the one that will turn this from a Claude-first methodology
capture into a true Claude-plus-Codex methodology lane.

## 9. Bottom Line

The central methodological fact of this repository is not merely that AI was
used. It is that AI-assisted theorem production was embedded inside an explicit
control structure:

- executable runners;
- bounded/retained/open labeling;
- no-go preservation;
- adversarial cross-tool review;
- selective landing;
- repo-hygiene and historical archiving.

That control structure is what made the resulting scientific package auditable.
