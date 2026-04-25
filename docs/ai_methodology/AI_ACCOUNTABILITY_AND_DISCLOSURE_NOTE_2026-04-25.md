# AI Accountability And Disclosure Note

**Date:** 2026-04-25  
**Status:** package-level disclosure note for the methodology lane

This note is the longer repository-facing companion to the short framing
paragraph used in papers.

## Disclosure

This project has used generative-AI systems extensively, especially Claude and
OpenAI Codex.

These tools were used for:

- derivation drafting;
- candidate theorem construction;
- executable runner generation;
- no-go and obstruction search;
- branch review;
- claim-surface audit;
- selective landing and repo integration.

They were not treated as authors.

## Human Responsibility

The human author retained responsibility for:

- the foundational choice of framework surface;
- the selection of which scientific targets mattered;
- acceptance or rejection of proposed results;
- the final claim boundary on `main`;
- manuscript posture and interpretation.

AI systems were used as research and engineering instruments inside that
decision structure, not as the final authority on scientific truth.

## Why This Is A Methodological Asset

The important point is not simply that AI was used. The important point is that
the repo was organized so that correctness could be checked independently of the
origin of a sentence.

That control surface includes:

- executable runner harnesses;
- explicit status labels (`retained`, `bounded`, `open`, `no-go`, `reject`);
- preserved no-go routes rather than positive-only storytelling;
- branch review and selective landing;
- explicit negative-boundary notes;
- active review and hygiene workflows.

The methodology claim is therefore stronger than "AI helped write the paper."
It is that AI-assisted theorem production was embedded in a repo structure that
made the results auditable.

## Reading Rule

- For the short manuscript paragraph, use
  [`CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`](./CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md).
- For the broader process description, use
  [`../AI_METHODOLOGY_NOTE_2026-04-25.md`](../AI_METHODOLOGY_NOTE_2026-04-25.md).
