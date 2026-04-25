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

## Why This Matters

The important point is not that AI was used. The important point is that a
sentence was not trusted just because an AI system wrote it. The repo was
organized so the claim could be checked against notes, runners, review, and
status labels.

That control surface includes:

- executable runner harnesses;
- explicit status labels (`retained`, `bounded`, `open`, `no-go`, `reject`);
- preserved no-go routes rather than positive-only storytelling;
- branch review and selective landing;
- explicit negative-boundary notes;
- active review and hygiene workflows.

The method is therefore plain: let the models generate and attack ideas, but
make the repo decide what is live.

## Reading Rule

- For the short manuscript paragraph, use
  [`CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`](./CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md).
- For the broader process description, use
  [`../AI_METHODOLOGY_NOTE_2026-04-25.md`](../AI_METHODOLOGY_NOTE_2026-04-25.md).
