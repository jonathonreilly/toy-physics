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

## Why the full branch was not landed as-is

### 1. The front-door note is explicitly raw and incomplete

The main note says:

- `Status: RAW INFO CAPTURE`
- Claude-only on this pass
- Codex/OpenAI history to be added later

That makes it a good working packet, but not yet a stable `main` lane. The
methodology lane on `main` needs to read as a curated, citable surface rather
than a temporary archive state.

### 2. The raw annex is too machine-local for a public mainline surface

The raw files carry:

- machine-local absolute paths;
- branch/base snapshots tied to a particular checkout moment;
- full prompt/session dumps;
- full protocol dumps;
- mixed archival and live material.

That material is useful as evidence, but it should not be the first public
surface readers encounter on `main` without a stronger sanitization/indexing
pass.

### 3. The Codex side of the methodology is not yet captured

The branch is heavily Claude-side. But the repo's actual working method is now
Claude-plus-Codex, especially on:

- branch review;
- overclaim detection;
- selective landing;
- repo-hygiene and claim-surface correction.

So a methodology lane that stops at the Claude capture is incomplete.

## What the selective landing preserved

The `main` landing keeps the part that is already mature enough to be public:

- a front-door methodology note;
- a methodology index;
- a short per-paper disclosure paragraph;
- a longer package-level accountability note.

It also keeps the methodology lane **out of the science claim surfaces**. This
is the right separation.

## Follow-up worker tasks

The next workers should extend the methodology lane by capturing the Codex side
at the same editorial standard:

1. Codex prompt/session capture.
2. `review.md` corpus and branch-review patterns.
3. Selective-landing case studies.
4. Repo-hygiene / claim-surface correction examples.
5. Cross-tool disagreement and reconciliation examples.
6. Sanitized archival index for raw prompt/protocol material, if that archive
   is still wanted on `main`.

## Bottom Line

This branch was the right raw evidence-gathering step, but not the right final
repo surface. The methodology lane now exists on `main` in a curated form, and
the remaining Codex/review/hygiene capture should build on that live lane
rather than trying to land the entire raw archive unchanged.
