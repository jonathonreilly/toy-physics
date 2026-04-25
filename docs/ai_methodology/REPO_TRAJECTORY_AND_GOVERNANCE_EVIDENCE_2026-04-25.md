# Repo Trajectory And Governance Evidence

**Date:** 2026-04-25
**Status:** methodology-paper evidence note; source packet for repo history,
reviewer backpressure, and organization methodology

This note fills the gap between the raw AI prompt archive and the current
methodology lane: the repo trajectory, governance rules, review pressure, and
organization layer that made the AI-assisted science auditable.

## Snapshot

Current capture from `origin/main` at `ccd30b82`:

| Surface | Count / value |
|---|---:|
| `origin/main` commits | 2672 |
| first commit | `2026-03-13 7a5f1dca Initial commit` |
| current captured tip | `2026-04-25 ccd30b82 Open frontier extension planning lanes` |
| markdown docs under `docs/` | 1530 |
| Python scripts under `scripts/` | 2096 |
| `frontier_*.py` runners | 1039 |
| raw AI-methodology Markdown files, including raw README | 62 |
| raw AI-methodology content lines, excluding raw README | 93099 |
| visible remote `origin/{claude,codex,review,frontier}/...` branches | 107 |
| visible `review.md` packets in active temp/worktree space | 4 |
| docs matching review/backpressure/demotion language | 179 |

These counts are not themselves the argument. They show the scale of the
research object that required explicit governance.

## Commit-Cadence Trajectory

The repo grew in four broad phases.

| Phase | Dates | Character |
|---|---|---|
| Seed and primitive search | 2026-03-13 to 2026-03-20 | Initial toy model, diagnostics, robustness sweeps, and mechanism tests. |
| High-throughput lane expansion | 2026-03-21 to 2026-04-10 | Hundreds of commits across frontier runners, generated geometry, gravity, gauge, action-law, and review-hardening work. |
| Governance hardening | 2026-04-11 to 2026-04-18 | Lane board, active review queue, controlled vocabulary, retest playbook, work-history archive, and retained logs became explicit. |
| Publication and methodology surfacing | 2026-04-19 to 2026-04-25 | Publication package, claim tables, external reviewer guide, selective landing, AI-methodology raw capture, and methodology-lane front door. |

Recent daily commit counts show the transition from raw search volume to
curated package work:

```text
  87 2026-03-30
 185 2026-03-31
 238 2026-04-01
 107 2026-04-02
 250 2026-04-03
 216 2026-04-04
 199 2026-04-05
 178 2026-04-06
  84 2026-04-07
  76 2026-04-08
  96 2026-04-09
 128 2026-04-10
  51 2026-04-11
  13 2026-04-12
  12 2026-04-13
  22 2026-04-14
  65 2026-04-15
  50 2026-04-16
  40 2026-04-17
  55 2026-04-18
  11 2026-04-19
   1 2026-04-20
   1 2026-04-21
  13 2026-04-22
   7 2026-04-23
  26 2026-04-24
  35 2026-04-25
```

Methodologically, the important pattern is that high-volume candidate
production was followed by progressively stricter control-plane surfaces rather
than being accepted as-is.

## Governance Primitives

The repo's control structure is now explicit.

| Primitive | Function | Main surface |
|---|---|---|
| Off-main lanes | Keep exploratory AI output away from the current claim boundary until reviewed | branch/worktree inventory; `raw/claude_review_structure.md`; `raw/codex_review_structure.md` |
| Note + runner pairing | Force prose claims to have an executable or replayable check | `../CANONICAL_HARNESS_INDEX.md`, publication validation maps |
| Controlled vocabulary | Prevent silent upgrade from support or bounded result to retained theorem | `../repo/CONTROLLED_VOCABULARY.md` |
| Active review queue | Keep unresolved review findings in one live location | `../repo/ACTIVE_REVIEW_QUEUE.md` |
| Review feedback workflow | Define triage buckets and narrow honest fixes | `../repo/REVIEW_FEEDBACK_WORKFLOW.md` |
| Retest playbook | Rerun the smallest honest surface when bugs or semantic drift are found | `../repo/RETEST_PLAYBOOK.md` |
| Work-history archive | Preserve resolved, superseded, or historical material without letting it become live authority | `../work_history/` |
| Publication package | Separate paper-facing claims from raw repo history | `../publication/ci3_z3/` |

The strongest reusable insight is that repo organization is not clerical. It is
part of the control method.

## Reviewer Backpressure Method

Reviewer backpressure is the conversion layer between AI abundance and
publishable science.

The live review workflow uses five disposition buckets:

- `fix on main`
- `support-only demotion`
- `science-needed`
- `reject`
- `historical only`

The method is the narrowest honest fix:

- wording, packaging, stale status language, or reproducible code bugs can be
  fixed on `main`;
- missing theorem steps cannot be patched with rhetoric;
- unsupported science stays off `main` or gets demoted;
- historical lanes stay in work history rather than masquerading as live
  blockers.

This is the main antidote to AI overproduction. The model can generate many
plausible bridges; the review loop decides which bridges are theorem-grade,
bounded support, still open, or rejected.

## Selective Landing Pattern

Selective landing is the normal integration move:

1. inspect a branch for real value and overclaim risk;
2. reject the branch as submitted if it is not clean enough;
3. salvage only the honest subset;
4. land that subset at the correct status;
5. keep branch-local review notes and raw evidence out of the public front
   door unless they belong in the raw annex.

The AI-methodology capture itself is a representative case. The raw branch was
valuable, but not approved verbatim. The curated live surface became the
methodology note, lane index, disclosure paragraph, accountability note, and
raw annex, while review details stayed as evidence rather than public authority.

## Organization As A Scientific Control Surface

The repo now distinguishes:

- `docs/publication/ci3_z3/` for paper-facing claims, predictions, validation,
  and non-claims;
- `docs/repo/` for live governance and review control;
- `docs/work_history/` for archived or historical material;
- `docs/ai_methodology/` for the AI-methodology evidence and transferable
  method;
- `scripts/` for executable runners, audits, and harnesses;
- `logs/retained/` for preserved runner outputs.

This organization gives later reviewers a stable reading rule: start from the
front-door package and validation maps, not from raw prompt output or branch
history.

## Paper-Relevant Claim

The methodology paper should frame this evidence as a concrete operating
system for AI-assisted theory work:

- LLMs are productive at candidate generation, theorem drafting, runner
  writing, and obstruction search.
- LLMs are also prone to rhetorical upgrade and over-broad closure language.
- The repo turns those tendencies into a controlled workflow by assigning
  status, preserving no-go routes, requiring executable checks, and using
  adversarial review before landing.

That is the transferable method: not "trust the AI", but "make the AI produce
artifacts that can be attacked, rerun, narrowed, archived, and selectively
landed."
